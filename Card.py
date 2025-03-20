class Card:
    """
    """
    def __init__(self, name, numof, card_num, 
                 set_code, printing, is_promo):
        """
        """
        self.name = name
        self.numof = numof
        self.card_num = card_num
        self.set_code = set_code
        self._printing = printing # 0 = normal | 1 = foil | 2 = etched
        self.is_promo = is_promo

    def to_dict(self):
        return self.__dict__

    def getPrinting(self):
        """
        source https://mtgjson.com/data-models/price/price-points/
        """
        match self._printing:
            case 0:
                return "normal"
            case 1:
                return "foil"
            case 2:
                return "etched"
            case _:
                raise KeyError("Invalid printing was used, please use 0,1, or 2.")
