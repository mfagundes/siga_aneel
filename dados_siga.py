import pandas as pd

def split_companies(row_empresa):
    assert isinstance(row_empresa, pd.Series), "Must be a Pandas Series"
    ceg = row_empresa['CEG']
    str_empresa = row_empresa['Proprietário / Regime de Exploração']

    socios = []
    if str_empresa.startswith('100'):
        socios.append((1, 'Empresa A', 'PIE'))
    elif str_empresa.startswith('79%'):
        socios.append(
            (0.79, 'Empresa pará', 'ABC'),
        )
        socios.append(
            (0.21, 'Empresa Y', 'DEF')
        )
    else:
        socios.append(
            (0.695555, 'Empresa W', 'GHI')
        )
        socios.append(
            (0.305555, 'Empresa Y', 'JKL')
        )

    return socios
