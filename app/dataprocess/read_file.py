import pandas as pd

class CustomFileReader():

    def __init__(self,path,year):
        """Permets la lecture des fichiers charges comptables et budget."""
        year = str(year)
        print("Charges"+year)
        try :
            self._read_charges(path+"Charges"+year+".xls")
        except:
            raise FileNotFoundError("Fichier de charges manquant pour l'annee "+year+" : Importez le via le menu importer sous la forme 'Charges"+year+".xls'")
        try:
            self._read_comptable(path+"PlanComptable"+year+".xls")
        except: 
            raise FileNotFoundError("Fichier Plan Comptable manquant pour l'annee "+year+" : Importez le via le menu importer sous la forme 'PlanComptable"+year+".xls'")
        try:
            self._read_budget(path+"Budget"+year+".xls")
        except:
            raise FileNotFoundError("Fichier budget manquant pour l'annee "+year+" : Importez le via le menu importer sous la forme 'Budget"+year+".xls'")

    def get_charges(self):
        return self._charges

    def get_budget(self):
        return self._budget

    def get_plan(self):
        return self._pc

    def _read_charges(self,path):
        try:
            charges = pd.read_excel(path) 
        except Exception as error:
            raise error
        charges = charges.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
        charges = charges.fillna(0)
        charges['POSTE'] = ''
        charges['SOUS POSTE'] = ''
        self._charges = charges

    def _read_comptable(self,path):
        """Conversion Excel -> DataFrame pandas."""
        dfCompteSite = pd.read_excel(path,header=1,usecols="A:D")
        dfCompteSite[['POSTE']] = dfCompteSite[['POSTE']].fillna(method='ffill')

        dfCompteStruct = pd.read_excel(path,header=1,usecols="E:H")
        dfCompteStruct[['POSTE.1']] = dfCompteStruct[['POSTE.1']].fillna(method='ffill')

        #On supprime toutes les lignes avec un sous poste nul
        dfCompteSite = dfCompteSite[pd.notnull(dfCompteSite['N° DE COMPTE'])]
        dfCompteStruct = dfCompteStruct[pd.notnull(dfCompteStruct['N° DE COMPTE.1'])]
        dfCompteStruct = dfCompteStruct.rename(columns={'N° DE COMPTE.1': 'N° DE COMPTE','POSTE.1' : 'POSTE','SOUS POSTE.1' : 'SOUS POSTE','EX..1':'EX.'})
        #dfCompteSite = dfCompteSite.append(dfCompteStruct,ignore_index=True)

        dfCompteSite['N° DE COMPTE'] = dfCompteSite['N° DE COMPTE'].apply(str)
        dfCompteStruct['N° DE COMPTE'] = dfCompteStruct['N° DE COMPTE'].apply(str)
        values = {'SOUS POSTE':'/'}
        dfCompteSite = dfCompteSite.fillna(value=values)
        dfCompteStruct = dfCompteStruct.fillna(value=values)
        self._pc = (dfCompteSite,dfCompteStruct)


    def _read_budget(self,path):
        dfBudget = pd.read_excel(path,header=3,usecols="A:J")
        #for (name,value) in dfBudget.iteritems():
         #   if (name != self.codeChantier and name != 'POSTE' and name != 'SOUS-POSTE'):
          #      dfBudget = dfBudget.drop(columns=name)

        dfBudget['POSTE'] = dfBudget['POSTE'].fillna(method='ffill')
        dfBudget = dfBudget[dfBudget['SOUS-POSTE'].notna()]
        dfBudget = dfBudget.fillna(0)
        #dfBudget = dfBudget.dropna()
        self._budget = dfBudget
