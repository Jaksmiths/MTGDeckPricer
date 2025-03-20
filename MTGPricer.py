import pandas as pd

from MTGFetcher import MTGFetcher
from Card import Card

class MTGPricer():
    """Fetch MTG card prices and other information
    """

    def __init__(self):
        """
        """
        fetcher = MTGFetcher()
        self.prices = fetcher.getPrices()
        self.printings = fetcher.getPrintings()
        self.retailers = ["cardkingdom", "cardmarket", "cardsphere", "tcgplayer"]

    def getCard(self, card):
        """
        """
        return self.printings.loc[card.set_code.upper()].loc["data"]["cards"][card.card_num - 1]
    
    def getPaperPrice(self, card):
        """
        """
        # Grab card's uuid
        uuid = self.getCard(card)["uuid"]
        # Grab card's price history in paper format
        if uuid not in self.prices.index:
            return pd.DataFrame()
        price_list = self.prices.loc[uuid].loc["data"]["paper"]
        #             Date   Retailer  Whelming Wave
        # 0     2024-12-13  TCGPlayer           2.35
        temp_list = pd.DataFrame()
        for retailer in self.retailers:
            if (price_list[retailer]["currency"] != "USD" or
                "retail" not in price_list[retailer] or
                card.getPrinting() not in price_list[retailer]["retail"]):
                continue

            # { <YYYY-MM-DD>: <Float>, ... } | { date: price, ... }
            retail_list = price_list[retailer]["retail"][card.getPrinting()]

            retail_list = pd.DataFrame(data={"Date": retail_list.keys(), 
                                             "Retailer": [retailer] * len(retail_list), 
                                             card.name: retail_list.values() }, 
                                       columns=["Date", 
                                                "Retailer", 
                                                card.name])
            temp_list = pd.concat([temp_list, retail_list], ignore_index=True)
        return temp_list