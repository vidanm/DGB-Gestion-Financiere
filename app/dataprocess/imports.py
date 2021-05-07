import pandas as pd
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

    column_to_drop = [
        'Type', 'Référence interne', 'Date réf. externe', 'Auxiliaire', 'N°',
        'Pièce', 'Libellé', 'Solde', 'Monnaie'
    ]

    expenses = expenses.drop(columns=column_to_drop, errors='ignore')
    expenses = expenses.fillna(0)
    # expenses = expenses['Section analytique'].str.strip()
    expenses['POSTE'] = ''
    expenses['SOUS POSTE'] = ''
    return expenses


def split_expenses_file_as_worksite_csv(filepath, outputpath):
    # worksites_names = []

    expenses = get_expenses_file(filepath)
    worksite_names = expenses["Section analytique"].unique()

    # for _, row in expenses.iternotrows():
    #    value = row['Section analytique']
    #
    #    if not is_in_dic(str(value), worksites_names):
    #        worksites_names.append(str(value))

    for name in worksite_names:
        sep = expenses.loc[expenses['Section analytique'] == name]
        sep = sep.sort_values(['Date'], ascending=True)
        sep['Year'] = pd.DatetimeIndex(sep['Date']).year

        # out = pd.DataFrame(columns=sep.columns)

        years = sep['Year'].unique()

        for year in years:
            sep.loc[sep['Year'] == year]\
             .drop(columns='Year')\
             .to_csv(outputpath + str(year) + "_" + name + ".csv")

        # for index, row in sep.iternotrows():
        #    if index == 0:
        #        current_year = row['Date'].year
        #        out = out.append(row)
        #    else:
        #        if current_year == row['Date'].year:
        #            out = out.append(row, ignore_index=True)
        #        else:
        #            out.to_csv(outputpath + str(current_year) + "_" + name +
        #                       ".csv")
        #            current_year = row['Date'].year
        #            out = pd.DataFrame(columns=sep.columns)
        #            out = out.append(row)
        # out.to_csv(outputpath + str(current_year) + "_" + name + ".csv")


def get_csv_expenses(filepath):
    return pd.read_csv(filepath)


def split_salary_file_as_salary_csv(filepath, outputpath):
    xl = pd.ExcelFile(filepath)
    for sheet in xl.sheet_names:
        if "AFFECTATION" in sheet:
            salary = get_salary_file(filepath, "B:D", sheet)
            salary = salary.append(get_salary_file(filepath, "E:G", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "H:J", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "K:M", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "N:P", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "Q:S", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "T:V", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "W:Y", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "Z:AB", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "AC:AE", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "AF:AH", sheet),
                                   ignore_index=True)
            salary = salary.append(get_salary_file(filepath, "AI:AK", sheet),
                                   ignore_index=True)

            salary["Section analytique"] = salary["Section analytique"].astype(str)
            salary = salary.sort_values("Section analytique")
            salary = salary.reset_index(drop=True)

            worksite_names = salary["Section analytique"].unique()
            for name in worksite_names:
                if name == "nan":
                    continue

                salary.loc[salary["Section analytique"] == name].to_csv(
                        str(outputpath) + sheet[-4::] + "SALAIRES" + "_" +
                        str(name) + ".csv")

            # current_code = ""
            # for _, row in salary.iternotrows():
            #    if row["Section analytique"] != current_code:
            #        if (str(current_code) != ""
            #                and str(current_code) != "nan"):
            #            csv.to_csv(
            #                str(outputpath) + sheet[-4::] + "SALAIRES" + "_" +
            #                str(current_code) + ".csv")
            #        current_code = row["Section analytique"]
            #        csv = pd.DataFrame([row])
            #    else:
            #        csv = csv.append(row)


def get_salary_file(filepath, columns, sheet):
    try:
        salary = pd.read_excel(filepath,
                               usecols=columns,
                               header=2,
                               sheet_name=sheet)
        date = ""
        for col in salary.columns:
            if isinstance(col, datetime.datetime):
                date = col
            else:
                if len(str(col).split('.')) == 2:
                    salary = salary.rename(
                        columns={col: (str(col).split('.')[0])})

        salary = salary.rename(
            columns={
                date: "Débit",
                "Code compt": "Général",
                "Code chantier": "Section analytique"
            })
        salary.insert(0, column="Date", value=date)
        salary.insert(0, column="Journal", value="ACH")
        salary.insert(0, column="Libellé", value="")
        salary.insert(0, column="Crédit", value=0)
        salary["Débit"] = salary["Débit"].fillna(0)
        # salary["Section analytique"] = \
        # salary["Section analytique"].str.strip()
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
        account_worksite = pd.read_excel(filepath, header=1, usecols="A:D")
        account_office = pd.read_excel(filepath, header=1, usecols="E:H")
        account_divers = pd.read_excel(filepath,header=1,usecols="I:K")
    except Exception as error:
        raise error

    account_worksite[['POSTE']] = account_worksite[['POSTE'
                                                    ]].fillna(method='ffill')
    account_office[['POSTE.1']] = account_office[['POSTE.1'
                                                  ]].fillna(method='ffill')
    account_divers[['POSTE.2']] = account_divers[['POSTE.2'
                                                  ]].fillna(method='ffill')

    # Delete all NA "SOUS POSTE" rows
    account_worksite = account_worksite[pd.notnull(
        account_worksite['N° DE COMPTE'])]
    account_office = account_office[pd.notnull(
        account_office['N° DE COMPTE.1'])]
    account_divers = account_divers[pd.notnull(
        account_divers['N° DE COMPTE.2'])]

    # Remove '.1' from all columns index in account_office Dataframe
    account_office = account_office.rename(
        columns={'N° DE COMPTE.1': 'N° DE COMPTE', 'POSTE.1': 'POSTE',
                 'SOUS POSTE.1': 'SOUS POSTE', 'EX..1': 'EX.'})

    account_divers = account_divers.rename(
            columns={'N° DE COMPTE.2': 'N° DE COMPTE', 'POSTE.2': 'POSTE',
                 'SOUS POSTE.2': 'SOUS POSTE'})

    # Accounting numbers conversion to string
    account_worksite['N° DE COMPTE'] = account_worksite['N° DE COMPTE'].apply(
        str)
    account_office['N° DE COMPTE'] = account_office['N° DE COMPTE'].apply(str)
    account_divers['N° DE COMPTE'] = account_divers['N° DE COMPTE'].apply(str)

    # Fill remaining NA in dataframes with '/'
    values = {'SOUS POSTE': '/'}
    account_worksite = account_worksite.fillna(value=values)
    account_divers = account_divers.fillna(value=values)
    account_office = account_office.fillna(value=values)

    account_worksite = pd.merge(account_worksite,account_divers,how='outer')
    account_worksite.append(account_divers)
    # account_worksite["POSTE"] = account_worksite["POSTE"].str.strip()
    # account_worksite["SOUS POSTE"] =\
    # account_worksite["SOUS POSTE"].str.strip()
    # account_office["POSTE"] = account_office["POSTE"].str.strip()
    # account_office["SOUS POSTE"] = account_office["SOUS POSTE"].str.strip()
    print(account_worksite)
    return (account_worksite, account_office)


def get_budget_file(filepath):
    """
    Will read the finances excel file at $filepath

    Args:
        param1: path to the finances file

    Returns:
        Dataframe of finances
    """
    try:
        finances = pd.read_excel(filepath, header=3, usecols="A:J")
        # A:J n'est pas generique
    except Exception as error:
        raise error

    finances['POSTE'] = finances['POSTE'].fillna(method='ffill')
    finances = finances[finances['SOUS-POSTE'].notna()]
    # finances = finances.set_index('SOUS-POSTE')
    finances = finances.fillna(0)
    # finances['POSTE'] = finances["POSTE"].str.strip()
    # finances['SOUS-POSTE'] = finances["SOUS-POSTE"].str.strip()

    return finances


if __name__ == "__main__":
    split_expenses_file_as_worksite_csv(
            filepath="~/DGB_Gesfin/var/Charges2020.xls",
            outputpath="~/DGB_Gesfin/var/csv/")
