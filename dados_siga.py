import pandas as pd
import re


def break_regime(emp_reg):
    if isinstance(emp_reg, str):
        emp_reg = [emp_reg]
    print(emp_reg)
    empresas = []
    regimes = []
    pat_regime = re.compile('\([A-Z]+\)')
    for er in emp_reg:
        print(er)
        empresas += [e.strip() for e in pat_regime.split(er) if e]
        print('empresas', empresas)
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


def split_companies(row_empresa):
    assert isinstance(row_empresa, pd.Series), "Must be a Pandas Series"
    ceg = row_empresa['CEG']
    str_empresa = row_empresa['Proprietário / Regime de Exploração']
    participacoes, empresas, regioes = break_percent(str_empresa)

    socios = []
    if str_empresa.startswith('100'):
        socios.append({
            'CEG': ceg,
            'Empresa': 'Empresa A',
            'Regime': 'PIE',
            'Participação': 1.0
        })
    elif str_empresa.startswith('79%'):
        socios.append(
            {
                'CEG': ceg,
                'Empresa': 'Empresa pará',
                'Regime': 'ABC',
                'Participação': 0.79
            }
        )
        socios.append(
            {
                'CEG': ceg,
                'Empresa': 'Empresa Y',
                'Regime': 'DEF',
                'Participação': 0.21
            }
        )
    else:
        socios.append(
            {
                'Participação': 0.695555,
                'Empresa': 'Empresa W',
                'Regime': 'GHI',
                'CEG': ceg
            }
        )
        socios.append(
            {
                'CEG': ceg,
                'Participação': 0.305555,
                'Regime': 'JKL',
                'Empresa': 'Empresa Y'
            }
        )

    return socios
