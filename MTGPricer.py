from MTGFetcher import MTGFetcher

class MTGPricer():
    """Fetch MTG card prices and other information
    """

    def __init__(self):
        """
        """
        fetcher = MTGFetcher()
        self.prices = fetcher.getPrices()
        self.printings = fetcher.getPrintings()

    def getCard(self, card_num, set_code):
        """
        """
        return self.printings.loc[set_code.upper()].loc["data"]["cards"][card_num - 1]
    
    def getPaperPrice(self, card_num, set_code):
        """
        """
        # Grab card's uuid
        uuid = self.getCard(card_num, set_code)["uuid"]
        # Grab card's price history in paper format
        return self.prices.loc[uuid].loc["data"]["paper"]



