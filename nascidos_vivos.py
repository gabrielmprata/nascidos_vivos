#######################
# Importando libraries
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

#######################
# Configuração da página
st.set_page_config(
    page_title="Como os Brasileiros chegam ao mundo",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# alt.themes.enable("dark")

#####################################################################
# Carregando dataset

url = "https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/datasets/df_sinasc.csv.bz2"
url2 = "https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/datasets/sinasc_ano_sexo.csv"
url5 = "https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/datasets/sinasc_hist_por_idade.csv"


df_sinasc = pd.read_csv(url, compression='bz2')
df_hist_sexo_ano = pd.read_csv(url2, encoding="Latin 1", sep=';')
df_hist_idade = pd.read_csv(url5, encoding="Latin 1", sep=';')

#####################################################################
# Construção dos Datasets
# 3.1 A história dos nascimentos no Brasil, 2000-2023

# 3.1.1 Histórico de nascidos-vivos no Brasil
# Historico 2000 a 2023
df_hist = df_hist_sexo_ano.groupby(["ano"])['qtd'].sum().reset_index()

# Variação
df_hist['qtd_ant'] = df_hist.qtd.shift(1)
df_hist['var'] = (((df_hist['qtd']/df_hist['qtd_ant'])*100)-100).round(2)
df_hist['dif'] = (df_hist['qtd']-df_hist['qtd_ant'])
df_hist['qtd'] = ((df_hist['qtd'])/1000000).round(2)
df_hist['dif'] = ((df_hist['dif'])/100000).round(2)
df_hist['color'] = np.where(df_hist['dif'] < 0, '#e8816e', '#4c60d6')

df_hist['var'] = df_hist['var'].fillna(0)
df_hist['dif'] = df_hist['dif'].fillna(0)

# 3.1.2 Nascem mais meninos ou meninas?
df_hist_sexo_ano['qtd_mm'] = (df_hist_sexo_ano['qtd']/1000000).round(2)

# 3.1.3 Histórico pela idade das mães
# Direto do Dataset

# ************************************************#
# 3.2 Como os brasileiros chegaram ao mundo em 2023
# 3.2.1 Nascidos-vivos por mês

df_total = df_sinasc.groupby(["ano_mes"])['qtd'].sum().reset_index()

# 3.2.2 Nascidos-vivos por dia da semana e hora
# Nascidos vivos por dia da semana e hora
df_wk_hora = (df_sinasc[["wk", "hora", "parto", "qtd"]][(df_sinasc["parto"] != "Ignorado")]).groupby(
    ["wk", "hora", "parto"])['qtd'].sum().reset_index()

# classificar dia da semana
# recebe o dia da semana em numeral, para depois poder ordenar de maneira correta
df_wk_hora["ordem"] = df_wk_hora["wk"]
dicwk = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
         3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
df_wk_hora = df_wk_hora.replace({'wk': dicwk})

#####################################################################
# Construção dos Gráficos
# 3.1 A história dos nascimentos no Brasil, 2000-2023

# 3.1.1 Histórico de nascidos-vivos no Brasil
# Nascidos vivos por mês em 2023
hist = px.line(df_hist, x='ano', y='qtd',
               height=390, width=1200,  # altura x largura
               labels=dict(ano="Ano",  qtd="Nascidos"), text="qtd",
               line_shape="spline", markers=True, template="plotly_white")
hist.update_traces(line_color='#4c60d6', line_width=2,
                   textposition='top center')
hist.update_yaxes(ticksuffix="MM", showgrid=True)
hist.update_layout(xaxis=dict(linecolor='rgba(0,0,0,1)', tickmode='array',
                   tickvals=df_hist['ano'], ticktext=df_hist['ano']))


hist2 = px.bar(df_hist, x="ano", y="dif", title="Diferença YxY(K)", template="plotly_white", text_auto=True,
               height=300, width=1160,  # largura
               labels=dict(ano="Ano",  qtd="Nascidos", dif='Diferença', var='Variação'), hover_data=['ano', 'dif', 'var']
               )
hist2.update_traces(textangle=0, textfont_size=12, textposition='outside',
                    cliponaxis=False, marker_color=df_hist["color"])
hist2.update_yaxes(showticklabels=False, showgrid=False,
                   visible=False, fixedrange=True)
hist2.update_xaxes(showgrid=False, visible=False, fixedrange=True)
hist2.update_layout(xaxis=dict(
    tickmode='array', tickvals=df_hist['ano'], ticktext=df_hist['ano']))

# 3.1.2 Nascem mais meninos ou meninas?

# Nascidos vivos por sexo historico


sexo = px.line(df_hist_sexo_ano, x='ano', y='qtd_mm', color='sexo',
               height=390, width=1200,
               color_discrete_sequence=["blue", "pink"],
               labels=dict(ano="Ano",  qtd="Nascidos", sexo='Sexo'), text="qtd_mm",
               line_shape="spline", markers=True, template="plotly_white")
sexo.update_traces(line_width=2, textposition='top center')
sexo.update_layout(xaxis=dict(linecolor='rgba(0,0,0,1)', tickmode='array',
                   tickvals=df_hist_sexo_ano['ano'], ticktext=df_hist_sexo_ano['ano']))

# 3.1.3 Histórico pela idade das mães
idade = px.histogram(df_hist_idade, x="faixa_etaria", y="qtd",
                     color='ano', barmode='group',
                     labels=dict(faixa_etaria="Faixa etária",
                                 ano="Ano", qtd="Nascidos"),
                     color_discrete_sequence=px.colors.sequential.Blues_r,
                     template="plotly_white",
                     height=400)
idade.update_layout(yaxis_title="Nascidos")

# ************************************************#
# 3.2 Como os brasileiros chegaram ao mundo em 2023
# 3.2.1 Nascidos-vivos por mês

# Nascidos vivos por mês em 2023
ano_mes = px.line(df_total, x='ano_mes', y='qtd',

                  markers=True, text='qtd',
                  height=500, width=800,  # altura x largura
                  labels=dict(ano_mes="Ano/Mês",  qtd="Nascidos"),
                  # color_discrete_sequence=px.colors.sequential.Blues_r,
                  # color_discrete_map={"qtd": "red"},
                  line_shape="spline",
                  template="plotly_white"
                  )
ano_mes.update_traces(line_color='#4c60d6', line_width=2,
                      textposition='top center')
# se o type for date, vai respeitar o intervalo
ano_mes.update_xaxes(type="category", title=None)

# 3.2.2 Nascidos-vivos por dia da semana e hora
diahora = px.bar((df_wk_hora.groupby(["ordem", "wk", "parto"])['qtd'].sum().reset_index()).sort_values(by='ordem', ascending=True),
                 x="wk", y="qtd", color="parto", labels=dict(wk="dia da semana", qtd="Nascidos"),
                 color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.2s',
                 category_orders={"parto": ["Vaginal", "Cesário"]},
                 template="plotly_white"
                 )
diahora.update_traces(textfont_size=12, textangle=0,
                      textposition="outside", cliponaxis=False)


#######################
# Dashboard Main Panel

st.image("https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/img/header_baby.png")
st.markdown("# 🏥Como os Brasileiros chegam ao mundo🤰👶")
st.markdown("## :blue[SINASC - Sistema de Informações sobre Nascidos Vivos]")

text = """:orange[**Introdução**]"""

with st.expander(text, expanded=True):
    st.markdown("""
                Os dados apresentados nesse estudo acadêmico, referem-se as características do nascimento dos brasileiros.
            
                As informações dos Nascidos Vivos, estão disponíveis nos **Dados Abertos** do OpenDataSus.

                O nascimento é um dos eventos vitais e seu monitoramento pode contribuir para o conhecimento da situação de saúde de uma população, pois permite a construção de indicadores que subsidiam o planejamento, a gestão e a avaliação de políticas e ações de vigilância e atenção à saúde na área da saúde materna e infantil.

                O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de mortalidade para a gestante e para a criança. No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.

""")

st.markdown("## :blue[Apresentação dos resultados]")
st.markdown("### :blue[Informações históricas, 2000-2023]")

text = """:blue[**Histórico de nascidos-vivos no Brasil:**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(hist, use_container_width=True)
    st.plotly_chart(hist2, use_container_width=True)
    st.markdown("""
        O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de morbimortalidade para a gestante e para a criança. No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.

        **No ano de 2023 o Brasil registrou 2,53 milhões de nascimentos, com uma queda de 1,17% em comparação com 2022, chegando ao menor patamar desde 1977.**

        O Brasil registra a quinta queda consecutiva, desde 2019.                        
    """)

text = """:blue[**Nascem mais meninos ou meninas?**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(sexo, use_container_width=True)
    st.markdown("""
    Bom, no histórico deste estudo, desde o ano 2000, nascem mais :blue[**MENINOS**] do que **meninas**.
    """)

text = """:blue[**Histórico pela idade das mães, 2018-2023**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(idade, use_container_width=True)
    st.markdown("""
    Outra informação importante, é a quantidade de nascimentos por faixa etáriae da mãe.

Esse dado é utilizado em estudos relacionados com o comportamento reprodutivo das mulheres, permitindo analisar as transformações demográficas que estão ocorrendo no Brasil.

Ao longo do período analisado, vemos uma tendência de crescimento relativo a mães com idade entre 40 e 44 anos.

E uma redução no nascimento por mães jovens, entre 15 e 19 anos.

E precisamos comemorar a redução na faixa etaria entre 10 e 14 anos, pois vida sexual abaixo de 14 anos é considerada estupro de vunerável. Mesmo que a relação seja consentida, perante a nossa lei é um **abuso sexual**.
    """)

st.markdown(
    "### :blue[Como os brasileiros chegaram ao mundo em :green[**2023**]]")

text = """:blue[**Por mês:**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(ano_mes, use_container_width=True)
    st.markdown("""
Em 2023, chegaram ao mundo 2.532.050 brasileiros!

Representando uma média mensal de 211 mil nascidos vivos.

Março foi o mês com mais nascimentos, 234.022, seguido por Maio, com 230.858

Na outra ponta, o mês de Novembro foi o que teve menos nascimentos, com 190.052.
""")

text = """:blue[**Nascidos por dia da semana e hora**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(diahora, use_container_width=True)
    st.markdown("""
Nascem mais crianças no início da semana, esse número cai nos finais de semana, por conta das cesárias, que geralmente são agendadas em dia úteis.

Os partos vaginais seguem a mesma tendência durante todos os dias da semana.
    """)
