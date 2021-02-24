from .basic_operations import is_in_dic

class ParentPoste():

    def __init__(self,dfPlanComptable):
        """Classe abstraite. Objet hérité par ChantierPoste et StructPoste."""
        self.nomPostes = []
        self.dicPostes = {}
        for _,row in dfPlanComptable.iterrows():
            value = row['POSTE']
            print(value)
            if not is_in_dic(str(value),self.nomPostes):
                self.nomPostes.append(str(value))

        for nom in self.nomPostes:
            # C'EST ICI CE QU'IL FAUT CORRIGER
            self.dicPostes[nom] = dfPlanComptable.loc[dfPlanComptable['POSTE'] == nom]
            self.dicPostes[nom] = self.dicPostes[nom].drop(columns=['POSTE','N° DE COMPTE','EX.'])
            self.dicPostes[nom]['Dépenses du mois'] = 0
            self.dicPostes[nom]["Dépenses de l'année"] = 0
            self.dicPostes[nom] = self.dicPostes[nom].set_index('SOUS POSTE')

    def _depenses_mois(self,row):
        """
        Ajoute une dépense du mois au dictionnaire des postes.

            Parameters:
            argument2 (pandas.Series): ligne des charges qui contient la dépense et le poste

            Returns:
            None

        """
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses du mois"] += round(row['Débit'] - row['Crédit'],2)
    
    def _depenses_annee(self,row):
        """
        Ajoute une dépense de l'année au dictionnaire des postes.

            Parameters:
            argument2 (pandas.Series): ligne des charges qui contient la dépense et le poste

            Returns:
            None

        """
        self.dicPostes[row['POSTE']].loc[row['SOUS POSTE'],"Dépenses de l'année"] += round(row['Débit'] - row['Crédit'],2)

    def round_2dec_df(self):
        for nom in self.dicPostes.keys():
            self.dicPostes[nom] = self.dicPostes[nom].round(2)

    def get_postes_names(self):
        return self.nomPostes

    def remove_poste(self,poste):
        self.dicPostes.pop(poste)
        

