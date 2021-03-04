import pandas as pd
from .basic_operations import is_in_dic

def get_expenses_file(filepath):
    """
    Will read the expenses excel file at $filepath

    Args:
        param1: path to the expenses file

    Returns:
        Dataframe of the expenses
    """
    try:
        expenses = pd.read_excel(filepath)
    except Exception as error:
        raise error

    expenses = expenses.drop(columns=['Type','Référence interne',\
                    'Date réf. externe','Auxiliaire','N°'])
    expenses = expenses.fillna(0)
    expenses['POSTE'] = ''
    expenses['SOUS POSTE'] = ''
    return expenses


def split_expenses_file_as_worksite_csv(filepath,outputpath):
    year = filepath[-8:-4]
    splitted_expenses = {}
    worksites_names = []
    expenses = get_expenses_file(filepath)
    
    for _,row in expenses.iterrows():
        value = row['Section analytique'] 

        if not is_in_dic(str(value),worksites_names):
            worksites_names.append(str(value))

    for name in worksites_names:
        expenses.loc[expenses['Section analytique'] == name].to_csv(outputpath+year+"_"+name+".csv")


def get_worksite_expenses_csv(filepath):
    return pd.read_csv(filepath)


def get_accounting_file(filepath):
    """
    Will read the accounting plan excel file at $filepath

    Args:
        param1: path to the accounting plan file

    Returns:
        Tuple of Dataframes 
        [0] = account_worksite
        [1] = account_office
    """

    try:
        account_worksite = pd.read_excel(filepath,header=1,usecols="A:D")
        account_office = pd.read_excel(filepath,header=1,usecols="E:H")
    except Exception as error:
        raise error

    account_worksite[['POSTE']] = account_worksite[['POSTE']].fillna(method='ffill')
    account_office[['POSTE.1']] = account_office[['POSTE.1']].fillna(method='ffill')

    #Delete all NA "SOUS POSTE" rows
    account_worksite = account_worksite[pd.notnull(account_worksite['N° DE COMPTE'])]
    account_office = account_office[pd.notnull(account_office['N° DE COMPTE.1'])]

    #Remove '.1' from all columns index in account_office Dataframe
    account_office = account_office.rename(columns={'N° DE COMPTE.1':'N° DE COMPTE',\
            'POSTE.1' : 'POSTE','SOUS POSTE.1' : 'SOUS POSTE','EX..1' : 'EX.'})

    #Accounting numbers conversion to string
    account_worksite['N° DE COMPTE'] = account_worksite['N° DE COMPTE'].apply(str)
    account_office['N° DE COMPTE'] = account_office['N° DE COMPTE'].apply(str)

    #Fill remaining NA in dataframes with '/'
    values = {'SOUS POSTE': '/'}
    account_worksite = account_worksite.fillna(value=values)
    account_office = account_office.fillna(value=values)

    return (account_worksite,account_office)

def get_budget_file(filepath):
    """
    Will read the finances excel file at $filepath

    Args:
        param1: path to the finances file

    Returns:
        Dataframe of finances
    """
    try :
        finances = pd.read_excel(filepath,header=3,usecols="A:J")
    except Exception as error:
        raise error
    
    finances['POSTE'] = finances['POSTE'].fillna(method='ffill')
    finances = finances[finances['SOUS-POSTE'].notna()]
    finances = finances.fillna(0)

    return finances

if __name__ == "__main__":
    split_expenses_file_as_worksite_csv(filepath="~/DGB_Gesfin/var/Charges2020.xls",\
            outputpath="~/DGB_Gesfin/var/csv/")

