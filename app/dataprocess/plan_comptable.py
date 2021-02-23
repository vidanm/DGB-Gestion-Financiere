import pandas as pd
import numpy as np

class PlanComptable():
    """On sépare le plan en structure/chantier car c'est le seul moyen qu'on a de savoir si un
    poste est un poste appartenant a la structure ou appartenant au chantier"""

    def get_poste_by_code(self,code):
        """Renvoie le poste en fonction du code donné"""
        return self._dfComptable.loc[self._dfComptable['N° DE COMPTE'].str.contains(code,na=False)]

    def get_pc_chantier(self):
        return self._dfPlanChantier

    def get_pc_structure(self):
        return self._dfPlanStruct

    def ajoute_code(self,code,poste,sous_poste):
        row = pd.DataFrame(np.array([[code,poste,sous_poste]]),
            columns=['N° DE COMPTE','POSTE','SOUS POSTE'])
        self._dfComptable = self._dfComptable.append(row,ignore_index=True)

    def __init__(self,plan):
        """Va s'occuper de traiter le fichier excel représentant le plan comptable."""
        (self._dfPlanChantier,self._dfPlanStruct) = plan
        self._dfComptable = self._dfPlanChantier.append(self._dfPlanStruct,ignore_index=True)
        self._dfComptable['N° DE COMPTE'] = self._dfComptable['N° DE COMPTE'].apply(str)

