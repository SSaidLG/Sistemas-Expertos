"""
Página principal (Landing).
Describe el sistema, sus capacidades y motiva al usuario a iniciar.
"""
from dash import html, dcc, register_page

from views.components.navbar import build_navbar


def _hero():
    return html.Section(
        className="hero",
        children=[
            html.Div(
                className="hero-content",
                children=[
                    html.Span("Sistema experto · Lógica difusa", className="eyebrow"),
                    html.H1(
                        [
                            "Vinos populares",
                            html.Br(),
                            html.Span("de Cuidad de México.", className="hero-accent"),
                        ],
                        className="hero-title",
                    ),
                    html.P(
                        "Un sistema experto que combina marcos de conocimiento, "
                        "reglas heurísticas y lógica difusa para recomendarte "
                        "el vino con mayor afinidad sensorial, dentro de tu "
                        "presupuesto y para tu ocasión.",
                        className="hero-subtitle",
                    ),
                    html.Div(
                        className="hero-actions",
                        children=[
                            dcc.Link(
                                "Comenzar ahora →",
                                href="/recomendar",
                                className="btn btn-primary",
                            ),
                            dcc.Link(
                                "Ver cómo funciona",
                                href="/como-funciona",
                                className="btn btn-ghost",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="hero-visual",
                children=[
                    html.Div(className="hero-bottle", **{"data-aos": "fade-left"}),
                ],
            ),
        ],
    )


def _features():
    items = [
        {
            "icon": "◐",
            "titulo": "Marcos de conocimiento",
            "texto": (
                "Cada vino es un frame con slots técnicos (cuerpo, taninos, acidez, "
                "dulzor) y comerciales (precio, popularidad, maridajes)."
            ),
        },
        {
            "icon": "≈",
            "titulo": "Lógica difusa híbrida",
            "texto": (
                "Funciones de pertenencia trapezoidales y lineales evalúan "
                "presupuesto, picor, grasa y complejidad sin recurrir a reglas duras."
            ),
        },
        {
            "icon": "✦",
            "titulo": "Razonamiento explicable",
            "texto": (
                "Cada recomendación incluye el grado de verdad sensorial, "
                "el ajuste de precio y los bonos contextuales que la justifican."
            ),
        },
    ]

    return html.Section(
        className="features",
        children=[
            html.Div(className="section-head", children=[
                html.Span("Por qué funciona", className="eyebrow"),
                html.H2("Tres capas de inteligencia trabajando para ti", className="section-title"),
            ]),
            html.Div(
                className="feature-grid",
                children=[
                    html.Div(
                        className="feature-card",
                        **{"data-aos": "fade-up"},
                        children=[
                            html.Div(f["icon"], className="feature-icon"),
                            html.H3(f["titulo"], className="feature-title"),
                            html.P(f["texto"], className="feature-text"),
                        ],
                    )
                    for f in items
                ],
            ),
        ],
    )


def _decision_help():
    return html.Section(
        className="decision-help",
        children=[
            html.Div(
                className="decision-content",
                children=[
                    html.Span("Toma decisiones mejores", className="eyebrow"),
                    html.H2(
                        "Elegir vino ya no debe ser un acto de fe.",
                        className="section-title",
                    ),
                    html.P(
                        "El sistema integra tres paradigmas clásicos de "
                        "Inteligencia Artificial Simbólica:",
                        className="decision-lead",
                    ),
                    html.Ul(
                        className="decision-list",
                        children=[
                            html.Li([html.Strong("Representación por marcos:"),
                                     " la base de conocimiento describe cada vino "
                                     "con slots tipados y verificables."]),
                            html.Li([html.Strong("Sistema de reglas heurísticas:"),
                                     " un conjunto de reglas afina los ideales "
                                     "según los rasgos sensoriales del platillo."]),
                            html.Li([html.Strong("Inferencia difusa:"),
                                     " el grado de pertenencia mide la similitud "
                                     "entre cada vino y el perfil ideal, evitando "
                                     "el típico 'todo o nada' de las reglas clásicas."]),
                        ],
                    ),
                    html.P(
                        "El resultado no es una sola respuesta, sino un ranking "
                        "transparente: tú decides qué tan dispuesto estás a ceder "
                        "en precio, en estilo o en tradición.",
                        className="decision-foot",
                    ),
                ],
            ),
            html.Div(
                className="decision-stats",
                children=[
                    html.Div(className="stat", children=[
                        html.Span("54", className="stat-num"),
                        html.Span("vinos catalogados", className="stat-label"),
                    ]),
                    html.Div(className="stat", children=[
                        html.Span("10", className="stat-num"),
                        html.Span("variables analizadas", className="stat-label"),
                    ]),
                    html.Div(className="stat", children=[
                        html.Span("6", className="stat-num"),
                        html.Span("reglas difusas", className="stat-label"),
                    ]),
                ],
            ),
        ],
    )


def _cta():
    return html.Section(
        className="cta",
        children=[
            html.H2("¿Listo para encontrar tu maridaje?", className="cta-title"),
            html.P("Responde 10 preguntas rápidas y obtén tus 3 mejores opciones.",
                   className="cta-text"),
            dcc.Link("Empezar el test →", href="/recomendar", className="btn btn-primary btn-large"),
        ],
    )


def _footer():
    return html.Footer(
        className="footer",
        children=[
            html.P("Sommelier Virtual · Sistema experto de maridaje · CDMX 2026"),
            html.P("Hecho con marcos, reglas y lógica difusa.",
                   className="footer-sub"),
        ],
    )


layout = html.Div(
    className="page",
    children=[
        build_navbar("inicio"),
        _hero(),
        _features(),
        _decision_help(),
        _cta(),
        _footer(),
    ],
)


register_page(__name__, path="/", name="Inicio", layout=layout)
