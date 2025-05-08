import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 🚨 DEVE SER O PRIMEIRO COMANDO STREAMLIT
st.set_page_config(page_title="Dashboard de Recursos Humanos", layout="wide")

# 🎨 Estilo visual inspirado no Spotify
st.markdown("""
    <style>
        /* Estilo geral para a descrição */
        .descricao-hover {
            transition: all 0.3s ease-in-out;
            padding: 5px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }

        .descricao-hover:hover {
            transform: scale(1.3); /* Aumenta o tamanho da descrição ao passar o mouse */
            font-size: 2em; /* Aumenta ainda mais o tamanho da fonte */
            color: #1DB954; /* Cor característica do Spotify */
            font-weight: bold; /* Deixa o texto mais destacado */
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.4); /* Fundo mais suave */
        }

        /* Fundo da área principal */
        .main {
            background-color: #121212; /* Cor escura como o fundo do Spotify */
            color: white;
        }

        /* Sidebar estilo Spotify */
        section[data-testid="stSidebar"] {
            background-color: #181818;
            color: white;
        }

        /* Cor do texto e widgets na sidebar */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] select {
            color: white !important;
        }

        /* Estilo dos gráficos */
        .plotly-graph-div {
            background-color: #121212; /* Cor de fundo escuro para os gráficos */
        }
        
        /* Animações para os gráficos */
        .plotly-graph-div .plotly {
            transition: all 0.3s ease-in-out;
        }

        .plotly-graph-div:hover {
            transform: scale(1.05); /* Efeito de zoom ao passar o mouse sobre os gráficos */
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 Função principal do app
def app():
    st.title("📊 Dashboard de Recursos Humanos")

    # Carregar os dados do CSV
    data = pd.read_csv('rh.csv')

    # 🎛️ Sidebar com filtros
    st.sidebar.header("🧩 Filtros")
    sexo_filter = st.sidebar.multiselect('Selecione o Sexo', options=data['Sexo'].unique(), default=data['Sexo'].unique())
    departamento_filter = st.sidebar.multiselect('Selecione o Departamento', options=data['Departamento'].unique(), default=data['Departamento'].unique())
    cargo_filter = st.sidebar.multiselect('Selecione o Cargo', options=data['Cargo'].unique(), default=data['Cargo'].unique())
    estado_civil_filter = st.sidebar.multiselect('Selecione o Estado Civil', options=data['Estado Civil'].unique(), default=data['Estado Civil'].unique())
    escolaridade_filter = st.sidebar.multiselect('Selecione o Nível de Escolaridade', options=data['Nível Escolaridade'].unique(), default=data['Nível Escolaridade'].unique())
    cidade_filter = st.sidebar.multiselect('Selecione a Cidade', options=data['Cidade'].unique(), default=data['Cidade'].unique())

    # Aplicando os filtros aos dados
    filtered_data = data[
        (data['Sexo'].isin(sexo_filter)) &
        (data['Departamento'].isin(departamento_filter)) &
        (data['Cargo'].isin(cargo_filter)) &
        (data['Estado Civil'].isin(estado_civil_filter)) &
        (data['Nível Escolaridade'].isin(escolaridade_filter)) &
        (data['Cidade'].isin(cidade_filter))
    ]

    st.success("✅ Dados carregados com sucesso!")

    # 📊 Layout dos gráficos
    col1, col2 = st.columns(2)

    # Gráfico 1: Gráfico de Pizza - Distribuição por Sexo
    col1.subheader("📊 Distribuição por Sexo", help="Este gráfico mostra a distribuição dos funcionários por sexo, ajudando na análise de diversidade.")
    sexo_counts = filtered_data['Sexo'].value_counts()
    fig1 = go.Figure(data=[go.Pie(labels=sexo_counts.index, values=sexo_counts, hole=0.3)])
    fig1.update_layout(
        title="Distribuição por Sexo",
        margin=dict(t=0, b=0, l=0, r=0),
        template="plotly_dark"  # Estilo escuro para o gráfico
    )
    col1.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Gráfico de Barras - Salário Médio por Departamento
    col2.subheader("📊 Salário Médio por Departamento", help="Este gráfico exibe o salário médio por departamento, facilitando comparações entre diferentes áreas.")
    salario_medio_departamento = filtered_data.groupby('Departamento')['Salario'].mean().sort_values()
    fig2 = px.bar(salario_medio_departamento.reset_index(), x='Departamento', y='Salario', color='Departamento',
                  color_discrete_sequence=px.colors.sequential.Viridis, title="Salário Médio por Departamento")
    fig2.update_layout(template="plotly_dark")  # Estilo escuro para o gráfico
    col2.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Gráfico de Dispersão - Idade x Salário
    col1.subheader("📊 Idade x Salário", help="Este gráfico mostra a relação entre idade e salário, destacando como a idade influencia o salário.")
    fig3 = px.scatter(filtered_data, x='Idade', y='Salario', color='Sexo', title="Idade vs Salário",
                      color_discrete_sequence=px.colors.sequential.Plasma)
    fig3.update_layout(template="plotly_dark")  # Estilo escuro para o gráfico
    col1.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Gráfico de Linhas - Tempo de Empresa Médio por Cargo
    col2.subheader("📊 Tempo de Empresa Médio por Cargo", help="Este gráfico mostra o tempo médio de permanência dos funcionários por cargo.")
    tempo_empresa_medio_cargo = filtered_data.groupby('Cargo')['Tempo Empresa (anos)'].mean().sort_values()
    fig4 = px.line(tempo_empresa_medio_cargo.reset_index(), x='Cargo', y='Tempo Empresa (anos)', markers=True,
                   line_shape="spline", color_discrete_sequence=["#1DB954"], title="Tempo Médio de Empresa por Cargo")
    fig4.update_layout(template="plotly_dark")  # Estilo escuro para o gráfico
    col2.plotly_chart(fig4, use_container_width=True)

# ▶️ Executar app
if __name__ == '__main__':
    app()
