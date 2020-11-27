from .charges import *
import pandas as pd
import datetime as dt

class Synthese():
    
    def __init__(self,charges):
        self.charges = charges
        self.synthese_annee = pd.DataFrame(None,None,columns=['CHANTIER','BUDGET','DEP. DU MOIS','DEP. CUMULEES','PFDC','MARGE THEORIQUE (€)','MARGE THEORIQUE (%)','MARGE BRUTE (€)','MARGE BRUTE (%)'])
        self.synthese_cumul = self.synthese_annee.copy(deep=True)

    def ajoute_synthese_annee(self,annee):
        
    def ajoute_synthese_cumul(self):

    def calcul_synthese(self,mois,annee):
        chantier_names = self.charges.get_chantier_names()
        for name in chantier_names:
            for index,row in self.charges.get_raw_chantier(name):
                if (row['Date'].year == annee):
                    row_annee

        return
