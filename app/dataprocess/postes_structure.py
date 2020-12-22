from .plan_comptable import *
from .charges import *
from .chiffreaffaire import *
import datetime as dt
from .postesparent import ParentPoste

class StructPoste(ParentPoste):
    def __init__(self,planComptable,dfStruct):
        super.__init__(planComptable)
        self.charges = dfStruct
        for nom in self.nomPostes
            self.dicPostes[nom]['%CA MOIS'] = 0
            self.dicPostes[nom]['%CA Cumul'] = 0

    def calcul_structure(mois,annee):
        for index,row in self.charges.iterrows():
            date = row['Date']
            if (date.year == annee):
                super._depenses_annee(row)
                if (date.month == mois):
                    super._depenses_mois(row)

    def _ajoute_chiffre_affaire(mois,annee):
        ca = ChiffreAffaire(self.charges)
        ca_mois = ca.calcul_ca_mois(mois,annee)
        ca_annee = ca.calcul_ca_annee(annee)
        for nom in self.nomPostes:
            #self.dicPostes[nom]['%CA MOIS'] =
            print("")
    
