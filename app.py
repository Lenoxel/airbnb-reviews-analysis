import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Airbnb - Ofertas de Hospedagem e Reviews",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_reviews_rio():
    return pd.read_parquet("data/airbnb-reviews-rio-merged.parquet")


df_listings = pd.read_csv("data/airbnb-listings-cleaned.csv")

df_reviews_rio = load_reviews_rio()

st.title("Airbnb - Ofertas de Hospedagem e Reviews")

with st.expander("Sobre o projeto"):
    st.write(
        """
        Dashboard desenvolvido para a Atividade 3 da disciplina de Análise de Dados.
        Entrega prevista até 30/08/2025.

        **Participantes do grupo:**
        - Bruno Venceslau Barbosa (bvb@cesar.school)
        - Carolina Queiroz de Sousa (cqs@cesar.school)
        - Gabriel Lenon Barros da Silva (glbs@cesar.school)
        - Karina Meireles Varela (kmv@cesar.school)
        - João Henrique Ayres Pereira (jhap@cesar.school)
        """
    )

st.markdown(
    """
    Bem-vindo ao dashboard de análise de hospedagens e reviews do Airbnb!

    Este projeto apresenta uma análise detalhada das ofertas de hospedagem e dos comentários dos hóspedes em quatro cidades: **Cape Town**, **Hawaii**, **Rio de Janeiro** e **Bangkok**, utilizando dados reais coletados entre 2010 e 2025.
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    df_reviews_rio_years = pd.to_datetime(
        df_reviews_rio["date"], errors="coerce"
    ).dt.year

    st.metric(
        "Período dos dados",
        f"{df_reviews_rio_years.min()} - {df_reviews_rio_years.max()}",
        border=True,
    )

with col2:
    st.metric("Total de Bairros", df_listings["neighbourhood"].nunique(), border=True)

with col3:
    st.metric(
        "Total de Hospedagens",
        f"{df_listings['name'].nunique():,}".replace(",", "."),
        border=True,
    )


with col4:
    unique_reviews = len(df_reviews_rio)

    st.metric(
        "Total de Reviews (RJ)", f"{unique_reviews:,}".replace(",", "."), border=True
    )

st.markdown(
    """
    ### O que você vai encontrar nos dashboards:

    - **Visão geral das ofertas de hospedagem (listings):**
        - Evolução do número de hospedagens ao longo dos anos.
        - Distribuição por tipo de acomodação, faixa de preço e localização.
        - Comparativo entre as cidades analisadas.

    - **Análise de sentimento dos comentários no Rio de Janeiro (reviews):**
        - Sentimento dos hóspedes sobre as hospedagens do Rio de Janeiro.
        - Tendências e mudanças no sentimento ao longo dos anos.
        - Comparativo entre os bairros analisados.

    ### Sobre os dados

    - **Listings:** Informações detalhadas sobre cada oferta de hospedagem, incluindo tipo, preço, localização e disponibilidade.
    - **Reviews:** Comentários dos hóspedes, analisados por técnicas de processamento de linguagem natural para identificar sentimentos.
    """
)
