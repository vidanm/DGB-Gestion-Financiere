from .expenses import Expenses
from .imports import get_csv_expenses
import pandas as pd
import warnings
import os

from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class Overview:
    def __init__(self, accounting_plan, month, year, csv_path="var/csv/"):
        """Calcule la synthese sur l'année \
                de toutes les dépenses de tout les chantiers."""

        self.worksite_names = []
        self.month = month
        self.year = year
        self.csv_path = csv_path
        self.expenses = self.__get_all_worksites_data(
            month, year, accounting_plan
        )
        self.data = pd.DataFrame(None, None, columns=self.col)
        self.cumulative_expenses_total = 0
        self.month_expenses_total = 0

    def __get_all_worksites_data(self, month, year, accounting_plan):
        """Permets la récupération de toutes les données nécessaires
        à la synthèse."""
        first_file_processed = False
        total = None
        for filename in os.listdir(self.csv_path):
            if str(year) in filename:  # and\
                #'STRUCT' not in filename and\
                #'DIV' not in filename:
                if not first_file_processed:
                    total = get_csv_expenses(self.csv_path + filename)
                    first_file_processed = True
                else:
                    total = total.append(
                        get_csv_expenses(self.csv_path + filename),
                        ignore_index=True,
                    )

                worksite_name = str(filename.split("_")[1].split(".")[0])
                if worksite_name not in self.worksite_names:
                    self.worksite_names.append(worksite_name)

        for filename in os.listdir(self.csv_path):
            for name in self.worksite_names:
                if name in filename and int(filename[0:4]) < year:
                    total = total.append(
                        get_csv_expenses(self.csv_path + filename),
                        ignore_index=True,
                    )

        return Expenses(total, accounting_plan, with_category=False)

    def precalc_pfdc(self, month, year):
        """Rajout des csv des chantiers\
                dont la synthese a deja ete calculatees."""
        csv_worksite = {}
        date = (
            str(year)
            + "-"
            + (str(month) if len(str(month)) == 2 else "0" + str(month))
        )
        if os.path.exists("bibl/" + date):
            for filename in os.listdir("bibl/" + date):
                worksite_name = filename[0:-7]
                if os.stat("bibl/" + date + "/" + filename).st_size != 0:
                    with open("bibl/" + date + "/" + filename, "rb") as file:
                        csv_worksite[worksite_name] = file.read()
                else:
                    csv_worksite[worksite_name] = 0

        return csv_worksite

    def ajoute_data(self, data):
        self.data = self.data.append(data, ignore_index=True)
