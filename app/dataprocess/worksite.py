from .categories import Categories
from .imports import get_worksite_expenses_csv
import pandas as pd
import os

class Worksite(Categories):

    def __init__(self,accounting_plan,worksite_name,csv_path="var/csv/"):
        """Trie les expenses d'un chantier par postes."""
        super(Worksite,self).__init__(accounting_plan.get_pc_chantier())
        self.worksite_name = worksite_name
        self.expenses = self.__get_all_data_of_worksite(accounting_plan)
        for name in self.category_names:
            self.categories[name]['Budget'] = 0
            self.categories[name]['RAD'] = 0
            self.categories[name]['PFDC'] = 0
            self.categories[name]['Ecart PFDC/Budget'] = 0

    def __get_all_data_of_worksite(self,accounting_plan):
        total = None
        for filename in os.listdir(self.csv_path):
            if self.worksite_name in filename and filename.endswith(".csv") :
                if total == None:
                    total = Expenses(get_worksite_expenses_csv(self.csv_path+filename),accounting_plan)
                else:
                    total += Expenses(get_worksite_expenses_csv(self.csv_path+filename),accounting_plan)
        return total
    
    def calculate_worksite(self,month,year,budget):
        for _,row in self.expenses.data.iterrows():
            date = row['Date']
            if (date.year <= annee):
                super(Worksite,self)._add_cumulative_expense(row)
                if (date.month == mois):
                    super(Worksite,self)._add_month_expense(row)
        
        self.__add_budget(budget)
        
    def __add_budget(self,budget):
        """Ajoute le budget dans les cases de postes correspondantes."""

        for _,row in budget.iterrows():
            try :
                self.categories[row['POSTE']].loc[row['SOUS-POSTE'],"Budget"] += round(row[self.worksite_name])
            except :
                raise ValueError("Le couple " + row['POSTE'] + " : " + row['SOUS-POSTE'] + "n'est pas présent dans le plan comptable")

    def add_rad(self,category,subcategory,rad):
        if rad.replace('.','').isnumeric():
            self.categories[category].loc[subcategory,"RAD"] = float(rad)

    def compose_pfdc_budget(self):
        """Calcul le pfdc et l'ecart pfdc budget."""
        for name in self.category_names:
            for _,row in self.categories[name].iterrows():
                pfdc = row['RAD'] + row["Dépenses de l'année"]
                self.categories[name].loc[row.name,"PFDC"] = pfdc
                self.categories[name].loc[row.name,"Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def add_category_total(self,name):
        totalmois = 0
        totalannee = 0
        totalbudget = 0
        totalrad = 0
        totalpfdc = 0
        totalecart = 0
        for index,row in self.categories[name].iterrows():
            totalannee += self.categories[name].loc[row.name,"Dépenses de l'année"]
            totalmois += self.categories[name].loc[row.name,"Dépenses du mois"]
            totalbudget += self.categories[name].loc[row.name,"Budget"]
            totalrad += self.categories[name].loc[row.name,"RAD"]
            totalpfdc += self.categories[name].loc[row.name,"PFDC"]
            totalecart += self.categories[name].loc[row.name,"Ecart PFDC/Budget"]

        total = pd.DataFrame(
                {"Dépenses de l'année":[totalannee],
                    "Dépenses du mois":[totalmois],
                    "Budget":[totalbudget],
                    "RAD":[totalrad],
                    "PFDC":[totalpfdc],
                    "Ecart PFDC/Budget":[totalecart]},["TOTAL"])

        self.categories[name] = self.categories[name].append(total)

    def add_worksite_total(self):
        """Calcul du total des dépenses."""
        for name in self.category_names:
            self.add_category_total(name)

    def calcul_ges_prev(self):
        """Calcul la gestion previsionnelle une fois que ttes les autres données ont été calculées."""
        for name in self.category_names:
            if name != "PRODUITS":
                if self.category_names.index(name) == 0:
                    gesprev = pd.DataFrame(columns=self.categories[name].columns.copy())
                line = self.categories[name].iloc[-1]
                line.name = name
                gesprev = gesprev.append(line,ignore_index=False)

        self.category_names.append("GESPREV")
        self.categories["GESPREV"] = gesprev
        self.add_category_total("GESPREV")

