from .categories import Categories
from .imports import get_csv_expenses
from .expenses import Expenses
from .revenues import Revenues
import datetime
import pandas as pd
import os
import logging


class Worksite(Categories):
    def __init__(self, accounting_plan, worksite_name, csv_path="var/csv/"):
        """Trie les expenses d'un chantier par postes."""
        super(Worksite, self).__init__(accounting_plan.get_worksite_plan())
        self.csv_path = csv_path
        self.worksite_name = worksite_name
        self.expenses = self.__get_all_data_of_worksite(accounting_plan)
        self.cumul_expenses = 0
        self.year_expenses = 0
        if self.expenses is None:
            raise ValueError("Pas de dépenses pour ce chantier pour ce mois")

        for name in self.category_names:
            self.categories[name]['Budget'] = 0
            self.categories[name]['RAD'] = 0
            self.categories[name]['PFDC'] = 0
            self.categories[name]['Ecart PFDC/Budget'] = 0

    def __get_all_data_of_worksite(self, accounting_plan):
        total = None
        for filename in os.listdir(self.csv_path):
            if self.worksite_name in filename and filename.endswith(".csv"):
                if (os.stat(self.csv_path + filename).st_size != 0):
                    print(filename)
                    if total is None:
                        total = Expenses(
                            get_csv_expenses(self.csv_path + filename),
                            accounting_plan)
                    else:
                        total += Expenses(
                            get_csv_expenses(self.csv_path + filename),
                            accounting_plan)
        return total

    def calculate_year_expenses(self, month, year):
        df = self.expenses.data
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df['Month'] = pd.DatetimeIndex(df['Date']).month

        exp = df.loc[(year == df['Year']) & (month >= df['Month'])]
        exp = exp.loc[(exp['Général'].astype(str).str.slice(stop=1) != '7')]

        return exp['Débit'].astype(float).sum() - exp['Crédit'].astype(
            float).sum()

    def calculate_cumul_expenses(self, month, year):
        df = self.expenses.data
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df['Month'] = pd.DatetimeIndex(df['Date']).month

        exp = df.loc[(year > df['Year']) | ((year == df['Year'])
                                            & (month >= df['Month']))]

        exp = exp.loc[(exp['Général'].astype(str).str.slice(stop=1) != '7')]

        print(exp.loc[exp['Débit'] == '19-PRO-NLG'])
        return exp['Débit'].astype(float).sum() - exp['Crédit'].astype(
            float).sum()

    def calculate_worksite(self, month, year, budget=None, only_year=False):

        if only_year:
            for _, row in self.expenses.data.iterrows():
                date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d")
                if (date.year == year and date.month <= month):
                    super(Worksite, self)._add_cumulative_expense(row)
                    if (date.month == month):
                        super(Worksite, self)._add_month_expense(row)

        else:
            for _, row in self.expenses.data.iterrows():
                date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d")
                if (date.year < year) or (date.month <= month
                                          and date.year == year):
                    super(Worksite, self)._add_cumulative_expense(row)
                    if (date.month == month and date.year == year):
                        super(Worksite, self)._add_month_expense(row)

        if (budget is not None):
            self.__add_budget(budget)

    def __add_budget(self, budget):
        """
        Ajoute le budget dans les cases de postes correspondantes.
        """
        logging.basicConfig(filename="log.txt",
                            format='%(message)s',
                            filemode='a+')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        not_used_rows = [
            "PRIX DE VENTE", "TOTAL", "ECART", "MONTANT MARCHE", "AVENANTS"
        ]
        for _, row in budget.iterrows():
            try:
                row[self.worksite_name]
            except Exception:
                logger.warning("Pas de budget associé a ce chantier")
                logging.shutdown()
                return
            try:
                if row['POSTE'] not in not_used_rows:
                    self.categories[row['POSTE']].loc[row['SOUS-POSTE'],
                                                      "Budget"] += round(row[
                                                          self.worksite_name])
            except Exception:
                logger.error("Le couple " + row['POSTE'] + " : " +
                             row['SOUS-POSTE'] +
                             " spécifié dans le fichier budget\
                             n'est pas un couple\
                             présent dans le plan comptable")
        logging.shutdown()
        return 1

    def add_rad(self, category, subcategory, rad):
        if rad.replace('.', '').isnumeric():
            self.categories[category].loc[subcategory, "RAD"] = float(rad)

    def get_pfdc_total(self):
        total = 0
        for name in self.category_names:
            if (name != 'PRODUITS' and name != 'DIVERS'):
                total += self.categories[name]['PFDC'][-1]
        return total

    def compose_pfdc_budget(self):
        """
        Calcul le pfdc et l'ecart pfdc budget.
        """
        for name in self.category_names:
            for _, row in self.categories[name].iterrows():
                pfdc = row['RAD'] + row["Dépenses cumulées"]
                self.categories[name].loc[row.name, "PFDC"] = pfdc
                self.categories[name].loc[
                    row.name, "Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def add_category_total(self, name):
        """
        Ajoute le total d'un poste à la fin de son tableau
        """
        totalmois = 0
        totalannee = 0
        totalbudget = 0
        totalrad = 0
        totalpfdc = 0
        totalecart = 0
        for index, row in self.categories[name].iterrows():
            totalannee += self.categories[name].loc[row.name,
                                                    "Dépenses cumulées"]
            totalmois += self.categories[name].loc[row.name,
                                                   "Dépenses du mois"]
            totalbudget += self.categories[name].loc[row.name, "Budget"]
            totalrad += self.categories[name].loc[row.name, "RAD"]
            totalpfdc += self.categories[name].loc[row.name, "PFDC"]
            totalecart += self.categories[name].loc[row.name,
                                                    "Ecart PFDC/Budget"]

        total = pd.DataFrame(
            {
                "Dépenses cumulées": [totalannee],
                "Dépenses du mois": [totalmois],
                "Budget": [totalbudget],
                "RAD": [totalrad],
                "PFDC": [totalpfdc],
                "Ecart PFDC/Budget": [totalecart]
            }, ["TOTAL"])

        self.categories[name] = self.categories[name].append(total)

    def add_worksite_total(self):
        """
        Calcul du total des dépenses.
        """
        for name in self.category_names:
            self.add_category_total(name)

    def calcul_divers_result(self, year):
        # Format divers tab and return result tab

        self.categories["DIVERS"] = self.categories["DIVERS"].drop(
            columns=['Budget', 'RAD', 'PFDC', 'Ecart PFDC/Budget'])

        ca_cumul = Revenues(self.expenses.data)\
            .calculate_year_revenues(year)

        dep_cumul = 0
        for key in self.categories.keys():
            dep_cumul += self.categories[key]["Dépenses cumulées"].sum()

        marge = ca_cumul - dep_cumul
        marge_percent = (marge / ca_cumul) * 100
        data = [[ca_cumul, dep_cumul, marge, marge_percent]]
        row_index = ["Resultat"]
        column_indexes = [
            'CA Cumulé', 'Dépenses cumulées', 'Marge brute', 'Marge brute %'
        ]

        out = pd.DataFrame(data=data, index=row_index, columns=column_indexes)

        out['CA Cumulé'] = out['CA Cumulé']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Dépenses cumulées'] = out['Dépenses cumulées']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Marge brute'] = out['Marge brute']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Marge brute %'] = out['Marge brute %']\
            .apply("{:0,.2f}%".format)

        return out

    def calcul_ges_prev(self):
        """
        Calcul la gestion previsionnelle une fois que \
                ttes les autres données ont été calculées.
        """
        for name in self.category_names:
            if name != "PRODUITS" and name != "DIVERS":
                if self.category_names.index(name) == 0:
                    gesprev = pd.DataFrame(
                        columns=self.categories[name].columns.copy())
                line = self.categories[name].iloc[-1]
                line.name = name
                gesprev = gesprev.append(line, ignore_index=False)

        self.category_names.append("GESPREV")
        self.categories["GESPREV"] = gesprev
        self.add_category_total("GESPREV")

    def get_formatted_data(self, category_name):
        formatted = self.categories[category_name].copy()
        formatted["Dépenses du mois"] = formatted["Dépenses du mois"].apply(
            "{:0,.2f}€".format)

        formatted["Dépenses cumulées"] = formatted["Dépenses cumulées"].apply(
            "{:0,.2f}€".format)

        if (category_name != "DIVERS"):
            formatted["Budget"] = formatted["Budget"].apply("{:0,.2f}€".format)
            formatted["RAD"] = formatted["RAD"].apply("{:0,.2f}€".format)
            formatted["PFDC"] = formatted["PFDC"].apply("{:0,.2f}€".format)
            formatted["Ecart PFDC/Budget"] = formatted["Ecart PFDC/Budget"]\
                .apply("{:0,.2f}€".format)
        return formatted
