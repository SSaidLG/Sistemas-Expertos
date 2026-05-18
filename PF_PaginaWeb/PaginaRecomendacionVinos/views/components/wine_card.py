"""Tarjeta de vino: usada tanto en el catálogo como en los resultados."""
from dash import html


def build_wine_card(vino: dict, score: float = None, ranking: int = None):
    """Compone una tarjeta visual para un vino."""
    badges = []
    if ranking is not None:
        badges.append(html.Span(f"#{ranking}", className="badge badge-rank"))
    badges.append(html.Span(vino["tipo"], className="badge badge-type"))
    if score is not None:
        badges.append(
            html.Span(f"{score:.1f}% match", className="badge badge-score")
        )

    return html.Article(
        className="wine-card",
        children=[
            html.Div(
                className="wine-card-image",
                style={
                    "backgroundImage": f"url({vino.get('imagen', '')})",
                },
            ),
            html.Div(
                className="wine-card-body",
                children=[
                    html.Div(className="wine-card-badges", children=badges),
                    html.H3(vino["nombre"], className="wine-card-title"),
                    html.P(
                        f"{vino['bodega']} · {vino.get('region', '')}",
                        className="wine-card-subtitle",
                    ),
                    html.P(vino.get("descripcion", ""), className="wine-card-desc"),
                    html.Div(
                        className="wine-card-meta",
                        children=[
                            html.Span(f"${vino['precio']:.0f} MXN", className="meta-price"),
                            html.Span(f"{vino['uva']}", className="meta-grape"),
                            html.Span(f"{vino['alcohol']}% vol", className="meta-alc"),
                        ],
                    ),
                ],
            ),
        ],
    )
