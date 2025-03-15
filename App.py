from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, ctx  # pip install dash (version 2.0.0 or higher)
from dash.exceptions import PreventUpdate
import urllib.request
from io import BytesIO
from zipfile import ZipFile

app = Dash(__name__)

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
        options=[MOX, TCG, TEXT],
        value=TEXT,
    ),

    dcc.Checklist(
        id="input_retailer",
        options=[TP, CK, CM],
        value=[TP],
        inline=True,
    ),

    dcc.Graph(id='price_plot', figure={})
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='price_plot', component_property='figure')],
    [Input(component_id='input_link', component_property='value')], 
    [State(component_id="input_decision", component_property="value"),
     State(component_id="input_retailer", component_property="value")]
)
def update_graph(input_link, input_decision, input_retailer):

    if input_link == '' or len(input_retailer) == 0:
        raise PreventUpdate

    total_p = pd.DataFrame()
    card_list = [TOTAL]

    if input_decision == MOX:
        print("given Moxfield link")
        with urllib.request.urlopen(urlrequester(input_link)) as url:
            soup = BeautifulSoup(url.read())
            print(soup.find_all(class_="decklist-card"))
    elif input_decision == TCG:
        print("given TCG link")
    else:
        print("given TEXT file")
        with open(input_link) as f:
            for line in f.readlines():
                
                card = datasplit(line)
                name = card["name"]
                temp_p = cardprice(card)

                if temp_p.empty:
                    continue
                
                card_list.append(name)

                if total_p.empty:
                    total_p = temp_p
                else:
                    total_p[TOTAL] = total_p[TOTAL] + temp_p[TOTAL]
                    total_p[name] = temp_p[name]


    print("MASK")
    print(total_p[total_p.Retailer.isin(input_retailer)])
    # mask = any(item in input_retailer[0] for item in total_p["Retailer"])
    # print(total_p[mask])
    fig = px.line(total_p[total_p.Retailer.isin(input_retailer)], x="Date", y=card_list, facet_col="Retailer" , markers=True)
    # fig = px.line(total_p, x="Date", y=card_list, facet_col="Retailer" , markers=True)
    fig.update_layout(legend_title="Cards", yaxis_title="Price (USD)",)
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name != TOTAL else {})
    # fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name != TOTAL else {})
    print("here")
    return [go.Figure(data=fig)]

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