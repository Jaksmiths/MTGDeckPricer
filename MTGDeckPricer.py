import pandas as pd

from MTGPricer import MTGPricer

class MTGDeckPricer:
    """
    """

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
        self.TOTAL = "Total"

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
                self.handleTextFile(input_link)
            case _:
                raise KeyError("invalid/missing input_decision.")

        mask = total_p[total_p.Retailer.isin(input_retailer)]       

    
    def handleTextFile(self, input_link):
        card_list = [self.TOTAL]
        all_prices = pd.DataFrame()

        with open("./TextFile/" + input_link) as f:
            for line in f.readlines():
                
                card_info = self.datasplit(line)
                
                card_prices = self.pricer.getPaperPrice(card_info["card_num"], card_info["set_code"])

                if card_prices.empty:
                    continue
                
                card_list.append(name)

                if all_prices.empty:
                    total_p = temp_p
                else:
                    total_p[TOTAL] = total_p[TOTAL] + temp_p[TOTAL]
                    total_p[name] = temp_p[name]

        return {
            "card_list": card_list,
            "all_prices": all_prices
        }

    def datasplit(self, line):
        line = line.split()
        
        # Num of this cards in the deck
        num_included = int(line[0])
        # Card's print number
        card_num = line[-1]
        # Set cards was in
        set = line[-2].strip("()").upper()
        
        return {
            "set_code": set,
            "num": num_included,
            "card_num": card_num,
        }

        