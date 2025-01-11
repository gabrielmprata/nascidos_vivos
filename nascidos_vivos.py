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

url2 = "https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/datasets/sinasc_ano_sexo.csv"

df_hist_sexo_ano = pd.read_csv(url2, encoding="Latin 1", sep=';')


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


#######################
# Dashboard Main Panel

st.image("https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/img/header_baby.png")
st.markdown("# 🏥Como os Brasileiros chegam ao mundo🤰👶")
st.markdown("## :blue[SINASC - Sistema de Informações sobre Nascidos Vivos]")

with st.expander("Introdução", expanded=True):
    st.markdown("""
                Os dados apresentados nesse estudo acadêmico, referem-se aos características do nascimento dos brasileiros.
            
                As informações dos Nascidos Vivos, estão disponíveis nos **Dados Abertos** do OpenDataSus.

                O nascimento é um dos eventos vitais e seu monitoramento pode contribuir para o conhecimento da situação de saúde de uma população, pois permite a construção de indicadores que subsidiam o planejamento, a gestão e a avaliação de políticas e ações de vigilância e atenção à saúde na área da saúde materna e infantil.

                O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de mortalidade para a gestante e para a criança. No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.

""")

st.markdown("## :blue[Apresentação dos resultados]")

text = """:blue[**Histórico de nascidos-vivos no Brasil:**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(hist, use_container_width=True)
    st.plotly_chart(hist2, use_container_width=True)
    st.markdown("""
        O pré-natal e a atenção ao parto são importantes estratégias para prevenir ou reduzir o risco de morbimortalidade para a gestante e para a criança. No Brasil, o Sistema de Informação sobre Nascidos Vivos (Sinasc) tem a finalidade de gerar indicadores sobre pré-natal, assistência ao parto e perfil epidemiológico dos nascidos vivos.

        No ano de 2023 o Brasil registrou 2,53 milhões de nascimentos, com uma queda de 1,17% em comparação com 2022, chegando ao menor patamar desde 1977.

        O Brasil registra a quinta queda consecutiva, desde 2019.                        
    """)

text = """:blue[**Nascem mais meninos ou meninas?**]"""

with st.expander(text, expanded=True):
    st.plotly_chart(sexo, use_container_width=True)
    st.markdown("""
    Bom, no histórico deste estudo, desde o ano 2000, nascem mais :blue[**MENINOS**] do que **meninas**.
    """)
