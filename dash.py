# pip install streamlit

import streamlit as st
import pandas as pd
import plotly.express as px #funções do python
from streamlit_option_menu import option_menu # ajuda a trabalhar com opções de filtros
from query import conexao # conexão com o banco query


# *** PRIMEIRA CONSULTA /  ATUALIZAÇÃO DE DADOS ***

query = "SELECT * FROM tb_carro"

# Carregar os dados e armazenar 
df = conexao(query) 

# Botão para atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)

# ****** ESTRUTURA LATERAL DE FILTROS ************
st.sidebar.header("Selecione o Filtro")  # para incluir a barra a lateral do dashboard

marca = st.sidebar.multiselect("Marca selecionada", # opção para selecionar mais do que uma opção
                               options=df["marca"].unique(), # opções disponíveis no df
                               default=df["marca"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )

modelo = st.sidebar.multiselect("Modelo selecionado", # opção para selecionar mais do que uma opção
                               options=df["modelo"].unique(), # opções disponíveis no df
                               default=df["modelo"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )

ano = st.sidebar.multiselect("Ano selecionada", # opção para selecionar mais do que uma opção
                               options=df["ano"].unique(), # opções disponíveis no df
                               default=df["ano"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )



valor = st.sidebar.multiselect("Valor selecionado", # opção para selecionar mais do que uma opção
                               options=df["valor"].unique(), # opções disponíveis no df
                               default=df["valor"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )

cor = st.sidebar.multiselect("Cor selecionada", # opção para selecionar mais do que uma opção
                               options=df["cor"].unique(), # opções disponíveis no df
                               default=df["cor"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )

numero_vendas = st.sidebar.multiselect("Numero de vendas selecionado", # opção para selecionar mais do que uma opção
                               options=df["numero_vendas"].unique(), # opções disponíveis no df
                               default=df["numero_vendas"].unique(), # opção para vir tudo marcada e o usuário escolhe o que não quer ver
                               
                               )

# Aplicar os filtros selecionados

df_selecionado = df[
    (df["marca"].isin(marca)) & # serve para checar se existe o item selecionado
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas))

 ]

# ******** EXIBIR VALORES MÉDIOS *********
def Home():
    with st.expander("Valores"):  # Cria uma caixa expansível com um título separado por seções
        mostrarDados = st.multiselect('Filter:', df_selecionado.columns, default=[])
    #Verifica se o usuário selecionou colunas para exibir
        if mostrarDados:
        # Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
    
    #Verifica se o Dataframe filtrado (df_selecionado) não está vazio
    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        #Cria três colunas para exibir os totais calculados
        total1, total2, total3 = st.columns(3,gap="large")
        #Estrutura de exibição
        with total1:
            st.info("Valor Total de Vendas dos Carros", icon='📌')
            st.metric(label="Total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("Valor Medio das Vendas dos Carros", icon='📌')
            st.metric(label="Média", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor mediano dos Carros", icon='📌')
            st.metric(label="Mediana", value=f"{venda_mediana:,.0f}")
    
    
    else: 
        st.warning("Nenhum dado ddisponível com os filtros selecionados")

    st.markdown("""---------""")


# **************************GRÁFICOS*********************
def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para gerar gráficos")
        # Interrompe a função
        return
    
    # Criação dos gráficos

    # 4 abas -> Graficos de Barras, Gráfico de linhas, Gráfico de Pizza e Dispersão
    graf1, graf2, graf3, graf4, graf5, graf6 = st.tabs(["Grafico de Barras","Gráfico de Linhas","Gráfico de Pizza","Gráfico de Dispersão","Gráfico de Linha 3D", "Gráfico de Área Empilhada"])  # O tabs serve para separar o dado por abas Depois procurar gráficos no Streamlit grafico
    
    with graf1:
        st.write("Gráfico de Barras")# Titulo
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        # Agrupa pela marca e conta o número de ocorrências da coluna valor. Depois ordena o resultao de fma descrescente
        #Contêm os dados sobre valores por marca
        #importante declarar como index o que será o principal do gráfico, o eixo x
        # a função<b> serve para deixar a frase em negrito no início <b> e no fim </b>
        fig_valores = px.bar(investimento, x=investimento.index, y= "valor",orientation="h",title="<b>Valores de Carros</b>", color_discrete_sequence=["#0083b3"])
        #Exibe a figura e ajusta na tela para ocupar toda a largura
        st.plotly_chart(fig_valores, use_container_width=True)
    
    with graf2:
        st.write("Gráfico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]
        # no px.line tem várias opções
        fig_valores2 = px.line(dados, x=dados.index, y="valor", title="<b>Valores por Marca</b>", color_discrete_sequence=["#0083b8"])

        st.plotly_chart(fig_valores2,use_container_width=True)

    with graf3:
        st.write("Gráfico de Pizza")
        dados2= df_selecionado.groupby("marca").sum()[["valor"]]
        fig_valores3 = px.pie(dados2, values="valor",names=dados2.index, title="<b> Distribuição de valores por Marca</b>")

        st.plotly_chart(fig_valores3, use_container_width=True)

    with graf4:
        st.write("Gráfico de Dispersão")
        dados3= df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])

        fig_valores4 = px.scatter(dados3, x= "marca", y="value",color="variable", title="<b>Dispersão de Valores por Marca</b>")

        st.plotly_chart(fig_valores4, use_container_width=True)
    
    with graf5:
        st.write("Gráfico de Linha 3D")
        dados = df_selecionado.groupby("modelo").count()[["valor"]]
       
        fig_valores5 = px.line_3d(dados, x=dados.index, y="valor", z="valor", title="<b>Carros por Valor</b>", color_discrete_sequence=["#0083b8"])

        st.plotly_chart(fig_valores5, use_container_width=True)

    
    with graf6:
        st.write("Gráfico de Área Empilhada")
        dados = df_selecionado.groupby(["ano", "marca"]).sum().reset_index()
        fig_valores6 = px.area(dados, x="ano", y="marca", color="ano", title="<b>Distribuição de Valores ao Longo do Tempo</b>", line_group="ano")
        st.plotly_chart(fig_valores6, use_container_width=True)

    # **********BARRA PROGRESSO ******************
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 200000
    percentual = round((valorAtual/objetivo * 100)) #roud serve para arredondar o valor
   

    if percentual > 100:
        st.subheader("Valores Atingidos!!!")
    
    else:
        st.write(f"Você tem {percentual}% de {objetivo}. Corra atrás filhão!")
        
        mybar = st.progress(0)
        for percentualcompleto in range(percentual):
            mybar.progress(percentualcompleto + 1, text= "Alvo %")



# ********************* MENU LATERAL **********************************

def menulateral():
    with st.sidebar:
        selecionado = option_menu(menu_title ="Menu", options= ["Home", "Progresso"],icons=["house","eye"], menu_icon = "cast", default_index=0)

    if selecionado == "Home":
        st.subheader(f"Página:{selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "Progresso":
        st.subheader(f"Página:{selecionado}")
        barraprogresso()
        graficos(df_selecionado)


# ************** AJUSTAR O CSS **********************



menulateral()

# graficos(df_selecionado)
# Home()

        
