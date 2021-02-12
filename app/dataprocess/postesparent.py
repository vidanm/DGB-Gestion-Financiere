from .plan_comptable import *
from .charges import *
import datetime as dt

class ParentPoste():

    def __init__(self,dfPlanComptable):
        self.nomPostes = []
        self.dicPostes = {}
        for index,row in dfPlanComptable.iterrows():
            value = row['POSTE']
            if not is_in_dic(str(value),self.nomPostes):
                self.nomPostes.append(str(value))

        for nom in self.nomPostes:
            # C'EST ICI CE QU'IL FAUT CORRIGER
            self.dicPostes[nom] = dfPlanComptable.loc[dfPlanComptable['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','N° DE COMPTE','EX.'])
            self.dicPostes[nom]['Dépenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom] = self.dicPostes[nom].set_index('SOUS POSTE')

    def _depenses_mois(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses du mois"] += round(row['Débit'] - row['Crédit'],2)
    
    def _depenses_annee(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses de l'année"] += round(row['Débit'] - row['Crédit'],2)

    def round_2dec_df(self):
        for nom in self.dicPostes.keys():
            self.dicPostes[nom] = self.dicPostes[nom].round(2)

    def get_postes_names(self):
        return self.nomPostes

    def remove_poste(self,poste):
        self.dicPostes.pop(poste)
        

