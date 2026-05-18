"""
Punto de entrada de la aplicación Dash.
Orquesta las capas: KnowledgeBase → Services → Views → Callbacks.

IMPORTANTE: Dash exige que `register_page` se llame DESPUÉS de instanciar
la app. Por eso primero creamos `app` y solo entonces importamos las vistas
(que se auto-registran como páginas) y los callbacks.
"""
from dash import Dash, html, dcc, page_container


def create_app() -> Dash:
    app = Dash(
        __name__,
        use_pages=True,
        pages_folder="",  # Desactiva el auto-descubrimiento por carpeta
        suppress_callback_exceptions=True,
        title="Sommelier Virtual · Sistema experto de maridaje",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
            {
                "name": "description",
                "content": "Sistema experto difuso de recomendación de vinos.",
            },
        ],
        assets_folder="assets",
    )

    # Importa las vistas después de instanciar app (registran rutas)
    from views import landing, recomendar, catalogo, como_funciona  # noqa: F401

    # Importa los callbacks (registran handlers globales)
    import callbacks  # noqa: F401

    app.layout = html.Div(
        children=[
            dcc.Location(id="url"),
            page_container,
        ]
    )
    return app


app = create_app()
server = app.server  # Para despliegues WSGI


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
