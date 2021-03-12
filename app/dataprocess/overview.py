from .revenues import Revenues
from .expenses import Expenses
from .imports import get_csv_expenses
import pandas as pd
import datetime
import numpy as np
import os

class Overview():

    def __init__(self,accounting_plan,month,year,csv_path="var/csv/"):
        """Calcule la synthese sur l'année de toutes les dépenses de tout les chantiers."""
        self.col = ['CHANTIER','BUDGET',"CA MOIS",'DEP DU MOIS',"MARGE MOIS","CA CUMUL",'DEP CUMULEES',"MARGE A FIN DE MOIS",'PFDC',"MARGE FDC"]
        self.worksite_names = []
        self.month = month
        self.year = year
        self.csv_path = csv_path
        self.expenses = self.__get_all_worksites_data(month,year,accounting_plan)
        self.data = pd.DataFrame(None,None,columns=self.col)
        self.cumulative_expenses_total = 0
        self.month_expenses_total = 0

    def __get_all_worksites_data(self,month,year,accounting_plan):
        first_file_processed = False
        total = None
        for filename in os.listdir(self.csv_path):
            if year in filename and 'STRUCT' not in filename and 'DIV' not in filename:
                if not first_file_processed:
                    total = get_csv_expenses(self.csv_path+filename)
                    first_file_processed = True
                else:
                    total = total.append(get_csv_expenses(self.csv_path+filename),ignore_index=True)
                
                print(filename)
                worksite_name = filename.split('_')[1].split('.')[0]
                if worksite_name not in self.worksite_names:
                    self.worksite_names.append(worksite_name)
                
            else :
                for name in self.worksite_names:
                    if name in filename and int(filename[0:4]) < year:
                        total = total.append(get_csv_expenses(self.csv_path+filename),ignore_index=True)
        return Expenses(total,accounting_plan)

    def precalc_pfdc(self,month,year):
        """Rajout des csv des chantiers dont la synthese a deja ete calculatees."""
        csv_worksite = {}
        date = str(year) + "-" + (str(month) if len(str(month)) == 2 else "0"+str(month))
        if (os.path.exists("bibl/"+date)):
            for filename in os.listdir('bibl/'+date):
                worksite_name = filename[0:-7]
                with open("bibl/"+date+"/"+filename,'rb') as file:
                    csv_worksite[worksite_name] = file.read()

        return csv_worksite

    def ajoute_data(self,data):
        self.data = self.data.append(data,ignore_index=True)

    def calculate_data(self,month,year,budget):
        """Calcul de la synthese des dépenses d'une année en omettant la structure."""
        csv_worksite = self.precalc_pfdc(month,year)
        for name in self.worksite_names:
            worksite_line = ["",0,0,0,0,0,0,0,0,0]
            worksite_line[0] = name
            if name in csv_worksite.keys():
                worksite_line[-2] = round(float(csv_worksite[name]),2)

            for _,row in self.expenses.data.loc[self.expenses.data["Section analytique"] == name].iterrows():
                #On itere sur toutes les actions d'un chantier particulier
                date = datetime.datetime.strptime(row['Date'],"%Y-%m-%d")
                if (row['Journal'] == 'ACH') and (date.month <= month):
                    #Une action est une dépense si son champ journal est 'ACH'
                    worksite_line[6] += row['Débit'] - row['Crédit']
                    if (date.month == month) and (date.year == year):
                        #Le calculate des dépenses prends en compte les avoirs
                        worksite_line[3] += row['Débit'] - row['Crédit']

            worksite_line[6] = round(worksite_line[6],2)
            worksite_line[3] = round(worksite_line[3],2)

            out = pd.DataFrame([worksite_line],columns=self.col)
            self.ajoute_data(out)
        
        self.data = self.data.set_index("CHANTIER")
        self.add_budget(budget)
        self.add_revenues()
        self.calculate_margin(budget)
        self.data = self.data.round(2)
        self._calculate_total()

    def add_revenues(self):
        for name in self.worksite_names:
            worksite_revenue = Revenues(self.expenses.data.loc[self.expenses.data["Section analytique"] == name])
            self.data.loc[name,"CA MOIS"] = round(worksite_revenue.calculate_month_revenues(self.month,self.year),2)
            self.data.loc[name,"CA CUMUL"] = round(worksite_revenue.calculate_cumulative_revenues(self.year),2)
            

    def add_budget(self,budget):
        """Ajoute les données dans la colonne budget de la synthèse."""
        for name in self.worksite_names:
            if name in budget.columns :
                for _,row in budget.iterrows():
                    if row['POSTE'] == 'TOTAL':
                        break;
                    self.data.loc[name,"BUDGET"] += row[name]
    
    def calculate_margin(self,budget):
        for name in self.worksite_names:
            if 'DIV' in name or 'STRUCT' in name:
                continue
            

            #budget = self.data.loc[name,"BUDGET"]
            pfdc = self.data.loc[name,"PFDC"]
            month_expenses = self.data.loc[name,"DEP DU MOIS"]
            month_revenues = self.data.loc[name,"CA MOIS"]
            cumulative_expenses = self.data.loc[name,"DEP CUMULEES"]
            cumulative_revenues = self.data.loc[name,"CA CUMUL"]
            
            sell_price = 0
            if name in budget.columns :
                for _,row in budget.iterrows():
                    if row["POSTE"] == "PRIX DE VENTE":
                        sell_price += row[name]
                    elif row["POSTE"] == "AVENANTS":
                        sell_price += row[name]

            self.data.loc[name,"MARGE MOIS"] = round(month_revenues - month_expenses,2)
            self.data.loc[name,"MARGE A FIN DE MOIS"] = round(cumulative_expenses - cumulative_revenues,2)
            self.data.loc[name,"MARGE FDC"] = round(sell_price-pfdc,2) #Le soustraire au prix de ente + avenants
            #if budget != 0:
            #    self.data.loc[name,"MARGE THEORIQUE (€)"] =  round(budget - pfdc,2)
            #    self.data.loc[name,"MARGE THEORIQUE (%)"] = round(pfdc*100/budget,2)
            #    self.data.loc[name,"MARGE BRUTE (€)"] =  round(budget-cumulative_expenses,2)
            #    self.data.loc[name,"MARGE BRUTE (%)"] = round(cumulative_expenses*100/budget,2)
    
    def _calculate_total(self):
        self.cumulative_expenses_total = round(self.data['DEP CUMULEES'].sum(),2)
        self.month_expenses_total = round(self.data['DEP DU MOIS'].sum(),2)
    
    def calculate_tableau_ca(self,month_revenues,cumulative_revenues):
        """Doit etre appele apres le calculate de la synthese et le calculate du total. Se charge de mettre en forme le tableau du chiffre d'affaire."""
        month_revenues = round(month_revenues,2)
        cumulative_revenues = round(cumulative_revenues,2)
        self.total_revenue_margin = pd.DataFrame(\
                np.array([\
                [month_revenues,\
                self.month_expenses_total,\
                month_revenues-self.month_expenses_total,\
                round(100*(self.month_expenses_total/month_revenues),2)],\
                [cumulative_revenues,\
                self.cumulative_expenses_total,\
                round(cumulative_revenues-self.cumulative_expenses_total,2),\
                round(100*(self.cumulative_expenses_total/cumulative_revenues),2)]\
                ]),\
            columns=["CA","Depenses","Marge brute","Marge brute %"])
        s = pd.Series(["Mois","Année"])
        self.total_revenue_margin = self.total_revenue_margin.set_index(s)

    def get_formatted_data(self):
        formatted = self.data.copy()
        formatted["DEP CUMULEES"] = formatted["DEP CUMULEES"].apply("{:0,.2f}€".format)
        formatted["CA MOIS"] = formatted["CA MOIS"].apply("{:0,.2f}€".format)
        formatted["DEP DU MOIS"] = formatted["DEP DU MOIS"].apply("{:0,.2f}€".format)
        formatted["CA CUMUL"] = formatted["CA CUMUL"].apply("{:0,.2f}€".format)
        formatted["MARGE MOIS"] = formatted["MARGE MOIS"].apply("{:0,.2f}€".format)
        formatted["MARGE A FIN DE MOIS"] = formatted["MARGE A FIN DE MOIS"].apply("{:0,.2f}€".format)
        formatted["PFDC"] = formatted["PFDC"].apply("{:0,.2f}€".format)
        formatted["MARGE FDC"] = formatted["MARGE FDC"].apply("{:0,.2f}€".format)
        formatted["BUDGET"] = formatted["BUDGET"].apply("{:0,.2f}€".format)
        
        return formatted


