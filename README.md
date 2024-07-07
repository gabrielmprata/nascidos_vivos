# Como os Brasileiros chegam ao mundo 🤰 👶
Sistema de Informações sobre Nascidos Vivos (SINASC)

![Como os Brasileiros chegam ao mundo](https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/27bbf386-0805-455d-aa9b-06848ee5d204)


<p align="left">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge" #vitrinedev/>  

<img src="http://img.shields.io/static/v1?label=vers%C3%A3o%20do%20projeto&message=v1.0.0&color=red&style=for-the-badge&logo=github"/>
</p>
<br>

## 🖥️ Demo App

# :radio_button: Objetivo 
Criar um simples Dashboard em **Python** e **Streamlit**, para mostrar caractéristicas do nascimento, destacando caractéristicas das mães, dos recém-nascidos, distribuição geográficas e socioeconômicas.

Com a analise dos dados, podemos fornecer informações para o planejamento e avaliação das políticas de saúde, auxiliando na tomada de decisões.
<br><br>
# :hammer: Ferramentas utilizadas
<img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" width="40" height="40"/>   <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/plotly/plotly-original-wordmark.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original-wordmark.svg" width="40" height="40"/>
<br></br>
# Introdução

Os dados apresentados nesse estudo acadêmico, referem-se aos características do nascimento dos brasileiros.

O nascimento é um dos eventos vitais e seu monitoramento pode contribuir para o conhecimento da situação de saúde de uma população, pois permite a construção de indicadores que subsidiam o planejamento, a gestão e a avaliação de políticas e ações de vigilância e atenção à saúde na área da saúde materna e infantil.

O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de mortalidade para a gestante e para a criança.
No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.

<br><br>
###
## **<font color=#85d338> 1. Definição do problema**
>
###
## **<font color=#85d338> 2. Coleta de Dados**
>
**2.1 Nascidos Vivos**
>
<p align="left"><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/b694a34c-eb8f-4498-9129-0a29a98492a5"></img>As informações dos Nascidos Vivos, estão no sítio de dados abertos do OpenDataSus:</p>

> Link: https://opendatasus.saude.gov.br/dataset/sistema-de-informacao-sobre-nascidos-vivos-sinasc

>
**2.2.1 CNES**
>
Dataset auxiliar, com as informações dos estabelecimentos de saúde.
>
> Link: https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/CNES/cnes_estabelecimentos.zip
>
**2.2.2 Municípios IBGE API**
>
```
pip install ibge
```
>
```
from ibge.localidades import *
```
<br>

## **<font color=#85d338> 3. Pré-porcessamento**
>
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1mulsenF2L_Vjm-yDFTv0t2o74Mhqx49L)
>
Esta é a etapa mais demorada e trabalhosa do projeto de ciência de dados, e estima-se que consuma pelo menos 70% do tempo total do projeto.
>
Após coletar e analisar os dados na etapa anterior, é necessário limpar, transformar e apresentar melhor os seus dados, a fim de obter, na próxima etapa, os melhores resultados possíveis nos algoritmos de machine learning ou simplesmente apresentar dados mais confiáveis para os clientes em soluções de
business intelligence.
>
Como o nosso objetivo é criar um Dashboard com **Python** e **Streamlit**, iremos minimizar ao máximo o tamanho e a granularidade dos Datasets disponibilizados, a fim de termos um ambiente mais "leve" para a leitura dos dados.
>
Principais técnicas utilizadas:
>
**Limpeza:** Consiste na verificação da consistência das informações, correção de possíveis erros de preenchimento ou eliminação de valores desconhecidos, redundantes ou não pertencentes ao domínio.
>
**Agregação:** Também pode ser considerada uma técnica de redução de dimensionalidade, pois reduz o número de linhas e colunas de um dataset.
>
**Tratamendo de dados faltantes (missing):** Identificamos e, em seguida, tratamos com um valor adequado. Não foi necessario a exclusão desses registros.
>
## **<font color=#85d338> 4. Apresentação dos resultados**
>
O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de morbimortalidade para a gestante e para a criança. No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.
>
No ano de 2023 o Brasil registrou 2,53 milhões de nascimentos, com uma queda de 1,17% em comparação com 2022, chegando ao menor patamar desde 1977.
>
O Brasil registra a quinta queda consecutiva, desde 2019.
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/0fca5553-b3d4-49cf-b267-f47cfa596217" alt="Top"  height="400">

Afinal, no Brasil nascem mais meninos ou meninas?
>
Bom, no histórico deste estudo, desde o ano 2000, nascem mais meninos do que meninas.
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/7364d00a-3ea5-48b5-b493-085cf90889cb" alt="Top"  height="270">

**Histórico pela idade das mães**
>
Outra informação importante, é a quantidade de nascimentos por faixa etáriae da mãe.
>
Esse dado é utilizado em estudos relacionados com o comportamento reprodutivo das mulheres, permitindo analisar as transformações demográficas que estão ocorrendo no Brasil.
>
Ao longo do período analisado, vemos uma tendência de crescimento relativo a mães com idade entre 40 e 44 anos.
>
E uma redução no nascimento por mães jovens, entre 15 e 19 anos.
>
E precisamos comemorar a redução na faixa etaria entre 10 e 14 anos, pois vida sexual abaixo de 14 anos é considerada estupro de vunerável. Mesmo que a relação seja consentida, perante a nossa lei é um abuso sexual.
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/de3ddc7f-fc14-4692-b642-cefa6ad97bcd" alt="Top"  height="270">

**Evolução das regiões e dos estados**
>
Nos últimos cinco anos, todas regiões também seguiram a tendência de queda.
>
A região Nordeste foi a que mais apresentou retração, seguida do sudeste, com -16,35% e -15,88% respectivamente.
>
Nesse período, somente a região Norte registrou em 2020 um aumento de registros de nascimento, 2,54% e em 2023, o Centro-Oeste teve um pequeno aumento de 0,76%.
>
O Sudeste mesmo com queda, continua sendo a região com mais registros de nascimento no Brasil.
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/7619c6c4-7a86-40a2-ab36-75ad0a1787b6" alt="Top"  height="350">

**Como os brasileiros chegaram ao mundo em 2023**
>
Em 2023, chegaram ao mundo **2.532.050** brasileiros!
>
Representando uma média mensal de 211 mil nascidos vivos.
>
Março foi o mês com mais nascimentos, 234.022, seguido por Maio, com 230.858
>
Na outra ponta, o mês de Novembro foi o que teve menos nascimentos, com 190.052.
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/6eba2dad-3c80-448d-8d09-d80272e90539" alt="Top"  height="350">

 **Nascidos-vivos por dia da semana e hora**
>
Nascem mais crianças no início da semana, esse número cai nos finais de semana, por conta das cesárias, que geralmente são agendadas em dia úteis.
>
Os partos vaginais seguem a mesma tendência durante todos os dias da semana.
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/9b06979b-38b9-42b7-adeb-6df9905431b0" alt="Top"  height="350">

Entre as 8 e as 11 horas da manhã e entre 14 e 17 horas da tarde, são os periodos em que ocorrem mais nascimentos.
>
As cesárias praticamente dominam esse periodo, enquanto que o parto vaginal mantem uma mesma constancia ao longo do dia.
>
**Em 2023, nasceram 288 crianças por hora, ou 4 por minuto, ou 6932 por dia.**
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/5f7e6d3a-9bac-4f7e-86fc-69e4b0a66b56" alt="Top"  height="350">

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/19bd5752-ff3c-40ae-93d8-ae7843f1b06f" alt="Top"  height="350">
