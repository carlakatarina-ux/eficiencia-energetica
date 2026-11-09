import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import sqlite3
from datetime import datetime
from io import BytesIO

# =========================================================
# BANCO DE DADOS
# =========================================================

def conectar_banco():
    return sqlite3.connect("energia.db")


def criar_banco():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_energia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidade TEXT NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            consumo REAL NOT NULL,
            producao REAL NOT NULL,
            area REAL,
            usuarios INTEGER,
            compressores REAL DEFAULT 0,
            bombas REAL DEFAULT 0,
            refrigeracao REAL DEFAULT 0,
            iluminacao REAL DEFAULT 0,
            outros REAL DEFAULT 0,
            data_cadastro TEXT
        )
    """)

    conexao.commit()
    conexao.close()


criar_banco()


# ==========================================
# IMAGEM DA SIDEBAR
# ==========================================

with open("imagens/plataforma3.png", "rb") as arquivo:
    imagem_plataforma = base64.b64encode(arquivo.read()).decode()

st.set_page_config(
    page_title="Eficiência Energética",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# ESTILO DO DASHBOARD
# ==========================================

st.markdown("""
<style>

/* =========================================
   MENU LATERAL
========================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #061827 0%,
        #09283d 100%
    );
    border-right: none;
}

section[data-testid="stSidebar"] {
    background-color: #061827 !important;

    background-image:
        url("data:image/png;base64,__IMAGEM__") !important;

    background-size: 92% auto !important;
    background-position: center bottom 15px !important;
    background-repeat: no-repeat !important;
}

/* Logo */

.logo-sidebar {
    padding: 10px 18px 30px 18px;
}

.logo-sidebar .gota {
    font-size: 45px;
    margin-bottom: 5px;
    transform: translateY(-40px);
}

.logo-sidebar h1 {
    color: white !important;
    font-size: 29px !important;
    margin: 0 !important;
    transform: translateY(-60px);
}

.logo-sidebar p {
    color: #a8b7c5;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 2px;
    transform: translateY(-60px);
}

/* =========================================
   CABEÇALHO
========================================= */

.cabecalho-titulo {
    margin-bottom: 25px;
}

.cabecalho-titulo p {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 25px;
}

.cabecalho-titulo h1 {
    font-size: 34px !important;
    color: #071a2f !important;
    margin: 0 !important;
    line-height: 1.2;
}

.cabecalho-titulo h2 {
    font-size: 25px !important;
    color: #334155 !important;
    font-weight: 400 !important;
    margin: 3px 0 6px 0 !important;
}

.cabecalho-titulo span {
    color: #64748b;
    font-size: 14px;
}


/* PERÍODO */

.periodo {
    background: white;
    border: 1px solid #dce3ea;
    border-radius: 9px;
    padding: 10px 14px;
    margin-top: 5px;
}

.periodo span {
    display: block;
    font-size: 11px;
    color: #64748b;
}

.periodo strong {
    display: block;
    color: #10243d;
    font-size: 14px;
    margin-top: 3px;
}


/* USUÁRIO */

.usuario-topo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 7px;
}

.avatar {
    width: 42px;
    height: 42px;

    background: #64748b;
    color: white;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 13px;
}

.usuario-topo strong {
    display: block;
    color: #10243d;
    font-size: 13px;
}

.usuario-topo span {
    display: block;
    color: #64748b;
    font-size: 11px;
    margin-top: 3px;
}

/* Remove o título "Menu" */

section[data-testid="stSidebar"] label {
    color: white;
}


/* Opções */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 11px 14px;
    border-radius: 8px;
    transition: 0.2s;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: rgba(255,255,255,0.08);
}


/* Texto das opções */

section[data-testid="stSidebar"] div[role="radiogroup"] p {
    color: #dce6ee !important;
    font-size: 15px;
}


/* Opção selecionada */

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        #ffb52e,
        #f5a623
    );
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #071a2f !important;
    font-weight: 600;
}


/* Esconde as bolinhas do radio */

section[data-testid="stSidebar"] div[role="radiogroup"] 
div[data-testid="stMarkdownContainer"] {
    margin-left: 0;
}

section[data-testid="stSidebar"] input[type="radio"] {
    display: none;
}


/* Rodapé */

.rodape-sidebar {
    margin-top: 45px;
    padding: 25px 18px;
    border-top: 1px solid rgba(255,255,255,0.2);
    transform: translateY(-60px);

    color: #8397a8;
    font-size: 11px;
    letter-spacing: 2px;
    line-height: 21px;
}

/* Fundo geral */
.stApp {
    background-color: #f7f9fc;
}

/* Área principal */
.block-container {
    padding-top: 3.5rem;
    padding-bottom: 1.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 1500px;
}

/* Fonte geral */
html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
    color: #0b1f35;
}

/* Título principal */
h1 {
    color: #071a2f;
    font-size: 38px !important;
    font-weight: 700 !important;
    margin-bottom: 0 !important;
}

/* Subtítulos */
h2, h3 {
    color: #10243d;
    font-weight: 600 !important;
}

/* CARDS DOS INDICADORES */

div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #dfe5ec;
    padding: 20px 22px;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.03);
    min-height: 125px;
}

/* Nome do indicador */
div[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #53657a;
}

/* Número principal */
div[data-testid="stMetricValue"] {
    color: #071a2f;
    font-size: 28px;
    font-weight: 700;
}

/* Gráficos */
div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 12px;
    padding: 10px;
}

/* Tabela */
div[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid #dfe5ec;
    border-radius: 10px;
    overflow: hidden;
}

/* Caixa de alerta */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Esconde rodapé padrão */
footer {
    visibility: hidden;
}

/* Ajuste para telas menores */
@media (max-width: 1400px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1250px;
    }

}

/* ===== SIDEBAR MAIS COMPACTA ===== */

section[data-testid="stSidebar"] {
    width: 225px !important;
    min-width: 225px !important;
}

section[data-testid="stSidebar"] > div {
    width: 225px !important;
}

/* Diminui um pouco os elementos da sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    font-size: 13px;
}

/* Espaçamento dos itens do menu */
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    line-height: 1.25;
}

/* Mantém o conteúdo da sidebar na frente da imagem */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    position: relative !important;
    z-index: 2 !important;
}

/* ===== COMPACTAR CONTEÚDO DA SIDEBAR ===== */

/* Diminui o espaço interno no topo da sidebar */
section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

/* Aproxima as opções do menu */
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    margin-bottom: 0px;
}

/* Diminui o espaço vertical entre as opções */
section[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 0.35rem;
}

/* Sobe o rodapé */
.rodape-sidebar {
    margin-top: 25px;
}

/* SUBIR SOMENTE O MENU DE OPÇÕES */
section[data-testid="stSidebar"] [data-testid="stRadio"] {
    transform: translateY(-45px);
}

</style>
""", unsafe_allow_html=True)

css_imagem = """
<style>

section[data-testid="stSidebar"]::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 55px;

    width: 100%;
    height: 260px;

    background-image:
        linear-gradient(
            to bottom,
            rgba(6, 24, 39, 1) 0%,
            rgba(6, 24, 39, 0.10) 45%,
            rgba(6, 24, 39, 0.65) 100%
        ),
        url("data:image/png;base64,__IMAGEM__");

    background-size: contain;
    background-position: center 45px;
    background-repeat: no-repeat;

    pointer-events: none;
}

</style>
"""

css_imagem = css_imagem.replace(
    "__IMAGEM__",
    imagem_plataforma
)

st.markdown(
    css_imagem,
    unsafe_allow_html=True
)

# =========================================================
# SISTEMA DE LOGIN
# =========================================================

# Cria o estado da sessão
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = ""


# =========================================================
# TELA DE LOGIN
# =========================================================

if not st.session_state.autenticado:

    # Esconde a sidebar enquanto o usuário não estiver logado
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }

            [data-testid="collapsedControl"] {
                display: none;
            }

            .login-logo {
                text-align: center;
                margin-top: 60px;
                margin-bottom: 25px;
            }

            .login-logo .fogo {
                font-size: 55px;
                margin-bottom: 5px;
            }

            .login-logo h1 {
                color: #0B2D45;
                font-size: 32px;
                margin: 0;
                font-weight: 700;
            }

            .login-logo h3 {
                color: #F5A623;
                font-size: 14px;
                letter-spacing: 3px;
                margin-top: 5px;
                font-weight: 600;
            }

            .login-subtitulo {
                text-align: center;
                color: #607D94;
                font-size: 14px;
                margin-bottom: 25px;
            }

            div[data-testid="stForm"] {
                background-color: white;
                border: 1px solid #D6DEE5;
                border-radius: 14px;
                padding: 25px 30px 30px 30px;
                box-shadow: 0px 4px 18px rgba(11, 45, 69, 0.08);
            }
        </style>
    """, unsafe_allow_html=True)


    # Centraliza o formulário
    col_esquerda, col_login, col_direita = st.columns(
        [1.3, 1, 1.3]
    )

    with col_login:

        st.markdown(
            """
        <div class="login-logo">
            <div class="fogo">🔥</div>
            <h1>O&amp;G</h1>
            <h3>GESTÃO ENERGÉTICA</h3>
        </div>
        <div class="login-subtitulo">
            Acesso à plataforma de gestão energética
        </div>
            """,
            unsafe_allow_html=True
        )


        with st.form("form_login"):

            usuario = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário"
            )

            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha"
            )

            entrar = st.form_submit_button(
                "Entrar",
                use_container_width=True
            )


            if entrar:

                if usuario == "admin" and senha == "admin123":

                    st.session_state.autenticado = True
                    st.session_state.usuario_nome = "Administrador"

                    st.rerun()

                else:

                    st.error(
                        "Usuário ou senha incorretos."
                    )


    # Impede que o restante do dashboard seja carregado
    st.stop()

# ==========================================
# MENU LATERAL
# ==========================================

with st.sidebar:

    st.markdown("""
        <div class="logo-sidebar">
            <div class="gota">🔥</div>
            <h1>O&G</h1>
            <p>GESTÃO ENERGÉTICA</p>
        </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Menu",
        [
            "🏠  Visão Geral",
            "🏢  Unidades",
            "📊  Indicadores",
            "📈  Comparativos",
            "📄  Relatórios",
            "⚙️  Configurações"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption("👤 Usuário conectado")
    st.markdown(
        f"**{st.session_state.usuario_nome}**"
    )

    if st.button(
        "🚪 Sair",
        use_container_width=True
    ):

        st.session_state.autenticado = False
        st.session_state.usuario_nome = ""

        st.rerun()

    st.markdown("""
        <div class="rodape-sidebar">
            EFICIÊNCIA<br>
            SEGURANÇA<br>
            SUSTENTABILIDADE
        </div>
    """, unsafe_allow_html=True)

if "Visão Geral" in pagina:

    # ==========================================
    # CONSULTA INICIAL DO PERÍODO
    # ==========================================

    conexao = conectar_banco()

    df_banco = pd.read_sql_query(
        """
        SELECT *
        FROM dados_energia
        ORDER BY ano DESC, mes DESC
        """,
        conexao
    )

    conexao.close()

    if not df_banco.empty:

        ano_atual = int(df_banco["ano"].max())

        mes_atual = int(
            df_banco[
                df_banco["ano"] == ano_atual
            ]["mes"].max()
        )

    else:
        ano_atual = 0
        mes_atual = 0

    # ==========================================
    # CABEÇALHO
    # ==========================================

    col_titulo, col_periodo, col_usuario = st.columns([5, 1.2, 1.5])

    with col_titulo:
        st.markdown(
            """
            <p style="margin:0; color:#64748b; font-size:13px;">
                Bem-vindo, Usuário
            </p>

            <h1 style="
                margin:8px 0 0 0;
                padding:0;
                font-size:34px;
                color:#071a2f;
            ">
                Eficiência Energética de Instalações
            </h1>

            <p style="
                margin:2px 0 0 0;
                font-size:24px;
                color:#334155;
            ">
                Setor de Petróleo e Gás
            </p>

            <p style="
                margin:5px 0 0 0;
                color:#64748b;
                font-size:14px;
            ">
                Monitore o consumo de energia, compare unidades e identifique oportunidades de melhoria.
            </p>
            """,
            unsafe_allow_html=True
        )

    with col_periodo:
        st.caption("📅 Período")

        nomes_meses = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }

        if mes_atual > 0:
            st.markdown(
                f"**{nomes_meses[mes_atual]}/{ano_atual}**"
            )
        else:
            st.markdown("**Sem dados**")

    with col_usuario:
        st.caption("👤 Usuário")
        st.markdown("**Carla Barone**")
        st.caption("Administrador")
            
    # ==========================================
    # DADOS DAS INSTALAÇÕES - BANCO DE DADOS
    # ==========================================

    if not df_banco.empty:

        df_periodo = df_banco[
            (df_banco["ano"] == ano_atual) &
            (df_banco["mes"] == mes_atual)
        ].copy()

        df = pd.DataFrame({
            "Unidade": df_periodo["unidade"],
            "Consumo_kWh": df_periodo["consumo"],
            "Area_m2": df_periodo["area"],
            "Producao_m3": df_periodo["producao"],
            "Usuarios": df_periodo["usuarios"]
        })

    else:

        df_periodo = pd.DataFrame()

        df = pd.DataFrame(
            columns=[
                "Unidade",
                "Consumo_kWh",
                "Area_m2",
                "Producao_m3",
                "Usuarios"
            ]
        )


    # ==========================================
    # CÁLCULOS
    # ==========================================

    consumo_total = df["Consumo_kWh"].sum()
    producao_total = df["Producao_m3"].sum()
    usuarios_total = df["Usuarios"].sum()
    area_total = df["Area_m2"].sum()


    # ==========================================
    # INDICADORES
    # ==========================================

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="⚡ Consumo Total",
            value=f"{consumo_total:,.0f} kWh".replace(",", "."),
            
        )

    with col2:
        st.metric(
            label="🏭 Produção Total",
            value=f"{producao_total:,.0f} m³".replace(",", "."),
            
        )

    with col3:
        st.metric(
            label="👥 Total de Usuários",
            value=usuarios_total,
            
        )

    with col4:
        st.metric(
            label="↗️ Área Total",
            value=f"{area_total:,.0f} m²".replace(",", "."),
            
        )
    # ==========================================
    # GRÁFICOS
    # ==========================================

    st.write("")

    col_grafico1, col_grafico2 = st.columns([1.4, 1])


    # ------------------------------------------
    # GRÁFICO DE BARRAS
    # ------------------------------------------

    with col_grafico1:

        st.subheader("Consumo de Energia por Unidade")

        fig_consumo = px.bar(
            df,
            x="Unidade",
            y="Consumo_kWh",
            text="Consumo_kWh",
            labels={
                "Unidade": "",
                "Consumo_kWh": "Consumo (kWh)"
            }
        )

        fig_consumo.update_traces(
        marker_color=[
            "#0B2940",
            "#A7B6C6",
            "#F5A623",
            "#879BAD",
            "#B8C4CF"
        ],
        texttemplate="%{text:,.0f}",
        textposition="outside"
        )

        fig_consumo.update_layout(
            showlegend=False,
            yaxis_title="Consumo (kWh)",
            xaxis_title="",
            height=400
        )

        st.plotly_chart(
            fig_consumo,
            use_container_width=True
        )


    # ------------------------------------------
    # GRÁFICO DE ROSCA
    # ------------------------------------------

    with col_grafico2:

        st.subheader("Distribuição do Consumo por Equipamento")

        equipamentos = pd.DataFrame({
            "Equipamento": [
                "Compressores",
                "Bombas",
                "Refrigeração",
                "Iluminação",
                "Outros"
            ],

            "Consumo": [
                df_periodo["compressores"].sum(),
                df_periodo["bombas"].sum(),
                df_periodo["refrigeracao"].sum(),
                df_periodo["iluminacao"].sum(),
                df_periodo["outros"].sum()
            ]
        })

        cores_equipamentos = [
                "#0B2D45",
                "#F5A623",
                "#8FA3B5",
                "#AEBBC8",
                "#607D94",
                "#D6DEE5"
        ]

        fig_equipamentos = px.pie(
            equipamentos,
            names="Equipamento",
            values="Consumo",
            hole=0.55,
            color_discrete_sequence=cores_equipamentos
        )

        fig_equipamentos.update_traces(
            textinfo="percent"
        )

        fig_equipamentos.update_layout(
            height=400,
            legend_title_text=""
        )

        st.plotly_chart(
            fig_equipamentos,
            use_container_width=True
        )
    # ==========================================
    # ANÁLISE DE EFICIÊNCIA DAS UNIDADES
    # ==========================================

    # Consumo específico:
    # quantidade de energia necessária para produzir 1 m³

    df["Consumo_Especifico"] = (
        df["Consumo_kWh"] / df["Producao_m3"]
    )

    # Arredondar para duas casas decimais
    df["Consumo_Especifico"] = df["Consumo_Especifico"].round(2)


    # ==========================================
    # CLASSIFICAÇÃO
    # ==========================================

    def classificar_eficiencia(consumo_especifico):

        if consumo_especifico <= 4.5:
            return "Eficiente"

        elif consumo_especifico <= 6.0:
            return "Atenção"

        else:
            return "Ineficiente"


    df["Status"] = df["Consumo_Especifico"].apply(
        classificar_eficiencia
    )

    # ==========================================
    # ÍNDICE DE EFICIÊNCIA
    # ==========================================

    meta_consumo = 4.5

    df["Indice_Eficiencia"] = (
        meta_consumo /
        df["Consumo_Especifico"]
    ) * 100

    df["Indice_Eficiencia"] = (
        df["Indice_Eficiencia"]
        .clip(upper=100)
        .round(0)
        .astype(int)
    )


    # ==========================================
    # EXIBIÇÃO DA TABELA
    # ==========================================

    st.subheader("Desempenho das Unidades")

    tabela = df[
        [
            "Unidade",
            "Consumo_kWh",
            "Area_m2",
            "Producao_m3",
            "Usuarios",
            "Consumo_Especifico",
            "Indice_Eficiencia",
            "Status"
        ]
    ].copy()

    tabela.columns = [
        "Unidade",
        "Consumo (kWh)",
        "Área (m²)",
        "Produção (m³)",
        "Usuários",
        "Consumo Específico (kWh/m³)",
        "Índice de Eficiência",
        "Status"
    ]

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True
    )
    # ==========================================
    # UNIDADE EM DESTAQUE
    # ==========================================

    # Localiza automaticamente a unidade
    # com maior consumo específico
    unidade_critica = df.loc[
        df["Consumo_Especifico"].idxmax()
    ]

    st.write("")
    st.subheader("⚠️ Unidade em Destaque")

    col_info1, col_info2, col_info3, col_info4 = st.columns(4)

    with col_info1:
        st.metric(
            "Unidade",
            unidade_critica["Unidade"]
        )

    with col_info2:
        st.metric(
            "Consumo de Energia",
            f'{unidade_critica["Consumo_kWh"]:,.0f} kWh'.replace(",", ".")
        )

    with col_info3:
        st.metric(
            "Produção",
            f'{unidade_critica["Producao_m3"]:,.0f} m³'.replace(",", ".")
        )

    with col_info4:
        st.metric(
            "Consumo Específico",
            f'{unidade_critica["Consumo_Especifico"]:.2f} kWh/m³'.replace(".", ",")
        )


    # ==========================================
    # COMPARAÇÃO COM A MÉDIA
    # ==========================================

    media_consumo_especifico = df["Consumo_Especifico"].mean()

    percentual_acima = (
        (
            unidade_critica["Consumo_Especifico"]
            - media_consumo_especifico
        )
        / media_consumo_especifico
    ) * 100


    # ==========================================
    # ALERTA AUTOMÁTICO
    # ==========================================

    st.warning(
        f'⚠️ **{unidade_critica["Unidade"]} apresenta consumo específico '
        f'{percentual_acima:.1f}% acima da média das unidades analisadas.** '
        f'Recomenda-se avaliar os equipamentos e processos de maior consumo.'
    )

elif "Unidades" in pagina:

    st.markdown("""
        <p style="margin:0; color:#64748b; font-size:13px;">
            Gestão por Unidade
        </p>

        <h1 style="
            margin:8px 0 0 0;
            padding:0;
            font-size:34px;
            color:#071a2f;
        ">
            Unidades Operacionais
        </h1>

        <p style="
            margin:5px 0 20px 0;
            color:#64748b;
            font-size:14px;
        ">
            Analise o desempenho energético individual de cada instalação.
        </p>
    """, unsafe_allow_html=True)

    # ============================================
    # SELETORES DE UNIDADE E PERÍODO
    # ============================================

    col_filtro, col_periodo, col_espaco = st.columns([2, 2, 3])

    with col_filtro:
        unidade_selecionada = st.selectbox(
            "Selecione a unidade",
            [
                "Plataforma A",
                "Plataforma B",
                "Terminal C",
                "Refinaria D",
                "Base E"
            ]
        )

    # Busca os períodos cadastrados para a unidade selecionada
    conexao = conectar_banco()

    df_periodos = pd.read_sql_query(
        """
        SELECT mes, ano
        FROM dados_energia
        WHERE unidade = ?
        ORDER BY ano DESC, mes DESC
        """,
        conexao,
        params=(unidade_selecionada,)
    )

    conexao.close()

    with col_periodo:

        if not df_periodos.empty:

            meses_abreviados = {
                1: "Jan",
                2: "Fev",
                3: "Mar",
                4: "Abr",
                5: "Mai",
                6: "Jun",
                7: "Jul",
                8: "Ago",
                9: "Set",
                10: "Out",
                11: "Nov",
                12: "Dez"
            }

            opcoes_periodo = [
                f"{meses_abreviados[int(linha['mes'])]}/{int(linha['ano'])}"
                for _, linha in df_periodos.iterrows()
            ]

            periodo_selecionado = st.selectbox(
                "Período",
                opcoes_periodo
            )

        else:
            periodo_selecionado = None
            st.selectbox(
                "Período",
                ["Sem dados cadastrados"],
                disabled=True
            )

    # ============================================
    # BUSCA OS DADOS DA UNIDADE E PERÍODO
    # ============================================

    if periodo_selecionado is not None:

        meses_numero = {
            "Jan": 1,
            "Fev": 2,
            "Mar": 3,
            "Abr": 4,
            "Mai": 5,
            "Jun": 6,
            "Jul": 7,
            "Ago": 8,
            "Set": 9,
            "Out": 10,
            "Nov": 11,
            "Dez": 12
        }

        mes_texto, ano_texto = periodo_selecionado.split("/")

        mes_selecionado = meses_numero[mes_texto]
        ano_selecionado = int(ano_texto)

        conexao = conectar_banco()

        df_unidade = pd.read_sql_query(
            """
            SELECT *
            FROM dados_energia
            WHERE unidade = ?
            AND mes = ?
            AND ano = ?
            LIMIT 1
            """,
            conexao,
            params=(
                unidade_selecionada,
                mes_selecionado,
                ano_selecionado
            )
        )

        conexao.close()

        if not df_unidade.empty:

            registro = df_unidade.iloc[0]

            dados = {
                "consumo": float(registro["consumo"]),
                "producao": float(registro["producao"]),
                "area": float(registro["area"]),
                "usuarios": int(registro["usuarios"]),
                "compressores": float(registro["compressores"]),
                "bombas": float(registro["bombas"]),
                "refrigeracao": float(registro["refrigeracao"]),
                "iluminacao": float(registro["iluminacao"]),
                "outros": float(registro["outros"])
            }

            dados["eficiencia"] = (
                dados["consumo"] / dados["producao"]
                if dados["producao"] > 0
                else 0
            )

    # ========================================
    # CARDS DA UNIDADE
    # ========================================

    consumo_especifico = dados["consumo"] / dados["producao"]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "⚡ Consumo de Energia",
            f'{dados["consumo"]:,.0f} kWh'.replace(",", ".")
        )

    with col2:
        st.metric(
            "🏭 Produção",
            f'{dados["producao"]:,.0f} m³'.replace(",", ".")
        )

    with col3:
        st.metric(
            "📐 Área",
            f'{dados["area"]:,.0f} m²'.replace(",", ".")
        )

    with col4:
        st.metric(
            "👥 Usuários",
            dados["usuarios"]
        )

    with col5:
        st.metric(
            "📊 Consumo Específico",
            f'{consumo_especifico:.2f} kWh/m³'.replace(".", ",")
        )
    # ============================================
    # EVOLUÇÃO MENSAL DA UNIDADE - BANCO DE DADOS
    # ============================================

    st.markdown("### Evolução do Consumo de Energia")

    # Busca todo o histórico da unidade selecionada
    conexao = conectar_banco()

    df_historico = pd.read_sql_query(
        """
        SELECT
            mes,
            ano,
            consumo
        FROM dados_energia
        WHERE unidade = ?
        ORDER BY ano ASC, mes ASC
        """,
        conexao,
        params=(unidade_selecionada,)
    )

    conexao.close()

    if not df_historico.empty:

        # Nomes dos meses
        nomes_meses = {
            1: "Jan",
            2: "Fev",
            3: "Mar",
            4: "Abr",
            5: "Mai",
            6: "Jun",
            7: "Jul",
            8: "Ago",
            9: "Set",
            10: "Out",
            11: "Nov",
            12: "Dez"
        }

        # Cria o texto que aparecerá no eixo X
        df_historico["Período"] = df_historico.apply(
            lambda linha: f"{nomes_meses[int(linha['mes'])]}/{int(linha['ano'])}",
            axis=1
        )

        fig_historico = px.line(
            df_historico,
            x="Período",
            y="consumo",
            markers=True
        )

        fig_historico.update_traces(
            line=dict(
                color="#0B2D45",
                width=3
            ),
            marker=dict(
                color="#F5A623",
                size=8
            )
        )

        fig_historico.update_layout(
            xaxis_title="",
            yaxis_title="Consumo (kWh)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig_historico,
            use_container_width=True
        )

    else:
        st.info(
            "Ainda não existem dados históricos cadastrados para esta unidade."
        )

    # ============================================
    # CONSUMO POR EQUIPAMENTO - DADOS DO BANCO
    # ============================================

    df_equipamentos = pd.DataFrame({
        "Equipamento": [
            "Compressores",
            "Bombas",
            "Refrigeração",
            "Iluminação",
            "Outros"
        ],
        "Consumo (kWh)": [
            dados["compressores"],
            dados["bombas"],
            dados["refrigeracao"],
            dados["iluminacao"],
            dados["outros"]
        ]
    })

    # Calcula o percentual automaticamente
    total_equipamentos = df_equipamentos["Consumo (kWh)"].sum()

    if total_equipamentos > 0:
        df_equipamentos["Percentual"] = (
            df_equipamentos["Consumo (kWh)"]
            / total_equipamentos
            * 100
        )
    else:
        df_equipamentos["Percentual"] = 0

    # Identifica automaticamente o equipamento com maior consumo
        
    principal_equipamento = df_equipamentos.loc[
        df_equipamentos["Percentual"].idxmax(),
        "Equipamento"
    ]


    # ==========================================
    # DISTRIBUIÇÃO + DIAGNÓSTICO DA UNIDADE
    # ==========================================

    st.markdown("## Análise do Consumo da Unidade")

    col_grafico, col_diagnostico = st.columns([1.7, 1], gap="large")

    # ------------------------------------------
    # GRÁFICO DE EQUIPAMENTOS
    # ------------------------------------------

    with col_grafico:

        st.markdown("### Distribuição do Consumo por Equipamento")

        cores_equipamentos = [
            "#0B2D45",
            "#F5A623",
            "#8FA3B5",
            "#AEBBC8",
            "#607D94",
            "#D6DEE5"
        ]

        fig_equip_unidade = px.pie(
            df_equipamentos,
            names="Equipamento",
            values="Consumo (kWh)",
            hole=0.55,
            color_discrete_sequence=cores_equipamentos,
            custom_data=["Percentual"]
        )

        fig_equip_unidade.update_traces(
            textinfo="percent",
            textposition="inside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Consumo: %{value:,.0f} kWh<br>"
                "Participação: %{percent}<extra></extra>"
            )
        )

        fig_equip_unidade.update_layout(
            height=380,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02
            )
        )

        st.plotly_chart(
            fig_equip_unidade,
            use_container_width=True
        )

    # ------------------------------------------
    # DIAGNÓSTICOS
    # ------------------------------------------

    diagnosticos = {

        "Plataforma A": {
            "status": "EFICIENTE",
            "cor": "#159957",
            "fundo": "#E8F7EF",
            "icone": "🟢",
            "principal": "Bombas",
            "texto": "A unidade apresenta bom desempenho energético em relação às demais instalações.",
            "recomendacao": "Manter o acompanhamento dos equipamentos e as práticas atuais de eficiência."
        },

        "Plataforma B": {
            "status": "ATENÇÃO",
            "cor": "#D98A00",
            "fundo": "#FFF4D9",
            "icone": "🟠",
            "principal": "Compressores",
            "texto": "O consumo específico indica oportunidade de melhoria na eficiência operacional.",
            "recomendacao": "Avaliar o funcionamento dos compressores e possíveis perdas durante a operação."
        },

        "Terminal C": {
            "status": "EFICIENTE",
            "cor": "#159957",
            "fundo": "#E8F7EF",
            "icone": "🟢",
            "principal": "Bombas",
            "texto": "Mesmo com alto consumo total, a produção elevada mantém um bom nível de eficiência energética.",
            "recomendacao": "Monitorar o sistema de bombeamento para preservar o desempenho atual."
        },

        "Refinaria D": {
            "status": "ATENÇÃO",
            "cor": "#D98A00",
            "fundo": "#FFF4D9",
            "icone": "🟠",
            "principal": "Sistemas Térmicos",
            "texto": "A unidade apresenta consumo específico elevado em comparação com unidades de desempenho semelhante.",
            "recomendacao": "Priorizar a análise dos sistemas térmicos, responsáveis pela maior parcela do consumo."
        },

        "Base E": {
            "status": "INEFICIENTE",
            "cor": "#D64545",
            "fundo": "#FDECEC",
            "icone": "🔴",
            "principal": "Compressores",
            "texto": "A unidade apresenta o maior consumo específico entre as instalações analisadas.",
            "recomendacao": "Realizar uma avaliação energética dos equipamentos e investigar perdas operacionais."
        }
    }

    diag = diagnosticos[unidade_selecionada]

    # Atualiza o principal ponto de atenção com os dados do período selecionado
    diag = diag.copy()
    diag["principal"] = principal_equipamento

    # Define o status automaticamente pelo consumo específico
    if consumo_especifico <= 4.5:
        diag["status"] = "EFICIENTE"
        diag["cor"] = "#159957"
        diag["fundo"] = "#E8F7EF"
        diag["icone"] = "🟢"

    elif consumo_especifico <= 6.0:
        diag["status"] = "ATENÇÃO"
        diag["cor"] = "#D98A00"
        diag["fundo"] = "#FFF4D9"
        diag["icone"] = "🟠"

    else:
        diag["status"] = "INEFICIENTE"
        diag["cor"] = "#D64545"
        diag["fundo"] = "#FDE8E8"
        diag["icone"] = "🔴"

    # Define texto e recomendação automaticamente conforme o status
    if consumo_especifico <= 4.5:
        diag["texto"] = (
            "A unidade apresenta bom desempenho energético no período analisado, "
            "mantendo o consumo específico dentro da meta estabelecida."
        )

        diag["recomendacao"] = (
            f"Manter o acompanhamento dos equipamentos e monitorar o consumo de "
            f"{principal_equipamento}, atualmente responsável pela maior parcela do consumo."
        )

    elif consumo_especifico <= 6.0:
        diag["texto"] = (
            "O consumo específico está acima da meta estabelecida, indicando "
            "oportunidade de melhoria na eficiência operacional."
        )

        diag["recomendacao"] = (
            f"Avaliar o funcionamento de {principal_equipamento} e investigar "
            f"possíveis perdas ou oportunidades de redução do consumo."
        )

    else:
        diag["texto"] = (
            "A unidade apresenta consumo específico elevado no período analisado, "
            "indicando necessidade de atenção ao desempenho energético."
        )

        diag["recomendacao"] = (
            f"Priorizar uma avaliação energética de {principal_equipamento} e dos "
            f"processos associados, buscando identificar desperdícios e possíveis ações corretivas."
        )


    # ------------------------------------------
    # CARD DE DIAGNÓSTICO
    # ------------------------------------------

    with col_diagnostico:

        st.markdown("### Diagnóstico da Unidade")

        html_diagnostico = f"""
        <div style="background:white; border:1px solid #D6DEE5; border-radius:12px; padding:24px; min-height:330px;">

        <div style="display:inline-block; background:{diag['fundo']}; color:{diag['cor']}; padding:6px 12px; border-radius:20px; font-size:13px; font-weight:700; margin-bottom:20px;">
        {diag['icone']} {diag['status']}
        </div>

        <div style="font-size:13px; color:#64748B; margin-bottom:4px;">
        Consumo específico
        </div>

        <div style="font-size:28px; font-weight:700; color:#071A2F; margin-bottom:18px;">
        {f"{consumo_especifico:.2f}".replace(".", ",")} kWh/m³
        </div>

        <div style="font-size:13px; color:#64748B;">
        Principal ponto de atenção
        </div>

        <div style="font-size:18px; font-weight:600; color:#071A2F; margin-bottom:18px;">
        {diag['principal']}
        </div>

        <div style="font-size:14px; color:#334155; line-height:1.5; margin-bottom:18px;">
        {diag['texto']}
        </div>

        <div style="border-top:1px solid #E2E8F0; padding-top:14px; font-size:13px; color:#334155; line-height:1.5;">
        <b>Recomendação</b><br>
        {diag['recomendacao']}
        </div>

        </div>
        """

        st.markdown(html_diagnostico, unsafe_allow_html=True)

elif pagina == "📊  Indicadores":

    # ==========================================
    # CABEÇALHO - INDICADORES
    # ==========================================

    st.markdown(
        """
        <p style="margin:0; color:#64748B; font-size:13px;">
            Indicadores de Desempenho
        </p>

        <h1 style="
            margin:8px 0 0 0;
            padding:0;
            font-size:34px;
            color:#071A2F;
        ">
            Indicadores Energéticos
        </h1>

        <p style="
            margin:5px 0 25px 0;
            color:#64748B;
            font-size:14px;
        ">
            Acompanhe os principais indicadores de eficiência e desempenho energético das instalações.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>

        .kpi-card {
            background: white;
            border: 1px solid #D6DEE5;
            border-radius: 12px;
            padding: 22px;
            min-height: 120px;
        }

        .kpi-label {
            color: #334155;
            font-size: 13px;
            margin-bottom: 6px;
        }

        .kpi-value {
            color: #071A2F;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .kpi-positive {
            display: inline-block;
            color: #159957;
            background: #E8F7EF;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }

        .kpi-neutral {
            display: inline-block;
            color: #607D94;
            background: #EEF2F6;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================================
    # DADOS DOS INDICADORES - BANCO DE DADOS
    # ==========================================

    conexao = conectar_banco()

    df_indicadores = pd.read_sql_query(
        """
        SELECT *
        FROM dados_energia
        ORDER BY ano DESC, mes DESC
        """,
        conexao
    )

    conexao.close()

    if not df_indicadores.empty:

        # Descobre o período mais recente cadastrado
        ano_atual = int(df_indicadores["ano"].max())

        mes_atual = int(
            df_indicadores[
                df_indicadores["ano"] == ano_atual
            ]["mes"].max()
        )

        # Mantém somente os registros do período mais recente
        df_periodo_atual = df_indicadores[
            (df_indicadores["ano"] == ano_atual) &
            (df_indicadores["mes"] == mes_atual)
        ].copy()

        # Calcula o consumo específico de cada unidade
        df_periodo_atual["consumo_especifico"] = (
            df_periodo_atual["consumo"] /
            df_periodo_atual["producao"]
        )

        # Média do consumo específico
        consumo_especifico_medio = (
            df_periodo_atual["consumo_especifico"].mean()
        )

        # ==========================================
        # ÍNDICE MÉDIO DE EFICIÊNCIA
        # ==========================================

        meta_consumo = 4.5

        df_periodo_atual["indice_eficiencia"] = (
            meta_consumo /
            df_periodo_atual["consumo_especifico"]
        ) * 100

        # O índice máximo será 100
        df_periodo_atual["indice_eficiencia"] = (
            df_periodo_atual["indice_eficiencia"].clip(upper=100)
        )

        indice_medio_eficiencia = (
            df_periodo_atual["indice_eficiencia"].mean()
        )

        # ==========================================
        # COMPARAÇÃO COM O MÊS ANTERIOR
        # ==========================================

        if mes_atual == 1:
            mes_anterior = 12
            ano_anterior = ano_atual - 1
        else:
            mes_anterior = mes_atual - 1
            ano_anterior = ano_atual

        df_periodo_anterior = df_indicadores[
            (df_indicadores["ano"] == ano_anterior) &
            (df_indicadores["mes"] == mes_anterior)
        ].copy()

        if not df_periodo_anterior.empty:

            df_periodo_anterior["consumo_especifico"] = (
                df_periodo_anterior["consumo"] /
                df_periodo_anterior["producao"]
            )

            consumo_especifico_anterior = (
                df_periodo_anterior["consumo_especifico"].mean()
            )

            variacao_consumo = (
                (consumo_especifico_medio - consumo_especifico_anterior)
                / consumo_especifico_anterior
            ) * 100

            if variacao_consumo < 0:
                texto_variacao = f"↓ {abs(variacao_consumo):.1f}% vs. mês anterior"
            elif variacao_consumo > 0:
                texto_variacao = f"↑ {variacao_consumo:.1f}% vs. mês anterior"
            else:
                texto_variacao = "Sem alteração vs. mês anterior"

        else:
            texto_variacao = "Sem dados do mês anterior"

        # ==========================================
        # VARIAÇÃO DO ÍNDICE DE EFICIÊNCIA
        # ==========================================

        if not df_periodo_anterior.empty:

            df_periodo_anterior["indice_eficiencia"] = (
                meta_consumo /
                df_periodo_anterior["consumo_especifico"]
            ) * 100

            df_periodo_anterior["indice_eficiencia"] = (
                df_periodo_anterior["indice_eficiencia"].clip(upper=100)
            )

            indice_anterior = (
                df_periodo_anterior["indice_eficiencia"].mean()
            )

            variacao_indice = (
                indice_medio_eficiencia - indice_anterior
            )

            if variacao_indice > 0:
                texto_variacao_indice = f"↑ {variacao_indice:.1f} pontos"

            elif variacao_indice < 0:
                texto_variacao_indice = f"↓ {abs(variacao_indice):.1f} pontos"

            else:
                texto_variacao_indice = "Sem alteração"

        else:
            texto_variacao_indice = "Sem dados anteriores"
        
    else:
        consumo_especifico_medio = 0

    # ==========================================
    # UNIDADES NA META
    # ==========================================

    total_unidades = len(df_periodo_atual)

    unidades_na_meta = (
        df_periodo_atual["consumo_especifico"] <= meta_consumo
    ).sum()

    if total_unidades > 0:
        percentual_na_meta = (
            unidades_na_meta / total_unidades
        ) * 100
    else:
        percentual_na_meta = 0

    # ==========================================
    # ECONOMIA ESTIMADA
    # ==========================================

    df_periodo_atual["consumo_meta"] = (
        df_periodo_atual["producao"] * meta_consumo
    )

    df_periodo_atual["economia_potencial"] = (
        df_periodo_atual["consumo"] -
        df_periodo_atual["consumo_meta"]
    )

    # Unidades que já estão dentro da meta
    # não possuem economia potencial neste cálculo
    df_periodo_atual["economia_potencial"] = (
        df_periodo_atual["economia_potencial"].clip(lower=0)
    )

    economia_estimada = (
        df_periodo_atual["economia_potencial"].sum()
    )


    # ==========================================
    # KPIs
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">⚡ Consumo Específico Médio</div>
                <div class="kpi-value">{consumo_especifico_medio:.2f} kWh/m³</div>
                <div class="kpi-positive">{texto_variacao}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">📊 Índice Médio de Eficiência</div>
                <div class="kpi-value">{indice_medio_eficiencia:.1f}</div>
                <div class="kpi-positive">{texto_variacao_indice}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">🎯 Unidades na Meta</div>
                <div class="kpi-value">{unidades_na_meta} de {total_unidades}</div>
                <div class="kpi-neutral">{percentual_na_meta:.0f}% das instalações</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">🌱 Economia Estimada</div>
                <div class="kpi-value">{economia_estimada:,.0f}</div>
                <div class="kpi-positive">↑ 6,1% no período</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    # ==========================================
    # CONSUMO ESPECÍFICO POR UNIDADE
    # ==========================================

    st.markdown("## Consumo Específico por Unidade")

    # Dados reais do período atual
    df_grafico_consumo = df_periodo_atual[
        ["unidade", "consumo_especifico"]
    ].copy()

    df_grafico_consumo = df_grafico_consumo.rename(
        columns={
            "unidade": "Unidade",
            "consumo_especifico": "Consumo Específico"
        }
    )

    fig_indicadores = px.bar(
        df_grafico_consumo,
        x="Unidade",
        y="Consumo Específico",
        text="Consumo Específico",
        color="Unidade",
        color_discrete_sequence=[
            "#0B2D45",
            "#8FA3B5",
            "#F5A623",
            "#607D94",
            "#D6DEE5"
        ]
    )

    fig_indicadores.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_indicadores.update_layout(
        height=380,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=30, b=20),

        xaxis=dict(
            title="",
            showgrid=False
        ),

        yaxis=dict(
            title="Consumo Específico (kWh/m³)",
            gridcolor="#E8EDF2",
            zeroline=False
        )
    )

    # Linha de meta
    fig_indicadores.add_hline(
        y=4.5,
        line_dash="dash",
        line_color="#F5A623",
        line_width=2,
        annotation_text="Meta: 4,5 kWh/m³",
        annotation_position="top left",
        annotation_font=dict(
            color="#F5A623",
            size=12
        )
    )

    st.plotly_chart(
        fig_indicadores,
        use_container_width=True
    )
    # ==========================================
    # ÍNDICE DE EFICIÊNCIA DAS UNIDADES
    # ==========================================

    st.markdown("## Índice de Eficiência das Unidades")

   # Dados reais de eficiência do período atual
    df_eficiencia = df_periodo_atual[
        ["unidade", "indice_eficiencia"]
    ].copy()

    df_eficiencia = df_eficiencia.rename(
        columns={
            "unidade": "Unidade",
            "indice_eficiencia": "Eficiência"
        }
    )

    fig_eficiencia = px.bar(
        df_eficiencia,
        x="Eficiência",
        y="Unidade",
        orientation="h",
        text="Eficiência",
        color="Unidade",
        color_discrete_sequence=[
            "#0B2D45",
            "#8FA3B5",
            "#F5A623",
            "#607D94",
            "#D6DEE5"
        ]
    )

    fig_eficiencia.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig_eficiencia.update_layout(
        height=360,
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=20, r=40, t=30, b=20),

        xaxis=dict(
            title="Índice de Eficiência",
            range=[0, 100],
            gridcolor="#E8EDF2",
            zeroline=False
        ),

        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=[
                "Base E",
                "Refinaria D",
                "Terminal C",
                "Plataforma B",
                "Plataforma A"
            ]
        )
    )

    fig_eficiencia.add_vline(
        x=70,
        line_dash="dash",
        line_color="#F5A623",
        line_width=2,
        annotation_text="Meta: 70",
        annotation_position="top",
        annotation_font=dict(
            color="#F5A623",
            size=12
        )
    )

    st.plotly_chart(
        fig_eficiencia,
        use_container_width=True
    )

    # =========================================================
    # UNIDADES QUE EXIGEM ATENÇÃO
    # =========================================================

    st.markdown("""
        <div style="margin-top: 25px;">
            <h2 style="color:#0B2D45; margin-bottom:5px;">
                Unidades que exigem atenção
            </h2>
            <p style="color:#607D94; margin-top:0;">
                Instalações que apresentam indicadores fora das metas estabelecidas.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Dados reais para geração dos alertas
    dados_alerta = {}

    for _, registro in df_periodo_atual.iterrows():

        dados_alerta[registro["unidade"]] = {
            "consumo": float(registro["consumo_especifico"]),
            "eficiencia": float(registro["indice_eficiencia"])
        }

    meta_consumo = 4.5
    meta_eficiencia = 70

    unidades_alerta = []

    for unidade, dados in dados_alerta.items():

        if (
            dados["consumo"] > meta_consumo
            or dados["eficiencia"] < meta_eficiencia
        ):

            if dados["consumo"] >= 6 or dados["eficiencia"] < 50:
                status = "CRÍTICO"
                cor = "#D9534F"
                fundo = "#FFF4F4"
                icone = "🔴"
            else:
                status = "ATENÇÃO"
                cor = "#F5A623"
                fundo = "#FFF8EA"
                icone = "⚠️"

            unidades_alerta.append(
                (unidade, dados, status, cor, fundo, icone)
            )

        col1, col2 = st.columns(2)

    for i, (unidade, dados, status, cor, fundo, icone) in enumerate(unidades_alerta):

        coluna = col1 if i % 2 == 0 else col2
        consumo_formatado = f"{dados['consumo']:.2f}".replace(".", ",")

        card_html = f"""
            <div style="background:{fundo}; border:1px solid {cor}; border-left:6px solid {cor}; border-radius:12px; padding:20px; margin-bottom:15px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="color:#0B2D45; margin:0;">{icone} {unidade}</h3>
            <span style="background:{cor}; color:white; padding:5px 10px; border-radius:20px; font-size:12px; font-weight:bold;">{status}</span>
            </div>
            <div style="display:flex; gap:35px; margin-top:18px;">
            <div>
            <div style="color:#607D94; font-size:12px;">Consumo específico</div>
            <div style="color:#0B2D45; font-size:20px; font-weight:bold;">{consumo_formatado} kWh/m³</div>
            </div>
            <div>
            <div style="color:#607D94; font-size:12px;">Índice de eficiência</div>
            <div style="color:#0B2D45; font-size:20px; font-weight:bold;">{dados["eficiencia"]}</div>
            </div>
            </div>
            </div>
            """

        with coluna:
            st.markdown(card_html, unsafe_allow_html=True)

elif pagina == "📈  Comparativos":

    # =========================================================
    # CABEÇALHO
    # =========================================================

    st.markdown("""
        <h1 style="
            color:#0B2D45;
            margin-bottom:5px;
        ">
            Comparativo entre Unidades
        </h1>

        <p style="
            color:#607D94;
            margin-top:0;
            margin-bottom:30px;
        ">
            Compare o desempenho energético de duas instalações.
        </p>
    """, unsafe_allow_html=True)

    # =========================================================
    # DADOS REAIS DAS UNIDADES - BANCO DE DADOS
    # =========================================================

    conexao = conectar_banco()

    df_comparativos = pd.read_sql_query(
        """
        SELECT *
        FROM dados_energia
        ORDER BY ano DESC, mes DESC
        """,
        conexao
    )

    conexao.close()

    dados_comparativos = {}

    if not df_comparativos.empty:

        # Lista das unidades que realmente possuem dados cadastrados
        unidades_disponiveis = sorted(
            df_comparativos["unidade"].unique().tolist()
        )

        for unidade in unidades_disponiveis:

            df_unidade_comp = df_comparativos[
                df_comparativos["unidade"] == unidade
            ].copy()

            # Pega o registro mais recente da unidade
            registro = df_unidade_comp.iloc[0]

            consumo_especifico = (
                float(registro["consumo"]) /
                float(registro["producao"])
                if float(registro["producao"]) > 0
                else 0
            )

            eficiencia = min(
                100,
                (4.5 / consumo_especifico) * 100
            ) if consumo_especifico > 0 else 0

            dados_comparativos[unidade] = {
                "consumo": float(registro["consumo"]),
                "producao": float(registro["producao"]),
                "area": float(registro["area"]),
                "usuarios": int(registro["usuarios"]),
                "consumo_especifico": consumo_especifico,
                "eficiencia": eficiencia
            }

    else:
        unidades_disponiveis = []


    # =========================================================
    # SELEÇÃO DAS UNIDADES
    # =========================================================

    col_select1, col_meio, col_select2 = st.columns([1, 0.12, 1])

    with col_select1:

        unidade_a = st.selectbox(
            "Unidade A",
            unidades_disponiveis,
            index=0,
            key="comparativo_a"
        )

    with col_meio:

        st.markdown("""
            <div style="
                text-align:center;
                font-size:24px;
                font-weight:bold;
                color:#F5A623;
                padding-top:30px;
            ">
                ×
            </div>
        """, unsafe_allow_html=True)

    with col_select2:

        unidade_b = st.selectbox(
            "Unidade B",
            unidades_disponiveis,
            index=1 if len(unidades_disponiveis) > 1 else 0,
            key="comparativo_b"
        )


    dados_a = dados_comparativos[unidade_a]
    dados_b = dados_comparativos[unidade_b]


    # =========================================================
    # TÍTULO DO CONFRONTO
    # =========================================================

    titulo_confronto = f"""
        <div style="text-align:center; margin-top:25px; margin-bottom:20px;">
        <span style="color:#0B2D45; font-size:24px; font-weight:bold;">{unidade_a}</span>
        <span style="color:#F5A623; font-size:22px; font-weight:bold; margin:0 15px;">VS</span>
        <span style="color:#0B2D45; font-size:24px; font-weight:bold;">{unidade_b}</span>
        </div>
        """

    st.markdown(titulo_confronto, unsafe_allow_html=True)

    # =========================================================
    # CARDS COMPARATIVOS
    # =========================================================

    indicadores = [
        ("⚡ Consumo", "consumo", "kWh", 0),
        ("🛢️ Produção", "producao", "m³", 0),
        ("📐 Área", "area", "m²", 0),
        ("👥 Usuários", "usuarios", "", 0),
        ("📊 Consumo Específico", "consumo_especifico", "kWh/m³", 2),
        ("📈 Eficiência", "eficiencia", "pontos", 0)
    ]

    for titulo, chave, unidade_medida, casas in indicadores:

        valor_a = dados_a[chave]
        valor_b = dados_b[chave]

        if casas == 2:
            texto_a = f"{valor_a:.2f}".replace(".", ",")
            texto_b = f"{valor_b:.2f}".replace(".", ",")
        else:
            texto_a = f"{valor_a:,.0f}".replace(",", ".")
            texto_b = f"{valor_b:,.0f}".replace(",", ".")

        col_a, col_nome, col_b = st.columns([1, 0.8, 1])

        with col_a:
            st.markdown(
                f"""
                <div style="background:white; border:1px solid #D6DEE5; border-radius:10px; padding:14px; text-align:center; margin-bottom:4px;">
                <div style="font-size:20px; font-weight:bold; color:#0B2D45;">{texto_a} {unidade_medida}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_nome:
            st.markdown(
                f"""
                <div style="text-align:center; padding-top:13px; color:#607D94; font-weight:600;">
                {titulo}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_b:
            st.markdown(
                f"""
                <div style="background:white; border:1px solid #D6DEE5; border-radius:10px; padding:14px; text-align:center; margin-bottom:4px;">
                <div style="font-size:20px; font-weight:bold; color:#0B2D45;">{texto_b} {unidade_medida}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    # =========================================================
    # ANÁLISE COMPARATIVA
    # =========================================================

    st.markdown("""
        <div style="margin-top:30px;">
            <h2 style="color:#0B2D45; margin-bottom:5px;">
                Análise Comparativa
            </h2>
            <p style="color:#607D94; margin-top:0;">
                Avaliação do desempenho energético das unidades selecionadas.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Define qual unidade possui melhor consumo específico
    if dados_a["consumo_especifico"] < dados_b["consumo_especifico"]:
        melhor_consumo = unidade_a
    elif dados_b["consumo_especifico"] < dados_a["consumo_especifico"]:
        melhor_consumo = unidade_b
    else:
        melhor_consumo = "Empate"

    # Define qual unidade possui maior índice de eficiência
    if dados_a["eficiencia"] > dados_b["eficiencia"]:
        melhor_eficiencia = unidade_a
    elif dados_b["eficiencia"] > dados_a["eficiencia"]:
        melhor_eficiencia = unidade_b
    else:
        melhor_eficiencia = "Empate"

    # Resultado geral
    pontos_a = 0
    pontos_b = 0

    if dados_a["consumo_especifico"] < dados_b["consumo_especifico"]:
        pontos_a += 1
    elif dados_b["consumo_especifico"] < dados_a["consumo_especifico"]:
        pontos_b += 1

    if dados_a["eficiencia"] > dados_b["eficiencia"]:
        pontos_a += 1
    elif dados_b["eficiencia"] > dados_a["eficiencia"]:
        pontos_b += 1

    if pontos_a > pontos_b:
        melhor_geral = unidade_a
        texto_resultado = f"{unidade_a} apresenta melhor desempenho energético geral."
    elif pontos_b > pontos_a:
        melhor_geral = unidade_b
        texto_resultado = f"{unidade_b} apresenta melhor desempenho energético geral."
    else:
        melhor_geral = "Equilíbrio"
        texto_resultado = "As unidades apresentam desempenho energético equilibrado nos critérios analisados."

    # Formatação dos valores
    consumo_a = f"{dados_a['consumo_especifico']:.2f}".replace(".", ",")
    consumo_b = f"{dados_b['consumo_especifico']:.2f}".replace(".", ",")

    analise_html = f"""
        <div style="background:white; border:1px solid #D6DEE5; border-radius:12px; padding:22px;">

        <div style="font-size:18px; font-weight:bold; color:#0B2D45; margin-bottom:15px;">
        🏆 {texto_resultado}
        </div>

        <div style="color:#607D94; line-height:1.8;">
        <b style="color:#0B2D45;">Consumo específico:</b>
        {unidade_a} apresenta {consumo_a} kWh/m³ e {unidade_b} apresenta {consumo_b} kWh/m³.
        Melhor resultado: <b>{melhor_consumo}</b>.
        <br>

        <b style="color:#0B2D45;">Índice de eficiência:</b>
        {unidade_a} possui {dados_a["eficiencia"]} pontos e {unidade_b} possui {dados_b["eficiencia"]} pontos.
        Melhor resultado: <b>{melhor_eficiencia}</b>.
        </div>

        </div>
        """

    st.markdown(analise_html, unsafe_allow_html=True)

    # =========================================================
    # EVOLUÇÃO COMPARATIVA
    # =========================================================

    st.markdown("""
        <div style="margin-top:30px;">
            <h2 style="color:#0B2D45; margin-bottom:5px;">
                Evolução do Consumo Específico
            </h2>
            <p style="color:#607D94; margin-top:0;">
                Comparação mensal do desempenho energético das unidades selecionadas.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # HISTÓRICO REAL DAS UNIDADES SELECIONADAS
    # =========================================================

    df_evolucao = df_comparativos[
        df_comparativos["unidade"].isin(
            [unidade_a, unidade_b]
        )
    ].copy()

    # Calcula o consumo específico
    df_evolucao["Consumo Específico"] = (
        df_evolucao["consumo"] /
        df_evolucao["producao"]
    )

    # Nomes dos meses
    nomes_meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }

    df_evolucao["Mês"] = df_evolucao.apply(
        lambda linha:
            f"{nomes_meses[int(linha['mes'])]}/{int(linha['ano'])}",
        axis=1
    )

    df_evolucao["Unidade"] = df_evolucao["unidade"]

    # Coluna auxiliar para ordenar cronologicamente
    df_evolucao["ordem_periodo"] = (
        df_evolucao["ano"] * 100 +
        df_evolucao["mes"]
    )

    df_evolucao = df_evolucao.sort_values(
        "ordem_periodo"
    )

    fig_evolucao = px.line(
        df_evolucao,
        x="Mês",
        y="Consumo Específico",
        color="Unidade",
        markers=True,
        color_discrete_sequence=[
            "#0B2D45",
            "#5DADE2"
        ]
    )

    fig_evolucao.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    fig_evolucao.update_layout(
        height=420,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=30, b=20),
        legend_title_text="Unidade",
        xaxis_title="",
        yaxis_title="Consumo Específico (kWh/m³)",
        font=dict(color="#607D94")
    )

    fig_evolucao.update_xaxes(
        showgrid=False
    )

    fig_evolucao.update_yaxes(
        gridcolor="#E8EDF2"
    )

    # Linha da meta
    fig_evolucao.add_hline(
        y=4.5,
        line_dash="dash",
        line_color="#F5A623",
        annotation_text="Meta: 4,5 kWh/m³",
        annotation_position="top left"
    )

    st.plotly_chart(
        fig_evolucao,
        use_container_width=True
    )

elif pagina == "📄  Relatórios":

    # =========================================================
    # CABEÇALHO
    # =========================================================

    st.markdown("""
        <h1 style="
            color:#0B2D45;
            margin-bottom:5px;
        ">
            Relatórios Energéticos
        </h1>

        <p style="
            color:#607D94;
            margin-top:0;
            margin-bottom:30px;
        ">
            Consulte, filtre e exporte os dados de desempenho energético das instalações.
        </p>
    """, unsafe_allow_html=True)


    # =========================================================
    # DADOS DO BANCO
    # =========================================================

    conexao = conectar_banco()

    df_relatorios = pd.read_sql_query(
        """
        SELECT *
        FROM dados_energia
        ORDER BY ano DESC, mes DESC, unidade
        """,
        conexao
    )

    conexao.close()


    if df_relatorios.empty:

        st.info(
            "Nenhum dado energético foi cadastrado para geração de relatórios."
        )

    else:

        # =====================================================
        # PREPARAÇÃO DOS DADOS
        # =====================================================

        nomes_meses = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }

        df_relatorios["Período"] = df_relatorios.apply(
            lambda linha:
                f"{nomes_meses[int(linha['mes'])]}/{int(linha['ano'])}",
            axis=1
        )

        df_relatorios["ordem_periodo"] = (
            df_relatorios["ano"] * 100 +
            df_relatorios["mes"]
        )

        df_relatorios["Consumo Específico"] = (
            df_relatorios["consumo"] /
            df_relatorios["producao"]
        )

        meta_consumo = 4.5

        df_relatorios["Índice de Eficiência"] = (
            meta_consumo /
            df_relatorios["Consumo Específico"]
        ) * 100

        df_relatorios["Índice de Eficiência"] = (
            df_relatorios["Índice de Eficiência"]
            .clip(upper=100)
        )


        # =====================================================
        # FILTROS
        # =====================================================

        st.markdown("### Filtros do Relatório")

        col_filtro1, col_filtro2 = st.columns(2)

        periodos_disponiveis = (
            df_relatorios[
                ["Período", "ordem_periodo"]
            ]
            .drop_duplicates()
            .sort_values(
                "ordem_periodo",
                ascending=False
            )
        )

        lista_periodos = (
            periodos_disponiveis["Período"].tolist()
        )

        with col_filtro1:

            periodo_selecionado = st.selectbox(
                "📅 Período",
                lista_periodos
            )

        unidades_relatorio = sorted(
            df_relatorios["unidade"]
            .dropna()
            .unique()
            .tolist()
        )

        with col_filtro2:

            unidade_selecionada_relatorio = st.selectbox(
                "🏢 Unidade",
                ["Todas as unidades"] + unidades_relatorio
            )


        # =====================================================
        # APLICAÇÃO DOS FILTROS
        # =====================================================

        df_filtrado = df_relatorios[
            df_relatorios["Período"] ==
            periodo_selecionado
        ].copy()

        if unidade_selecionada_relatorio != "Todas as unidades":

            df_filtrado = df_filtrado[
                df_filtrado["unidade"] ==
                unidade_selecionada_relatorio
            ].copy()


        # =====================================================
        # INDICADORES DO RELATÓRIO
        # =====================================================

        consumo_relatorio = (
            df_filtrado["consumo"].sum()
        )

        producao_relatorio = (
            df_filtrado["producao"].sum()
        )

        if not df_filtrado.empty:

            consumo_especifico_relatorio = (
                df_filtrado[
                    "Consumo Específico"
                ].mean()
            )

            eficiencia_relatorio = (
                df_filtrado[
                    "Índice de Eficiência"
                ].mean()
            )

        else:

            consumo_especifico_relatorio = 0
            eficiencia_relatorio = 0


        st.write("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "⚡ Consumo Total",
                f"{consumo_relatorio:,.0f} kWh"
                .replace(",", ".")
            )

        with col2:

            st.metric(
                "🏭 Produção Total",
                f"{producao_relatorio:,.0f} m³"
                .replace(",", ".")
            )

        with col3:

            st.metric(
                "📊 Consumo Específico Médio",
                (
                    f"{consumo_especifico_relatorio:.2f}"
                    .replace(".", ",")
                    + " kWh/m³"
                )
            )

        with col4:

            st.metric(
                "📈 Índice Médio de Eficiência",
                (
                    f"{eficiencia_relatorio:.1f}"
                    .replace(".", ",")
                    + " pontos"
                )
            )


        # =====================================================
        # TABELA DO RELATÓRIO
        # =====================================================

        st.write("")
        st.markdown("### Dados do Relatório")

        tabela_relatorio = df_filtrado[
            [
                "unidade",
                "Período",
                "consumo",
                "producao",
                "area",
                "usuarios",
                "Consumo Específico",
                "Índice de Eficiência"
            ]
        ].copy()

        tabela_relatorio.columns = [
            "Unidade",
            "Período",
            "Consumo (kWh)",
            "Produção (m³)",
            "Área (m²)",
            "Usuários",
            "Consumo Específico (kWh/m³)",
            "Índice de Eficiência"
        ]

        tabela_relatorio[
            "Consumo Específico (kWh/m³)"
        ] = tabela_relatorio[
            "Consumo Específico (kWh/m³)"
        ].round(2)

        tabela_relatorio[
            "Índice de Eficiência"
        ] = tabela_relatorio[
            "Índice de Eficiência"
        ].round(1)

        st.dataframe(
            tabela_relatorio,
            use_container_width=True,
            hide_index=True
        )


        # =====================================================
        # EXPORTAÇÃO
        # =====================================================

        st.write("")
        st.markdown("### Exportar Relatório")

        csv_relatorio = tabela_relatorio.to_csv(
            index=False,
            sep=";",
            decimal=","
        ).encode("utf-8-sig")

        st.download_button(
            label="📥 Baixar relatório em CSV",
            data=csv_relatorio,
            file_name="relatorio_energetico.csv",
            mime="text/csv"
        )



elif pagina == "⚙️  Configurações":

    # =========================================================
    # CABEÇALHO
    # =========================================================

    st.markdown("""
        <h1 style="color:#0B2D45; margin-bottom:5px;">
            Configurações
        </h1>
        <p style="color:#607D94; margin-top:0; margin-bottom:30px;">
            Gerencie os dados utilizados pela plataforma.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h2 style="color:#0B2D45; margin-bottom:5px;">
            Gestão de Dados
        </h2>
        <p style="color:#607D94; margin-top:0;">
            Cadastre informações energéticas das unidades operacionais.
        </p>
    """, unsafe_allow_html=True)


    # =========================================================
    # FORMULÁRIO DE CADASTRO
    # =========================================================

    with st.form("form_dados_energia"):

        st.markdown("### 📋 Cadastro de dados da unidade")

        col1, col2, col3 = st.columns(3)

        with col1:
            unidade = st.selectbox(
                "Unidade",
                [
                    "Plataforma A",
                    "Plataforma B",
                    "Terminal C",
                    "Refinaria D",
                    "Base E"
                ]
            )

        with col2:
            mes = st.selectbox(
                "Mês",
                list(range(1, 13)),
                format_func=lambda x: [
                    "Janeiro", "Fevereiro", "Março", "Abril",
                    "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro"
                ][x - 1]
            )

        with col3:
            ano = st.number_input(
                "Ano",
                min_value=2020,
                max_value=2100,
                value=2026,
                step=1
            )


        st.markdown("#### Dados operacionais")

        col1, col2 = st.columns(2)

        with col1:
            consumo = st.number_input(
                "Consumo de energia (kWh)",
                min_value=0.0,
                step=100.0
            )

            area = st.number_input(
                "Área da instalação (m²)",
                min_value=0.0,
                step=100.0
            )

        with col2:
            producao = st.number_input(
                "Produção (m³)",
                min_value=0.0,
                step=100.0
            )

            usuarios = st.number_input(
                "Número de usuários",
                min_value=0,
                step=1
            )


        # Cálculo apenas para visualização
        if producao > 0:
            consumo_especifico_preview = consumo / producao

            st.info(
                f"Consumo específico calculado: "
                f"{consumo_especifico_preview:.2f} kWh/m³"
            )


        st.markdown("#### Consumo por equipamento")

        col1, col2, col3 = st.columns(3)

        with col1:
            compressores = st.number_input(
                "Compressores (kWh)",
                min_value=0.0
            )

            bombas = st.number_input(
                "Bombas (kWh)",
                min_value=0.0
            )

        with col2:
            refrigeracao = st.number_input(
                "Refrigeração (kWh)",
                min_value=0.0
            )

            iluminacao = st.number_input(
                "Iluminação (kWh)",
                min_value=0.0
            )

        with col3:
            outros = st.number_input(
                "Outros equipamentos (kWh)",
                min_value=0.0
            )


        salvar = st.form_submit_button(
            "💾 Salvar dados",
            use_container_width=True
        )


    # =========================================================
    # SALVAR NO BANCO
    # =========================================================

    if salvar:

        if consumo <= 0 or producao <= 0:

            st.error(
                "Informe valores maiores que zero para consumo e produção."
            )

        else:

            conexao = conectar_banco()
            cursor = conexao.cursor()

            # Verifica se já existe registro da unidade no mesmo período
            cursor.execute("""
                SELECT id
                FROM dados_energia
                WHERE unidade = ?
                AND mes = ?
                AND ano = ?
            """, (
                unidade,
                mes,
                ano
            ))

            registro_existente = cursor.fetchone()

            if registro_existente:

                conexao.close()

                st.warning(
                    f"Já existem dados cadastrados para "
                    f"{unidade} neste período. "
                    f"O registro não foi duplicado."
                )

            else:

                cursor.execute("""
                    INSERT INTO dados_energia (
                        unidade,
                        mes,
                        ano,
                        consumo,
                        producao,
                        area,
                        usuarios,
                        compressores,
                        bombas,
                        refrigeracao,
                        iluminacao,
                        outros,
                        data_cadastro
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    unidade,
                    mes,
                    ano,
                    consumo,
                    producao,
                    area,
                    usuarios,
                    compressores,
                    bombas,
                    refrigeracao,
                    iluminacao,
                    outros,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                conexao.commit()
                conexao.close()

                consumo_especifico = consumo / producao

                st.success(
                    f"Dados de {unidade} salvos com sucesso! "
                    f"Consumo específico: "
                    f"{consumo_especifico:.2f} kWh/m³"
                )
    # =========================================================
    # REGISTROS CADASTRADOS
    # =========================================================

    st.markdown("""
        <div style="margin-top:35px;">
            <h2 style="color:#0B2D45; margin-bottom:5px;">
                Dados cadastrados
            </h2>
            <p style="color:#607D94; margin-top:0;">
                Consulte os registros armazenados na plataforma.
            </p>
        </div>
    """, unsafe_allow_html=True)

    conexao = conectar_banco()

    df_registros = pd.read_sql_query("""
        SELECT
            id,
            unidade,
            mes,
            ano,
            consumo,
            producao,
            area,
            usuarios,
            compressores,
            bombas,
            refrigeracao,
            iluminacao,
            outros
        FROM dados_energia
        ORDER BY ano DESC, mes DESC, unidade
    """, conexao)

    conexao.close()

    if df_registros.empty:

        st.info("Nenhum dado cadastrado.")

    else:

        # Calcula o consumo específico automaticamente
        df_registros["consumo_especifico"] = (
            df_registros["consumo"] /
            df_registros["producao"]
        ).round(2)

        nomes_meses = {
            1: "Jan",
            2: "Fev",
            3: "Mar",
            4: "Abr",
            5: "Mai",
            6: "Jun",
            7: "Jul",
            8: "Ago",
            9: "Set",
            10: "Out",
            11: "Nov",
            12: "Dez"
        }

        df_registros["Período"] = (
            df_registros["mes"].map(nomes_meses)
            + "/"
            + df_registros["ano"].astype(str)
        )

        tabela = df_registros[
            [
                "unidade",
                "Período",
                "consumo",
                "producao",
                "consumo_especifico"
            ]
        ].copy()

        tabela.columns = [
            "Unidade",
            "Período",
            "Consumo (kWh)",
            "Produção (m³)",
            "Consumo específico (kWh/m³)"
        ]

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )
        # =========================================================
    # GERENCIAR REGISTROS
    # =========================================================

    if not df_registros.empty:

        st.markdown("""
            <div style="margin-top:35px;">
                <h2 style="color:#0B2D45; margin-bottom:5px;">
                    Gerenciar registros
                </h2>
                <p style="color:#607D94; margin-top:0;">
                    Edite ou exclua informações já cadastradas.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Cria uma identificação amigável para cada registro
        df_registros["registro_nome"] = (
            df_registros["unidade"]
            + " — "
            + df_registros["mes"].map(nomes_meses)
            + "/"
            + df_registros["ano"].astype(str)
        )

        registro_selecionado = st.selectbox(
            "Selecione o registro",
            df_registros["registro_nome"].tolist(),
            key="registro_gerenciar"
        )

        registro = df_registros[
            df_registros["registro_nome"] == registro_selecionado
        ].iloc[0]

        id_registro = int(registro["id"])


        # =====================================================
        # FORMULÁRIO DE EDIÇÃO
        # =====================================================

        with st.expander("✏️ Editar registro"):

            with st.form("form_editar_registro"):

                st.markdown(
                    f"### {registro['unidade']} — "
                    f"{nomes_meses[registro['mes']]}/{registro['ano']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    novo_consumo = st.number_input(
                        "Consumo de energia (kWh)",
                        min_value=0.0,
                        value=float(registro["consumo"]),
                        step=100.0,
                        key="editar_consumo"
                    )

                    nova_area = st.number_input(
                        "Área da instalação (m²)",
                        min_value=0.0,
                        value=float(registro["area"]),
                        step=100.0,
                        key="editar_area"
                    )

                with col2:

                    nova_producao = st.number_input(
                        "Produção (m³)",
                        min_value=0.0,
                        value=float(registro["producao"]),
                        step=100.0,
                        key="editar_producao"
                    )

                    novos_usuarios = st.number_input(
                        "Número de usuários",
                        min_value=0,
                        value=int(registro["usuarios"]),
                        step=1,
                        key="editar_usuarios"
                    )


                st.markdown("#### Consumo por equipamento")

                col1, col2, col3 = st.columns(3)

                with col1:

                    novos_compressores = st.number_input(
                        "Compressores (kWh)",
                        min_value=0.0,
                        value=float(registro["compressores"]),
                        key="editar_compressores"
                    )

                    novas_bombas = st.number_input(
                        "Bombas (kWh)",
                        min_value=0.0,
                        value=float(registro["bombas"]),
                        key="editar_bombas"
                    )

                with col2:

                    nova_refrigeracao = st.number_input(
                        "Refrigeração (kWh)",
                        min_value=0.0,
                        value=float(registro["refrigeracao"]),
                        key="editar_refrigeracao"
                    )

                    nova_iluminacao = st.number_input(
                        "Iluminação (kWh)",
                        min_value=0.0,
                        value=float(registro["iluminacao"]),
                        key="editar_iluminacao"
                    )

                with col3:

                    novos_outros = st.number_input(
                        "Outros equipamentos (kWh)",
                        min_value=0.0,
                        value=float(registro["outros"]),
                        key="editar_outros"
                    )


                if nova_producao > 0:

                    novo_consumo_especifico = (
                        novo_consumo / nova_producao
                    )

                    st.info(
                        f"Novo consumo específico: "
                        f"{novo_consumo_especifico:.2f} kWh/m³"
                    )


                atualizar = st.form_submit_button(
                    "💾 Salvar alterações",
                    use_container_width=True
                )


            if atualizar:

                if novo_consumo <= 0 or nova_producao <= 0:

                    st.error(
                        "Consumo e produção devem ser maiores que zero."
                    )

                else:

                    conexao = conectar_banco()
                    cursor = conexao.cursor()

                    cursor.execute("""
                        UPDATE dados_energia
                        SET
                            consumo = ?,
                            producao = ?,
                            area = ?,
                            usuarios = ?,
                            compressores = ?,
                            bombas = ?,
                            refrigeracao = ?,
                            iluminacao = ?,
                            outros = ?
                        WHERE id = ?
                    """, (
                        novo_consumo,
                        nova_producao,
                        nova_area,
                        novos_usuarios,
                        novos_compressores,
                        novas_bombas,
                        nova_refrigeracao,
                        nova_iluminacao,
                        novos_outros,
                        id_registro
                    ))

                    conexao.commit()
                    conexao.close()

                    st.success(
                        "Registro atualizado com sucesso!"
                    )

                    st.rerun()


        # =====================================================
        # EXCLUIR REGISTRO
        # =====================================================

        with st.expander("🗑️ Excluir registro"):

            st.warning(
                f"Você está prestes a excluir os dados de "
                f"{registro['unidade']} — "
                f"{nomes_meses[registro['mes']]}/{registro['ano']}."
            )

            confirmar_exclusao = st.checkbox(
                "Confirmo que desejo excluir este registro.",
                key="confirmar_exclusao"
            )

            if st.button(
                "🗑️ Excluir definitivamente",
                type="primary",
                disabled=not confirmar_exclusao
            ):

                conexao = conectar_banco()
                cursor = conexao.cursor()

                cursor.execute(
                    "DELETE FROM dados_energia WHERE id = ?",
                    (id_registro,)
                )

                conexao.commit()
                conexao.close()

                st.success(
                    "Registro excluído com sucesso!"
                )

                st.rerun()
    # =========================================================
    # IMPORTAÇÃO DE PLANILHA
    # =========================================================

    st.markdown("""
        <div style="margin-top:40px;">
            <h2 style="color:#0B2D45; margin-bottom:5px;">
                Importar dados
            </h2>
            <p style="color:#607D94; margin-top:0;">
                Importe vários registros de uma única vez utilizando uma planilha.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================================================
    # MODELO DE PLANILHA
    # =========================================================

    modelo_planilha = pd.DataFrame({
        "unidade": ["Plataforma A"],
        "mes": [10],
        "ano": [2026],
        "consumo": [28000],
        "producao": [7300],
        "area": [4800],
        "usuarios": [120],
        "compressores": [9000],
        "bombas": [6000],
        "refrigeracao": [5000],
        "iluminacao": [2000],
        "outros": [6000]
    })

    arquivo_modelo = BytesIO()

    with pd.ExcelWriter(
        arquivo_modelo,
        engine="openpyxl"
    ) as writer:

        modelo_planilha.to_excel(
            writer,
            index=False,
            sheet_name="Dados Energéticos"
        )

    arquivo_modelo.seek(0)

    st.download_button(
        label="📥 Baixar modelo de planilha",
        data=arquivo_modelo,
        file_name="modelo_dados_energeticos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.caption(
        "Utilize este modelo para garantir que os dados estejam "
        "no formato correto para importação."
    )



    arquivo_importado = st.file_uploader(
        "Selecione uma planilha",
        type=["xlsx", "csv"],
        help="Formatos aceitos: Excel (.xlsx) ou CSV (.csv)"
    )

    if arquivo_importado is not None:

        try:

            # Identifica o tipo do arquivo
            if arquivo_importado.name.endswith(".csv"):

                df_importacao = pd.read_csv(
                    arquivo_importado
                )

            else:

                df_importacao = pd.read_excel(
                    arquivo_importado
                )

            st.success(
                "Arquivo carregado com sucesso!"
            )

            st.markdown("#### Pré-visualização")

            st.dataframe(
                df_importacao,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"{len(df_importacao)} registro(s) encontrado(s) na planilha."
            )

            # =====================================================
            # VALIDAÇÃO DA PLANILHA
            # =====================================================

            colunas_obrigatorias = [
                "unidade",
                "mes",
                "ano",
                "consumo",
                "producao",
                "area",
                "usuarios",
                "compressores",
                "bombas",
                "refrigeracao",
                "iluminacao",
                "outros"
            ]

            colunas_faltando = [
                coluna
                for coluna in colunas_obrigatorias
                if coluna not in df_importacao.columns
            ]

            if colunas_faltando:

                st.error(
                    "❌ A planilha não possui todas as colunas obrigatórias."
                )

                st.write(
                    "Colunas ausentes:",
                    ", ".join(colunas_faltando)
                )

            else:

                registros_validos = []
                registros_invalidos = []

                for indice, linha in df_importacao.iterrows():

                    erros = []

                    # ---------------------------------------------
                    # Unidade
                    # ---------------------------------------------

                    if pd.isna(linha["unidade"]) or str(linha["unidade"]).strip() == "":
                        erros.append("Unidade não informada")

                    # ---------------------------------------------
                    # Mês
                    # ---------------------------------------------

                    try:
                        mes_linha = int(linha["mes"])

                        if mes_linha < 1 or mes_linha > 12:
                            erros.append("Mês deve estar entre 1 e 12")

                    except:
                        erros.append("Mês inválido")

                    # ---------------------------------------------
                    # Ano
                    # ---------------------------------------------

                    try:
                        ano_linha = int(linha["ano"])

                        if ano_linha < 2000:
                            erros.append("Ano inválido")

                    except:
                        erros.append("Ano inválido")

                    # ---------------------------------------------
                    # Consumo e produção
                    # ---------------------------------------------

                    try:
                        consumo_linha = float(linha["consumo"])

                        if consumo_linha <= 0:
                            erros.append(
                                "Consumo deve ser maior que zero"
                            )

                    except:
                        erros.append("Consumo inválido")
                        consumo_linha = 0

                    try:
                        producao_linha = float(linha["producao"])

                        if producao_linha <= 0:
                            erros.append(
                                "Produção deve ser maior que zero"
                            )

                    except:
                        erros.append("Produção inválida")
                        producao_linha = 0

                    # ---------------------------------------------
                    # Valores que não podem ser negativos
                    # ---------------------------------------------

                    campos_nao_negativos = [
                        "area",
                        "usuarios",
                        "compressores",
                        "bombas",
                        "refrigeracao",
                        "iluminacao",
                        "outros"
                    ]

                    for campo in campos_nao_negativos:

                        try:

                            if float(linha[campo]) < 0:
                                erros.append(
                                    f"{campo.capitalize()} não pode ser negativo"
                                )

                        except:
                            erros.append(
                                f"{campo.capitalize()} inválido"
                            )

                    # ---------------------------------------------
                    # Soma dos equipamentos
                    # ---------------------------------------------

                    try:

                        total_equipamentos = (
                            float(linha["compressores"])
                            + float(linha["bombas"])
                            + float(linha["refrigeracao"])
                            + float(linha["iluminacao"])
                            + float(linha["outros"])
                        )

                        diferenca = abs(
                            consumo_linha - total_equipamentos
                        )

                        if diferenca > 0.01:

                            erros.append(
                                f"Soma dos equipamentos difere "
                                f"do consumo total em "
                                f"{diferenca:.2f} kWh"
                            )

                    except:
                        erros.append(
                            "Não foi possível validar os equipamentos"
                        )

                    # ---------------------------------------------
                    # Resultado da linha
                    # ---------------------------------------------

                    if erros:

                        registros_invalidos.append({
                            "Linha": indice + 2,
                            "Unidade": linha["unidade"],
                            "Problemas": " | ".join(erros)
                        })

                    else:

                        registros_validos.append(indice)


                # =================================================
                # RESUMO DA VALIDAÇÃO
                # =================================================

                st.markdown("### 🔎 Resultado da validação")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Registros encontrados",
                        len(df_importacao)
                    )

                with col2:
                    st.metric(
                        "Registros válidos",
                        len(registros_validos)
                    )

                with col3:
                    st.metric(
                        "Com inconsistências",
                        len(registros_invalidos)
                    )


                if len(registros_invalidos) == 0:

                    st.success(
                        "✅ Todos os registros passaram pela validação."
                    )
                                        # =============================================
                    # IMPORTAR REGISTROS PARA O BANCO
                    # =============================================

                    if st.button(
                        "💾 Importar dados para a plataforma",
                        use_container_width=True,
                        type="primary"
                    ):

                        conexao = conectar_banco()
                        cursor = conexao.cursor()

                        importados = 0
                        duplicados = 0

                        for indice in registros_validos:

                            linha = df_importacao.loc[indice]

                            unidade_importada = str(
                                linha["unidade"]
                            ).strip()

                            mes_importado = int(linha["mes"])
                            ano_importado = int(linha["ano"])

                            # Verifica se o período já existe
                            cursor.execute("""
                                SELECT id
                                FROM dados_energia
                                WHERE unidade = ?
                                AND mes = ?
                                AND ano = ?
                            """, (
                                unidade_importada,
                                mes_importado,
                                ano_importado
                            ))

                            registro_existente = cursor.fetchone()

                            if registro_existente:

                                duplicados += 1
                                continue

                            # Insere no banco
                            cursor.execute("""
                                INSERT INTO dados_energia (
                                    unidade,
                                    mes,
                                    ano,
                                    consumo,
                                    producao,
                                    area,
                                    usuarios,
                                    compressores,
                                    bombas,
                                    refrigeracao,
                                    iluminacao,
                                    outros
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                unidade_importada,
                                mes_importado,
                                ano_importado,
                                float(linha["consumo"]),
                                float(linha["producao"]),
                                float(linha["area"]),
                                int(linha["usuarios"]),
                                float(linha["compressores"]),
                                float(linha["bombas"]),
                                float(linha["refrigeracao"]),
                                float(linha["iluminacao"]),
                                float(linha["outros"])
                            ))

                            importados += 1

                        conexao.commit()
                        conexao.close()

                        if importados > 0:

                            st.success(
                                f"✅ {importados} registro(s) "
                                f"importado(s) com sucesso!"
                            )

                        if duplicados > 0:

                            st.warning(
                                f"⚠️ {duplicados} registro(s) já existiam "
                                f"na plataforma e não foram duplicados."
                            )

                        if importados == 0 and duplicados > 0:

                            st.info(
                                "Nenhum novo registro foi importado."
                            )                
                else:

                    st.warning(
                        "⚠️ Alguns registros possuem inconsistências "
                        "e precisam ser corrigidos antes da importação."
                    )

                    df_erros = pd.DataFrame(
                        registros_invalidos
                    )

                    st.dataframe(
                        df_erros,
                        use_container_width=True,
                        hide_index=True
                    )

        except Exception as erro:

            st.error(
                f"Não foi possível ler o arquivo: {erro}"
            )