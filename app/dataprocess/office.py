from .revenues import Revenues
from .categories import Categories
import pandas as pd

class Office(Categories):

    def __init__(self,accounting_plan,year_expenses,csv_path="/var/csv"):
        """Trie les expenses de la structure par postes."""
        super(StructPoste,self).__init__(accounting_plan.get_pc_structure())
        self.expenses = expenses.get_struct()
        self.expensesglob = expenses.get_raw_expenses()
        for name in self.namePostes:
            self.categories[name]['%CA MOIS'] = 0
            self.categories[name]['%CA Cumul'] = 0

    def calculate_office(self,mois,annee):
        mois = int(mois)
        annee = int(annee)
        for _,row in self.expenses.iterrows():
            date = row['Date']
            if (row['POSTE'] in self.namePostes):
                if (date.year == annee):
                    super(StructPoste,self)._depenses_annee(row)
                    if (date.month == mois):
                        super(StructPoste,self)._depenses_mois(row)
        self._ajoute_chiffre_affaire(mois,annee)

    def format_for_pdf(self):
        self.ajoute_total_poste()
        self.row_names = [1] #On garde les positions des names de poste pour pouvoir les colorier différemment
        for name in self.namePostes:
            if (self.namePostes.index(name) == 0):
                title = pd.DataFrame([[]],[name])
                dfStruct = pd.DataFrame(self.categories[name])
                dfStruct = title.append(dfStruct)
            else:
                self.row_names.append(len(dfStruct)+1)
                title = pd.DataFrame([[]],[name])
                dfStruct = dfStruct.append(title)
                dfStruct = dfStruct.append(self.categories[name])

        return dfStruct

    def _add_revenues(self,mois,annee):
        revenues = Revenues(self.year_expense.data)
        month_revenue = revenues.calculate_month_revenues(self.year_expense.data)
        #year_revenue = revenues.calculate_year_revenues
        ca_mois = ca.calcul_ca_mois(mois,annee)
        ca_annee = ca.calcul_ca_annee(annee)
        for name in self.namePostes:
            for _,row in self.categories[name].iterrows():
                depenses_mois = self.categories[name].loc[row.name,'Dépenses du mois']
                depenses_cumul = self.categories[name].loc[row.name,"Dépenses de l'année"]
                self.categories[name].loc[row.name,'%CA MOIS'] = depenses_mois*100 / ca_mois
                self.categories[name].loc[row.name,'%CA Cumul'] = depenses_cumul*100 / ca_annee

    def add_category_total(self,name):
        totalmois = 0
        totalannee = 0
        camois = 0
        caannee = 0
        for index,row in self.categories[name].iterrows():
            totalmois += self.categories[name].loc[row.name,"Dépenses du mois"]
            totalannee += self.categories[name].loc[row.name,"Dépenses de l'année"]
            camois += self.categories[name].loc[row.name,"%CA MOIS"]
            caannee += self.categories[name].loc[row.name,"%CA Cumul"]

        total = pd.DataFrame(
                {"Dépenses du mois":[totalmois],
                    "Dépenses de l'année":[totalannee],
                    "%CA MOIS":[camois],
                    "%CA Cumul":[caannee]},["TOTAL"])
        
        self.categories[name] = self.categories[name].append(total)

    def add_office_total(self):
        for name in self.category_names:
            self.add_category_total(name)
