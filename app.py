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