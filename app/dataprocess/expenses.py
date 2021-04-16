from .accounting_plan import AccountingPlan
from .imports import get_accounting_file, get_csv_expenses
import time


class Expenses():

    def __init__(self, data, accounting_plan, with_category=True):
        self.data = data
        self.accounting_plan = accounting_plan
        if with_category:
            self.__remove_unknown_accounts()
            self.__compose_accounts_with_category_name()

    def __add__(self, other):
        a = self.data
        b = other.data
        return Expenses(a.append(b, ignore_index=True), self.accounting_plan)

    def __str__(self):
        return self.data.to_string()

    def __remove_unknown_accounts(self):
        log = open("static/log.txt", "a+")
        accounts = self.data["Général"].unique()
        for account in accounts:
            if self.accounting_plan.get_poste_by_code(str(account)).empty:
                if(str(account).isnumeric() and int(account/100000) == 7):
                    self.accounting_plan.add_code_to_plan(
                            account, "Unknown category",
                            "Unknown sub-category")
                else:
                    self.data = self.data.loc[self.data["Général"] != account]
                    log.write("Compte " + str(account) +
                              " pas dans le plan comptable\n")
        log.close()
        return

    def __compose_accounts_with_category_name(self):
        tic = time.perf_counter()
        # for index, value in self.data["Général"].iteritems():
        #    category = self.accounting_plan.get_poste_by_code(
        #        str(value))['POSTE'].values[0]
        #    subcategory = self.accounting_plan.get_poste_by_code(
        #        str(value))['SOUS POSTE'].values[0]
        #    self.data.loc[index, 'POSTE'] = category
        #    self.data.loc[index, 'SOUS POSTE'] = subcategory """

        self.data['POSTE'] = self.data['Général'].apply(
                lambda x: (self.accounting_plan
                           .get_poste_by_code(str(x)))['POSTE']
                .values[0])

        self.data['SOUS POSTE'] = self.data['Général'].apply(
                lambda x: (self.accounting_plan
                           .get_poste_by_code(str(x)))['SOUS POSTE']
                .values[0])

        toc = time.perf_counter()
        print(f"__compose_accounts..__ : {toc - tic :0.4f} seconds")


if __name__ == "__main__":
    a = Expenses(
            get_csv_expenses(
                "~/DGB_Gesfin/var/csv/2020_20-DIV0000.csv"),
            AccountingPlan(
                get_accounting_file(
                    "~/DGB_Gesfin/var/PlanComptable2020.xls"
                    )
                )
            )

    b = Expenses(
            get_csv_expenses(
                "~/DGB_Gesfin/var/csv/2020_19-BD-LAIG.csv"),
            AccountingPlan(
                get_accounting_file(
                    "~/DGB_Gesfin/var/PlanComptable2020.xls")
                )
            )

    c = a + b
