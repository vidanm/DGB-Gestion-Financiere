from .worksite import Worksite
from .revenues import Revenues
import pandas as pd

class ForwardPlanning():

    def __init__(self,worksite):
        self.worksite = worksite
        for name in worksite.category_names:
            if name != "PRODUITS":
                if worksite.category_names.index(name) == 0:
                    self.forward_planning = pd.DataFrame(
                        columns=worksite.categories[name].columns.copy())
                line = worksite.categories[name].iloc[-1] #ligne du total
                line.name = name
                self.forward_planning = self.forward_planning.append(line,ignore_index=False)

    def calculate_margins(self,month,year,with_year=True,with_cumul=False):
        #Concerne le tableau marge à l'avancement
        revenues = Revenues(self.worksite.expenses.data) # Verifier si les lignes de ventes sont bien dedans
        year_revenues = revenues.calculate_year_revenues(year)
        anterior_revenues = revenues.calculate_cumulative_with_year_limit(year-1)
        cumulative_revenues = year_revenues + anterior_revenues
        
        year_expenses = self.worksite.calculate_year_expenses(month,year)
        cumulative_expenses = self.worksite.calculate_cumul_expenses(month,year)
        anterior_expenses = cumulative_expenses - year_expenses

        margin_year = year_revenues - year_expenses
        margin_anterior = anterior_revenues - anterior_expenses
        margin_total = cumulative_revenues - cumulative_expenses

        percent_margin_year = (margin_year/year_expenses)*100
        percent_margin_anterior = (margin_anterior/anterior_expenses)*100
        percent_margin_total = (margin_total/cumulative_expenses)*100

        row_indexes = []
        data = []
        column_indexes = ["CA","Dépenses","Marge brute","Marge brute %"]

        if with_year:
            for i in ["Année courante","Années antérieures"]:
                row_indexes.append(i)

            for i in [[year_revenues,year_expenses,margin_year,percent_margin_year],
                    [anterior_revenues,anterior_expenses,margin_anterior,percent_margin_anterior]]:
                data.append(i)
        
        if with_cumul:
            for i in ["Cumulé"]:
                row_indexes.append(i)
            
            for i in [[cumulative_revenues,cumulative_expenses,margin_total,percent_margin_total]]:
                data.append(i)
            

        out = pd.DataFrame(data=data,index=row_indexes,columns=column_indexes)
        out["CA"] = out["CA"].apply("{:0,.2f}€".format)
        out["Dépenses"] = out["Dépenses"].apply("{:0,.2f}€".format)
        out["Marge brute"] =  out["Marge brute"].apply("{:0,.2f}€".format)
        out["Marge brute %"] = out["Marge brute %"].apply("{:0,.2f}%".format)

        return out

    def calculate_pfdc_tab(self,budget):
        # Concerne le tableau Marge à fin de chantier
        column_indexes = ["PFDC"]
        row_indexes = ["Marge brute","Marge brute %"]
        
        try:
            sell_price = int(budget.loc[budget["POSTE"] == "PRIX DE VENTE",
                self.worksite.worksite_name]) if budget is not None else 0
        except Exception:
            sell_price = 0

        try:
            avenants = int(budget.loc[budget["POSTE"] == "AVENANTS",
                self.worksite.worksite_name]) if budget is not None else 0
        except Exception:
            avenants = 0

        total_sell = (sell_price + avenants) - self.worksite.get_pfdc_total() 
        percent = total_sell/(sell_price+avenants) if (sell_price+avenants) != 0 else 0
        data = [total_sell,percent*100]
    
        out = pd.DataFrame(data=data,index=row_indexes,columns=column_indexes)
        out.loc["Marge brute"] = out.loc["Marge brute"].apply("{:0,.2f}€".format)
        out.loc["Marge brute %"] = out.loc["Marge brute %"].apply("{:0,.2f}%".format)
        return out
