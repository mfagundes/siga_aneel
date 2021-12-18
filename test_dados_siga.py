from dados_siga import split_companies, break_percent, split_ceg, create_types_df
from fixtures import *


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


def test_split_ceg(siga_df, ceg_df) -> None:
    """
    Recebe o DataFrame do Siga e separa o CEG dos seus componentes
    :param siga_df: dataframe do Siga
    :type: pd.DataFrame
    :param ceg_df: fixture esperada
    :return: None
    """
    df_res = split_ceg(siga_df)
    assert df_res.equals(ceg_df)


def test_create_type_list(siga_df: pd.DataFrame, tipos_df: pd.DataFrame) -> None:
    """
    Como o Siga usa o tipo por extenso, criamos uma tabela, baseada no código
    que compõe o CEG, para fazer uma tabela de relacionamentos entre o código
    do tipo e seu nome por extenso
    :param siga_df: dataframe do Siga
    :type: pd.DataFrame
    :return: None
    """
    res = create_types_df(siga_df)
    assert res.equals(tipos_df)


def test_dataframe(siga_df: pd.DataFrame) -> None:
    """
    Testa se a fixture siga_df é um DataFrame do pandas
    :param siga_df: pd.Dataframe
    :return:
    """
    assert isinstance(siga_df, pd.DataFrame)
