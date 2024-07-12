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

**Mapa do Brasil**
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/30d2aa66-8ab4-4597-9bf3-f00e8cc9eda2" alt="Top"  height="350">

O estado com o maior número de nascimentos foi **São Paulo**, com 505.331, representando quse 20% dos nascimentos no Brasil.
>
Em São Paulo nascem 118% a mais que Minas Gerais, que é o segundo estado com mais nascimentos.
>
|uf|Nascidos|Percentual|ranking|
|--|--------|----------|-------|
|SP|505331|19.96|1|
|MG|232270|9.17|2|
|RJ|175934|6.95|3|
|BA|165239|6.53|4|
|PR|140002|5.53|5|
|PA|123806|4.89|6|
|RS|120893|4.77|7|
|PE|116416|4.6|8|
|CE|111388|4.4|9|
|SC|96359|3.81|10|

**Por Região**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/d591be81-52b7-4604-ac78-781201f29951" alt="Top"  height="300"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/753ed1df-45f5-4e09-aa32-4ae4a19814fd" alt="Top"  height="300"> </td>
    </tr>
</table>

A região sudeste é a que concentra o maior número de nascidos vivos, 38%, seguida do Nordeste com 28%.

**Nascidos Vivos segundo sexo**
>
<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/87fab485-760a-44b8-a758-8cd2f5de9ba5" alt="Top"  height="200">

No Brasil em 2023 nasceram 1,29 milhões de meninos(51,2%) e 1,23 milhões de meninas(48,8%).

**Distribuição nascidos vivos de acordo com o sexo e por região**

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/27b9e0be-90dc-4e15-9727-4a66608fdc87" alt="Top"  height="300">

Nas regiões, temos o mesmo comportamento na proporção de nascimento por sexo.

**Nascidos Vivos segundo local de nascimento**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/69ed9ae2-6c12-4e98-9a3f-e332fba5fc80" alt="Top"  height="200"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/49fc25b8-2d5a-417e-a603-92d8f9125576" alt="Top"  height="300"> </td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/4c6af08e-e375-44d0-9e1d-223d13d06a7d" alt="Top"  height="200"> </td>
    </tr>
</table>

A maioria dos nascimentos segue sendo em Hospitais, cerca de 98%, mas ainda há uma quantidade consideravel de nascimentos em domicílios, cerca de 15 mil.
>
Os hospitais de gestão Municipal, são os que mais realizam partos, 1.62 milhões, representando 65% do total.
>
Outro dado importante é a quantidade de nascimentos em aldeias indíginas, cerca de 1.779 no ano de 2023.

**Nascidos Vivos com anomalias congênitas segundo região**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/5c9f2d48-c293-4644-9f39-d8840b43ef84" alt="Top"  height="200"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/b46bb28d-9c3d-4ce4-9bf1-9b36cada190f" alt="Top"  height="300"> </td>
    </tr>
</table>

As anomalias congênitas são um grupo de alterações estruturais ou funcionais que ocorrem durante a vida intrauterina e que podem ser detectadas antes, durante ou após o nascimento.
>
Podem afetar diversos órgãos e sistemas do corpo humano e são causadas por um ou mais fatores genéticos, infecciosos, nutricionais e ambientais, podendo ser resultado de uma combinação desses fatores.
>
No ano de 2023, em 97% dos partos não foram identificadas anomalias, e em apenas 0,98% (24.770) foram identificadas.
>
A região Sudeste registra 44,1% dos nascidos vivos com anomalias, seguido pelo Nordeste com 26,9%.

**Nascidos Vivos de acordo com score Apgar no 1º e 5º minuto**

Cerca de 90% dos bebês nascem em ótimas condições, com nota geral de 8 a 10. Abaixo disso, os índices revelam dificuldades: 7 (leve), de 4 a 6 (moderada) e de 0 a 3 (grave).
>
Crianças com pontuações inferiores a 7, recebem assistência imediata visando o aumento da classificação.
>
A primeira média é dada no primeiro minuto, depois no quinto e no décimo minutos.
>
Segundo a média, em todo o mundo, cerca de 4% dos recém-nascidos obtêm índice inferior a 7. Em alguns casos, os pequenos precisam ser encaminhados para a Unidade de Terapia Neonatal (UTI) Neonatal.
>
Nascimento prematuro, gravidez de risco, parto cesárea, tipo de anestesia aplicada e complicações no trabalho de parto estão entre os fatores que podem afetar a pontuação.

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/3c066e65-5b1b-40c9-848b-ab104b8be5a5" alt="Top"  height="300">

**Nascidos Vivos de acordo com peso**

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/336e5305-b2f1-4e9f-a515-a8272967ed47" alt="Top"  height="300">

Em 2023, 62% dos recém-nascidos, estão na faixa de 3000 a 3999 gramas.

**Nascidos vivos segundo idade da mãe**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/fd497d7b-19c1-462c-8f63-9033569d6817" alt="Top"  height="200"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/7e07b1f3-3977-410d-b582-57ed77d41bc2" alt="Top"  height="300"> </td>
    </tr>
</table>

Mães entre 25 e 29 anos, foram as que mais fizeram partos, sendo 26 anos a idade com mais partos.
>
O número de mães com menos de 19 anos corresponde a 12% do total de nascidos vivos em 2023.
>
Quase metade dos nascidos vivos são de mães entre 20 e 29 anos.(49,2%)
>
Mães com mais de 40 anos representam 4,33% do total.

**Proporção segundo raça/cor da mãe por região**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/a67e8a26-31ba-481e-b05d-4d6173e56843" alt="Top"  height="200"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/b5d4306e-2680-43e7-91ae-4461f1bfabec" alt="Top"  height="300"> </td>
    </tr>
</table>

No Brasil 55,5% das mães são pardas, seguidas por mães brancas com 32,9% do total de nascimentos.
>
Na região Norte predomina as mães pardas, enquanto que no Sul, a predominancia são de mães brancas.
>
Na região Norte encontramos a maior quantidade de mães Indigenas.

**Nascidos vivos segundo situação conjugal da mãe**

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/07b61987-8e12-49a2-bbee-10a6ef92b50c" alt="Top"  height="300">

Metade das mães são solteiras, 51,3%.
>
Em seguida podemos dizer que que 46,9% das mães estão em um relacionamento(Casada+União estável).

**Nascidos vivos segundo escolaridade da mãe**

<table border="1">
    <tr>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/c583fe88-62b0-47d1-a123-d5f4ce9b3642" alt="Top"  height="200"></td>
        <td><img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/5cd2820a-084c-4e71-8174-190ad64863d2" alt="Top"  height="300"> </td>
    </tr>
</table>

Quanto a escolaridade das mães 34,5% possuem ensino médio completo, 20.9% incompleto.
>
Apenas 18,9% possui ensino superior completo.

**Nascidos vivos segundo profissão da mãe**

A Classificação Brasileira de Ocupações - CBO, instituída por portaria ministerial nº. 397, de 9 de outubro de 2002, tem por finalidade a identificação das ocupações no mercado de trabalho, para fins classificatórios.
>
Essa informação no SISNAC, tem 7% dos registros sem o preeenchimento do código.
>
Destacamos aqui as 10 principais profissões.

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/c6268345-c82b-4e0b-bbc7-fd5d669cf0d1" alt="Top"  height="300">

**Características da gestação e parto**

**Nascidos vivos segundo tipo gravidez**

<img src="https://github.com/gabrielmprata/nascidos_vivos/assets/119508139/3c32a818-4a98-453e-830b-538b079031da" alt="Top"  height="300">

No Brasil, cerca de 98% dos nascidos vivos, são de getações únicas, e apenas 2% são de gemêos.

**NASC**
registros dos nascidos vivos no Brasil
