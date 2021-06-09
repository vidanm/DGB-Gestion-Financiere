import datetime


class Revenues():
    def __init__(self, data):
        """Calcule et stocke le chiffre d'affaire en fonction des expenses."""
        self.data = data
        self._delete_ach_lines()
        # self._month_revenues = pd.DataFrame()
        # self._year_revenues = pd.DataFrame()

    def _delete_ach_lines(self):
        """Elimine toutes les lignes d'achats pour ne garder que les ventes."""
        self.data = self.data.loc[self.data['Journal'] == 'VEN']
        # for index, value in self.data['Journal'].iteritems():
        #    if value != 'VEN':
        #        self.data = self.data.drop(index=index)

    def calculate_month_revenues(self, month, year):
        """Calcul le chiffre d'affaire du mois de l'année donné en argument."""
        result = 0.0
        for _, row in self.data.iterrows():
            # La lecture d'un csv ou d'un xls change le type de row date
            if (isinstance(row['Date'], datetime.datetime)):
                date = row['Date']
            else:
                date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d")

            if (int(date.month) == int(month) and int(date.year) == int(year)):
                result += row['Crédit']

        return result

    def calculate_year_revenues(self, year):
        """Calcul le chiffre d'affaire de l'année donnée en argument."""
        today = datetime.date.today()
        result = 0.0
        if (int(today.year) == int(year)):
            for i in range(1, today.month + 1):
                result += self.calculate_month_revenues(i, year)
        else:
            for i in range(1, 13):
                result += self.calculate_month_revenues(i, year)

        return result

    def calculate_cumulative_with_year_limit(self, year):
        return (self.calculate_cumulative_revenues(year) -
                self.calculate_year_revenues(year + 1))

    def calculate_cumulative_revenues(self, year):
        # N'est pas borné au mois demandée
        result = self.data['Crédit'].sum()
        # for _, row in self.data.iternotrows():
        #    result += row['Crédit']

        return result
