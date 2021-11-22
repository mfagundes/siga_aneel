import pandas as pd
import pytest

from dados_siga import split_companies, break_percent, break_regime

"""
Formato final dos dados para geração do DataFrame. Posteriormente, 
fazer a separação das empresas em uma tabela separada, assim teremos
o relacionamento N:N correto

data = [
    (ceg, empresa, regime, participacao)
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


def test_split_all_companies(siga_df):
    """
    Testa a criação do novo dataframe (deve ter 5 linhas e quatro colunas, pois temos 3 usinas no teste,
    a primeira com apenas um sócio e as outras duas com 2 sócios cada. O dataframe tem 4 colunas, que
    são: CEG, Empresa, Regime, Participação
    :param siga_df: dataframe de testes
    :return: None
    """
    df_empresas = split_companies(siga_df)
    assert isinstance(df_empresas, pd.DataFrame)
    assert df_empresas.shape == (5, 4)


def test_split_percent_3(siga_df):
    """
    Testa retorno da linha 2, onde os percentuais são decimais
    :param siga_df: dataframe de teste
    :return: None
    """
    companies_cel = siga_df.loc[2, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [0.695555, 0.305555]
    assert empresas == ['Empresa W', 'Empresa V']
    assert regimes == ['GHI', 'JKL']


def test_split_percent_2(siga_df):
    """
    Testa retorno da linha um (dois sócios, com percentuais inteiros)
    :param siga_df: dataframe de teste
    :return: None
    """
    companies_cel = siga_df.loc[1, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [0.79, 0.21]
    assert empresas == ['Empresa pará', 'Empresa Y']
    assert regimes == ['ABC', 'DEF']


def test_split_percent_1(siga_df):
    """
    Testa retorno da linha zero (um sócio, com 100%)
    :param siga_df: dataframe de teste
    :return: None
    """
    companies_cel = siga_df.loc[0, 'Proprietário / Regime de Exploração']
    participacoes, empresas, regimes = break_percent(companies_cel)
    assert participacoes == [1.0]
    assert empresas == ['Empresa A']
    assert regimes == ['PIE']


def test_dataframe(siga_df):
    """Fixture é um DataFrame"""
    assert isinstance(siga_df, pd.DataFrame)
