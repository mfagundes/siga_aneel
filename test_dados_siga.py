import pandas as pd
import pytest

from dados_siga import split_companies, break_percent, break_regime

"""
Formato final dos dados para geração do DataFrame. Posteriormente, 
fazer a separação das empresas em uma tabela separada, assim teremos
o relacionamento N:N correto

data = [
    {
        'CEG': <identificador_CEG>', 
        'Empresa': '<Nome da Empresa>', 
        'Regime': '<regime_de_contratação>',
        'Participação': float(<percentual_participação>)
    }
]
"""

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


def test_split_percent_3(siga_df):
    companies_cel = siga_df.loc[2, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [0.695555, 0.305555]
    assert empresas == ['Empresa W', 'Empresa V']
    assert regimes == ['GHI', 'JKL']


def test_split_percent_2(siga_df):
    companies_cel = siga_df.loc[1, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [0.79, 0.21]
    assert empresas == ['Empresa pará', 'Empresa Y']
    assert regimes == ['ABC', 'DEF']

def test_split_percent_1(siga_df):
    companies_cel = siga_df.loc[0, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [1.0]
    assert empresas == ['Empresa A']
    assert regimes == ['PIE']


def test_3(siga_df):
    socios = siga_df.loc[2]
    assert split_companies(socios) == [
        {
            'CEG': 'PIE.AA.BB.123456-7',
            'Empresa': 'Empresa W',
            'Regime': 'GHI',
            'Participação': 0.695555
        },
        {
            'CEG': 'PIE.AA.BB.123456-7',
            'Empresa': 'Empresa Y',
            'Regime': 'JKL',
            'Participação': 0.305555
        }
    ]


def test_2(siga_df):
    socios = siga_df.loc[1]
    assert split_companies(socios) == [
        {
            'CEG': 'UHE.YY.ZZ.123456-7',
            'Empresa': 'Empresa pará',
            'Regime': 'ABC',
            'Participação': 0.79
        },
        {
            'CEG': 'UHE.YY.ZZ.123456-7',
            'Empresa': 'Empresa Y',
            'Regime': 'DEF',
            'Participação': 0.21
        }

    ]


def test_1(siga_df):
    socios = siga_df.loc[0]
    assert split_companies(socios) == [
        {
            'CEG': 'UTE.XX.XX.123456-7',
            'Empresa': 'Empresa A',
            'Regime': 'PIE',
            'Participação': 1.0
        }
    ]


def test_dataframe(siga_df):
    assert isinstance(siga_df, pd.DataFrame)
