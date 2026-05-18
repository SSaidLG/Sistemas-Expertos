"""
Página 'Cómo funciona': diagrama del pipeline + explicación del motor.
"""
from dash import html, dcc, register_page
import plotly.graph_objects as go

from views.components.navbar import build_navbar


def _diagrama_pipeline():
    """Diagrama del flujo del sistema experto usando un Sankey simplificado."""
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=18,
            thickness=20,
            line=dict(color="#e5e7eb", width=0.5),
            label=[
                "Cuestionario\n(10 variables)",
                "Marcos de vinos",
                "Reglas de sabor",
                "Fusificación",
                "Perfil ideal",
                "Afinidad sensorial",
                "Pertenencia precio",
                "Bonos contextuales",
                "Ranking final",
            ],
            color=[
                "#1f2937", "#1f2937", "#1f2937",
                "#b45309", "#b45309", "#b45309",
                "#b45309", "#b45309", "#0f766e",
            ],
        ),
        link=dict(
            source=[0, 0, 1, 2, 3, 0, 0, 4, 5, 6, 7],
            target=[3, 4, 5, 4, 4, 6, 7, 5, 8, 8, 8],
            value=[2, 2, 2, 2, 1, 2, 2, 1, 3, 2, 1],
            color="rgba(180, 83, 9, 0.18)",
        ),
    ))
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui", size=12, color="#374151"),
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def _funcion_pertenencia():
    """Gráfica de la función de pertenencia del presupuesto."""
    presupuesto = 500
    precios = [i for i in range(50, 700, 10)]
    mu = []
    for p in precios:
        if p <= presupuesto * 0.8:
            mu.append(1.0)
        elif p <= presupuesto:
            mu.append((presupuesto - p) / (presupuesto * 0.2))
        else:
            mu.append(0.0)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=precios, y=mu,
        mode="lines",
        line=dict(color="#b45309", width=3, shape="linear"),
        fill="tozeroy", fillcolor="rgba(180, 83, 9, 0.10)",
        name="μ(precio)",
    ))
    fig.add_vline(x=400, line_dash="dot", line_color="#9ca3af",
                  annotation_text="80% del presupuesto",
                  annotation_position="top left")
    fig.add_vline(x=500, line_dash="dot", line_color="#9ca3af",
                  annotation_text="Presupuesto", annotation_position="top right")
    fig.update_layout(
        height=320,
        xaxis_title="Precio del vino (MXN)",
        yaxis_title="Grado de pertenencia μ",
        yaxis=dict(range=[-0.05, 1.1]),
        margin=dict(l=40, r=20, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui", size=12, color="#374151"),
        showlegend=False,
    )
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def _section(eyebrow, titulo, contenido, extra=None):
    return html.Section(
        className="explain-section",
        children=[
            html.Div(className="section-head", children=[
                html.Span(eyebrow, className="eyebrow"),
                html.H2(titulo, className="section-title"),
            ]),
            html.Div(className="explain-body", children=[
                html.Div(contenido, className="explain-text"),
                html.Div(extra, className="explain-visual") if extra is not None else None,
            ]),
        ],
    )


layout = html.Div(
    className="page",
    children=[
        build_navbar("como_funciona"),
        html.Section(
            className="page-intro",
            children=[
                html.Span("Detrás del sistema experto", className="eyebrow"),
                html.H1("Cómo funciona el motor de inferencia", className="page-title"),
                html.P(
                    "Un recorrido por los tres paradigmas que sustentan las "
                    "recomendaciones: representación por marcos, reglas heurísticas "
                    "y lógica difusa.",
                    className="page-subtitle",
                ),
            ],
        ),
        _section(
            "Paso 1 · Representación",
            "Marcos de conocimiento",
            html.Div([
                html.P("Cada vino se modela como un marco (frame) con slots tipados:"),
                html.Pre(
                    "{\n"
                    "  nombre: 'Casa Madero 3V',\n"
                    "  tipo: 'Tinto',\n"
                    "  uva: 'Blend (C-M-S)',\n"
                    "  precio: 550,\n"
                    "  cuerpo: 0.7,  taninos: 0.7,\n"
                    "  acidez: 0.6, dulzor: 0.1,\n"
                    "  maridajes: ['mole', 'pato', ...]\n"
                    "}",
                    className="code-block",
                ),
                html.P("Estos slots son la materia prima del razonamiento."),
            ]),
        ),
        _section(
            "Paso 2 · Heurística",
            "Reglas de sabor",
            html.Div([
                html.P("La base contiene una matriz que vincula los rasgos del "
                       "platillo con el perfil ideal del vino:"),
                html.Ul(className="rule-list", children=[
                    html.Li("Picante → vino con dulzor alto y bajos taninos"),
                    html.Li("Grasoso → vino con acidez alta y taninos firmes"),
                    html.Li("Pesado → vino con cuerpo y estructura"),
                    html.Li("Ligero → vino fresco y de poca extracción"),
                ]),
            ]),
        ),
        _section(
            "Paso 3 · Inferencia",
            "Lógica difusa",
            html.Div([
                html.P("La función de pertenencia traduce el precio en un grado "
                       "de aceptabilidad. Por debajo del 80% del presupuesto es "
                       "totalmente aceptable; entre ese umbral y el techo decae "
                       "linealmente; al rebasarlo se anula."),
                html.P("La afinidad sensorial usa distancia euclidiana entre el "
                       "perfil del vino y el perfil ideal compuesto desde las "
                       "respuestas del usuario."),
            ]),
            _funcion_pertenencia(),
        ),
        _section(
            "Paso 4 · Composición",
            "Score difuso final",
            html.Div([
                html.P("El motor combina varios grados con pesos definidos en la "
                       "base de reglas:"),
                html.Pre(
                    "score = μ_sensorial * 0.50\n"
                    "      + μ_precio    * 0.20\n"
                    "      + bono_maridaje  (0.25)\n"
                    "      + bono_ocasion   (0.10–0.15)\n"
                    "      + bono_clima     (0.15)",
                    className="code-block",
                ),
                html.P("La salida es un ranking con explicaciones desagregadas."),
            ]),
            _diagrama_pipeline(),
        ),
        html.Section(
            className="cta",
            children=[
                html.H2("¿Lo probamos con tu próxima comida?", className="cta-title"),
                dcc.Link("Empezar el test →", href="/recomendar",
                         className="btn btn-primary btn-large"),
            ],
        ),
    ],
)


register_page(__name__, path="/como-funciona", name="Cómo funciona", layout=layout)
