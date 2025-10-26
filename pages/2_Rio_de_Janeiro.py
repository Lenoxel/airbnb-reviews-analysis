import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Reviews de hospedagens no Rio de Janeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

df_columns = ["listing_id", "name", "neighbourhood", "review_feeling", "date"]


@st.cache_data
def load_reviews_rio():
    return pd.read_parquet("data/airbnb-reviews-rio-merged.parquet", columns=df_columns)


df_reviews_rio = load_reviews_rio()

df_reviews_rio["date"] = pd.to_datetime(df_reviews_rio["date"])

st.title("Reviews de hospedagens no Rio de Janeiro")

min_year = df_reviews_rio["date"].dt.year.min()
max_year = df_reviews_rio["date"].dt.year.max()

[min_year_selected, max_year_selected] = st.slider(
    "Selecione o intervalo de anos para análise",
    min_value=min_year,
    max_value=max_year,
    value=(max_year - 5, max_year),
    step=1,
)

df_reviews_rio = df_reviews_rio[
    (df_reviews_rio["date"].dt.year >= min_year_selected)
    & (df_reviews_rio["date"].dt.year <= max_year_selected)
].copy()

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
    value=df_reviews_rio_aggregated["total"].quantile(0.99).astype(int),
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
    color_continuous_scale="Blues",
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
        font_size=16, font_family="Arial", font_color="black", bgcolor="white"
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

st.subheader("📊 Análise Temporal de Reviews")

listing_names = st.multiselect("Selecione as hospedagens", ranking["name"].tolist())

df_listing = df_reviews_rio[df_reviews_rio["name"].isin(listing_names)].copy()

df_listing["month_year"] = df_listing["date"].dt.to_period("M").dt.to_timestamp()

df_time_analysis = (
    df_listing.groupby(["month_year", "review_feeling", "name"])
    .agg(total=("review_feeling", "count"))
    .reset_index()
)

if len(listing_names) == 0:
    st.info("Selecione pelo menos uma hospedagem para visualizar a análise temporal.")
    st.stop()

if len(listing_names) == 1:
    fig2 = px.line(
        df_time_analysis,
        x="month_year",
        y="total",
        color="review_feeling",
        title=f"Análise Temporal de Reviews",
        custom_data=["review_feeling"],
        line_shape="spline",
        markers=True,
        color_discrete_map={
            "Positive": "#1f77b4",
            "Negative": "#d62728",
            "Neutral": "#7f7f7f",
        },
    )

    fig2.update_traces(
        hovertemplate="<b>%{x|%b %Y}</b><br>"
        + "Sentimento: %{customdata[0]}<br>"
        + "Total de Reviews: %{y}<extra></extra>",
        hoverlabel=dict(
            font_size=16, font_family="Arial", font_color="black", bgcolor="white"
        ),
    )

    fig2.update_layout(
        xaxis_title="Mês e Ano",
        yaxis_title="Total de Reviews",
        title_font=dict(size=22),
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    st.plotly_chart(fig2, use_container_width=True)
else:
    df_listing_positive = df_listing[df_listing["review_feeling"] == "Positive"].copy()

    df_time_analysis_positive = (
        df_listing_positive.groupby(["month_year", "review_feeling", "name"])
        .agg(total=("review_feeling", "count"))
        .reset_index()
    )

    fig2 = px.line(
        df_time_analysis_positive,
        x="month_year",
        y="total",
        color="name",
        title=f"Análise Temporal Comparativa de Reviews Positivos",
        custom_data=["name", "review_feeling"],
        line_shape="spline",
        markers=False,
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )

    fig2.update_traces(
        hovertemplate="<b>%{x|%b %Y}</b><br>"
        + "Hospedagem: %{customdata[0]}<br>"
        + "Total de Reviews Positivos: %{y}<extra></extra>",
        hoverlabel=dict(
            font_size=16, font_family="Arial", font_color="black", bgcolor="white"
        ),
    )

    fig2.update_layout(
        xaxis_title="Mês e Ano",
        yaxis_title="Total de Reviews Positivos",
        title_font=dict(size=22),
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(t=50, b=50, l=50, r=50),
    )

    st.plotly_chart(fig2, use_container_width=True)
