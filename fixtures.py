import pandas as pd
import pytest

@pytest.fixture
def siga_df():
    df = pd.DataFrame([
        {
            'CEG': 'UTE.PH.RS.123456-7',
            'UF': 'RS',
            'Fonte': 'UHE',
            'Tipo': 'Potencial Hidráulico',
            'Proprietário / Regime de Exploração': '100% para Empresa A (PIE)'
        },
        {
            'CEG': 'UHE.PE.SC.123456-7',
            'UF': 'SC',
            'Fonte': 'UTE',
            'Tipo': 'Petróleo',
            'Proprietário / Regime de Exploração': '79% para Empresa pará (ABC) 21% para Empresa Y (DEF)'
        },
        {
            'CEG': 'PIE.PE.MG.123456-7',
            'UF': 'MG',
            'Fonte': 'UTE',
            'Tipo': 'Petróleo',
            'Proprietário / Regime de Exploração':'69.5555% para Empresa W (GHI) 30.5555% para Empresa V (JKL)'
        }
    ])
    return df

@pytest.fixture
def ceg_df():
    dict_res = [
        {
            'ceg': 'UTE.PH.RS.123456-7',
            'uf': 'RS',
            'fonte': 'UHE',
            'tipo': 'Potencial Hidráulico',
            'nucleo_ceg': '123456',
            'dv': '7'
        },
        {
            'ceg': 'UHE.PE.SC.123456-7',
            'uf': 'SC',
            'fonte': 'UTE',
            'tipo': 'Petróleo',
            'nucleo_ceg': '123456',
            'dv': '7'
        },
        {
            'ceg': 'PIE.PE.MG.123456-7',
            'uf': 'MG',
            'fonte': 'UTE',
            'tipo': 'Petróleo',
            'nucleo_ceg': '123456',
            'dv': '7'
        }
    ]
    ceg_df = pd.DataFrame(dict_res)
    ceg_df = ceg_df[['ceg', 'fonte', 'tipo', 'uf', 'nucleo_ceg', 'dv']]
    return ceg_df


@pytest.fixture
def tipos_df():
    tipos_df = pd.DataFrame([['PE', 'Petróleo'], ['PH', 'Potencial Hidráulico']], columns=['tipo_id', 'tipo_ext'])
    return tipos_df
