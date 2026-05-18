"""Radar chart Plotly: compara el perfil sensorial del vino vs. el ideal."""
import plotly.graph_objects as go
from dash import dcc


CATEGORIES = ["Cuerpo", "Taninos", "Acidez", "Dulzor"]


def build_radar_chart(vino: dict, perfil_ideal: dict = None, height: int = 320):
    """Construye un gráfico radar con el perfil del vino (y opcionalmente el ideal)."""
    valores_vino = [
        vino["cuerpo"],
        vino["taninos"],
        vino["acidez"],
        vino["dulzor"],
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=valores_vino + [valores_vino[0]],
            theta=CATEGORIES + [CATEGORIES[0]],
            fill="toself",
            name=vino["nombre"],
            line=dict(color="#1f2937", width=2),
            fillcolor="rgba(31, 41, 55, 0.18)",
        )
    )

    if perfil_ideal:
        valores_ideal = [
            perfil_ideal.get("cuerpo", 0.5),
            perfil_ideal.get("taninos", 0.5),
            perfil_ideal.get("acidez", 0.5),
            perfil_ideal.get("dulzor", 0.5),
        ]
        fig.add_trace(
            go.Scatterpolar(
                r=valores_ideal + [valores_ideal[0]],
                theta=CATEGORIES + [CATEGORIES[0]],
                fill="toself",
                name="Perfil ideal",
                line=dict(color="#b45309", width=2, dash="dot"),
                fillcolor="rgba(180, 83, 9, 0.10)",
            )
        )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=False,
                gridcolor="#e5e7eb",
                tickfont=dict(size=10, color="#6b7280"),
            ),
            angularaxis=dict(
                gridcolor="#e5e7eb",
                tickfont=dict(size=11, color="#374151"),
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        margin=dict(l=20, r=20, t=10, b=30),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})
