from .plan_comptable import *
from .charges import *
import datetime as dt

class Postes():
    def __init__(self,planComptable):
        pc = planComptable.get_dataframe()
        nomPostes = []
        self.dicPostes = {}
        for index,row in pc.iterrows():
            value = row['POSTE']
            if not is_in_dic(str(value),nomPostes):
                nomPostes.append(str(value))

        for nom in nomPostes:
            self.dicPostes[nom] = pc.loc[pc['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','EX.','N° DE COMPTE','EX. '])
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['Dépenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0
            self.dicPostes[nom] = self.dicPostes[nom].set_index('SOUS POSTE')

    def __depenses_mois_chantier(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses du mois"] += round(row['Débit'] - row['Crédit'],2)
        return 0

    def __depenses_annee_chantier(self,row):
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses de l'année"] += round(row['Débit'] - row['Crédit'],2)
        return 0

    def calcul_chantier(self,dfChantier,mois):
        for index,row in dfChantier.iterrows():
            date = row['Date']
            if (date.month <= mois):
                self.__depenses_mois_chantier(row)
            self.__depenses_annee_chantier(row)

        #self.__calcul_total_chantier(mois)
    
    def __calcul_total_chantier(self,mois):
        totalmois = 0
        totalannee = 0
        for poste in self.dicPostes:
            for sousPoste in poste:
                totalannee += round(self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses de l'année"],2)
                totalmois += round(self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses du mois"],2)
        total = pd.DataFrame([[0,totalmois,totalannee,0,0,0]])
        self.dicPostes.append(total)
"""
plan = PlanComptable("~/Documents/DGB/Resultat_chantier/plan comptable/PLAN COMPTABLE DGB 2020.xlsx")
codes_missing = open("missing_numbers.txt","w")
cha = Charges("~/Documents/DGB/Resultat_chantier/Compte de charges/Compte de charges.xlsx",plan,codes_missing)
post = Postes(plan)
post.calcul_chantier(cha.get_raw_chantier('19-GP-ROSN'),6)
print(post.dicPostes['MO'])
"""
