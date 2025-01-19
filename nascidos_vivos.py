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

UF_flag = pd.read_csv(
    'https://raw.githubusercontent.com/gabrielmprata/anatel/refs/heads/main/datasets/UF_flags.csv', encoding="utf_8", sep=';')

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

# Pivot table para o heatmap de hora por dia da semana
df_por_hora = pd.pivot_table(
    df_wk_hora, index=['ordem'], aggfunc='sum', columns=['hora'], values=['qtd'])

# 3.2.4 Representatividade por UF
# Dataframe agrupando por região
df_total_regiao = df_sinasc.groupby(["regiao", "uf"])[
    'qtd'].sum().reset_index()

df_total_regiao = pd.merge(df_total_regiao, UF_flag,
                           left_on='uf', right_on='uf')

# Histórico por região
df_evol_regiao = df_sinasc.groupby(["ano_mes", "regiao"])[
    'qtd'].sum().reset_index()

df_evol_regiao['qtd'] = (df_evol_regiao['qtd']/1000).round(2)

# 3.2.6 Nascidos Vivos segundo sexo
# por sexo
df_sexo = (df_sinasc[["ano_mes", "regiao", "sexo", 'qtd']]
           [(df_sinasc['sexo'] != 'Ignorado')]
           ).groupby(["ano_mes", "regiao", "sexo"])['qtd'].sum().reset_index()

# Distribuição nascidos vivos de acordo com o sexo e por região
df_sexo_bar = df_sexo.groupby(["regiao", "sexo"])['qtd'].sum().reset_index()

df_sexo_bar['perc'] = (100 * df_sexo_bar['qtd'] /
                       df_sexo_bar.groupby('regiao')['qtd'].transform('sum')).round(2)

# 3.2.7 Nascidos Vivos segundo local de nascimento
df_locnasc = (df_sinasc[["regiao", "locnasc", 'qtd']]
              [(df_sinasc['locnasc'] != 'Ignorado')]
              ).groupby(["regiao", "locnasc"])['qtd'].sum().reset_index()

# Proporçao de nascidos por local e regiao
df_locnasc_prop = df_sinasc.groupby(
    ['regiao', 'locnasc']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por regiao
df_locnasc_prop['prop'] = (df_locnasc_prop.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(0)

# por tipo de gestao hospitalar
df_gestao = (df_sinasc[["regiao", "tp_gestao", 'qtd']]
             [(df_sinasc['tp_gestao'] != 'NI')]
             ).groupby(["regiao", "tp_gestao"])['qtd'].sum().reset_index()


# 3.2.8 Nascidos Vivos com anomalias congênitas segundo região
# por anomalia
df_anomalia_perc = df_sinasc.groupby(["idanomal"])['qtd'].sum().reset_index()


df_anomalia = (df_sinasc[['ano_mes', 'regiao', 'qtd']]
               [(df_sinasc['idanomal'] == 'Sim')]
               ).groupby(['ano_mes', 'regiao'])['qtd'].sum().reset_index()


#####################################################################
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

heat_hr = px.imshow(df_por_hora,
                    labels=dict(x="Hora", y="Dia da semana"),
                    x=[0,  1,  2,  3,  4,  5,  6,  7,  8, 9, 10, 11,
                        12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                    y=['segunda-feira', 'terça-feira', 'quarta-feira',
                        'quinta-feira', 'sexta-feira', 'sábado', 'domingo'],
                    color_continuous_scale="Blues",
                    text_auto=True
                    )
heat_hr.update_layout(
    xaxis=dict(
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        ticktext=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    )
)


parto_hr = px.bar(df_wk_hora.groupby(["hora", "parto"])['qtd'].sum().reset_index(),
                  x="hora", y="qtd", color="parto", labels=dict(hora="Hora", qtd="Nascidos", parto="Parto"),
                  color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.2s', template="plotly_white"
                  )
parto_hr.update_layout(xaxis=dict(
    tickvals=df_wk_hora['hora'], ticktext=df_wk_hora['hora']))
parto_hr.update_traces(textfont_size=12, textangle=0,
                       textposition="outside", cliponaxis=False)


parto_hora = px.bar(df_wk_hora.groupby(["hora", "parto"])['qtd'].sum().reset_index(),
                    x="hora", y="qtd", color="parto", labels=dict(hora="Hora", qtd="Nascidos", parto="Parto"),
                    category_orders={"parto": ["Vaginal", "Cesário"]},
                    color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.2s', template="plotly_white"
                    )
parto_hora.update_layout(xaxis=dict(
    tickvals=df_wk_hora['hora'], ticktext=df_wk_hora['hora']))
parto_hora.update_traces(textfont_size=12, textangle=0,
                         textposition="outside", cliponaxis=False)

# 3.2.4 Representatividade por UF
# Dataframe agrupando por região

tot_regiao = px.pie(df_total_regiao, values='qtd', names='regiao', labels=dict(regiao="Região", qtd="Nascidos"),
                    height=350, width=350, color_discrete_sequence=px.colors.sequential.Blues_r
                    )
tot_regiao.update_layout(showlegend=False)
tot_regiao.update_traces(textposition='outside', textinfo='percent+label')

sun_uf = px.sunburst(df_total_regiao, path=['regiao', 'uf'], values='qtd',
                     labels=dict(regiao="Região", qtd="Nascidos"),
                     template="plotly_white",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
sun_uf.update_traces(textinfo="label+percent parent")


reg_evol = px.line(df_evol_regiao, x="ano_mes", y="qtd", color='regiao',
                   markers=True, text='qtd',
                   labels=dict(regiao="Região", ano_mes="Ano/Mês",
                               qtd="Nascidos (k)"),
                   color_discrete_sequence=px.colors.sequential.Blues_r,
                   line_shape="spline",
                   template="plotly_white"
                   )
reg_evol.update_traces(textposition='top center')
reg_evol.for_each_trace(lambda t: reg_evol.add_annotation(
    x=t.x[-1], y=t.y[-1], text=t.name,
    font_color=t.line.color,
    ax=5, ay=0, xanchor="left", showarrow=False
))
reg_evol.update_xaxes(type="category")

# 3.2.6 Nascidos Vivos segundo sexo
gr_sexo = px.pie(df_sexo, names='sexo', values='qtd', height=300, width=600, hole=0.7,
                 color_discrete_sequence=["magenta", "blue"],
                 category_orders={"sexo": ["Feminino", "Masculino"]},
                 )
gr_sexo.update_traces(hovertemplate=None, textposition='outside',
                      textinfo='percent+label', rotation=50)
gr_sexo.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False)
gr_sexo.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/img/genero.png",
        x=0.66, y=0.3, xref="paper", yref="paper", xanchor="right", yanchor="bottom", sizing="contain",
        sizex=0.4, sizey=0.4)  # tamanho da imagem
)


# Agrupando
gr_sexo_bar = px.bar(df_sexo_bar, x="regiao", y="perc", color="sexo",
                     labels=dict(regiao="Região", sexo="Sexo",
                                 perc="Percentual"),
                     color_discrete_sequence=["magenta", "blue"],
                     template="plotly_white", text="perc"
                     )

# 3.2.7 Nascidos Vivos segundo local de nascimento

# Total de Nascidos vivos segundo local de nascimento. Brasil, 2023


gr_locnasc_prop = px.bar(df_locnasc_prop.reset_index(), x='regiao', y='prop', color='locnasc',
                         height=500, width=800,
                         labels=dict(regiao="Região", locnasc="Local",
                                     prop="Proporção(%)", qtd="Nascidos"),
                         hover_data=['regiao', 'locnasc', 'prop', 'qtd'],
                         category_orders={"locnasc": [
                             "Hospital", "Outros estab. de saúde", "Domicílio", "Outros", "Aldeia Indígina", "Ignorado"]},
                         color_discrete_sequence=px.colors.sequential.Blues_r,
                         template="plotly_white", text="locnasc"
                         )
gr_locnasc_prop.update_layout(legend=dict(
    yanchor="top",
    y=-0.1,
    xanchor="left",
    x=0.01
))

# por tipo de gestao hospitalar df_gestao
gr_locnasc_gestao = px.pie(df_gestao,
                           values='qtd',
                           names='tp_gestao',
                           labels=dict(tp_gestao="Gestão", qtd="Nascidos"),
                           height=350,  # altura
                           width=350,  # largura
                           color_discrete_sequence=px.colors.sequential.Blues_r
                           )
gr_locnasc_gestao.update_layout(showlegend=False)
gr_locnasc_gestao.update_traces(textposition='outside',
                                textinfo='percent+label')


# 3.2.8 Nascidos Vivos com anomalias congênitas segundo região
anom_tot = px.pie(df_anomalia_perc, values='qtd', names='idanomal',
                  labels=dict(idanomal="Anomalia?", qtd="Nascidos"),
                  height=350,  # altura
                  width=350,  # largura
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
anom_tot.update_layout(showlegend=False)
anom_tot.update_traces(textposition='outside',
                       textinfo='percent+label')

anom_reg = px.pie(df_anomalia, values='qtd', names='regiao',
                  labels=dict(regiao="Região", qtd="Nascidos"),
                  height=350,  # altura
                  width=350,  # largura
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
anom_reg.update_layout(showlegend=False)
anom_reg.update_traces(textposition='outside',
                       textinfo='percent+label')


anom_hist = px.bar(df_anomalia, x="ano_mes", y="qtd", color="regiao",
                   labels=dict(regiao="Região",
                               ano_mes="Ano/Mês", qtd="Nascidos"),
                   color_discrete_sequence=px.colors.sequential.Blues_r,
                   template="plotly_white", text="regiao"
                   )
anom_hist.update_xaxes(type="category")


############################################################################
############################################################################
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
    st.write(" ")
    st.write(":blue[Por hora e dia da semana:]")
    st.plotly_chart(heat_hr, use_container_width=True)
    st.write(" ")
    st.write(":blue[Por tipo de parto:]")
    st.plotly_chart(parto_hora, use_container_width=True)
    st.write(" ")
    st.markdown("""
                Entre as 8 e as 11 horas da manhã e entre 14 e 17 horas da tarde, são os períodos em que ocorrem mais nascimentos.

As cesárias praticamente dominam esse período, enquanto que o parto vaginal mantém uma mesma constância ao longo do dia.

**Em 2023, nasceram 288 crianças por hora, ou 4 por minuto, ou 6932 por dia.**
                """)

text = """:blue[**Nascidos por Estado e Região**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 4.5, 4.1), gap='medium')

    with col[0]:
        st.dataframe(
            df_total_regiao.sort_values(by='qtd', ascending=False),
            column_order=("flag", "uf", "qtd"),
            column_config={
                "flag": st.column_config.ImageColumn(" ", width="small"),
                "uf": "UF",
                "qtd": "2023"
            },
            hide_index=True,
        )

    with col[1]:
        st.plotly_chart(tot_regiao, use_container_width=True)

    with col[2]:
        st.plotly_chart(sun_uf, use_container_width=True)

    st.write(" ")
    st.markdown("""
                O estado com o maior número de nascimentos foi **São Paulo, com 505.331**, representando quase 20% dos nascimentos no Brasil.

Em São Paulo nascem 118% a mais que Minas Gerais, que é o segundo estado com mais nascimentos.

A região sudeste é a que concentra o maior número de nascidos vivos, 38%, seguida do Nordeste com 28%.
                """)
    st.write(" ")
    st.plotly_chart(reg_evol, use_container_width=True)

text = """:blue[**Nascidos por Sexo**]"""

with st.expander(text, expanded=True):

    col = st.columns((4.2, 4.2), gap='medium')

    with col[0]:
        st.plotly_chart(gr_sexo, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_sexo_bar, use_container_width=True)

    st.write(" ")
    st.markdown("""
                No Brasil em 2023 nasceram 1,29 milhões de meninos(51,2%) e 1,23 milhões de meninas(48,8%).

                Nas regiões, temos o mesmo comportamento na proporção de nascimento por sexo.
                """)

text = """:blue[**Nascidos Vivos segundo local de nascimento**]"""

with st.expander(text, expanded=True):

    col = st.columns((5.1, 3.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_locnasc_prop, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_locnasc_gestao, use_container_width=True)

    st.write(" ")
    st.markdown("""
    A maioria dos nascimentos segue sendo em Hospitais, cerca de 98%, mas ainda há uma quantidade consideravel de nascimentos em domicílios, cerca de 15 mil.

Os hospitais de gestão Municipal, são os que mais realizam partos, 1.62 milhões, representando 65% do total.

Outro dado importante é a quantidade de nascimentos em aldeias indíginas, cerca de 1.779 no ano de 2023.

    """)

text = """:blue[**Nascidos Vivos com anomalias congênitas**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 3.3), gap='medium')

    with col[0]:
        st.plotly_chart(anom_tot, use_container_width=True)

    with col[1]:
        st.plotly_chart(anom_reg, use_container_width=True)

    st.plotly_chart(anom_hist, use_container_width=True)

    st.write(" ")
    st.markdown("""
        As anomalias congênitas são um grupo de alterações estruturais ou funcionais que ocorrem durante a vida intrauterina e que podem ser detectadas antes, durante ou após o nascimento.

    Podem afetar diversos órgãos e sistemas do corpo humano e são causadas por um ou mais fatores genéticos, infecciosos, nutricionais e ambientais, podendo ser resultado de uma combinação desses fatores.

    No ano de 2023, em 97% dos partos não foram identificadas anomalias, e em apenas 0,98% (24.770) foram identificadas.

    A região Sudeste registra 44,1% dos nascidos vivos com anomalias, seguido pelo Nordeste com 26,9%.
        """)
