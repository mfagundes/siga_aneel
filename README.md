# Banco de dados do SIGA (Sistema de Informações de Geração da Aneel)

A Aneel fornece [um relatório feito em PowerBI](https://app.powerbi.com/view?r=eyJrIjoiNjc4OGYyYjQtYWM2ZC00YjllLWJlYmEtYzdkNTQ1MTc1NjM2IiwidCI6IjQwZDZmOWI4LWVjYTctNDZhMi05MmQ0LWVhNGU5YzAxNzBlMSIsImMiOjR9) que, apesar de atualizado constantemente, possui apenas um link para download dos dados de empreendimentos outorgados. Este arquivo (formato Excel) é atualizado apenas no início de cada mês, com os dados históricos do mês anterior.

Ao longo do tempo, já tive dois problemas distintos:

1. alteração de coordenadas das usinas: as colunas de coordenadas decimais foram apagadas e substituídas por DMS (Degree Minute Second), sendo que pouco menos de 10% estavam localizadas. A partir de localizações anteriores, pude reconstruir os dados
2. mudança de nome de coluna (a simples inserção de um espaço no nome quebrava a limpeza automatizada feita pelo PowerQuery)

Além disso a participação dos investidores em cada projeto é feito de forma textual, sendo difícil de levantar os valores ponderados. E vários empreendimentos possuem participação de SPEs (Sociedade de Propósito Específico) que têm participação de outras empresas do setor. Isso inviabiliza a agregação dos valores, a menos que se faça um relacionamento dessas sociedades com seus participantes.

Tal separação será feita posteriormente

Como são dados em formato de planilha, temos diversos campos de relacionamento, que podem ser reaproveitados. O objetivo deste trabalho é gerar um fluxo mensal que atualize os dados e os consolide, de forma que a atualização mensal apenas atualize os dados novos e mantenha um relacionamento mais estável, permitindo criar um pipeline de atualização mensal mais limpo e confiável

Este primeiro trabalho irá gerar tais tabelas e salvá-las ainda em arquivos CSV. Posteriormente estes poderão ser migrados para alguma forma de armazenamento, seja um Data Lake ou Data Warehouse.

**Referências**

Atualmente uso como referências os seguintes projetos:
- [Datasette](https://datasette.io/) que, conforme o próprio autor [Simon Willison](https://simonwillison.net/) surgiu de uma necessidade de um veículo de comunicação (The Guardian)
- [FiveThirdyEight](https://fivethirtyeight.com/), que usa o próprio Datasette
- [CKAN](https://ckan.org/), muito utilizado por diversas organizações no planeta - e que contém APIs para acesso aos dados com autenticação via token
- [Brasil.io](https://brasil.io/home/) projeto de repositório de dados públicos


## Datasette
Neste [vídeo](https://www.youtube.com/watch?v=7kDFBnXaw-c) do Simon Willison, ele cita o motivo de usar o [SQLite](https://www.sqlite.org/index.html) (a partir [deste momento](https://youtu.be/7kDFBnXaw-c?t=300)) com base na realidade que ele encontrou no The Guardian. Neste momento é um caso interessante para o meu propósito atual e, considerando que o SQLite já cria uma base de dados relacional, utilizando apenas arquivos binários, ele já é uma boa base para uma futura migração para ferramentas mais complexas. Considero que esta pode ser uma ferramenta bem útil para o meu caso.

**À medida que outras soluções forem avaliadas, irei atualizando este documento**