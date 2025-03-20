import pandas as pd

from MTGPricer import MTGPricer
from Card import Card

class MTGDeckPricer:
    """
    """
    class DeckInfo:
        """
        """
        def __init__(self, card_list, price_list, error_list):
            """
            """
            self.card_list = card_list
            self.price_list = price_list
            self.error_list = error_list

    def __init__(self):
        """
        """
        self.pricer = MTGPricer()
        # User's link type
        self.MOX = "MOX"
        self.TCG = "TCG"
        self.TXT = "TEXT"
        # Retailer names
        self.CK = "CardKingdom"
        self.CM = "Cardmarket"
        self.TP = "TCGPlayer"
        # Total pricing of the deck
        # self.TOTAL = "Total"

    def getDeckPrice(self, input_link, input_decision, input_retailer):
        """
        """
        match input_decision:
            case self.MOX: # WIP
                print("given Moxfield link")
                # with urllib.request.urlopen(urlrequester(input_link)) as url:
                #     soup = BeautifulSoup(url.read())
                #     print(soup.find_all(class_="decklist-card"))            
            case self.TCG: # WIP
                print("given TCG link")
            case self.TXT:
                print("given TEXT file")
                info = self.handleTextFile(input_link)
            case _:
                raise KeyError("invalid/missing input_decision.")

        # filter out retaliers
        info.price_list = info.price_list[info.price_list.Retailer.isin(input_retailer)]

        return info  

    
    def handleTextFile(self, input_link):
        """
        """
        card_list = []
        error_list = []
        all_prices = pd.DataFrame()

        with open("./TextFile/" + input_link) as f:
            for line in f.readlines():
            
                card = self.parseMoxfield(line)

                card_prices = self.pricer.getPaperPrice(card)

                # print(card_prices)

                if card_prices.empty:
                    # add unmatched list here
                    error_list.append(card)
                    continue
                
                card_list.append(card.name)

                if all_prices.empty:
                    all_prices = card_prices
                else:
                    # all_prices.add(card_prices, axis="columns", fill_value=0.0) 
                    all_prices[card.name] = card_prices[card.name]

        # sum columns (card_list) for each row (date)
        all_prices["Total"] = all_prices[card_list].sum(axis=1)

        return self.DeckInfo(
            card_list,
            all_prices,
            error_list
        )
    
    def parseMoxfield(self, line):
        """
        """
        line = line.split()
                
        num_included = int(line[0])
        
        name = line[1]
        for word in line[2:-2]:
            name += " " + word
        
        offset = -1
        printing = 0
        if line[-1] == "*F*":
            printing = 1
            offset = -2
        if line[-1] == "*E*":
            printing = 2
            offset = -2
            
        
        card_num = line[offset]

        is_promo = 0
        if card_num[-1] == 'p':
            is_promo = 1
            card_num = card_num[:-1]

        card_num = int(card_num)

        set_code = line[-1 + offset].strip("()")

        return Card(
            name,
            num_included,
            card_num,
            set_code,
            printing,
            is_promo
        )
    
# t = MTGDeckPricer()
# v = t.getDeckPrice("Rage.txt", "TEXT", ["tcgplayer"])
# print(v.card_list)
# print(v.error_list)
# print(v.price_list)