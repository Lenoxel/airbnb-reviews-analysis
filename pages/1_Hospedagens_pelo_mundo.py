import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Hospedagens pelo mundo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    return pd.read_csv("data/airbnb-listings-cleaned.csv")


def plot_reviews_per_month(df):
    st.subheader("📊 Reviews das Hospedagens por Cidade")

    room_types = ["Todos"] + sorted(df["room_type"].unique().tolist())

    selected_room_type = st.selectbox("Selecione o tipo de hospedagem", room_types)

    if selected_room_type != "Todos":
        summary = (
            df.groupby(["city", "room_type"])
            .agg(
                total=("name", "count"),
                reviews_per_month_count=("reviews_per_month", "mean"),
            )
            .reset_index()
        )

        plot_data = summary[summary["room_type"] == selected_room_type]
    else:
        plot_data = (
            df.groupby("city")
            .agg(
                total=("name", "count"),
                reviews_per_month_count=("reviews_per_month", "mean"),
            )
            .reset_index()
        )

    fig = px.bar(
        plot_data,
        x="city",
        y="reviews_per_month_count",
        color="reviews_per_month_count",
        color_continuous_scale="Blues",
        text="reviews_per_month_count",
        title=f"Média de Reviews por Mês ({selected_room_type})",
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Média Reviews por Mês: %{y:.2f}<extra></extra>",
        texttemplate="%{text:.2f}",
        textfont_size=18,
        textposition="auto",
        hoverlabel=dict(
            font_size=16, font_family="Arial", font_color="black", bgcolor="white"
        ),
    )

    fig.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Média de Reviews por Mês",
        showlegend=False,
        title_font=dict(size=22),
        title_font_size=22,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        margin=dict(t=50, b=50, l=50, r=50),
        coloraxis_colorbar=dict(title="Média Reviews por Mês"),
    )

    st.plotly_chart(fig, use_container_width=True)


# def plot_reviews_vs_price(df):
#     st.subheader("💲 Relação entre Preço e Avaliações")

#     df = df[df["price"] <= 500]
#     df["reviews_percentage"] = (
#         df["number_of_reviews"] / df["number_of_reviews"].max()
#     ) * 100

#     price_bins = pd.cut(df["price"], bins=30)
#     avg_reviews = df.groupby(price_bins)["reviews_percentage"].mean().reset_index()

#     avg_reviews["price_left"] = avg_reviews["price"].apply(lambda x: x.left)
#     avg_reviews["price_right"] = avg_reviews["price"].apply(lambda x: x.right)

#     avg_reviews["price_range"] = [
#         f"${int(b.left)}–{int(b.right)}" for b in avg_reviews["price"]
#     ]

#     min_price, max_price = st.slider(
#         "Selecione faixa de preço",
#         min_value=0,
#         max_value=500,
#         value=(0, 500),
#         step=10,
#     )

#     avg_reviews["price_left"] = pd.to_numeric(
#         avg_reviews["price_left"], errors="coerce"
#     )
#     avg_reviews["price_right"] = pd.to_numeric(
#         avg_reviews["price_right"], errors="coerce"
#     )

#     filtered_data = avg_reviews[
#         (avg_reviews["price_left"] >= min_price)
#         & (avg_reviews["price_right"] <= max_price)
#     ]

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=filtered_data["price_range"],
#             y=filtered_data["reviews_percentage"],
#             mode="lines+markers",
#             marker=dict(size=8, color="blue"),
#             line=dict(color="royalblue"),
#             hovertemplate="<b>Faixa:</b> %{x}<br>Média Reviews: %{y:.2f}%<extra></extra>",
#         )
#     )
#     fig.update_layout(
#         title="Média de avaliações (%) por faixa de preço",
#         xaxis=dict(title="Faixa de preço (USD)", tickangle=45),
#         yaxis=dict(title="Média de Reviews (%)", range=[0, 100]),
#     )
#     st.plotly_chart(fig, use_container_width=True)


def plot_room_type_distribution(df):
    st.subheader("🏨 Distribuição dos Tipos de Quarto")

    cities = ["Todas"] + sorted(df["city"].unique())
    selected_city = st.selectbox("Selecione a cidade", cities)

    filtered_df = df if selected_city == "Todas" else df[df["city"] == selected_city]

    room_type_counts = filtered_df["room_type"].value_counts().reset_index()
    room_type_counts.columns = ["room_type", "count"]

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            room_type_counts,
            x="room_type",
            y="count",
            text="count",
            color="room_type",
            title="Hospedagens por tipo de quarto",
            text_auto=True,
        )

        fig_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<extra></extra>",
            textfont_size=18,
            textposition="auto",
            hoverlabel=dict(
                font_size=16, font_family="Arial", font_color="black", bgcolor="white"
            ),
        )

        fig_bar.update_layout(
            xaxis_title="Tipo de Quarto",
            yaxis_title="Quantidade de Hospedagens",
            showlegend=False,
            title_font=dict(size=22),
            title_font_size=22,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis_tickfont_size=16,
            yaxis_tickfont_size=16,
            margin=dict(t=50, b=50, l=50, r=50),
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(
            room_type_counts,
            names="room_type",
            values="count",
            title="Proporção dos tipos de quarto",
            hole=0.4,
        )

        fig_pie.update_traces(
            hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<extra></extra>",
            textposition="auto",
            textinfo="percent+label",
            textfont_size=16,
        )

        fig_pie.update_layout(
            title_font=dict(size=22),
            title_font_size=22,
            margin=dict(t=50, b=50, l=50, r=50),
        )

        st.plotly_chart(fig_pie, use_container_width=True)


st.title("🌍 Hospedagens pelo mundo")

listings_df = load_data()

listings_df["date"] = pd.to_datetime(
    listings_df["last_review"].replace("Nunca Avaliado", pd.NaT), errors="coerce"
)

valid_dates_df = listings_df.dropna(subset=["date"])

min_date = valid_dates_df["date"].min().date()
max_date = valid_dates_df["date"].max().date()

[min_year_selected, max_year_selected] = st.slider(
    "Selecione o intervalo de anos para análise",
    min_value=min_date.year,
    max_value=max_date.year,
    value=(max_date.year - 5, max_date.year),
    step=1,
)

listings_df_filtered = listings_df[
    (listings_df["date"].dt.year >= min_year_selected)
    & (listings_df["date"].dt.year <= max_year_selected)
].copy()


plot_room_type_distribution(listings_df_filtered)
# plot_reviews_vs_price(listings_df_filtered)
plot_reviews_per_month(listings_df_filtered)
