"""Barra de navegación superior compartida por todas las páginas."""
from dash import html, dcc


def build_navbar(active: str = "inicio"):
    """Construye el navbar.

    Args:
        active: id de la página activa para resaltar.
    """
    links = [
        ("inicio", "Inicio", "/"),
        ("recomendar", "Recomendar", "/recomendar"),
        ("catalogo", "Catálogo", "/catalogo"),
        ("como_funciona", "Cómo funciona", "/como-funciona"),
    ]

    return html.Header(
        className="navbar",
        children=[
            html.Div(
                className="navbar-inner",
                children=[
                    dcc.Link(
                        children=[
                            html.Span("◍", className="logo-mark"),
                            html.Span("Sommelier", className="logo-text"),
                            html.Span("Virtual", className="logo-suffix"),
                        ],
                        href="/",
                        className="logo",
                    ),
                    html.Nav(
                        className="nav-links",
                        children=[
                            dcc.Link(
                                label,
                                href=href,
                                className=(
                                    "nav-link active" if key == active else "nav-link"
                                ),
                            )
                            for key, label, href in links
                        ],
                    ),
                ],
            )
        ],
    )
