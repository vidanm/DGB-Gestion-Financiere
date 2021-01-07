from .plan_comptable import *
from .charges import *
import datetime as dt
from .read_file import read_budget
from .postesparent import ParentPoste

class ChantierPoste(ParentPoste):

    def __init__(self,planComptable,charges,codeChantier):
        super(ChantierPoste,self).__init__(planComptable.get_pc_chantier())
        self.charges = charges.get_raw_chantier(codeChantier)
        self.codeChantier = codeChantier
        for nom in self.nomPostes:
            self.dicPostes[nom]['Budget'] = 0
            self.dicPostes[nom]['RAD'] = 0
            self.dicPostes[nom]['PFDC'] = 0
            self.dicPostes[nom]['Ecart PFDC/Budget'] = 0

    
    def calcul_chantier(self,mois,annee,dfBudget):
        for index,row in self.charges.iterrows():
            date = row['Date']
            if (date.year == annee):
                super(ChantierPoste,self)._depenses_annee(row)
                if (date.month == mois):
                    super(ChantierPoste,self)._depenses_mois(row)
        self.calcul_pfdc_budget(dfBudget)
        self.calcul_total_chantier(mois)
                    
    def _ajoute_budget_chantier(self,dfBudget):
        '''Ajoute le budget dans les cases de postes correspondantes'''
        for index,row in dfBudget.iterrows():
            self.dicPostes[row['POSTE']].loc[row['SOUS-POSTE'],"Budget"] += round(row[self.codeChantier])

    
    def calcul_pfdc_budget(self,dfBudget):
        '''Calcul le pfdc et l'ecart pfdc budget'''
        self._ajoute_budget_chantier(dfBudget)
        for nom in self.nomPostes:
            for index,row in self.dicPostes[nom].iterrows():
                pfdc = row['RAD'] + row["Dépenses de l'année"]
                self.dicPostes[nom].loc[row.name,"PFDC"] = pfdc
                self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def calcul_total_chantier(self,mois):
        '''Calcul du total des dépenses'''
        for nom in self.nomPostes:
            totalmois = 0
            totalannee = 0
            totalbudget = 0
            totalrad = 0
            totalpfdc = 0
            totalecart = 0
            for index,row in self.dicPostes[nom].iterrows():
                totalannee += self.dicPostes[nom].loc[row.name,"Dépenses de l'année"]
                totalmois += self.dicPostes[nom].loc[row.name,"Dépenses du mois"]
                totalbudget += self.dicPostes[nom].loc[row.name,"Budget"]
                totalrad += self.dicPostes[nom].loc[row.name,"RAD"]
                totalpfdc += self.dicPostes[nom].loc[row.name,"PFDC"]
                totalecart += self.dicPostes[nom].loc[row.name,"Ecart PFDC/Budget"]

            total = pd.DataFrame(
                    {"Dépenses de l'année":[totalannee],
                        "Dépenses du mois":[totalmois],
                        "Budget":[totalbudget],
                        "RAD":[totalrad],
                        "PFDC":[totalpfdc],
                        "Ecart PFDC/Budget":[totalecart]},["TOTAL"])
            self.dicPostes[nom] = self.dicPostes[nom].append(total)

    def calcul_ges_prev(self):
        '''Calcul la gestion previsionnelle une fois que ttes 
        les autres données ont été calculées'''
        for nom in self.nomPostes:
            if self.nomPostes.index(nom) == 0:
                gesprev = pd.DataFrame(self.dicPostes[nom].iloc[-1])
            else :
                gesprev = gesprev.append(self.dicPostes[nom].iloc[-1],ignore_index=True)
        return gesprev

