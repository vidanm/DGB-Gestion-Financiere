import pandas as pd
from .basic_operations import is_in_dic
import datetime

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


def get_csv_expenses(filepath):
    return pd.read_csv(filepath)

def split_salary_file_as_salary_csv(filepath,outputpath):
    salary = get_salary_file(filepath,columns="B:D")
    salary = salary.append(get_salary_file(filepath,columns="E:G"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="H:J"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="K:M"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="N:P"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="Q:S"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="T:V"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="W:Y"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="Z:AB"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="AC:AE"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="AF:AH"),ignore_index=True)
    salary = salary.append(get_salary_file(filepath,columns="AI:AK"),ignore_index=True)

    salary = salary.sort_values("Section analytique")
    salary = salary.reset_index(drop=True)

    csv = pd.DataFrame()
    current_code = ""
    for _,row in salary.iterrows():
        if row["Section analytique"] != current_code:
            if (current_code != ""):
                csv.to_csv(str(outputpath)+"SALAIRES2020"+"_"+str(current_code)+".csv")
            current_code = row["Section analytique"]
            csv = pd.DataFrame([row])
        else :
            csv = csv.append(row)

def get_salary_file(filepath,columns):
    try:
        salary = pd.read_excel(filepath,usecols=columns,header=2)
        date = ""
        for col in salary.columns:
            if isinstance(col,datetime.datetime):
                date = col
            else:
                if len(str(col).split('.')) == 2:
                    salary = salary.rename(columns={col:(str(col).split('.')[0])})
        
        salary = salary.rename(columns={date:"Débit","Code compt":"Général","Code chantier":"Section analytique"})
        salary.insert(0,column="Date",value=date)
        salary.insert(0,column="Journal",value="ACH")
        salary.insert(0,column="Libellé",value="")
        salary.insert(0,column="Crédit",value=0)
        return salary
    except Exception as error:
        raise error

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

