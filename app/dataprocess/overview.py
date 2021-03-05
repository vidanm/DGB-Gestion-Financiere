import pandas as pd
import numpy as np
import os

class Overview():

    def __init__(self,expenses):
        """Calcule la synthese sur l'année de toutes les dépenses de tout les chantiers."""
        self.col = ['CHANTIER','BUDGET',"CA MOIS",'DEP DU MOIS',"MARGE MOIS","CA CUMUL",'DEP CUMULEES',"MARGE A FIN DE",'PFDC',"MARGE FDC"]

        self.expenses = expenses
        self.overview_data = pd.DataFrame(None,None,columns=self.col)

        self.cumulative_expenses_total = 0
        self.month_expenses_total = 0
   
    
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

    def ajoute_overview_data(self,data):
        self.overview_data = self.overview_data.append(data,ignore_index=True)

    def calculate_overview_data(self,month,year,budget):
        """Calcul de la synthese des dépenses d'une année en omettant la structure."""
        worksite_names = self.expenses.get_worksite_names()
        csv_worksite = self.precalc_pfdc(month,year)
        
        for name in worksite_names:
            
            if 'DIV' in name or 'STRUCT' in name:
                continue

            worksite_line = ["",0,0,0,0,0,0,0,0,0]
            worksite_line[0] = name
            if name in csv_worksite.keys():
                worksite_line[4] = round(float(csv_worksite[name]),2)

            for _,row in self.expenses.get_raw_chantier(name).iterrows():
                #On itere sur toutes les actions d'un chantier particulier
                date = row['Date']
                if (row['Journal'] == 'ACH') and (date.month <= month) and (date.year == year):
                    #Une action est une dépense si son champ journal est 'ACH'
                    worksite_line[3] += row['Débit'] - row['Crédit']
                    if (date.month == month):
                        #Le calculate des dépenses prends en compte les avoirs
                        worksite_line[2] += row['Débit'] - row['Crédit']

            out = pd.DataFrame([worksite_line],columns=self.col)
            self.ajoute_overview_data(out)
        
        self.overview_data = self.overview_data.set_index("CHANTIER")
        self.add_budget(budget)
        self.calculate_margin()
        self.overview_data = self.overview_data.round(2)
        self._calculate_total()

    def add_budget(self,budget):
        """Ajoute les données dans la colonne budget de la synthèse."""
        worksite_names = self.expenses.get_worksite_names()
        for name in worksite_names:
            if name in budget.columns :
                for _,row in budget.iterrows():
                    self.overview_data.loc[name,"BUDGET"] += row[name]
    
    def calculate_margin(self):
        worksite_names = self.expenses.get_worksite_names()
        for name in worksite_names:
            if 'DIV' in name or 'STRUCT' in name:
                continue
            
            budget = self.overview_data.loc[name,"BUDGET"]
            pfdc = self.overview_data.loc[name,"PFDC"]
            cumulative_expenses = self.overview_data.loc[name,"DEP CUMULEES"]
            
            if budget != 0:
                self.overview_data.loc[name,"MARGE THEORIQUE (€)"] =  round(budget - pfdc,2)
                self.overview_data.loc[name,"MARGE THEORIQUE (%)"] = round(pfdc*100/budget,2)
                self.overview_data.loc[name,"MARGE BRUTE (€)"] =  round(budget-cumulative_expenses,2)
                self.overview_data.loc[name,"MARGE BRUTE (%)"] = round(cumulative_expenses*100/budget,2)
    
    def _calculate_total(self):
        self.cumulative_expenses_total = round(self.overview_data['DEP CUMULEES'].sum(),2)
        self.month_expenses_total = round(self.overview_data['DEP DU MOIS'].sum(),2)
    
    def calculate_tableau_ca(self,month_revenues,cumulative_revenues):
        """Doit etre appele apres le calculate de la synthese et le calculate du total. Se charge de mettre en forme le tableau du chiffre d'affaire."""
        month_revenues = round(month_revenues,2)
        cumulative_revenues = round(cumulative_revenues,2)
        self.total_revenue_margin = pd.DataFrame(np.array([[month_revenues,self.month_expenses_total,month_revenues-self.month_expenses_total,round(100*(self.month_expenses_total/month_revenues),2)],[cumulative_revenues,self.cumulative_expenses_total,round(cumulative_revenues-self.cumulative_expenses_total,2),round(100*(self.cumulative_expenses_total/cumulative_revenues),2)]]),columns=["CA","Depenses","Marge brute","Marge brute %"])
        s = pd.Series(["Mois","Année"])
        self.total_revenue_margin = self.total_revenue_margin.set_index(s)
        print(self.total_revenue_margin)
