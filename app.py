import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/airbnb-listings-cleaned.csv")

st.title("Dashboard Airbnb - Análise de Reviews")
st.write("""
Dashboard desenvolvido para a Atividade 3 da disciplina de Análise de Dados.  
Entrega prevista até 30/08/2025.  

**Participantes do grupo:**  
- Bruno Venceslau Barbosa (bvb@cesar.school)
- Carolina Queiroz de Sousa (cqs@cesar.school)
- Gabriel Lenon Barros da Silva (glbs@cesar.school)
- Karina Meireles Varela (kmv@cesar.school) 
- João Henrique Ayres Pereira (jhap@cesar.school)
""")

# --- Início do gráfico de percentual de reviews ---

# Título/legenda do gráfico
st.subheader("📊 Percentual de Hospedagens com Review por Cidade")

resumo_tipo = df.groupby(['city', 'room_type']).agg(
    total_listings=('name', 'count'),
    com_review=('number_of_reviews', lambda x: (x > 0).sum())
).reset_index()

resumo_tipo['percentual_review'] = (
    resumo_tipo['com_review'] / resumo_tipo['total_listings']
) * 100

resumo_geral = df.groupby("city").agg(
        total_listings=('name', 'count'),
        com_review=('number_of_reviews', lambda x: (x > 0).sum())
).reset_index()

resumo_geral['percentual_review'] = (
        resumo_geral['com_review'] / resumo_geral['total_listings']
) * 100

opcoes = ["Todos"] + resumo_tipo["room_type"].unique().tolist()

data_plot = resumo_geral

fig = px.bar(
    data_plot,
    x="city",
    y="percentual_review",
    text="percentual_review",
    color_discrete_sequence=["skyblue"],
)

fig.update_traces(
    textfont_size=12,
    texttemplate="%{text:.1f}%",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Percentual: %{y:.1f}%<extra></extra>",
)

fig.update_layout(
    plot_bgcolor="#f0f4f8",  
    paper_bgcolor="#f0f4f8",  
    font_color="black",   
    yaxis=dict(
        title=dict(text="Percentual (%)", font=dict(color="black")),
        tickfont=dict(color="black"),
        range=[0, 100],
    ),
    xaxis=dict(
        title=dict(text="Cidade", font=dict(color="black")),
        tickfont=dict(color="black")
    ),
    bargap=0.3,
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label=tipo,
                    method="update",
                    args=[
                        {"y": [ 
                            (resumo_tipo[resumo_tipo["room_type"] == tipo]["percentual_review"]
                             if tipo != "Todos" 
                             else resumo_geral["percentual_review"])
                        ]}
                    ]
                )
                for tipo in opcoes
            ],
            direction="down",
            showactive=True,
            x=0.0,
            y=1.15
        )
    ],
    margin=dict(l=60, r=60, t=80, b=60) 
)

st.plotly_chart(fig, use_container_width=True)

# --- Fim do gráfico de percentual de reviews ---


# --- gráfico do percentual da média de avaliações  por faixa de preço:

import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Criar coluna percentual de reviews
df["reviews_percent"] = (df["number_of_reviews"] / df["number_of_reviews"].max()) * 100

# Filtrar preços até 500
df = df[df["price"] <= 500]

# Criar bins de preço
price_bins = pd.cut(df["price"], bins=30)  # pode ajustar o número de bins
avg_reviews = df.groupby(price_bins)["reviews_percent"].mean().reset_index()

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
    unsafe_allow_html=True
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
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered_data["price_range"],
    y=filtered_data["reviews_percent"],
    mode="markers",
    marker=dict(size=8, color="blue", line=dict(width=1, color="black")),
    name="Média de reviews (%)",
    hovertemplate="<b>Faixa de preço:</b> %{x}<br><b>Média Reviews:</b> %{y:.2f}%<extra></extra>"
))

fig.update_layout(
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
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)


# --- fim gráfico do percentual da média de avaliações  por faixa de preço: