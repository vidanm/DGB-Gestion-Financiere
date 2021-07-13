from .categories import Categories
from .imports import get_csv_expenses
from .expenses import Expenses
from .revenues import Revenues
import datetime
import pandas as pd
import os


class Worksite(Categories):
    def __init__(self, accounting_plan, worksite_name, csv_path="var/csv/"):
        """Trie les expenses d'un chantier par postes."""
        super(Worksite, self).__init__(accounting_plan.get_plan())
        self.csv_path = csv_path
        self.worksite_name = worksite_name
        self.expenses = self.__get_all_data_of_worksite(accounting_plan)
        self.cumul_expenses = 0
        self.year_expenses = 0
        if self.expenses is None:
            raise ValueError("Pas de dépenses pour ce chantier pour ce mois")

        for name in self.category_names:
            self.categories[name]['Budget'] = 0
            self.categories[name]['RAD'] = 0
            self.categories[name]['PFDC'] = 0
            self.categories[name]['Ecart PFDC/Budget'] = 0

    def __get_all_data_of_worksite(self, accounting_plan):
        total = None
        for filename in os.listdir(self.csv_path):
            if self.worksite_name in filename and filename.endswith(".csv"):
                if (os.stat(self.csv_path + filename).st_size != 0):
                    print(filename)
                    if total is None:
                        total = Expenses(
                            get_csv_expenses(self.csv_path + filename),
                            accounting_plan)
                    else:
                        total += Expenses(
                            get_csv_expenses(self.csv_path + filename),
                            accounting_plan)
        return total

    def calculate_year_expenses(self, month, year):
        df = self.expenses.data
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df['Month'] = pd.DatetimeIndex(df['Date']).month

        exp = df.loc[(year == df['Year']) & (month >= df['Month'])]
        exp = exp.loc[(exp['Général'].astype(str).str.slice(stop=1) != '7')]

        return exp['Débit'].astype(float).sum() - exp['Crédit'].astype(
            float).sum()

    def calculate_cumul_expenses(self, month, year):
        df = self.expenses.data
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df['Month'] = pd.DatetimeIndex(df['Date']).month

        exp = df.loc[(year > df['Year']) | ((year == df['Year'])
                                            & (month >= df['Month']))]

        exp = exp.loc[(exp['Général'].astype(str).str.slice(stop=1) != '7')]

        return exp['Débit'].astype(float).sum() - exp['Crédit'].astype(
            float).sum()

    def calculate_month_expenses(self, month, year):
        df = self.expenses.data
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df['Month'] = pd.DatetimeIndex(df['Date']).month

        exp = df.loc[(year == df['Year']) & (month == df['Month'])]
        exp = exp.loc[(exp['Général'].astype(str).str.slice(stop=1) != '7')]
        return exp['Débit'].astype(float).sum() - exp['Crédit'].astype(
            float).sum()


    def calculate_worksite(self, month, year, budget=None, only_year=False):

        if only_year:
            for _, row in self.expenses.data.iterrows():
                date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d")
                if (date.year == year and date.month <= month):
                    super(Worksite, self)._add_cumulative_expense(row)
                    if (date.month == month):
                        super(Worksite, self)._add_month_expense(row)

        else:
            for _, row in self.expenses.data.iterrows():
                date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d")
                if (date.year < year) or (date.month <= month
                                          and date.year == year):
                    super(Worksite, self)._add_cumulative_expense(row)
                    if (date.month == month and date.year == year):
                        super(Worksite, self)._add_month_expense(row)

        if (budget is not None):
            self.__add_budget(budget)

    def calculate_bab(self, budMas, csvBab):
        return ( self.__calculate_bois(budMas, csvBab),
                self.__calculate_aciers(budMas, csvBab),
                self.__calculate_beton(budMas, csvBab))

    def __calculate_bois(self, budMas, csvBab):
        sp = ["CONTREPLAQUE"]
        outCol = ["Poste","Surface coffrante (m²)","M² consommé mois","M² consommé cumul",
                  "Ratio consommation", "PU Moyen", "Ratio €/m²"]

        out = pd.DataFrame(data=None,columns=outCol)

        csvBab = csvBab.loc[csvBab['POSTE'] == 'BOIS']
        budMas = budMas.loc[budMas['POSTE'] == 'BOIS']

        for poste in sp:
            surface_coffrante = budMas[self.worksite_name+"-MQ"].loc[budMas['SOUS-POSTE'] == poste].sum()

            metre_consomme_mois = csvBab.loc[(csvBab["TYPE"] == "M") & (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            metre_consomme_cumul = csvBab.loc[(csvBab["TYPE"] == "C") & (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            ratio_consommation = metre_consomme_cumul / surface_coffrante if surface_coffrante != 0 else 0

            dep_cumul = self.categories["BOIS"].loc[poste,"Dépenses cumulées"].sum()
            print("\n\n\nDPENESES IJDQWILDJ : "+str(dep_cumul)+"\n\n\n")

            pumoyen = dep_cumul / metre_consomme_cumul if metre_consomme_cumul != 0 else 0
            ratio_euro_metre = dep_cumul / surface_coffrante if surface_coffrante != 0 else 0
            tmp = pd.DataFrame(data=[[
                        poste,
                        surface_coffrante,
                        metre_consomme_mois,
                        metre_consomme_cumul,
                        ratio_consommation,
                        pumoyen,
                        ratio_euro_metre
                       ]],columns=outCol)
            out = out.append(tmp)

        out = out.set_index("Poste")
        return out


    def __calculate_aciers(self, budMas, csvBab):
        sp = ["ACIERS HA","TRELLIS"]
        outCol = ["Poste","Dépenses du mois (kg)","Dépenses cumulées (kg)","Budget (kg)",
                  "RAD","PFDC (kg)","Ecart","PU Moyen etude","PU Moyen chantier"]
        
        out = pd.DataFrame(data=None,columns=outCol)
        
        csvBab = csvBab.loc[csvBab['POSTE'] == 'ACIERS']
        budMas = budMas.loc[budMas['POSTE'] == 'ACIERS']
        # budMas['SOUS-POSTE'] = budMas['SOUS-POSTE'].filter(items=sp)
        
        for poste in sp:
            type_acier = poste
            depenses_mois_kg = csvBab.loc[(csvBab["TYPE"] == "M") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            depenses_cumul_kg = csvBab.loc[(csvBab["TYPE"] == "C") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            reste_a_depenser = csvBab.loc[(csvBab["TYPE"] == "R") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()

            dep_cumul = self.categories["ACIERS"].loc[poste,"Dépenses cumulées"].sum()
            budget_kg = budMas[self.worksite_name+"-MQ"].loc[budMas['SOUS-POSTE'] == poste].sum()
            pfdc = depenses_cumul_kg + reste_a_depenser
            ecart = budget_kg - pfdc
            pu_moyen_etude =  budMas[self.worksite_name+"-AP"].loc[budMas['SOUS-POSTE'] == poste].sum()
            pu_moyen_chantier = dep_cumul / depenses_cumul_kg if depenses_cumul_kg != 0 else 0
            
            tmp = pd.DataFrame(data=[[
                        poste,
                        depenses_mois_kg,
                        depenses_cumul_kg,
                        budget_kg,
                        reste_a_depenser,
                        pfdc,
                        ecart,
                        pu_moyen_etude,
                        pu_moyen_chantier
                       ]],columns=outCol)
            out = out.append(tmp)

        out = out.set_index("Poste")
        return out
    
    def __calculate_beton(self, budMas, csvBab):
        sp = ["BETON C25/30","BETON C30/37","BETON C40/50",
              "BETON C50/60"]
        outCol = ["Poste","Quantité du mois (m³)","Quantité cumulée (m³)","M³ Étude",
                  "Quantité restante (m³)","PFDC","Ecart","PU Moyen etude","PU Moyen chantier"]

        out = pd.DataFrame(data=None, columns=outCol)

        csvBab = csvBab.loc[csvBab['POSTE'] == 'BETON']
        budMas = budMas.loc[budMas['POSTE'] == 'BETON']
        # budMas['SOUS-POSTE'] = budMas['SOUS-POSTE'].filter(items=sp)

        for poste in sp:
            type_beton = poste
            quantite_du_mois = csvBab.loc[(csvBab["TYPE"] == "M") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            quantite_cumul = csvBab.loc[(csvBab["TYPE"] == "C") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()
            quantite_restante = csvBab.loc[(csvBab["TYPE"] == "R") &\
                    (csvBab["SOUS-POSTE"] == poste)]["VALEUR"].sum()

            
            dep_cumul = self.categories["BETON"].loc[poste,"Dépenses cumulées"].sum()
            pfdc = quantite_cumul + quantite_restante
            budget_kg = budMas[self.worksite_name+"-MQ"].loc[budMas['SOUS-POSTE'] == poste].sum()
            ecart = budget_kg - pfdc
            pu_moyen_etude =  budMas[self.worksite_name+"-AP"].loc[budMas['SOUS-POSTE'] == poste].sum()
            pu_moyen_chantier = dep_cumul/quantite_cumul if quantite_cumul != 0 else 0
            
            tmp = pd.DataFrame(data=[[
                        poste,
                        quantite_du_mois,
                        quantite_cumul,
                        budget_kg,
                        quantite_restante,
                        pfdc,
                        ecart,
                        pu_moyen_etude,
                        pu_moyen_chantier
                       ]],columns=outCol)
            out = out.append(tmp)

        out = out.set_index("Poste")
        return out

    def __add_budget(self, budget):
        """
        Ajoute le budget dans les cases de postes correspondantes.
        """
        logging = open("log.txt","a+")
        not_used_rows = [
            "PRIX DE VENTE", "TOTAL", "ECART", "MONTANT MARCHE", "AVENANTS"
        ]
        for _, row in budget.iterrows():
            try:
                row[self.worksite_name]
            except Exception:
                logging.write("Pas de budget associé a ce chantier")
                logging.close()
                return
            try:
                if row['POSTE'] not in not_used_rows:
                    self.categories[row['POSTE']].loc[row['SOUS-POSTE'],
                                                      "Budget"] += round(row[
                                                          self.worksite_name])
            except Exception:
                logging.write("Le couple " + row['POSTE'] + " : " +
                             row['SOUS-POSTE'] +
                             " spécifié dans le fichier budget\
                             n'est pas un couple\
                             présent dans le plan comptable")
        logging.close()
        return 1

    def add_marche_avenants(self, budMas):
        budMas = budMas.loc[budMas["POSTE"] != "BETON"]
        budMas = budMas.loc[budMas["POSTE"] != "ACIERS"]
        budMas = budMas.loc[budMas["POSTE"] != "BOIS"]


        for poste in budMas["POSTE"].unique():
            tmp = budMas.loc[budMas["POSTE"] == poste]
            self.categories[poste]['Marché'] = 0
            self.categories[poste]['Avenants'] = 0
            print("\nPOSTE : "+str(poste))
            for sp in tmp["SOUS-POSTE"]:
                self.categories[poste].loc[sp,'Marché'] = budMas[self.worksite_name+'-MQ']\
                                                            .loc[budMas['SOUS-POSTE'] == sp].sum()
                self.categories[poste].loc[sp,'Avenants'] = budMas[self.worksite_name+'-AP']\
                                                            .loc[budMas['SOUS-POSTE'] == sp].sum()

                print(sp)
                

    def add_rad(self, category, subcategory, rad):
        if rad.replace('.', '').isnumeric():
            self.categories[category].loc[subcategory, "RAD"] = float(rad)

    def get_pfdc_total(self):
        total = 0
        for name in self.category_names:
            if (name != 'PRODUITS' and name != 'DIVERS'):
                total += self.categories[name]['PFDC'][-1]
        return total

    def compose_pfdc_budget(self):
        """
        Calcul le pfdc et l'ecart pfdc budget.
        """
        for name in self.category_names:
            for _, row in self.categories[name].iterrows():
                pfdc = row['RAD'] + row["Dépenses cumulées"]
                self.categories[name].loc[row.name, "PFDC"] = pfdc
                self.categories[name].loc[
                    row.name, "Ecart PFDC/Budget"] = row['Budget'] - pfdc

    def add_category_total(self, name):
        """
        Ajoute le total d'un poste à la fin de son tableau
        """
        totalmois = 0
        totalannee = 0
        totalbudget = 0
        totalrad = 0
        totalpfdc = 0
        totalecart = 0
        for index, row in self.categories[name].iterrows():
            totalannee += self.categories[name].loc[row.name,
                                                    "Dépenses cumulées"]
            totalmois += self.categories[name].loc[row.name,
                                                   "Dépenses du mois"]
            totalbudget += self.categories[name].loc[row.name, "Budget"]
            totalrad += self.categories[name].loc[row.name, "RAD"]
            totalpfdc += self.categories[name].loc[row.name, "PFDC"]
            totalecart += self.categories[name].loc[row.name,
                                                    "Ecart PFDC/Budget"]

        total = pd.DataFrame(
            {
                "Dépenses cumulées": [totalannee],
                "Dépenses du mois": [totalmois],
                "Budget": [totalbudget],
                "RAD": [totalrad],
                "PFDC": [totalpfdc],
                "Ecart PFDC/Budget": [totalecart]
            }, ["TOTAL"])

        self.categories[name] = self.categories[name].append(total)

    def add_worksite_total(self):
        """
        Calcul du total des dépenses.
        """
        for name in self.category_names:
            self.add_category_total(name)

    def calcul_divers_result(self, year):
        # Format divers tab and return result tab

        self.categories["DIVERS"] = self.categories["DIVERS"].drop(
            columns=['Budget', 'RAD', 'PFDC', 'Ecart PFDC/Budget'])

        ca_cumul = Revenues(self.expenses.data)\
            .calculate_year_revenues(year)

        dep_cumul = 0
        dep_cumul = self.categories["DIVERS"]["Dépenses cumulées"].sum() -\
                self.categories["DIVERS"]["Dépenses cumulées"].iat[-1]

        marge = ca_cumul - dep_cumul
        marge_percent = (marge / ca_cumul) * 100 if ca_cumul != 0 else 0
        data = [[ca_cumul, dep_cumul, marge, marge_percent]]
        row_index = ["Resultat"]
        column_indexes = [
            'CA Cumulé', 'Dépenses cumulées', 'Marge brute', 'Marge brute %'
        ]

        out = pd.DataFrame(data=data, index=row_index, columns=column_indexes)

        out['CA Cumulé'] = out['CA Cumulé']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Dépenses cumulées'] = out['Dépenses cumulées']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Marge brute'] = out['Marge brute']\
            .astype(int).apply("{:0,.2f}€".format)

        out['Marge brute %'] = out['Marge brute %']\
            .apply("{:0,.2f}%".format)

        return out

    def calcul_ges_prev(self):
        """
        Calcul la gestion previsionnelle une fois que \
                ttes les autres données ont été calculées.
        """
        for name in self.category_names:
            if name != "PRODUITS" and name != "DIVERS":
                if self.category_names.index(name) == 0:
                    gesprev = pd.DataFrame(
                        columns=self.categories[name].columns.copy())
                line = self.categories[name].iloc[-1]
                line.name = name
                gesprev = gesprev.append(line, ignore_index=False)

        self.category_names.append("GESPREV")
        self.categories["GESPREV"] = gesprev
        self.categories["GESPREV"] = self.categories["GESPREV"]\
                                        .sort_values("Dépenses cumulées",ascending=False)
        self.add_category_total("GESPREV")

    def get_formatted_data(self, category_name):
        formatted = self.categories[category_name].copy()
        formatted["Dépenses du mois"] = formatted["Dépenses du mois"].apply(
            "{:0,.2f}€".format)

        formatted["Dépenses cumulées"] = formatted["Dépenses cumulées"].apply(
            "{:0,.2f}€".format)

        if (category_name != "DIVERS"):
            formatted["Budget"] = formatted["Budget"].apply("{:0,.2f}€".format)
            formatted["RAD"] = formatted["RAD"].apply("{:0,.2f}€".format)
            formatted["PFDC"] = formatted["PFDC"].apply("{:0,.2f}€".format)
            formatted["Ecart PFDC/Budget"] = formatted["Ecart PFDC/Budget"]\
                .apply("{:0,.2f}€".format)
        return formatted
