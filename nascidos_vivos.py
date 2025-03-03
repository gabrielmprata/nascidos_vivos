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

# 3.2.9 Nascidos Vivos de acordo com score Apgar no 1º e 5º minuto
df_apgar1 = df_sinasc.groupby(["ano_mes", "apgar1"])['qtd'].sum().reset_index()

tot = sum(df_apgar1.qtd)  # Total de acessos

df_apgar1['perc'] = ((df_apgar1['qtd']/tot)*100).round(2)
df_apgar1.groupby(["apgar1"])['perc'].sum().reset_index()

# 3.2.10 Nascidos Vivos de acordo com peso
# por peso
df_peso = df_sinasc.groupby(["faixa_peso"])['qtd'].sum().reset_index()

df_peso = (df_sinasc[["faixa_peso", 'qtd']]
           [(df_sinasc['faixa_peso'] != 'Ignorado')]
           ).groupby(["faixa_peso"])['qtd'].sum().reset_index()

# Criando o campo ordem com a faixa de peso
df_peso['ordem'] = df_peso['faixa_peso']

dictpeso = {
    'Ignorado': 1,
    '< 500': 2,
    '500 a 999': 3,
    '1000 a 1499': 4,
    '1500 a 2499': 5,
    '2500 a 2999': 6,
    '3000 a 3999': 7,
    '4000 a +': 8
}

# Fazer o replace nos atributos conforme o dicionario
df_peso = df_peso.replace({
    'ordem': dictpeso
})


# 3.3 Características maternas ######################################
# 3.3.1 Nascidos vivos segundo idade da mãe

# por idade
df_idade = (df_sinasc[['faixa_etaria', 'idademae', 'qtd']]
            [(df_sinasc['idademae'] > 0) & (df_sinasc['idademae'] < 99)]
            ).groupby(['faixa_etaria', "idademae"])['qtd'].sum().reset_index()

# Proporção segundo raça/cor da mãe por região
# por raça/cor
df_raca = df_sinasc.groupby(["racacormae"])['qtd'].sum().reset_index()
df_racamae = df_sinasc.groupby(['regiao', 'racacormae']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por regiao
df_racamae['prop'] = (df_racamae.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(0)


# 3.3.3 Nascidos vivos segundo situação conjugal da mãe
# por estado civil
df_estcivil = (df_sinasc[['estcivmae', 'qtd']]
               [(df_sinasc['estcivmae'] != 'Ignorado')
                & (df_sinasc['estcivmae'] != 'NI')]
               ).groupby(['estcivmae'])['qtd'].sum().reset_index()

# 3.3.4 Nascidos vivos segundo escolaridade da mãe

# por escolaridade
df_escmae = (df_sinasc[['escmaeagr1', 'qtd']]
             [(df_sinasc['escmaeagr1'] != 'NI')]
             ).groupby(['escmaeagr1'])['qtd'].sum().reset_index()

# 3.4 Características da gestação e parto
# 3.4.1 Nascidos vivos segundo tipo gravidez
# por tipo gravidez
df_gravidez = df_sinasc.groupby(["gravidez"])['qtd'].sum().reset_index()

# por semana de gestação
df_semana = (df_sinasc[["gestacao", "semagestac", 'qtd']]
             [(df_sinasc['semagestac'] < 99)]
             ).groupby(["gestacao", "semagestac"])['qtd'].sum().reset_index()

# por idade gestacional
df_gestacional = (df_sinasc[["gestacao", "regiao", 'qtd']]
                  [(df_sinasc['semagestac'] < 99)]
                  ).groupby(["gestacao", "regiao"])['qtd'].sum().reset_index()

# Incluindo a idade gestacional na faixa de semanas
df_gestacional['gestacional'] = df_gestacional['gestacao']

dictgestacao = {

    "22 a 27 semanas": "Prematuro muito extremo (22 a 27 semanas)",
    "28 a 31 semanas": "Prematuro extremo (28 a 31 semanas)",
    "32 a 36 semanas": "Prematuro leve (32 a 36 semanas)",
    "37 a 41 semanas": "A termo (37 a 41 semanas)",
    "42 semanas e mais": "Pós-termo (42 semanas ou mais)"
}

# Fazer o replace nos atributos conforme o dicionario
df_gestacional = df_gestacional.replace({
    'gestacional': dictgestacao
})


# 3.4.3 Nascidos vivos segundo consultas pré-natal
# por consultas
df_consultas = (df_sinasc[["consultas", "regiao", "qtd"]]
                [(df_sinasc["consultas"] != "Ignorado")]
                ).groupby(["consultas", "regiao"])['qtd'].sum().reset_index()


# Criando o campo ordem com a faixa de peso
df_consultas['ordem'] = df_consultas['consultas']

dictconsultas = {
    "Nenhuma":  1,
    "de 1 a 3": 2,
    "de 4 a 6": 3,
    "7 e mais": 4,
    "Ignorado": 5
}

# Fazer o replace nos atributos conforme o dicionario
df_consultas = df_consultas.replace({
    'ordem': dictconsultas
})

# por regiao e consultas
df_consultas_prop = df_sinasc.groupby(
    ['regiao', 'consultas']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por regiao
df_consultas_prop['prop'] = (df_consultas_prop.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(0)

# 3.4.4 Nascidos vivos por tipo de parto e ano mês
# por tipo de parto
df_parto = (df_sinasc[["parto", "qtd"]]
            [(df_sinasc["parto"] != "Ignorado")]
            ).groupby(["parto"])['qtd'].sum().reset_index()

# por tipo de parto e região
df_parto_prop = df_sinasc.groupby(['regiao', 'parto']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por regiao
df_parto_prop['prop'] = (df_parto_prop.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(1)

# 3.4.5 Nascidos vivos segundo assistência

# por regiao e consultas
df_tpnascassi_prop = df_sinasc.groupby(
    ['regiao', 'tpnascassi']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por regiao
df_tpnascassi_prop['prop'] = (df_tpnascassi_prop.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(0)

# 3.4.6 Nascidos vivos segundo Grupos de Robson

# por grupo de Robson
df_tprobson = df_sinasc.groupby(["ano_mes", "gr_robson"])[
    'qtd'].sum().reset_index()

# por gruo de Robson e região
df_tprobson_reg = df_sinasc.loc[df_sinasc.tprobson < 11].groupby(
    ['regiao', 'tprobson']).agg({'qtd': 'count'})

# Calcula a proporção em percentual agrupado por UF
df_tprobson_reg['prop'] = (df_tprobson_reg.groupby(level=0).apply(
    lambda x: 100*x/x.sum()).reset_index(level=0, drop=True)).round(1)

df_tprobson_reg = df_tprobson_reg.reset_index()

# Criando o campo ordem com os grupos (se usar o campo do tipo inteiro, o gráfico não ficará com a legenda por grupo)
df_tprobson_reg['ordem'] = df_tprobson_reg['tprobson']

dicescmaeagr1 = {1: "Grupo 1", 2: "Grupo 2", 3: "Grupo 3", 4: "Grupo 4", 5: "Grupo 5",
                 6: "Grupo 6", 7: "Grupo 7", 8: "Grupo 8", 9: "Grupo 9", 10: "Grupo 10"}
# Fazer o replace nos atributos conforme o dicionario
df_tprobson_reg = df_tprobson_reg.replace({'ordem': dicescmaeagr1})


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
gr_locnasc_gestao = px.pie(df_gestao, values='qtd', names='tp_gestao',
                           labels=dict(tp_gestao="Gestão", qtd="Nascidos"),
                           height=350, width=350,  # largura
                           color_discrete_sequence=px.colors.sequential.Blues_r
                           )
gr_locnasc_gestao.update_layout(showlegend=False)
gr_locnasc_gestao.update_traces(
    textposition='outside', textinfo='percent+label')


# 3.2.8 Nascidos Vivos com anomalias congênitas segundo região
anom_tot = px.pie(df_anomalia_perc, values='qtd', names='idanomal',
                  labels=dict(idanomal="Anomalia?", qtd="Nascidos"),
                  height=350, width=350,  # largura
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
anom_tot.update_layout(showlegend=False)
anom_tot.update_traces(textposition='outside', textinfo='percent+label')

anom_reg = px.pie(df_anomalia, values='qtd', names='regiao',
                  labels=dict(regiao="Região", qtd="Nascidos"),
                  height=350, width=350,  # largura
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
anom_reg.update_layout(showlegend=False)
anom_reg.update_traces(textposition='outside', textinfo='percent+label')


anom_hist = px.bar(df_anomalia, x="ano_mes", y="qtd", color="regiao",
                   labels=dict(regiao="Região",
                               ano_mes="Ano/Mês", qtd="Nascidos"),
                   color_discrete_sequence=px.colors.sequential.Blues_r,
                   template="plotly_white", text="regiao"
                   )
anom_hist.update_xaxes(type="category")

# 3.2.9 Nascidos Vivos de acordo com score Apgar no 1º e 5º minuto
# por apgar1

gr_apgar1 = px.pie(df_apgar1, values='qtd', names='apgar1',
                   labels=dict(apgar1="Apgar 1", qtd="Nascidos"),
                   height=350, width=350,  # largura
                   color_discrete_sequence=px.colors.sequential.Blues_r
                   )
gr_apgar1.update_layout(showlegend=False)
gr_apgar1.update_traces(textposition='outside', textinfo='percent+label')


gr_apgar1_hs = px.bar(df_apgar1, x="ano_mes", y="qtd", color="apgar1",
                      labels=dict(apgar1="Apgar 1",
                                  ano_mes="Ano/Mês", qtd="Nascidos"),
                      category_orders={"apgar1": [
                          "Apgar ignorado", "Apgar < 7", "Apgar >= 7"]},
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      template="plotly_white"
                      )
gr_apgar1_hs.update_xaxes(type="category")

# 3.2.10 Nascidos Vivos de acordo com peso

gr_peso = px.bar(df_peso.sort_values(by='ordem', ascending=True), x="faixa_peso", y="qtd",
                 labels=dict(faixa_peso="Faixa de peso", qtd="Nascidos"),
                 color_discrete_sequence=px.colors.sequential.Blues_r, text_auto='.2s',
                 template="plotly_white"
                 )
gr_peso.update_traces(textfont_size=12, textangle=0,
                      textposition="outside", cliponaxis=False)

# 3.3 Características maternas ######################################
# 3.3.1 Nascidos vivos segundo idade da mãe

gr_idade_mae = px.bar(df_idade.sort_values(by='idademae', ascending=True), x="idademae", y="qtd",
                      labels=dict(idademae="Idade Mãe",
                                  faixa_etaria="Faixa etária", qtd="Nascidos"),
                      hover_data=['idademae', 'faixa_etaria'],
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      template="plotly_white"
                      )
gr_idade_mae.update_xaxes(type="category")

gr_faixa_etaria_mae = px.pie(df_idade, values='qtd', names='faixa_etaria',
                             labels=dict(
                                 faixa_etaria="Faixa etária", qtd="Nascidos"),
                             height=350, width=350, title='Por faixa etária da mãe',
                             color_discrete_sequence=px.colors.sequential.Blues_r
                             )
gr_faixa_etaria_mae.update_layout(showlegend=False)
gr_faixa_etaria_mae.update_traces(
    textposition='outside', textinfo='percent+label')

# Proporção segundo raça/cor da mãe por região
gr_raca_cor = px.pie(df_raca, values='qtd', names='racacormae', hole=0.5,
                     labels=dict(racacormae="Raça/cor mãe", qtd="Nascidos"),
                     height=350, width=350, title='Por Raça/cor da mãe',
                     color_discrete_sequence=px.colors.sequential.Blues_r
                     )
gr_raca_cor.update_layout(showlegend=False)
gr_raca_cor.update_traces(textposition='outside', textinfo='percent+label')

gr_raca_cor_prop = px.bar(df_racamae.reset_index(), x='regiao', y='prop', color='racacormae',
                          labels=dict(regiao="Região", racacormae="Raça/Cor",
                                      prop="Proporção(%)", qtd="Nascidos"), title='Proporção por região',
                          hover_data=['regiao', 'racacormae', 'prop', 'qtd'],
                          color_discrete_sequence=px.colors.sequential.Blues_r,
                          template="plotly_white", text="racacormae"
                          )
gr_raca_cor_prop.update_yaxes(
    ticksuffix="%", showgrid=True)  # the y-axis is in percent

# 3.3.3 Nascidos vivos segundo situação conjugal da mãe
# por estado civil
gr_estado_civil = px.pie(df_estcivil, values='qtd', names='estcivmae',
                         labels=dict(estcivmae="Estado civil", qtd="Nascidos"),
                         height=350, width=350,
                         color_discrete_sequence=px.colors.sequential.Blues_r
                         )
gr_estado_civil.update_layout(showlegend=False)
gr_estado_civil.update_traces(textposition='outside', textinfo='percent+label')

# 3.3.4 Nascidos vivos segundo escolaridade da mãe
gr_escola = px.pie(df_escmae, values='qtd', names='escmaeagr1',
                   labels=dict(escmaeagr1="Escolaridade", qtd="Nascidos"),
                   height=450, width=450,
                   color_discrete_sequence=px.colors.sequential.Blues_r
                   )
gr_escola.update_layout(showlegend=False)
gr_escola.update_traces(textposition='outside', textinfo='percent+label')


# 3.4 Características da gestação e parto
# 3.4.1 Nascidos vivos segundo tipo gravidez
gr_gravidez = px.pie(df_gravidez, values='qtd', names='gravidez', hole=0.5,
                     labels=dict(gravidez="Tipo", qtd="Nascidos"),
                     height=350, width=350,
                     color_discrete_sequence=px.colors.sequential.Blues_r
                     )
# gr_gravidez.update_layout(showlegend=False)
# gr_gravidez.update_traces(textposition='outside', textinfo='percent+label')


gr_semanas = px.pie(df_semana, values='qtd', names='gestacao',  hole=0.5,
                    labels=dict(gestacao="Semanas", qtd="Nascidos"),
                    height=350, width=350,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                    )
# gr_semanas.update_layout(showlegend=False)
# gr_semanas.update_traces(textposition='outside', textinfo='percent+label')
# gr_semanas.update_layout(height=350, width=350, margin=dict(t=2, b=0, l=0, r=0))


gr_semanas_bar = px.bar(df_semana.sort_values(by='semagestac', ascending=True), x="semagestac", y="qtd",
                        labels=dict(semagestac="Semanas",
                                    gestacao="Faixa", qtd="Nascidos"),
                        hover_data=['semagestac', 'gestacao'],
                        color_discrete_sequence=px.colors.sequential.Blues_r,  text_auto='.2s',
                        template="plotly_white"
                        )
gr_semanas_bar.update_xaxes(type="category")
gr_semanas_bar.update_traces(
    textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

gr_gestacional = px.bar(df_gestacional, x="regiao", y="qtd", color="gestacional",
                        labels=dict(
                            regiao="Região", gestacional="Idade gestacional", qtd="Nascidos"),
                        title='Idade gestacional por região',
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        template="plotly_white"
                        )

# 3.4.3 Nascidos vivos segundo consultas pré-natal
gr_consultas = px.pie(df_consultas, values='qtd', names='consultas', hole=0.5,
                      labels=dict(consultas="Consultas", qtd="Nascidos"),
                      height=350,  # altura
                      width=350,
                      color_discrete_sequence=px.colors.sequential.Blues_r
                      )
gr_consultas.update_layout(showlegend=False)
gr_consultas.update_traces(textposition='outside', textinfo='percent+label')

# Total nascidos
gr_consultas_reg = px.bar(df_consultas.sort_values(by='ordem', ascending=True), x="regiao", y="qtd", color='consultas', barmode='group',
                          labels=dict(consultas="Consultas",
                                      regiao="Região", qtd="Nascidos"),
                          color_discrete_sequence=px.colors.sequential.Blues_r,
                          template="plotly_white"
                          )

gr_consultas_prop = px.bar(df_consultas_prop.reset_index(), x='regiao', y='prop', color='consultas',
                           labels=dict(regiao="Região", consultas="Consultas",
                                       prop="Proporção(%)", qtd="Nascidos"),
                           title='Proporção por região',
                           hover_data=['regiao', 'consultas', 'prop', 'qtd'],
                           color_discrete_sequence=px.colors.sequential.Blues_r,
                           template="plotly_white", text="consultas"
                           )

# 3.4.4 Nascidos vivos por tipo de parto e ano mês

gr_parto = px.pie(df_parto, values='qtd', names='parto', hole=0.7,
                  # largura
                  labels=dict(parto="Parto", qtd="Nascidos"), height=350, width=350,
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
gr_parto.update_layout(showlegend=False)
gr_parto.update_traces(textposition='outside',
                       textinfo='percent+label')

gr_parto_reg = px.bar(df_parto_prop.reset_index(), x='regiao', y='prop', color='parto',
                      labels=dict(regiao="Região", df_parto_prop="Parto",
                                  prop="Proporção(%)", qtd="Nascidos"),
                      # hover_data=['regiao', 'consultas','prop','qtd'],
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      template="plotly_white", text="prop"
                      )

# 3.4.5 Nascidos vivos segundo assistência

gr_assis = px.pie(df_tpnascassi_prop.reset_index(), values='qtd', names='tpnascassi', hole=0.7,
                  labels=dict(tpnascassi="Assistente", qtd="Nascidos"), height=350, width=350,
                  color_discrete_sequence=px.colors.sequential.Blues_r
                  )
gr_assis.update_layout(showlegend=False, margin=dict(t=40, b=0, l=20, r=20))
gr_assis.update_traces(textposition='outside',
                       textinfo='percent+label')

gr_assis_prop = px.bar(df_tpnascassi_prop.reset_index(), x='regiao', y='prop', color='tpnascassi',
                       labels=dict(regiao="Região", tpnascassi="",
                                   prop="Proporção(%)", qtd="Nascidos"),
                       # hover_data=['regiao', 'consultas','prop','qtd'],
                       color_discrete_sequence=px.colors.sequential.Blues_r,
                       template="plotly_white", text="tpnascassi"
                       )

# 3.4.8 Nascidos vivos segundo número de filhos anteriores
df_gestant = (df_sinasc[['regiao', "qtdgestant", 'qtd']]
              ).groupby(['regiao', "qtdgestant"])['qtd'].sum().reset_index()

# Cria o atributo com as idades
df_gestant['faixa_gestant'] = df_gestant['qtdgestant']

# Range das faixas
classes = [-1, 0, 1, 2, 98, 500]

# Nome das faixas
labels = ['Zero', 'Um', 'Dois', 'Três ou mais', 'Ignorado']

# Aplica faixas
classes = pd.cut(x=df_gestant.faixa_gestant, bins=classes, labels=labels)
df_gestant['faixa_gestant'] = classes

# Como o tipo é category, vamos transformar em STR
df_gestant['faixa_gestant'] = df_gestant['faixa_gestant'].astype(str)

# 3.4.8 Nascidos vivos segundo número de filhos anteriores
gr_gestant = px.pie(df_gestant, values='qtd', names='faixa_gestant', hole=0.7,
                    labels=dict(faixa_gestant="Faixa", qtd="Nascidos"), height=350, width=350,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                    )
gr_gestant.update_layout(showlegend=False, margin=dict(t=40, b=0, l=20, r=20))
gr_gestant.update_traces(textposition='outside',
                         textinfo='percent+label')

gr_gestant_bar = px.bar(df_gestant.groupby(["regiao", 'faixa_gestant'])['qtd'].sum().reset_index(), x="regiao", y="qtd", color='faixa_gestant', barmode='group',
                        category_orders={"faixa_gestant": [
                            "Zero", "Um", "Dois", "Três ou mais", "Ignorado"]},
                        labels=dict(faixa_gestant="",
                                    regiao="Região", qtd="Nascidos"),
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        template="plotly_white"
                        )


# 3.4.6 Nascidos vivos segundo Grupos de Robson
gr_tprobson = px.bar(df_tprobson.reset_index(), x='ano_mes', y='qtd', color='gr_robson',
                     labels=dict(ano_mes="Ano/Mês",
                                 gr_robson="", qtd="Nascidos"),
                     category_orders={"gr_robson": ["Grupos 1 a 4 - maior chance de parto vaginal", "Grupo 5 - alguma chance de parto vaginal",
                                                    "Grupos 6 a 10 - menor chance de parto vaginal", "Ignorado"]
                                      },
                     color_discrete_sequence=px.colors.sequential.Blues_r,
                     template="plotly_white",  # text="racacormae"
                     )
gr_tprobson.update_xaxes(type="category", title=None)
gr_tprobson.update_layout(legend=dict(
    yanchor="top",
    y=-0.1,
    xanchor="left",
    x=0.01
))

gr_tprobson_reg = px.bar(df_tprobson_reg, x='regiao', y='prop', color='ordem',
                         labels=dict(regiao="Região", tprobson="Classificacao de Robson",
                                     prop="Proporção(%)", qtd="Nascidos"),
                         hover_data=['regiao', 'tprobson', 'prop', 'qtd'],
                         color_discrete_sequence=px.colors.sequential.Blues_r,
                         template="plotly_white", text="prop"
                         )

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
st.markdown("### :blue[Nascidos Vivos de acordo com score Apgar]")
text2 = """:blue[**O que é score Apgar? (Expandir)**]"""

with st.expander(text2, expanded=False):
    st.image(
        "https://raw.githubusercontent.com/gabrielmprata/nascidos_vivos/main/img/teste-apgar.jpg")
    st.markdown("""
        O score Apgar no primeiro minuto de vida do bebê indica como ele tolerou o parto.
Ele é um teste rápido que avalia a saúde geral do recém-nascido. 
O score Apgar é uma escala de 0 a 10, sendo que quanto maior a pontuação, melhor o estado do bebê. 
O que é avaliado no score Apgar? Cor da pele, Frequência cardíaca. 

Quando é realizado o score Apgar? 
No primeiro minuto de vida
No quinto minuto de vida
Em alguns casos, no décimo minuto de vida

O que o score Apgar indica? 
Se o bebê tolerou bem o parto
Se o bebê está se adaptando bem à vida fora do útero
Se o bebê precisa de cuidados médicos imediatos

O que uma pontuação baixa indica?
Não necessariamente que o bebê terá problemas de saúde sérios ou de longo prazo 
Que o bebê pode precisar de cuidados médicos imediatos

        """)

text = """:blue[**Score Apgar no 1º minuto**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_apgar1, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_apgar1_hs, use_container_width=True)

    st.write(" ")
    st.markdown("""
        Cerca de 90% dos bebês nascem em ótimas condições, com nota geral de 8 a 10. Abaixo disso, os índices revelam dificuldades: 7 (leve), de 4 a 6 (moderada) e de 0 a 3 (grave).

Crianças com pontuações inferiores a 7, recebem assistência imediata visando o aumento da classificação.

A primeira média é dada no primeiro minuto, depois no quinto e no décimo minutos.

Segundo a média, em todo o mundo, cerca de 4% dos recém-nascidos obtêm índice inferior a 7. Em alguns casos, os pequenos precisam ser encaminhados para a Unidade de Terapia Neonatal (UTI) Neonatal.

Nascimento prematuro, gravidez de risco, parto cesárea, tipo de anestesia aplicada e complicações no trabalho de parto estão entre os fatores que podem afetar a pontuação.
        """)

text = """:blue[**Nascidos Vivos de acordo com peso**]"""

with st.expander(text, expanded=True):

    st.plotly_chart(gr_peso, use_container_width=True)

    st.write(" ")
    st.markdown("""
        Em 2023, 62% dos recém-nascidos, estão na faixa de 3000 a 3999 gramas.
        """)

################################################################################################
st.markdown("### :blue[🤰Características maternas]")


text = """:blue[**Nascidos vivos segundo idade da mãe**]"""

with st.expander(text, expanded=True):

    st.plotly_chart(gr_idade_mae, use_container_width=True)

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_faixa_etaria_mae, use_container_width=True)

    st.write(" ")
    st.markdown("""
        Mães entre 25 e 29 anos, foram as que mais fizeram partos, sendo 26 anos a idade com mais partos.

O número de mães com menos de 19 anos corresponde a 12% do total de nascidos vivos em 2023.

Quase metade dos nascidos vivos são de mães entre 20 e 29 anos.(49,2%)

Mães com mais de 40 anos representam 4,33% do total.
        """)

text = """:blue[**Nascidos por raça/cor da mãe**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_raca_cor, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_raca_cor_prop, use_container_width=True)

    st.write(" ")
    st.markdown("""
        No Brasil 55,5% das mães são pardas, seguidas por mães brancas com 32,9% do total de nascimentos.

Na região Norte predomina as mães pardas, enquanto que no Sul, a predominancia são de mães brancas.

Na região Norte encontramos a maior quantidade de mães Indigenas.
        """)

text = """:blue[**Nascidos segundo estado civil e escolaridade da mãe**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_estado_civil, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_escola, use_container_width=True)

    st.write(" ")
    st.markdown("""
        Metade das mães são solteiras, 51,3%.

Em seguida podemos dizer que que 46,9% das mães estão em um relacionamento(Casada+União estável).

Quanto a escolaridade das mães 34,5% possuem ensino médio completo, 20.9% incompleto.

Apenas 18,9% possui ensino superior completo.

        """)


st.markdown("### :blue[🤰Características da gestação e do parto]")


text = """:blue[**Nascidos Vivos segundo tipo de gravidez e tempo de gestação**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 3.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_gravidez, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_semanas, use_container_width=True)

    st.plotly_chart(gr_semanas_bar, use_container_width=True)

    st.write(" ")
    st.markdown("""
        No Brasil, cerca de 98% dos nascidos vivos, são de getações únicas, e apenas 2% são de gemêos.

        Cerca de 86% dos partos são realizados entre a 37º e a 41º semana de gestação.
                """)
    st.write(" ")
    st.plotly_chart(gr_gestacional, use_container_width=True)

text = """:blue[**Nascidos Vivos segundo consultas pré-natal**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_consultas, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_consultas_reg, use_container_width=True)

    st.write(" ")
    st.plotly_chart(gr_consultas_prop, use_container_width=True)

    st.write(" ")
    st.markdown("""
        Um grande avanço na saúde das mães e dos bebês, é o acesso ao pré-natal, onde registramos 77,5% de mães com 7 ou mais consultas pré-natal, considerado "Mais do que adequado" e 16,6% considerado como "Adequado", totalizando 94,1%.

Em 2015 70,2% das mulheres tiveram acesso ao pré-natal, somando “Mais que adequado” e “Adequado”.

Um grande salto na melhoria ao acompanhamento das futuras mamães.

A região Norte é a que está mais abaixo da média nacional, alcançando apenas 62% das mães, e em 2015 o percentual era de 53,1%.
                """)

text = """:blue[**Nascidos Vivos por tipo de parto**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_parto, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_parto_reg, use_container_width=True)

    st.write(" ")
    st.markdown("""
    A Maioria dos partos são feitos por cesária.

A região centro-oeste tem a maior proporção de cesárias, seguida da região Sul.

No Norte, a proporção de cesárias é menor entre as regiões.
                """)


text = """:blue[**Nascidos Vivos segundo assistência**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_assis, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_assis_prop, use_container_width=True)

    st.write(" ")
    st.markdown("""
    Nossos recém-nascidos chegam ao mundo, na grande maioria das regiões, pelas mãos de médicos.

A região Norte, é a que mais registra nascimentos assistidos por enfermagem e por parteiras.
                """)


text = """:blue[**Nascidos vivos segundo número de filhos anteriores**]"""

with st.expander(text, expanded=True):

    col = st.columns((3.1, 5.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_gestant, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_gestant_bar, use_container_width=True)

    st.write(" ")
    st.markdown("""
    No Brasil 35% das mães são de primeira viagem, seguida de 29% de mães que já possuem um filho, e de 17% de mães com dois filhos.

Esse comportamento se repete em todas as regiões.


                """)

text = """:blue[**Nascidos vivos segundo Grupos de Robson**]"""

with st.expander(text, expanded=True):

    st.markdown("""
    **Classificação de Robson** serve para contribuir com a análise da taxa de cesarianas realizadas, bem como seu aumento ou diminuição de acordo com os grupos propostos.

A planilha de Classificação de Robson deve ser utilizada pelo gestor local. O preenchimento adequado dessa planilha ajudará a analisar o panorama que se tem no que diz respeito às taxas de cesárea e sua indicação.

1 - Nulípara, feto único, cefálico, ≥ 37 semanas, trabalho de parto (TP) espontâneo

2 - Nulípara, feto único, cefálico, ≥ 37 semanas, induzido ou cesárea fora do TP

3 - Multípara sem cesárea anterior, feto único, cefálico, ≥ 37 semanas, TP espontâneo

4 - Multípara sem cesárea anterior, feto único, cefálico, ≥ 37 semanas, TP induzido ou cesárea fora do TP

5 - Multípara com cesárea prévia, feto único, cefálico, ≥ 37 semanas

6 - Todas as nulíparas com apresentação pélvica

7 - Todas as multíparas com apresentação pélvica (incluindo com cesárea prévia)

8 - Todas as gestações múltiplas (incluindo com cesárea prévia)

9 - Todas as gestações córmicas ou oblíquas (incluindo com cesárea prévia)

10 - Gestação única, feto cefálico, ≤ 36 semanas (inclusive com cesárea prévia)
                """)

    col = st.columns((4.1, 4.3), gap='medium')

    with col[0]:
        st.plotly_chart(gr_tprobson, use_container_width=True)

    with col[1]:
        st.plotly_chart(gr_tprobson_reg, use_container_width=True)

    st.write(" ")
    st.markdown("""
    No gráfico, percebe-se que os nascimentos classificados nos grupos de 1 a 4 (nos quais o risco de cesárea é teoricamente menor) representa cerca 60% do total de nascimentos.

Já o grupo 5 (com antecedente de cesárea, gestação única, cefálica, ≥37 semanas) representa cerca de 25%.

Assim, constata-se que os grupos de 1 a 5 concentram 85% dos nascimentos.
                """)
