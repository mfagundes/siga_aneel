from typing import List, Tuple

import pandas as pd
import re


def break_percent(company: str) -> Tuple[List, List, List]:
    """
    Function to separate the participation cell by company. Generates a sequence of percentage values,
    in the form of a float from 0 to 1 and a sequence of companies and regimes, which are separated in
    the function break_regime, returning the sequence of companies and their hiring regimes

    :param company: cell Participação / Regime do SIGA (Participation / SIGA Regime
    :type: str
    :return: tuple of 3 lists: percentual of participation, company name and hiring regime
    :rtype: Tuple[List, List, List]
    """
    pattern = r'\d+\.*\d+%'  # regex for percentages, in the form of [0]0.0000%
    pat = re.compile(pattern)

    # finds the percentages and save them in a sequential list, calculating  percentage
    # rounded for 6 digit floats - SIGA uses the pattern of 4 decimal digits.
    part = pat.findall(company)  # find all percentuals
    participations = [round(float(p.strip('%'))/100, ndigits=6) for p in part]

    # re.split finds all occurrences of percentages in the line and breaks it, creating a list
    # with companies names and an empty string where regex exists
    comp_regime = [c.replace('para', '').strip() for c in re.split(pat, company) if c]
    companies, regimes = break_regime(comp_regime)
    return participations, companies, regimes


def break_regime(comp_reg: list) -> Tuple[List, List]:
    """
    Function to separate, in the owners list, their names and respective types of contracts
    :param comp_reg: list of companies and their respective hiring regimes
    :type: list
    :return: tuple of lists with companies names and hiring regimes
    :rtype: Tuple[List, List]
    """
    if isinstance(comp_reg, str):
        emp_reg = [comp_reg]
    companies = []
    regimes = []
    pattern = r'\([A-Z]+\)'
    pat_regime = re.compile(pattern)  # padrão para os regimes, p.ex. (PIE)
    for company in comp_reg:
        # the list comp_reg is split with re.split, which creates a list with the
        # names of the companies and an empty string where it matches the pattern
        companies += [e.strip() for e in pat_regime.split(company) if e]

        # finds all regimes using re.findall an insert it in the list of regimes,
        # without parenthesis
        regimes_all = pat_regime.findall(company)
        regimes += [r[1:-1] for r in regimes_all]
    return companies, regimes


def split_companies(df_companies):
    """
    Function to separate the companies according to their participation and hiring regime
    :param df_companies: dataframe do SIGA
    :type: pd.DataFrame
    :return: Dataframe with CEG (enterprise identifier) containing the CEG column and participation data
    :rtype: pd.DataFrame
    """
    partners = []
    for id, row_company in df_companies.iterrows():
        company = row_company['Proprietário / Regime de Exploração']
        if company and str(company) != 'nan':
            # breaks company string in percentuals and, later, in their hiring regime
            participations, companies, regimes = break_percent(company)

            # CEGS is a list of current CEG according to the number of returned companies
            # This is necessary to zip the values to create a relationship table (n:n)
            cegs = [row_company['CEG']] * len(companies)

            # cria uma lista de tuplas contendo (ceg, empresa, regime, participacao)
            partner = zip(cegs, companies, regimes, participations)

            # inserts each partner (tuple above) in the partners list
            # insere cada sócio (a tupla acima) na lista de socios
            for s in list(partner):
                partners.append(s)
    df = pd.DataFrame(partners, columns=['ceg', 'empresa', 'regime', 'participacao'])
    return df


def split_ceg(siga_df):
    """
    CEG variable is, in fact, the union of several fields. Therefore we can use the enterprise data
    to generate them. This can be useful in case of future changes in the files
    CEG =>  Fonte (Source) (UHE, UTE, etc) .
            Tipo (Type) (acronym that identifies the Type (Tipo) in words (eg. PH: Potencial Hidráulico) .
            UF (state abbreviation)
            Núcleo CEG: unique number with identification digit (dv)
    :param siga_df: DataFrame from SIGA
    :type: str
    :return: DataFrame with data separated according with CEG structure, with the following columns
            CEG: object,
            fonte: object,
            tipo: object,
            uf: object,
            nucleo_ceg: int,
            dv: int
    :rtype: pd.DataFrame
    """

    all_ceg = []

    for _, row in siga_df.iterrows():
        all_ceg.append(break_ceg_into_columns(row))

    ceg_df = pd.DataFrame(all_ceg,)
    return ceg_df


def break_ceg_into_columns(row: pd.Series) -> dict:
    """
    Given a CEG number, split into columns to create DataFrame with
    all values that composes the CEG identifier
    :param row: line of the DataFrame that will have CEG to be separated
    :type: pd.Series
    :return: dict
    """
    ceg = row['CEG']
    source = row['Fonte']
    type_ = row['Tipo']
    uf = row['UF']
    ceg_number = ceg.split('.')[-1].split('-')[0]
    verification_digit = ceg.split('.')[-1].split('-')[1]
    return {
        'ceg':ceg,
        'fonte': source,
        'tipo': type_,
        'uf': uf,
        'nucleo_ceg': ceg_number,
        'dv': verification_digit
    }


def create_types_df(siga_df):
    """
    From SIGA table, we create a new table with types in words and their respective
    ids, used to form the final CEG
    :param siga_df: SIGA DataFrame
    :type: pd.DataFrame
    :return: dataframe with columns of type ids and their respective names
    :rtype: pd.DataFrame
    """
    types_id = []
    types_ext = []
    for _, row in siga_df.iterrows():
        type_id = row['CEG'].split('.')[1]
        if type_id not in types_id:
            types_id.append(type_id)
            types_ext.append(row['Tipo'])
    types_data = zip(types_id, types_ext)
    df_types = pd.DataFrame(types_data, columns=['tipo_id', 'tipo_ext'])
    df_types.sort_values('tipo_id', inplace=True)
    df_types.reset_index(inplace=True, drop=True)
    return df_types
