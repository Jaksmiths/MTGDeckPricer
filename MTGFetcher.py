from Fetcher import Fetcher

class MTGFetcher(Fetcher):
    """Fetch MTGJSON json.zip files online into pandas dataframes
    """

    def __init__(self):
        super().__init__()
        self.MTGJSON = "https://mtgjson.com/api/v5/"
        self.PRICE = "AllPrices.json"
        self.PRINTING = "AllPrintings.json"

    def processMTGJSON(self, filename):
        """Builds url request then cleans up the returned dataframe object

        Args:
            filename: MTGJSON json.zip string file name
        
        Returns:
            pandas dataframe of the data, minus meta data
        """
        request = self.urlRequester(self.MTGJSON + filename + ".zip")
        file = self.fetchRequester(request, filename).drop(index=["version", "date"], columns="meta")
        return file

    def getPrices(self):
        """Get a list of MTG card prices, uuid -> price list
        
        uuid {
            mtgo: <'cardhoarder', PriceList[]>;
            paper: <'cardkingdom' | 'cardmarket' | 'cardsphere' | 'tcgplayer', PriceList[]>;
        }

        Returns:
            pandas dataframe with indices of uuid with data of it's price list
        """
        return self.processMTGJSON(self.PRICE)

    def getPrintings(self):
        """Get a list of MTG card uuids, set code -> card set

        set code {
            ...
            cards: CardSet[]
        }

        Returns:
            pandas dataframe with indices of set code (uppercase) 
            with data of it's card set 
            (sorted by colorless, WUBERG, multicolor, artifact, land with each alphabetical)
        """
        return self.processMTGJSON(self.PRINTING)


# test = MTGFetcher()

# print("SETUP: grabbing price data")
# price_list = test.getPrices()
# print(price_list)
# print(price_list.loc["4fde93cb-8afc-5fcf-8464-dd32f91794c2"].loc["data"]["paper"])

# print("SETUP: grabbing card data")
# printing_list = test.getPrintings()
# print(printing_list)
# print((printing_list.loc["C21"].loc["data"]["cards"][409-1]["uuid"]))

# EXAMPLE: 1
# 1 Yavimaya Coast (c21) 409
# print((printing_list.loc["C21"].loc["data"]["cards"][409 - 1]))


# EXAMPLE 2:
# 1 Tatyova, Benthic Druid (dom) 206

# either use the card # to index the set (card # - 1) OR linear search

