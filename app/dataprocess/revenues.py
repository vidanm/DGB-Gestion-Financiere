import pandas as pd
from datetime import date

class Revenues():

    def __init__(self,expenses):
        """Calcule et stocke le chiffre d'affaire en fonction des expenses."""
        self._expenses = expenses
        self._delete_ach_lines()
        #self._month_revenues = pd.DataFrame()
        #self._year_revenues = pd.DataFrame()

    def _delete_ach_lines(self):
        """Elimine toutes les lignes d'achats pour ne garder que les ventes."""
        for index,value in self._expenses['Journal'].data.iteritems():
            if value != 'VEN':
                self._expenses = self._expenses.drop(index=index)

    def calculate_month_revenues(self,mois,annee):
        """Calcul le chiffre d'affaire du mois de l'année donné en argument."""
        result = 0.0
        for _,row in self._expenses.data.iterrows():
            date = row['Date']
            if (date.month == mois and date.year == annee):
                result += row['Crédit']

        return result

    def calculate_year_revenues(self,annee):
        """Calcul le chiffre d'affaire de l'année donnée en argument."""
        today = date.today()
        result = 0.0
        if (today.year == annee):
            for i in range (1,today.month):
                result += self.calcul_ca_mois(i,annee)
        else:
            for i in range(1,12):
                result += self.calcul_ca_mois(i,annee)

        return result

    def calculate_cumulative_revenues(self,year):
        today = date.today()
        result = 0.0
        for _,row in self._expenses.data.iterrows():
            result += row['Crédit']

        return result
