from .plan_comptable import *
from .charges import *
import datetime as dt
from .read_file import read_budget

class ParentPoste():
    
    def __init__(self,planComptable):
        pc = planComptable.get_dataframe()
        self.nomPostes = []
        self.dicPostes = {}
        for index,row in pc.iterrows():
            value = row['POSTE']
            if not is_in_dic(str(value),self.nomPostes):
                self.nomPostes.append(str(value))

        for nom in self.nomPostes:
            self.dicPostes[nom] = pc.loc['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','EX.','N° DE COMPTE','EX. '])
            self.dicPostes[nom]['Dépenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom] = self.dicPostes[nom].set_index('SOUS POSTE')

    def _depenses_mois(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses du mois"] += round(row['Débit'] - row['Crédit'],2)
        return 0;

    def _depenses_annee(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses de l'année"] += round(row['Débit'] - row['Crédit'],2)
        return 0;

    def round_2dec_df(self):
        for nom in self.nomPostes:
            self.dicPostes[nom] = self.dicPostes[nom].round(2)

    def get_postes_names(self):
        return self.nomPostes

        

