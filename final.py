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

# Constants ---
# user's link type
MOX = "MOX"
TCG = "TCG"
TEXT = "TEXT"
# retailer names
CK = "CardKingdom"
CM = "Cardmarket"
TP = "TCGPlayer"
# total pricing of the deck
TOTAL = "Total"

# Pricing
total_p = pd.DataFrame()

# ------------------------------------------------------------------------------
# Import data
def urlrequester(url):
    return urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} )

reqprice = urlrequester("https://mtgjson.com/api/v5/AllPrices.json.zip")
reqcards = urlrequester("https://mtgjson.com/api/v5/AllPrintings.json.zip")

# Grab Price Data
print("SETUP: grabbing price data")
with urllib.request.urlopen(reqprice) as url:
    zipf = ZipFile(BytesIO(url.read()))
    price_list = pd.read_json(zipf.open("AllPrices.json"))
# Grab Card Data
print("SETUP: grabbing card data")
with urllib.request.urlopen(reqcards) as url:
    zipf = ZipFile(BytesIO(url.read()))
    printing_list = pd.read_json(zipf.open("AllPrintings.json"))
    printing_list = printing_list.drop(index=["version", "date"], columns="meta")
    printing_list = printing_list.transpose()
    

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
    print(input_link)
    print(input_decision)
    print(input_retailer)

    if invalidlink(input_link) or len(input_retailer) == 0:
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

def invalidlink(link):
    return link == ''

# Handles a line from the input and gets card data
def datasplit(line):
    line = line.split()
    
    # Num of this cards in the deck
    num_included = int(line[0])
    # Card's print number
    card_num = line[-1]
    # Set cards was in
    set = line[-2].strip("()").upper()
    
    # Name of the card
    name = line[1]
    for word in line[2:-2]:
        name += " " + word
    
    # MTGJSON's unique idenifier for the card (Change to Binary Search to improv.)
    uuid = ""
    df = printing_list[set]["data"]["cards"]
    for card in df:
        if card["name"] == name and card["number"] == card_num:
            if "//" in line:
                uuid = [card["otherFaceIds"][0], card["uuid"]]
            else:
                uuid = [card["uuid"]]
            break

    content = {
        "name": name,
        "uuid": uuid,
        "numof": num_included,
        "cardnum": card_num,
    }

    return content

# Given a dict cardinfo containing the card's info, returns pricing info as dict
def cardprice(cardinfo):
    # Pricing data for the paper (NOT digital) card
    listing = pd.DataFrame()
    for uuid in cardinfo["uuid"]:
        if uuid in price_list["data"].index.tolist():
            pricing = price_list["data"][uuid]["paper"]
            numof = cardinfo["numof"]
            name = cardinfo["name"]

            if "tcgplayer" in pricing and "retail" in pricing["tcgplayer"]:
                listing = pd.concat([listing, pricehistory(pricing["tcgplayer"]["retail"], numof, name, TP)], ignore_index=True)
                # listing.append(pricehistory(pricing["tcgplayer"]["retail"], numof, name, TP))
                print(listing)
            
            if "cardkingdom" in pricing and "retail" in pricing["cardkingdom"]:
                listing = pd.concat([listing, pricehistory(pricing["cardkingdom"]["retail"], numof, name, CK)], ignore_index=True)
                print(listing)
                # listing.append(pricehistory(pricing["cardkingdom"]["retail"], numof, name, CK))
            
            if "cardmarket" in pricing and "retail" in pricing["cardmarket"]:
                listing = pd.concat([listing, pricehistory(pricing["cardmarket"]["retail"], numof, name, CM)], ignore_index=True)
                print(listing)
                # listing.append(pricehistory(pricing["cardmarket"]["retail"], numof, name, CM))

            print(listing)
    return listing

# returns paper retail prices
def pricehistory(pricing, numof, name, retailer):
    if "normal" in pricing.keys():
        # if nonfoil exists use that pricing
        price = pricing["normal"]
    else:
        # else use the foil pricing
        price = pricing["foil"]

    for date, cost in price.items():
        price[date] = cost * numof

    # print(price)

    costs = list(price.values())
    dates = list(price.keys())
    # print(costs)
    # print(dates)

    test = pd.DataFrame(data={TOTAL: costs, "Date": dates, "Retailer": [retailer] * len(price), name: costs }, 
                        columns=[TOTAL, "Date", "Retailer", name])
    return test

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