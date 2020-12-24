from .plan_comptable import *
from .charges import *
from .chiffreaffaire import *
import datetime as dt
from .postesparent import ParentPoste

class StructPoste(ParentPoste):
    def __init__(self,planComptable,charges):
        super(StructPoste,self).__init__(planComptable.get_pc_structure())
        self.charges = charges.get_struct()
        self.chargesglob = charges.get_raw_charges()
        for nom in self.nomPostes:
            self.dicPostes[nom]['%CA MOIS'] = 0
            self.dicPostes[nom]['%CA Cumul'] = 0

    def calcul_structure(self,mois,annee):
        for index,row in self.charges.iterrows():
            date = row['Date']
            print(row)
            if (date.year == annee):
                super(StructPoste,self)._depenses_annee(row)
                if (date.month == mois):
                    super(StructPoste,self)._depenses_mois(row)
        self._ajoute_chiffre_affaire(mois,annee)

    def _ajoute_chiffre_affaire(self,mois,annee):
        ca = ChiffreAffaire(self.chargesglob)
        ca_mois = ca.calcul_ca_mois(mois,annee)
        ca_annee = ca.calcul_ca_annee(annee)
        for nom in self.nomPostes:
            for index,row in self.dicPostes[nom].iterrows():
                depenses_mois = self.dicPostes[nom].loc[row.name,'Dépenses du mois']
                depenses_cumul = self.dicPostes[nom].loc[row.name,"Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,'%CA MOIS'] = depenses_mois / ca_mois
                self.dicPostes[nom].loc[row.name,'%CA Cumul'] = depenses_cumul / ca_annee
    
