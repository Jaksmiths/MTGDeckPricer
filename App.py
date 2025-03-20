from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State, dash_table  # pip install dash (version 2.0.0 or higher)
from dash.exceptions import PreventUpdate
from io import BytesIO
from zipfile import ZipFile

from MTGDeckPricer import MTGDeckPricer

app = Dash(__name__)
pricer = MTGDeckPricer()

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("MTG Deck Price History Generator", style={'text-align': 'center'}),
    html.H2("By Jake Smith, using Python with Dash and Plotly", style={'text-align': 'center','font-size': '12px'}),

    dcc.Input(
        id="input_link",
        type="text",
        placeholder="input TCG/Moxfield decklist link",
        value="test_data.txt", # default
        debounce=True, # wait until enter is pressed to submit
    ),

    dcc.Dropdown(
        id="input_decision",
        options=["MOX", "TCG", "TEXT"],
        value="TEXT",
    ),

    dcc.Checklist(
        id="input_retailer",
        options=["tcgplayer", "cardmarket", "cardkingdom"],
        value=["tcgplayer"],
        inline=True,
    ),

    dash_table.DataTable(id="error_table",page_size=5),

    dcc.Graph(id='price_plot', figure={})
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='price_plot', component_property='figure'),
     Output(component_id='error_table', component_property='data')],
    [Input(component_id='input_link', component_property='value')], 
    [State(component_id="input_decision", component_property="value"),
     State(component_id="input_retailer", component_property="value")]
)
def update_graph(input_link, input_decision, input_retailer):

    if input_link == '' or len(input_retailer) == 0:
        raise PreventUpdate
    print(input_retailer)
    info = pricer.getDeckPrice(input_link, input_decision, input_retailer)

    # fig = make_subplots(rows=len(input_retailer), cols=1)
    # r = 1
    # for retailer in input_retailer:
    #     print(info.price_list[info.price_list["Retailer"] == retailer])
    #     fig.add_trace(px.line(info.price_list[info.price_list["Retailer"] == retailer], x="Date", y=info.card_list, facet_col="Retailer" , markers=True),
    #                   row=r,
    #                   col=1)
    #     r += 1
    print(info.price_list)

    fig = px.line(info.price_list, x="Date", y=info.card_list + ["Total"], facet_col="Retailer" , markers=True)
    fig.update_layout(legend_title="Cards", yaxis_title="Price (USD)",)
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name != "Total" else {})

    return [go.Figure(data=fig), [card.to_dict() for card in info.error_list]]

@app.callback(
    [Output(component_id='input_link', component_property='value')],
    [Input(component_id="input_decision", component_property="value")],
    prevent_initial_call=True
)
def empty_input_link(n):
    # Empty the input_link when input_decision is changed
    return [""]

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)