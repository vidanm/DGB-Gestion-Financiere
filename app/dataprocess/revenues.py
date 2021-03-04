import pandas as pd
from datetime import date

class ChiffreAffaire():

    def __init__(self,charges):
        """Calcule et stocke le chiffre d'affaire en fonction des charges."""
        self._charges = charges
        self._delete_ach_lines()
        self._ca_mois = pd.DataFrame()
        self._ca_annee = pd.DataFrame()

    def _delete_ach_lines(self):
        """Elimine toutes les lignes d'achats pour ne garder que les ventes."""
        for index,value in self._charges['Journal'].iteritems():
            if value != 'VEN':
                self._charges = self._charges.drop(index=index)

    def calcul_ca_mois(self,mois,annee):
        """Calcul le chiffre d'affaire du mois de l'année donné en argument."""
        result = 0.0
        for _,row in self._charges.iterrows():
            date = row['Date']
            if (date.month == mois and date.year == annee):
                result += row['Crédit']
        return result

    def calcul_ca_annee(self,annee):
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

