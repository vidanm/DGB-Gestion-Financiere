from .plan_comptable import *
from .charges import *
import datetime as dt
from .read_file import read_budget
from .postesparent import ParentPoste

class ChantierPoste(ParentPoste):

    def __init__(self,planComptable,dfChantier):
        super.__init__(planComptable)
        self.charges = dfChantier
        for nom in self.nomPostes:
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0

    
    def calcul_chantier(mois,annee):
        for index,row in self.charges.iterrows():
            date = row['Date']
            if (date.year == annee):
                super._depenses_annees(row)
                if (date.month == mois):
                    super._depenses_mois(row)
                    
    def _ajoute_budget_chantier(self,dfBudget):
        '''Ajoute le budget dans les cases de postes correspondantes'''
        for index,row in dfBudget.iterrows():
            self.dicPostes[row['POSTE']].loc[row['SOUS-POSTE'],"Budget"] += round(row[self.codeChantier])


    def calcul_pfdc_budget(self,dfBudget):
        '''Calcul le pfdc et l'ecart pfdc budget'''
        self._ajoute_budget_chantier(dfBudget)
        for nom in self.nomPostes:
            for index,row in self.dicPostes[nom].iterrows():
                print(row)
                pfdc = row['RAD'] + row["Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,"PFDC"] = round(pfdc)
                self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def calcul_total_chantier(self,mois):
        '''Calcul du total des dépenses'''
        totalmois = 0
        totalannee = 0
        for poste in self.dicPostes:
            for sousPoste in poste:
                totalannee += self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses de l'année"]
                totalmois += self.dicPostes[self.dicPostes[poste].loc[sousPoste],"Dépenses du mois"]
                total = pd.DataFrame([[0,totalmois,totalannee,0,0,0]])
                self.dicPostes.append(total)
