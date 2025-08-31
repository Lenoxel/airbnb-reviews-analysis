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

st.title("Hospedagens pelo mundo")

df_listings = pd.read_csv("data/airbnb-listings-cleaned.csv")

# --- Início do gráfico de percentual de reviews ---

# Título/legenda do gráfico
st.subheader("📊 Percentual de Hospedagens com Review por Cidade")
st.write("Selecione o tipo de Hospedagem:")

resumo_tipo = (
    df_listings.groupby(["city", "room_type"])
    .agg(
        total_listings=("name", "count"),
        com_review=("number_of_reviews", lambda x: (x > 0).sum()),
    )
    .reset_index()
)

resumo_tipo["percentual_review"] = (
    resumo_tipo["com_review"] / resumo_tipo["total_listings"]
) * 100

resumo_geral = (
    df_listings.groupby("city")
    .agg(
        total_listings=("name", "count"),
        com_review=("number_of_reviews", lambda x: (x > 0).sum()),
    )
    .reset_index()
)

resumo_geral["percentual_review"] = (
    resumo_geral["com_review"] / resumo_geral["total_listings"]
) * 100

opcoes = ["Todos"] + resumo_tipo["room_type"].unique().tolist()

data_plot = resumo_geral

fig1 = px.bar(
    data_plot,
    x="city",
    y="percentual_review",
    text="percentual_review",
    color_discrete_sequence=["skyblue"],
)

fig1.update_traces(
    textfont_size=14,
    texttemplate="%{text:.1f}%",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Percentual: %{y:.1f}%<extra></extra>",
)

fig1.update_layout(
    font_color="white",
    yaxis=dict(title=dict(text="Percentual (%)"), range=[0, 100]),
    xaxis=dict(title=dict(text="Cidade")),
    bargap=0.3,
    title_font=dict(size=22),
    title_font_size=24,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    xaxis_tickfont_size=16,
    yaxis_tickfont_size=16,
    hoverlabel=dict(font_size=16, font_family="Arial"),
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label=tipo,
                    method="update",
                    args=[
                        {
                            "y": [
                                (
                                    resumo_tipo[resumo_tipo["room_type"] == tipo][
                                        "percentual_review"
                                    ]
                                    if tipo != "Todos"
                                    else resumo_geral["percentual_review"]
                                )
                            ]
                        }
                    ],
                )
                for tipo in opcoes
            ],
            direction="down",
            showactive=True,
            x=0,
            xanchor="left",
            y=1.25,
            yanchor="top",
            pad={"r": 0, "t": 10, "l": 0},
            bgcolor="black",
            font=dict(color="skyblue", size=14),
            bordercolor="skyblue",
        )
    ],
)

st.plotly_chart(fig1, use_container_width=True)

# --- Fim do gráfico de percentual de reviews ---


# --- gráfico do percentual da média de avaliações  por faixa de preço:

# Criar coluna percentual de reviews
df_listings["reviews_percent"] = (
    df_listings["number_of_reviews"] / df_listings["number_of_reviews"].max()
) * 100

# Filtrar preços até 500
df_listings = df_listings[df_listings["price"] <= 500]

# Criar bins de preço
price_bins = pd.cut(df_listings["price"], bins=30)  # pode ajustar o número de bins
avg_reviews = df_listings.groupby(price_bins)["reviews_percent"].mean().reset_index()

# Labels no formato "$min–max"
avg_reviews["price_range"] = [
    f"${int(b.left)}–{int(b.right)}" for b in avg_reviews["price"]
]

# Criar gráfico de pontos

# --- WIDGET: botões de seleção de faixa ---
st.markdown("### 🔎 Selecione a faixa de preços")

# CSS customizado para estilizar os botões
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: black;
        color: #1E90FF; /* Azul vivo */
        border-radius: 10px;
        border: 1px solid #1E90FF;
        padding: 0.6em 1em;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #1E90FF;
        color: black;
        border: 1px solid black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Lista de opções
price_ranges = avg_reviews["price_range"].unique()

# Dicionário para guardar seleções
selected_ranges = []

cols = st.columns(4)  # divide em 4 colunas (ajuste se quiser)

for i, price in enumerate(price_ranges):
    if cols[i % 4].button(price):
        if price not in selected_ranges:
            selected_ranges.append(price)

# Se nada for escolhido, mostra todas
if not selected_ranges:
    selected_ranges = price_ranges

# --- Filtra os dados ---
filtered_data = avg_reviews[avg_reviews["price_range"].isin(selected_ranges)]

# --- Gráfico ---
fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=filtered_data["price_range"],
        y=filtered_data["reviews_percent"],
        mode="markers",
        marker=dict(size=8, color="blue", line=dict(width=1, color="black")),
        name="Média de reviews (%)",
        hovertemplate="<b>Faixa de preço:</b> %{x}<br><b>Média Reviews:</b> %{y:.2f}%<extra></extra>",
    )
)

fig2.update_layout(
    title="Média de avaliações (%) por faixa de preço",
    title_font=dict(size=22),
    xaxis=dict(
        title="Faixa de preço (USD)",
        tickangle=45,
        title_font=dict(size=18),
        tickfont=dict(size=14),
    ),
    yaxis=dict(
        title="Avaliações (%)",
        tickformat=".1%",
        title_font=dict(size=18),
        tickfont=dict(size=14),
    ),
    font=dict(size=14),
)

st.plotly_chart(fig2, use_container_width=True)


# --- fim gráfico do percentual da média de avaliações  por faixa de preço:

#  Gráfico comparativo de quantidade por tipo de quarto

st.markdown("### 📊 Tipos de quarto que mais são procurados")

cities = df_listings["city"].unique()
selected_city = st.selectbox("Selecione a cidade", ["Todas", *sorted(cities)])

df_listings_filtered_by_city = (
    df_listings[df_listings["city"] == selected_city]
    if selected_city != "Todas"
    else df_listings
)

room_type_counts = (
    df_listings_filtered_by_city["room_type"].value_counts().reset_index()
)
room_type_counts.columns = ["room_type", "count"]

total_listings = room_type_counts["count"].sum()

hotel_room_row = room_type_counts[room_type_counts["room_type"] == "Hotel room"]

if not hotel_room_row.empty:
    hotel_room_percentage = (hotel_room_row["count"].iloc[0] / total_listings) * 100
else:
    hotel_room_percentage = 0

fig3 = px.bar(
    room_type_counts,
    x="room_type",
    y="count",
    color="room_type",
    text="count",
    title="Hospedagens disponíveis por tipo de Quarto",
)

fig3.update_layout(
    xaxis_title="Tipo de Quarto",
    xaxis=dict(showgrid=False),
    yaxis_title="Quantidade",
    yaxis=dict(showgrid=False),
    xaxis_tickangle=-45,
    showlegend=False,
    title_font=dict(size=22),
    title_font_size=24,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    xaxis_tickfont_size=16,
    yaxis_tickfont_size=16,
    hoverlabel=dict(font_size=16, font_family="Arial"),
)

fig3.update_traces(
    textfont_size=22,
    hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<extra></extra>",
)

st.plotly_chart(fig3, use_container_width=True)

# Fim do gráfico comparativo de quantidade port tipo de quarto
