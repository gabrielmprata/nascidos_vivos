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
Criar um simples Dashboard em **Python** e **Streamlit**, para mostrar caractéristicas do nascimento, destacando caractéristicas das mães, dos recém-nascidos, distribuição geográfica, socioeconômicas.

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
# **<font color=#85d338> 4. Apresentação dos resultados**
>
