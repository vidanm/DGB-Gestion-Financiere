from .revenues import Revenues
from .expenses import Expenses
from .imports import get_csv_expenses
from .overview import Overview
import pandas as pd
import warnings
import numpy as np
import os

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class YearOverview(Overview):
    def __init__(self, accounting_plan, month, year, csv_path="var/csv/"):
        """Calcule la synthese sur l'année \
                de toutes les dépenses de tout les chantiers."""
        self.col = [
            "CHANTIER","CA","Dépenses","Reste à facturer","Marge €","Marge %",
            "Marge fin annee €","Marge fin annee %"
        ]

        self.csv_pfdc = self.precalc_pfdc(month, year)
        super(YearOverview, self).__init__(accounting_plan,month,year,csv_path)


    def calculate_data(self, month, year, budget=None):
        """Calcul de la synthese des dépenses d'une année\
                en omettant la structure."""
        for name in self.worksite_names:
            print(name)
            worksite_line = ["", 0, 0, 0, 0, 0, 0, 0]
            worksite_line[0] = name

            tmp = self.expenses.data.loc[
                    self.expenses.data["Section analytique"].astype(str) ==
                    name]
            tmp['Date'] = pd.to_datetime(tmp['Date'])
            tmp = tmp.loc[tmp["Journal"] != "VEN"]
            tmp = tmp.loc[tmp["Journal"] != "ANO"]

            tmp = tmp[((tmp['Date'].dt.month <= month) &
                            (tmp['Date'].dt.year == year))]

            year_debit = pd.to_numeric(tmp['Débit'], errors='coerce')\
                .sum()

            year_credit = pd.to_numeric(tmp['Crédit'], errors='coerce')\
                .sum()
        
            worksite_line[2] = year_debit - year_credit

            out = pd.DataFrame([worksite_line], columns=self.col)
            super(YearOverview, self).ajoute_data(out)

        self.data = self.data.set_index("CHANTIER")

        self.add_revenues()
        self.calculate_margin(budget)
        self.data = self.data.round(2)

    def add_revenues(self):
        """Ajout des chiffres d'affaires."""
        for name in self.worksite_names:
            worksite_revenue = Revenues(self.expenses.data.loc[
                self.expenses.data["Section analytique"].astype(str) == name])

            self.data.loc[name, "CA"] =\
                worksite_revenue.calculate_year_revenues(
                    self.year)

    def add_total(self,budget):
        """Ajout du total de la synthèse."""

        sell_price = 0
        pfdc = 0
        for name in self.worksite_names:

            if budget is not None:
                tmp = budget.loc[(budget['POSTE'] == 'PRIX DE VENTE')]
                try:
                    sell_price += tmp[name].sum()
                except:
                    print("") # useless
        
            try:
                pfdc += int(self.csv_pfdc[name])
            except:
                print("") # useless



        
        totalca = self.data["CA"].sum()
        totaldep = self.data["Dépenses"].sum()
        totalraf = self.data["Reste à facturer"].sum()
        totalmarg = self.data["Marge €"].sum()
        totalmargper = ((totalca - totaldep)/totalca) * 100 if totalca > 0 else 0
        totalmargyear = self.data["Marge fin annee €"].sum()
        totalmargyearper = (sell_price - pfdc)/(totalraf)\

        total = pd.DataFrame(
            {
                "CA": [totalca],
                "Dépenses": [totaldep],
                "Reste à facturer": [totalraf],
                "Marge €": [totalmarg],
                "Marge %": [totalmargper],
                "Marge fin annee €": [totalmargyear],
                "Marge fin annee %": [totalmargyearper],
            }, ["TOTAL"])

        self.data = self.data.append(total)

    def calculate_margin(self, budget=None):
        """Calcul des marges."""
        for name in self.worksite_names:
            if 'DIV' in name or 'STRUCT' in name:
                continue

            # budget = self.data.loc[name,"BUDGET"]
            expenses = self.data.loc[name, "Dépenses"]
            revenues = self.data.loc[name, "CA"]
            pfdc = 0

            try:
                pfdc = int(self.csv_pfdc[name])
            except Exception:
                print("Pas de pfdc pour le chantier "+str(name))
            
            worksite_revenue = Revenues(self.expenses.data.loc[
                self.expenses.data["Section analytique"] == name])

            anterior_revenues =\
                worksite_revenue.calculate_cumulative_with_year_limit(self.year-1)

            sell_price = 0
            if budget is not None and name in budget.columns:
                tmp = budget.loc[(budget['POSTE'] == 'PRIX DE VENTE')]
                sell_price = tmp[name].sum()


            self.data.loc[name, "Reste à facturer"] =\
                    (sell_price - anterior_revenues)

            self.data.loc[name, "Marge €"] =\
                revenues - expenses
            self.data.loc[name, "Marge %"] =\
                ((revenues - expenses)/revenues) * 100\
                if revenues > 0 else 0

            self.data.loc[name,"Marge fin annee €"] =\
                (sell_price - pfdc) - (revenues - expenses)

            self.data.loc[name, "Marge fin annee %"] =\
                ((sell_price - pfdc) - (revenues - expenses))/(sell_price - anterior_revenues)\
                if (sell_price - anterior_revenues) > 0 else 0

    def get_formatted_data(self):
        formatted = self.data.copy()
        formatted["Dépenses"] = formatted["Dépenses"].apply(
            "{:0,.2f}€".format)
        formatted["CA"] = formatted["CA"].apply("{:0,.2f}€".format)
        formatted["Reste à facturer"] = formatted["Reste à facturer"].apply(
            "{:0,.2f}€".format)
        formatted["Marge €"] = formatted["Marge €"].apply("{:0,.2f}€".format)
        formatted["Marge %"] = formatted["Marge %"].apply(
            "{:0,.2f}%".format)
        formatted["Marge fin annee €"] = formatted[
            "Marge fin annee €"].apply("{:0,.2f}€".format)
        formatted["Marge fin annee %"] = formatted["Marge fin annee %"].apply(
            "{:0,.2f}%".format)

        return formatted
