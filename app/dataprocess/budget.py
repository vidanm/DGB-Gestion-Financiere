import pandas as pd
import get_budget_file from imports

class Budget():
    def __init__(self,filepath):
        rawBudget = get_budget_file(filepath)
        postesMas = ["TRELLIS","ACIERS HA","CP","GROS BETON","C 25/30","C 30/37","C 40/50","C 50/60"]
        self.budEur, self.budMas = self.split_budget(rawBudget, postesMas) 
        # budEur = budget exprimé en euros
        # budMas = budget exprimé en kg ou m² ou m³
        

    def __split_budget(self,rawBudget,postesMas):
        
        budEur = DataFrame()
        budMas = DataFrame()

        for key in rawBudget:
            if key in postesMas:
                # Place cette ligne dans budMas
                pass
            else:
                pass
                # Place cette ligne dans budEur
        
        return (budEur, budMas)
