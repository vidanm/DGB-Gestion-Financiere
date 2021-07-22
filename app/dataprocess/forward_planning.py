from .revenues import Revenues
import pandas as pd


class ForwardPlanning:
    def __init__(self, worksite):
        """Gestion prévisionnelle ( à la fin de la synthèse chantier )."""
        self.worksite = worksite
        for name in worksite.category_names:
            if name != "PRODUITS":
                if worksite.category_names.index(name) == 0:
                    self.forward_planning = pd.DataFrame(
                        columns=worksite.categories[name].columns.copy()
                    )
                line = worksite.categories[name].iloc[-1]  # ligne du total
                line.name = name
                self.forward_planning = self.forward_planning.append(
                    line, ignore_index=False
                )

    def calculate_margins(
        self, month, year, with_year=True, with_cumul=False, with_month=False
    ):
        # Calcule et crée le tableau de marge à l'avancement
        revenues = Revenues(self.worksite.expenses.data)
        year_revenues = revenues.calculate_year_revenues(year)
        anterior_revenues = revenues.calculate_cumulative_with_year_limit(
            year - 1
        )
        cumulative_revenues = year_revenues + anterior_revenues
        month_revenues = revenues.calculate_month_revenues(month, year)

        year_expenses = self.worksite.calculate_year_expenses(month, year)
        cumulative_expenses = self.worksite.calculate_cumul_expenses(
            month, year
        )
        anterior_expenses = cumulative_expenses - year_expenses
        month_expenses = self.worksite.calculate_month_expenses(month, year)

        margin_year = year_revenues - year_expenses
        margin_anterior = anterior_revenues - anterior_expenses
        margin_total = cumulative_revenues - cumulative_expenses
        margin_month = month_revenues - month_expenses

        percent_margin_year = (
            (margin_year / year_revenues) * 100 if year_revenues != 0 else 0
        )
        percent_margin_anterior = (
            (margin_anterior / anterior_revenues) * 100
            if anterior_revenues != 0
            else 0
        )
        percent_margin_total = (
            (margin_total / cumulative_revenues) * 100
            if cumulative_revenues != 0
            else 0
        )
        percent_margin_month = (
            (margin_month / month_revenues) * 100 if month_revenues != 0 else 0
        )

        row_indexes = []
        data = []
        column_indexes = ["CA", "Dépenses", "Marge brute", "Marge brute %"]

        if with_year:
            for i in ["Année courante", "Années antérieures"]:
                row_indexes.append(i)

            for i in [
                [
                    year_revenues,
                    year_expenses,
                    margin_year,
                    percent_margin_year,
                ],
                [
                    anterior_revenues,
                    anterior_expenses,
                    margin_anterior,
                    percent_margin_anterior,
                ],
            ]:
                data.append(i)

        if with_cumul:
            for i in ["Cumulé"]:
                row_indexes.append(i)

            for i in [
                [
                    cumulative_revenues,
                    cumulative_expenses,
                    margin_total,
                    percent_margin_total,
                ]
            ]:
                data.append(i)

        if with_month:
            for i in ["Mois"]:
                row_indexes.append(i)

            for i in [
                [
                    month_revenues,
                    month_expenses,
                    margin_month,
                    percent_margin_month,
                ]
            ]:
                data.append(i)

        out = pd.DataFrame( # Création du tableau
            data=data, index=row_indexes, columns=column_indexes
        )
        out["CA"] = out["CA"].apply("{:0,.2f}€".format)
        out["Dépenses"] = out["Dépenses"].apply("{:0,.2f}€".format)
        out["Marge brute"] = out["Marge brute"].apply("{:0,.2f}€".format)
        out["Marge brute %"] = out["Marge brute %"].apply("{:0,.2f}%".format)

        return out

    def calculate_pfdc_tab(self, budget):
        # Calcule et crée le tableau Marge à fin de chantier
        column_indexes = ["PFDC"]
        row_indexes = ["CA Chantier", "Marge brute", "Marge brute %"]

        try:
            sell_price = (
                budget.loc[
                    budget["POSTE"] == "PRIX DE VENTE",
                    self.worksite.worksite_name,
                ].sum()
                if budget is not None
                else 0
            )
        except Exception:
            sell_price = 0

        total_sell = sell_price - self.worksite.get_pfdc_total()
        percent = total_sell / (sell_price) if (sell_price) != 0 else 0

        data = [sell_price, total_sell, percent * 100]

        out = pd.DataFrame( # Création du tableau
            data=data, index=row_indexes, columns=column_indexes
        )

        out.loc["CA Chantier"] = out.loc["CA Chantier"].apply(
            "{:0,.2f}€".format
        )

        out.loc["Marge brute"] = out.loc["Marge brute"].apply(
            "{:0,.2f}€".format
        )

        out.loc["Marge brute %"] = out.loc["Marge brute %"].apply(
            "{:0,.2f}%".format
        )
        return out
