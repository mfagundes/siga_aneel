import pandas as pd
import re


def break_regime(emp_reg):
    if isinstance(emp_reg, str):
        emp_reg = [emp_reg]
    empresas = []
    regimes = []
    pat_regime = re.compile('\([A-Z]+\)')
    for er in emp_reg:
        empresas += [e.strip() for e in pat_regime.split(er) if e]
        regimes_all = pat_regime.findall(er)
        regimes += [r[1:-1] for r in regimes_all]
    return empresas, regimes


def break_percent(empresa):
    pattern = r'\d+\.*\d+%'
    pat = re.compile(pattern)
    part = pat.findall(empresa)
    participacoes = [round(float(p.strip('%'))/100, ndigits=6) for p in part]

    emp_regime = [emp.replace('para', '').strip() for emp in re.split(pat, empresa) if emp]
    empresas, regimes = break_regime(emp_regime)
    return participacoes, empresas, regimes


def split_companies(df_empresas):
    socios = []
    for id, row_empresa in df_empresas.iterrows():
        str_empresa = row_empresa['Proprietário / Regime de Exploração']
        participacoes, empresas, regimes = break_percent(str_empresa)
        cegs = [row_empresa['CEG']] * len(empresas)
        socio = zip(cegs, empresas, regimes, participacoes)
        for s in list(socio):
            socios.append(s)
    df = pd.DataFrame(socios, columns=['ceg', 'empresa', 'regime', 'participacao'])
    return df
