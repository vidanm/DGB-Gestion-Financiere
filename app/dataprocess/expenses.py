from .accounting_plan import AccountingPlan
from .imports import get_accounting_file, get_csv_expenses


class Expenses:
    def __init__(self, data, accounting_plan, with_category=True):
        """Traite les dépenses ( provenant de l'extraction comptable )."""

        self.data = data
        self.accounting_plan = accounting_plan
        if with_category:
            self.__remove_unknown_accounts()
            self.__compose_accounts_with_category_name()

    def __add__(self, other):
        """Concatene 2 dépenses."""
        a = self.data
        b = other.data
        return Expenses(
            a.append(b, ignore_index=True),
            self.accounting_plan,
            with_category=False,
        )

    def __str__(self):
        """Representation de dépenses."""
        return self.data.to_string()

    def __remove_unknown_accounts(self):
        """Supprime les comptes qui n'ont pas de poste associé dans 
        le plan comptable."""
        logging = open("log.txt", "a+")
        accounts = self.data["Général"].unique()
        for account in accounts:
            if self.accounting_plan.get_poste_by_code(str(account)).empty:
                if str(account).isnumeric() and int(account / 100000) == 7:
                    self.accounting_plan.add_code_to_plan(
                        account, "Unknown category", "Unknown sub-category"
                    )
                else:
                    print(
                        "Compte "
                        + str(account)
                        + " pas dans le plan comptable"
                    )
                    logging.write(
                        "Compte "
                        + str(account)
                        + " pas dans le plan comptable\n"
                    )
                    self.data = self.data.loc[self.data["Général"] != account]
        logging.close()
        return 1

    def __compose_accounts_with_category_name(self):
        """Rajoute les noms des postes et sous postes au tableau de dépenses"""
        for index, value in self.data["Général"].iteritems():
            if (
                len(self.accounting_plan.get_poste_by_code(str(value)).values)
                > 0
            ):
                category = self.accounting_plan.get_poste_by_code(str(value))[
                    "POSTE"
                ].values[0]
                subcategory = self.accounting_plan.get_poste_by_code(
                    str(value)
                )["SOUS POSTE"].values[0]
                self.data.loc[index, "POSTE"] = category
                self.data.loc[index, "SOUS POSTE"] = subcategory
