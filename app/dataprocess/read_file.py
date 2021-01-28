import pandas as pd

def read_charges(path):
    charges = pd.read_excel(path)
    charges = charges.drop(columns=['Type','Référence interne','Date réf. externe','Auxiliaire','N°'])
    charges = charges.fillna(0)
    charges['POSTE'] = ''
    charges['SOUS POSTE'] = ''
    return charges



def read_comptable(path):
    '''Conversion Excel -> DataFrame pandas'''
    dfCompteSite = pd.read_excel(path,header=1,usecols="A:D")
    dfCompteSite[['POSTE']] = dfCompteSite[['POSTE']].fillna(method='ffill')

    dfCompteStruct = pd.read_excel(path,header=1,usecols="E:H")
    dfCompteStruct[['POSTE.1']] = dfCompteStruct[['POSTE.1']].fillna(method='ffill')

    #On supprime toutes les lignes avec un sous poste nul
    dfCompteSite = dfCompteSite[pd.notnull(dfCompteSite['N° DE COMPTE'])]
    dfCompteStruct = dfCompteStruct[pd.notnull(dfCompteStruct['N° DE COMPTE.1'])]
    dfCompteStruct = dfCompteStruct.rename(columns={'N° DE COMPTE.1': 'N° DE COMPTE','POSTE.1' : 'POSTE','SOUS POSTE.1' : 'SOUS POSTE','EX..1':'EX.'})
    '''dfCompteSite = dfCompteSite.append(dfCompteStruct,ignore_index=True)'''
    
    dfCompteSite['N° DE COMPTE'] = dfCompteSite['N° DE COMPTE'].apply(str)
    dfCompteStruct['N° DE COMPTE'] = dfCompteStruct['N° DE COMPTE'].apply(str)
    
    values = {'SOUS POSTE':'/'}
    dfCompteSite = dfCompteSite.fillna(value=values)
    dfCompteStruct = dfCompteStruct.fillna(value=values)
    return (dfCompteSite,dfCompteStruct)


def read_budget(path):
    dfBudget = pd.read_excel(path,header=3,usecols="A:J")
    #for (name,value) in dfBudget.iteritems():
     #   if (name != self.codeChantier and name != 'POSTE' and name != 'SOUS-POSTE'):
      #      dfBudget = dfBudget.drop(columns=name)

    dfBudget['POSTE'] = dfBudget['POSTE'].fillna(method='ffill')
    dfBudget = dfBudget[dfBudget['SOUS-POSTE'].notna()]
    dfBudget = dfBudget.fillna(0)
    #dfBudget = dfBudget.dropna()
    return dfBudget


