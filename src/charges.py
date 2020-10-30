class Charges():
    
    def __init__(self,path):
        self.__dicCharges = self.__read_charges(path)
        self.__dicChantiers = {}

    def __read_charges(path):
        charges = pd.read_excel(path)
        charges = chantier.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])

