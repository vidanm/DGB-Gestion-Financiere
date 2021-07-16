class Categories:
    def __init__(self, accounting_plan):
        """Classe abstraite. Objet hérité par ChantierPoste et StructPoste."""
        self.category_names = accounting_plan["POSTE"].unique().tolist()
        self.categories = {}

        for name in self.category_names:
            self.categories[name] = accounting_plan.loc[
                accounting_plan["POSTE"] == name
            ]

            self.categories[name].columns = [
                x.strip() for x in self.categories[name].columns
            ]

            self.categories[name] = self.categories[name].drop(
                columns=["POSTE", "N° DE COMPTE", "EX."], errors="ignore"
            )
            # drop EX. si présent
            self.categories[name]["Dépenses du mois"] = 0
            self.categories[name]["Dépenses cumulées"] = 0
            self.categories[name] = self.categories[name].set_index(
                "SOUS POSTE"
            )

    def _add_month_expense(self, row):
        """
        Ajoute une dépense du mois au dictionnaire des postes.

            Parameters:
            argument2 (pandas.Series):
            ligne des charges qui contient la dépense et le poste

            Returns:
            None

        """
        try:
            self.categories[row["POSTE"]].loc[
                row["SOUS POSTE"], "Dépenses du mois"
            ] += round(row["Débit"] - row["Crédit"], 2)
        except Exception:
            print(
                "La dépense associé au compte "
                + str(row["Général"])
                + " n'est pas une dépense de structure/chantier"
            )

    def _add_cumulative_expense(self, row):
        """
        Ajoute une dépense de l'année au dictionnaire des postes.

            Parameters:
            argument2 (pandas.Series):
            ligne des charges qui contient la dépense et le poste

            Returns:
            None

        """
        try:
            self.categories[row["POSTE"]].loc[
                row["SOUS POSTE"], "Dépenses cumulées"
            ] += round(row["Débit"] - row["Crédit"], 2)
        except Exception:
            print(
                "La dépense associé au compte "
                + str(row["Général"])
                + " n'est pas une dépense de structure/chantier"
            )

    def round_2dec_df(self):
        for name in self.categories.keys():
            self.categories[name] = self.categories[name].round(2)

    def get_category_names(self):
        return self.category_names

    def remove_category(self, category):
        self.categories.pop(category)
