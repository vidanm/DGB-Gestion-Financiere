from .chiffreaffaire import ChiffreAffaire
from .postesparent import ParentPoste
import pandas as pd

class Office(ParentPoste):

    def __init__(self,accounting_plan,expenses):
        """Trie les expenses de la structure par postes."""
        super(StructPoste,self).__init__(accounting_plan.get_pc_structure())
        self.expenses = expenses.get_struct()
        self.expensesglob = expenses.get_raw_expenses()
        for nom in self.nomPostes:
            self.categories[nom]['%CA MOIS'] = 0
            self.categories[nom]['%CA Cumul'] = 0

    def calculate_office(self,mois,annee):
        mois = int(mois)
        annee = int(annee)
        for _,row in self.expenses.iterrows():
            date = row['Date']
            if (row['POSTE'] in self.nomPostes):
                if (date.year == annee):
                    super(StructPoste,self)._depenses_annee(row)
                    if (date.month == mois):
                        super(StructPoste,self)._depenses_mois(row)
        self._ajoute_chiffre_affaire(mois,annee)

    def format_for_pdf(self):
        self.ajoute_total_poste()
        self.row_noms = [1] #On garde les positions des noms de poste pour pouvoir les colorier différemment
        for nom in self.nomPostes:
            if (self.nomPostes.index(nom) == 0):
                title = pd.DataFrame([[]],[nom])
                dfStruct = pd.DataFrame(self.categories[nom])
                dfStruct = title.append(dfStruct)
            else:
                self.row_noms.append(len(dfStruct)+1)
                title = pd.DataFrame([[]],[nom])
                dfStruct = dfStruct.append(title)
                dfStruct = dfStruct.append(self.categories[nom])

        return dfStruct

    def _ajoute_chiffre_affaire(self,mois,annee):
        ca = ChiffreAffaire(self.expensesglob)
        ca_mois = ca.calcul_ca_mois(mois,annee)
        ca_annee = ca.calcul_ca_annee(annee)
        for nom in self.nomPostes:
            for _,row in self.categories[nom].iterrows():
                depenses_mois = self.categories[nom].loc[row.name,'Dépenses du mois']
                depenses_cumul = self.categories[nom].loc[row.name,"Dépenses de l'année"]
                self.categories[nom].loc[row.name,'%CA MOIS'] = depenses_mois*100 / ca_mois
                self.categories[nom].loc[row.name,'%CA Cumul'] = depenses_cumul*100 / ca_annee

    def ajoute_total_poste(self):
        totalmois = 0
        totalannee = 0
        camois = 0
        caannee = 0
        for nom in self.nomPostes:
            for index,row in self.categories[nom].iterrows():
                totalmois += self.categories[nom].loc[row.name,"Dépenses du mois"]
                totalannee += self.categories[nom].loc[row.name,"Dépenses de l'année"]
                camois += self.categories[nom].loc[row.name,"%CA MOIS"]
                caannee += self.categories[nom].loc[row.name,"%CA Cumul"]

        total = pd.DataFrame(
                {"Dépenses du mois":[totalmois],
                    "Dépenses de l'année":[totalannee],
                    "%CA MOIS":[camois],
                    "%CA Cumul":[caannee]},["TOTAL"])
        
        self.categories[nom] = self.categories[nom].append(total)

