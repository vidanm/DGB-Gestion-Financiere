from .accounting_plan import AccountingPlan
from .imports import get_accounting_file, get_csv_expenses
import logging


class Expenses():
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
        return Expenses(a.append(b, ignore_index=True),
                        self.accounting_plan,
                        with_category=False)

    def __str__(self):
        """Representation de dépenses."""
        return self.data.to_string()

    def __remove_unknown_accounts(self):
        logging.basicConfig(filename="log.txt",
                            format='%(message)s',
                            filemode='a+')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        accounts = self.data["Général"].unique()
        for account in accounts:
            if self.accounting_plan.get_poste_by_code(str(account)).empty:
                if (str(account).isnumeric() and int(account / 100000) == 7):
                    self.accounting_plan.add_code_to_plan(
                        account, "Unknown category", "Unknown sub-category")
                else:
                    self.data = self.data.loc[self.data["Général"] != account]
                    logger.warning("Compte " + str(account) +
                                   " pas dans le plan comptable\n")
        logging.shutdown()
        return 1

    def __compose_accounts_with_category_name(self):
        for index, value in self.data["Général"].iteritems():
            if len(self.accounting_plan.get_poste_by_code(
                    str(value)).values) > 0:
                category = self.accounting_plan.get_poste_by_code(
                    str(value))['POSTE'].values[0]
                subcategory = self.accounting_plan.get_poste_by_code(
                    str(value))['SOUS POSTE'].values[0]
                self.data.loc[index, 'POSTE'] = category
                self.data.loc[index, 'SOUS POSTE'] = subcategory

        # self.data['POSTE'] = self.data['Général'].apply(
        #        lambda x: (self.accounting_plan
        #                   .get_poste_by_code(str(x)))['POSTE']
        #        .values[0])

        # self.data['SOUS POSTE'] = self.data['Général'].apply(
        #        lambda x: (self.accounting_plan
        #                   .get_poste_by_code(str(x)))['SOUS POSTE']
        #        .values[0])


if __name__ == "__main__":
    a = Expenses(
        get_csv_expenses("~/DGB_Gesfin/var/csv/2020_20-DIV0000.csv"),
        AccountingPlan(
            get_accounting_file("~/DGB_Gesfin/var/PlanComptable2020.xls")))

    b = Expenses(
        get_csv_expenses("~/DGB_Gesfin/var/csv/2020_19-BD-LAIG.csv"),
        AccountingPlan(
            get_accounting_file("~/DGB_Gesfin/var/PlanComptable2020.xls")))

    c = a + b
