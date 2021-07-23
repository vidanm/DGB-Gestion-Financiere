from .revenues import Revenues
from .overview import Overview
import pandas as pd
import warnings
import numpy as np
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class GlobalOverview(Overview):
    def __init__(self, accounting_plan, month, year, csv_path="var/csv/"):
        """Calcule la synthese sur l'année \
                de toutes les dépenses de tout les chantiers."""
        self.col = [
            "CHANTIER",
            "BUDGET",
            "CA MOIS",
            "DEP DU MOIS",
            "MARGE MOIS",
            "CA CUMUL",
            "DEP CUMULEES",
            "MARGE A FIN DE MOIS",
            "PFDC",
            "MARGE FDC",
        ]
        super(GlobalOverview, self).__init__(
            accounting_plan, month, year, csv_path
        )

    def calculate_data(self, month, year, budget=None):
        """Calcul de la synthese des dépenses d'une année\
                en omettant la structure."""
        csv_worksite = super(GlobalOverview, self).precalc_pfdc(month, year)
        for name in self.worksite_names:
            worksite_line = ["", 0, 0, 0, 0, 0, 0, 0, 0, 0]
            worksite_line[0] = name
            if name in csv_worksite.keys():
                worksite_line[-2] = round(float(csv_worksite[name]), 2)

            tmp = self.expenses.data.loc[
                self.expenses.data["Section analytique"].astype(str) == name
            ]
            tmp["Date"] = pd.to_datetime(tmp["Date"])
            tmp = tmp.loc[tmp["Journal"] != "VEN"]
            tmp = tmp.loc[tmp["Journal"] != "ANO"]

            month_tmp = tmp[
                (
                    (tmp["Date"].dt.month == month)
                    & (tmp["Date"].dt.year == year)
                )
            ]
            cumul_tmp = tmp[
                (
                    (tmp["Date"].dt.month <= month)
                    | (tmp["Date"].dt.year < year)
                )
            ]

            # On parse avant de faire la somme
            # au cas ou un index se serait glissé entre les données
            cumul_debit = pd.to_numeric(
                cumul_tmp["Débit"], errors="coerce"
            ).sum()

            cumul_credit = pd.to_numeric(
                cumul_tmp["Crédit"], errors="coerce"
            ).sum()

            month_debit = pd.to_numeric(
                month_tmp["Débit"], errors="coerce"
            ).sum()

            month_credit = pd.to_numeric(
                month_tmp["Crédit"], errors="coerce"
            ).sum()

            worksite_line[6] = cumul_debit - cumul_credit
            worksite_line[3] = month_debit - month_credit

            worksite_line[6] = round(worksite_line[6], 2)
            worksite_line[3] = round(worksite_line[3], 2)

            out = pd.DataFrame([worksite_line], columns=self.col)
            self.ajoute_data(out)

        self.data = self.data.set_index("CHANTIER")
        if budget is not None:
            self.add_budget(budget)

        self.add_revenues()
        self.calculate_margin(budget)
        self.data = self.data.round(2)
        self._calculate_total()
        self.data = self.data.sort_values("DEP CUMULEES", ascending=False)

    def add_revenues(self):
        """Ajout des chiffres d'affaires."""
        for name in self.worksite_names:
            worksite_revenue = Revenues(
                self.expenses.data.loc[
                    self.expenses.data["Section analytique"].astype(str)
                    == name
                ]
            )
            self.data.loc[name, "CA MOIS"] = round(
                worksite_revenue.calculate_month_revenues(
                    self.month, self.year
                ),
                2,
            )
            self.data.loc[name, "CA CUMUL"] = round(
                worksite_revenue.calculate_cumulative_revenues(self.year), 2
            )

    def add_budget(self, budget):
        """Ajoute les données dans la colonne budget de la synthèse."""
        for name in self.worksite_names:
            tmp = budget.loc[budget["POSTE"] != "TOTAL"]
            tmp = tmp.loc[tmp["POSTE"] != "PRIX DE VENTE"]
            if name in budget.columns:
                self.data.loc[name, "BUDGET"] = tmp[name].sum()

    def add_total(self):
        """Ajout du total de la synthèse."""
        totalbudget = self.data["BUDGET"].sum()
        totalcamois = self.data["CA MOIS"].sum()
        totaldepmois = self.data["DEP DU MOIS"].sum()
        totalmargmois = self.data["MARGE MOIS"].sum()
        totalcacumul = self.data["CA CUMUL"].sum()
        totaldepcumul = self.data["DEP CUMULEES"].sum()
        totalmargcumul = self.data["MARGE A FIN DE MOIS"].sum()
        totalpfdc = self.data["PFDC"].sum()
        totalmargefdc = self.data["MARGE FDC"].sum()

        total = pd.DataFrame(
            {
                "BUDGET": [totalbudget],
                "CA MOIS": [totalcamois],
                "DEP DU MOIS": [totaldepmois],
                "MARGE MOIS": [totalmargmois],
                "CA CUMUL": [totalcacumul],
                "DEP CUMULEES": [totaldepcumul],
                "MARGE A FIN DE MOIS": [totalmargcumul],
                "PFDC": [totalpfdc],
                "MARGE FDC": [totalmargefdc],
            },
            ["TOTAL"],
        )

        self.data = self.data.append(total)

    def calculate_margin(self, budget=None):
        """Calcul des marges."""
        for name in self.worksite_names:
            pfdc = self.data.loc[name, "PFDC"]
            month_expenses = self.data.loc[name, "DEP DU MOIS"]
            month_revenues = self.data.loc[name, "CA MOIS"]
            cumulative_expenses = self.data.loc[name, "DEP CUMULEES"]
            cumulative_revenues = self.data.loc[name, "CA CUMUL"]

            sell_price = 0
            if budget is not None and name in budget.columns:
                tmp = budget.loc[(budget["POSTE"] == "PRIX DE VENTE")]
                sell_price = tmp[name].sum()

            self.data.loc[name, "MARGE MOIS"] = round(
                month_revenues - month_expenses, 2
            )
            self.data.loc[name, "MARGE A FIN DE MOIS"] = round(
                cumulative_revenues - cumulative_expenses, 2
            )
            self.data.loc[name, "MARGE FDC"] = round(sell_price - pfdc, 2)

    def _calculate_total(self):
        self.cumulative_expenses_total = round(
            self.data["DEP CUMULEES"].sum(), 2
        )
        self.month_expenses_total = round(self.data["DEP DU MOIS"].sum(), 2)

    def calculate_tableau_ca(self, month_revenues, cumulative_revenues):
        """Doit etre appele apres le calculate de la synthese \
                et le calculate du total. \
                Se charge de mettre en forme le \
                tableau du chiffre d'affaire."""
        month_revenues = round(month_revenues, 2)
        cumulative_revenues = round(cumulative_revenues, 2)
        self.total_revenue_margin = pd.DataFrame(
            np.array(
                [
                    [
                        month_revenues,
                        self.month_expenses_total,
                        month_revenues - self.month_expenses_total,
                        round(
                            100 * (self.month_expenses_total / month_revenues),
                            2,
                        ),
                    ],
                    [
                        cumulative_revenues,
                        self.cumulative_expenses_total,
                        round(
                            cumulative_revenues
                            - self.cumulative_expenses_total,
                            2,
                        ),
                        round(
                            100
                            * (
                                self.cumulative_expenses_total
                                / cumulative_revenues
                            ),
                            2,
                        ),
                    ],
                ]
            ),
            columns=["CA", "Depenses", "Marge brute", "Marge brute %"],
        )

        s = pd.Series(["Mois", "Année"])
        self.total_revenue_margin = self.total_revenue_margin.set_index(s)

    def get_formatted_data(self):
        formatted = self.data.copy()
        formatted["DEP CUMULEES"] = formatted["DEP CUMULEES"].apply(
            "{:0,.2f}€".format
        )
        formatted["CA MOIS"] = formatted["CA MOIS"].apply("{:0,.2f}€".format)
        formatted["DEP DU MOIS"] = formatted["DEP DU MOIS"].apply(
            "{:0,.2f}€".format
        )
        formatted["CA CUMUL"] = formatted["CA CUMUL"].apply("{:0,.2f}€".format)
        formatted["MARGE MOIS"] = formatted["MARGE MOIS"].apply(
            "{:0,.2f}€".format
        )
        formatted["MARGE A FIN DE MOIS"] = formatted[
            "MARGE A FIN DE MOIS"
        ].apply("{:0,.2f}€".format)
        formatted["PFDC"] = formatted["PFDC"].apply("{:0,.2f}€".format)
        formatted["MARGE FDC"] = formatted["MARGE FDC"].apply(
            "{:0,.2f}€".format
        )
        formatted["BUDGET"] = formatted["BUDGET"].apply("{:0,.2f}€".format)

        return formatted
