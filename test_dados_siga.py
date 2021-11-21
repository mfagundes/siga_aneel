import pandas as pd
import pytest

from dados_siga import split_companies

@pytest.fixture
def siga_df():
    df = pd.DataFrame([
        {
            'CEG': 'UTE.XX.XX.123456-7',
            'Proprietário / Regime de Exploração': '100% para Empresa A (PIE)'
        },
        {
            'CEG': 'UHE.YY.ZZ.123456-7',
            'Proprietário / Regime de Exploração': '79% para Empresa pará (ABC) 21% para Empresa Y (DEF)'
        },
        {
            'CEG': 'PIE.AA.BB.123456-7',
            'Proprietário / Regime de Exploração':'69.5555% para Empresa W (GHI) 30.5555% para Empresa V (JKL)'
        }
    ])
    return df


def test_3(siga_df):
    socios = siga_df.loc[2]
    assert split_companies(socios) == [
        (0.695555, 'Empresa W', 'GHI'),
        (0.305555, 'Empresa Y', 'JKL')
    ]

#
def test_2(siga_df):
    socios = siga_df.loc[1]
    assert split_companies(socios) == [
        (0.79, 'Empresa pará', 'ABC'),
        (0.21, 'Empresa Y', 'DEF')
    ]

def test_1(siga_df):
    socios = siga_df.loc[0]
    assert split_companies(socios) == [(1, 'Empresa A', 'PIE')]


def test_dataframe(siga_df):
    assert isinstance(siga_df, pd.DataFrame)
