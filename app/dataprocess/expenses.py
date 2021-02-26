from basic_operations import is_in_dic
from accounting_plan import AccountingPlan
from imports import get_expenses_file,get_accounting_file,get_worksite_expenses_csv

class Expenses():
    
    """
         Journal Date       Général Section analytique Libellé       Débit     Crédit POSTE     SOUS POSTE
         ACH     2020-11-05 616131  20-STRUCT0         ALLIANZ       89.88     0.00   VEHICULE  CREDIT BAIL
         ACH     2020-10-08 616150  20-STRUCT0         CM - CIC BAIL 9.95      0.00   VEHICULE  CREDIT BAIL
         ACH     2020-10-08 616140  20-STRUCT0         CM - CIC BAIL 11.94     0.00   VEHICULE  CREDIT BAIL
         ACH     2020-10-08 612200  20-STRUCT0         CM - CIC BAIL 395.32    0.00   VEHICULE  CREDIT BAIL
         ACH     2020-10-05 616131  20-STRUCT0         ALLIANZ       89.88     0.00   VEHICULE  CREDIT BAIL
         ACH     2020-10-05 616130  20-STRUCT0         ALLIANZ       80.93     0.00   VEHICULE  ASSURANCE
    """
    def __init__(self,data,accounting_plan):
        self.data = data
        self.accounting_plan = accounting_plan
        self.__remove_unknown_accounts()
        self.__compose_accounts_with_category_name()

    def __add__(self,other):
        a = self.data
        b = other.data
        return a.append(b,ignore_index=True)
    
    def __str__(self):
        return self.data.to_string()

    def __remove_unknown_accounts(self):
        unknown_accounts = []

        for index,value in self.data["Général"].iteritems():
            
            if self.accounting_plan.get_poste_by_code(str(value)).empty:
                if (int(value/100000) == 7):
                    #All account beginning with a 7 is a sell, 
                    #contributing to revenues calculation,
                    #so it needs to be included
                    accounting_plan.add_code_to_plan(value,"Unknown category","Unknown sub-category")
                else :
                    self.data = self.data.drop(index=index)
                    
                    if value not in unknown_accounts:
                        print("Account number : "+str(value)+" not in the accounting plan")
                        unknown_accounts.append(value)
        
        return unknown_accounts       

    def __compose_accounts_with_category_name(self):
        
        for index,value in self.data["Général"].iteritems():
            category = self.accounting_plan.get_poste_by_code(str(value))['POSTE'].values[0]
            subcategory = self.accounting_plan.get_poste_by_code(str(value))['SOUS POSTE'].values[0]
            self.data.loc[index,'POSTE'] = category
            self.data.loc[index,'SOUS POSTE'] = subcategory

if __name__ == "__main__":
    a = Expenses(\
            get_worksite_expenses_csv("~/DGB_Gesfin/var/csv/2020_20-DIV0000.csv"),\
            AccountingPlan(get_accounting_file("~/DGB_Gesfin/var/PlanComptable2020.xls"))\
            )
    
    b = Expenses(\
            get_worksite_expenses_csv("~/DGB_Gesfin/var/csv/2020_19-BD-LAIG.csv"),\
            AccountingPlan(get_accounting_file("~/DGB_Gesfin/var/PlanComptable2020.xls"))\
            )

    c = a + b
    print(c)
