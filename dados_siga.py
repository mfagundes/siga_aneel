import pandas as pd
import re


def break_regime(emp_reg):
    """
    Função para separar, em cada uma das empresas da lista, os seus nomes e respectivos regimes de contratação
    :param emp_reg: lista de empresas e regimes
    :type: list
    :return: tupla de listas dos nomes de empresas e regimes de contratação
    :rtype: tuple
    """
    if isinstance(emp_reg, str):
        emp_reg = [emp_reg]
    empresas = []
    regimes = []
    pat_regime = re.compile('\([A-Z]+\)')  # padrão para os regimes, p.ex. (PIE)
    for er in emp_reg:
        # em cada elemento da lista emp_reg é feito um split, o que retorna
        # uma lista de nome de enpresas
        empresas += [e.strip() for e in pat_regime.split(er) if e]

        # localiza todos os regimes usando o re.findall e insere na lista de regimes,
        # eliminando os parênteses
        regimes_all = pat_regime.findall(er)
        regimes += [r[1:-1] for r in regimes_all]
    return empresas, regimes


def break_percent(empresa):
    """
    Função para separar a célula de participações por empresa. Gera uma sequência de valores percentuais,
    na forma de um float de 0 a 1 e uma sequência de empresas e regimes, que são separadas na função
    break_regime, retornando a sequência de empresas e seus regimes de contratação
    :param empresa: célula de Participação / Regime do SIGA
    :type: str
    :return: tupla de listas, com as sequências de percentual, nome da empresa e regimes
    :rtype: tuple
    """
    pattern = r'\d+\.*\d+%'  # regex para os percentuais, na forma 00.0000%
    pat = re.compile(pattern)

    # localiza os percentuais e salva numa lista sequencial, calculando o valor percentual como
    # um float com 6 dígitos - o Siga usa o padrão de 4 casa decimais, assim teremos as duas
    # casas do inteiro e as quatro decimais compondo o valor
    part = pat.findall(empresa)  # localiza todos os percentuais
    participacoes = [round(float(p.strip('%'))/100, ndigits=6) for p in part]

    # re.split busca as ocorrências de percentuais na linha e quebra a linha, gerando uma lista
    # com os nomes das empresas e vazio onde o regex é atingido
    emp_regime = [emp.replace('para', '').strip() for emp in re.split(pat, empresa) if emp]
    empresas, regimes = break_regime(emp_regime)
    return participacoes, empresas, regimes


def split_companies(df_empresas):
    """
    Função para separar as empresa de acordo com sua participação e regime de contratação

    :param df_empresas: dataframe do SIGA
    :type: pd.DataFrame
    :return: Dataframe contendo a coluna identificadora da usina (CEG) e os dados de participação
    :rtype: pd.DataFrame
    """
    socios = []
    for id, row_empresa in df_empresas.iterrows():
        str_empresa = row_empresa['Proprietário / Regime de Exploração']

        # quebra a string nos percentuais e, depois, nos regimes de contratação
        participacoes, empresas, regimes = break_percent(str_empresa)

        # o CEG da usina é inserido na lista de acordo com o número de empresas retornadas
        cegs = [row_empresa['CEG']] * len(empresas)

        # cria uma lista de tuplas contendo (ceg, empresa, regime, participacao)
        socio = zip(cegs, empresas, regimes, participacoes)

        # insere cada sócio (a tupla acima) na lista de socios
        for s in list(socio):
            socios.append(s)
    df = pd.DataFrame(socios, columns=['ceg', 'empresa', 'regime', 'participacao'])  # gera o dataframe para salvar
    return df
