import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Reviews de hospedagens no Rio de Janeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

df_columns = ["listing_id", "name", "neighbourhood", "review_feeling"]


@st.cache_data
def load_reviews_rio():
    return pd.read_parquet("data/airbnb-reviews-rio-merged.parquet", columns=df_columns)


df_reviews_rio = load_reviews_rio()

st.title("Reviews de hospedagens no Rio de Janeiro")

df_reviews_rio_aggregated = (
    df_reviews_rio.groupby(["listing_id", "name", "neighbourhood"])
    .agg(
        total=("review_feeling", "count"),
        positives=("review_feeling", lambda x: (x == "Positive").sum()),
    )
    .reset_index()
)

col1, col2 = st.columns(2)

neighbourhood = col1.multiselect(
    "Selecione o(s) bairro(s)",
    options=df_reviews_rio["neighbourhood"].unique(),
    default=None,
)

min_evaluation_quantity = col2.slider(
    "Escolha a quantidade mínima de avaliações",
    min_value=int(df_reviews_rio_aggregated["total"].min()),
    max_value=int(df_reviews_rio_aggregated["total"].max()),
    value=df_reviews_rio_aggregated["total"].quantile(0.75).astype(int),
    step=1,
)

df_aggregated = df_reviews_rio_aggregated[
    df_reviews_rio_aggregated["total"] >= min_evaluation_quantity
].copy()

if len(neighbourhood):
    df_aggregated = df_aggregated[
        df_aggregated["neighbourhood"].isin(neighbourhood)
    ].copy()

if df_aggregated.empty:
    st.warning(
        "Nenhum resultado encontrado para os filtros selecionados. "
        "Por favor, ajuste os filtros e tente novamente."
    )
    st.stop()

df_aggregated["percentual_positive"] = (
    df_aggregated["positives"] / df_aggregated["total"]
) * 100

quantity_to_show = len(df_aggregated) if len(df_aggregated) < 10 else 10

ranking = df_aggregated.sort_values("percentual_positive", ascending=False).head(
    quantity_to_show if quantity_to_show < 10 else 10
)

fig = px.bar(
    ranking,
    x="name",
    y="percentual_positive",
    title=f"Top {quantity_to_show} hospedagens mais bem avaliadas",
    text=ranking["percentual_positive"].round(1).astype(str) + "%",
    color="percentual_positive",
    color_continuous_scale="YlGn",
    height=700,
)

fig.update_traces(
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>"
    + "Bairro: %{customdata[2]}<br>"
    + "Percentual positivo: %{y:.2f}%<br>"
    + "Total de reviews: %{customdata[0]}<br>"
    + "Positivos: %{customdata[1]}<extra></extra>",
    customdata=ranking[["total", "positives", "neighbourhood"]].values,
    textfont_size=22,
    hoverlabel=dict(
        font_size=16, font_family="Arial", font_color="black", bgcolor="lightyellow"
    ),
)

min_range = float(ranking["percentual_positive"].iloc[-1]) - 1
max_range = 100

fig.update_layout(
    xaxis_title="Lugar",
    xaxis=dict(showgrid=False),
    yaxis_title="Reviews Positivos (%)",
    yaxis=dict(range=[min_range, max_range], showgrid=False),
    coloraxis_colorbar=dict(title="Percentual"),
    title_font=dict(size=22),
    title_font_size=24,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    xaxis_tickfont_size=16,
    yaxis_tickfont_size=16,
    bargap=0.3,
)

st.plotly_chart(fig, use_container_width=True)
