import pandas as pd
import numpy as np

class AccountingPlan():
    
    """On sépare le plan en structure/chantier car c'est le seul moyen qu'on a de savoir si un
    poste est un poste appartenant a la structure ou appartenant au chantier."""

    def get_poste_by_code(self,code):
        """Renvoie le poste en fonction du code donné."""
        return self.general_plan.loc[self.general_plan['N° DE COMPTE'].str.contains(code,na=False)]

    def get_worksite_plan(self):
        #Verifier l'utilité 
        return self.working_site_plan

    def get_office_plan(self):
        #Verifier l'utilité
        return self.office_plan

    def add_code_to_plan(self,code,poste,sous_poste):
        row = pd.DataFrame(np.array([[code,poste,sous_poste]]),
            columns=['N° DE COMPTE','POSTE','SOUS POSTE'])
        self.general_plan = self.general_plan.append(row,ignore_index=True)

    def __init__(self,plan):
        """Va s'occuper de traiter le fichier excel représentant le plan comptable."""
        (self.working_site_plan,self.office_plan) = plan
        self.general_plan = self.working_site_plan.append(self.office_plan,ignore_index=True)
        self.general_plan['N° DE COMPTE'] = self.general_plan['N° DE COMPTE'].apply(str)

