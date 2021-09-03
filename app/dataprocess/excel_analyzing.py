"""
1) Verifier la présence dans les charges des champs :
- Journal
- Date
- Crédit
- Débit
- Section analytique
- Général

2) Verifier la présence à la deuxieme ligne dans le plan comptable des champs :
- Poste
- Sous Poste
- Ex.
- Numero de compte
dans les 3 sous parties du plan comptable
Stocker les postes du plan comptable pour pouvoir les comparer plus tard avec ceux du budget

3) Verifier dans le budget que le tableau commence bien a la 4e ligne avec :
- POSTE
- SOUS-POSTE
et ensuite les noms de chantier
Dans les 2 feuilles

4) Verifier que dans le budget les noms des postes et des sous postes correspondent au plan comptable

5) 
"""
import pandas as pd

def verify_expenses_file(filepath):
    "On va vérifier la présence des colonnes nécessaire au\
     traitement des données"
    try:
        expenses = pd.read_excel(filepath)
    except Exception as error:
        raise error

    column_to_check = ["Section analytique","Date","Journal","Général","Crédit","Débit"]
    columns = expenses.columns

    for i in column_to_check:
        if i not in columns:
            raise ValueError("Mauvais format de fichier : la colonne '"+i+"' n'est pas dans les charges")
        

def verify_accounting_file(filepath):
    """On va vérifier la présence des colonnes et données nécessaire\
    au traitement du fichier"""
    worksite_column_to_check = ["N° DE COMPTE","POSTE","SOUS POSTE"]
    office_column_to_check = ["N° DE COMPTE.1","POSTE.1","SOUS POSTE.1"]
    divers_column_to_check = ["N° DE COMPTE.2","POSTE.2","SOUS POSTE.2"]

    try:
        account_worksite = pd.read_excel(filepath, header=1, usecols="A:D")
        account_office = pd.read_excel(filepath, header=1, usecols="E:H")
        account_divers = pd.read_excel(filepath, header=1, usecols="I:K")
    except Exception as error:
        raise error

    columns = account_worksite.columns

    for i in worksite_column_to_check:
        if i not in columns:
            raise ValueError("Mauvais format de fichier : \
                    la colonne "+i+" n'est pas dans la partie chantier du plan comptable.")

    columns = account_office.columns
    for i in office_column_to_check:
        if i not in columns:
            raise ValueError("Mauvais format de fichier : \
                    la colonne "+i+" n'est pas dans la partie structure du plan comptable.")

    columns = account_divers.columns

    for i in divers_column_to_check:
        if i not in columns:
            raise ValueError("Mauvais format de fichier : \
                    la colonne "+i+" n'est pas dans la partie divers du plan comptable.")

