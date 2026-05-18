# Sommelier Virtual — Sistema experto difuso de maridaje

Sistema experto de recomendación de vinos para platillos basados en
**marcos de conocimiento**, **reglas heurísticas** y **lógica difusa**.
Frontend, backend y motor de inferencia construidos sobre **Dash** (que
integra Flask + React + Plotly internamente).

## Arquitectura por capas (MVC)

```
wine-expert-system/
├── app.py                       # Punto de entrada Dash
├── data/                        # Base de conocimiento fraccionada en JSON
│   ├── vinos.json               # Marcos (frames) de vinos
│   ├── reglas_sabor.json        # Reglas y pesos del motor
│   ├── meta.json                # Metadatos (tipos, ocasiones, climas)
│   └── preguntas.json           # Esquema dinámico del cuestionario
├── models/                      # Capa de datos
│   ├── wine_frame.py            # Modelo dataclass de un vino
│   └── knowledge_base.py        # Singleton que carga los JSON
├── services/                    # Capa de lógica
│   ├── fuzzy_engine.py          # Funciones de pertenencia y afinidad
│   └── recommendation_service.py  # Orquestador del pipeline
├── views/                       # Capa de presentación (páginas Dash)
│   ├── landing.py
│   ├── recomendar.py
│   ├── catalogo.py
│   ├── como_funciona.py
│   └── components/              # Navbar, WineCard, RadarChart
├── callbacks/                   # Controladores (eventos)
│   ├── questionnaire_callbacks.py
│   └── catalog_callbacks.py
└── assets/                      # CSS, JS de animaciones
    ├── styles.css
    └── animations.js
```

## Páginas

- `/` — Landing: explica el sistema, sus tres paradigmas y motiva a empezar.
- `/recomendar` — Cuestionario de 10 preguntas con resultados en vivo.
- `/catalogo` — Base de conocimiento navegable con filtros.
- `/como-funciona` — Diagrama y explicación del motor de inferencia.

## Cómo levantar la aplicación

Con Docker (recomendado), un solo comando:

```bash
docker compose up --build
```

Después abre en tu navegador:

```
http://localhost:8050
```

Para detener:

```bash
docker compose down
```

## Desarrollo local sin Docker

```bash
python -m venv venv && source venv/bin/activate     # o .\\venv\\Scripts\\activate en Windows
pip install -r requirements.txt
python app.py
```

## Motor difuso — resumen formal

```
μ_presupuesto(p) = { 1                            si p ≤ 0.8·P
                   (P - p) / (0.2·P)              si 0.8·P < p ≤ P
                   0                              si p > P }

afinidad_sensorial(v, ideal) = 1 - d(v, ideal) / 2
  donde d = √Σ (vi - ideali)²  para i ∈ {cuerpo, taninos, acidez, dulzor}

score = μ_sensorial · 0.50
      + μ_precio    · 0.20
      + bono_maridaje  + bono_ocasion + bono_clima
```

Todos los pesos se leen de `data/reglas_sabor.json`, de modo que el
comportamiento del sistema se puede ajustar sin tocar el código.

## Personalización

- **Agregar vinos**: edita `data/vinos.json`. Cada entrada debe respetar
  los slots del `WineFrame` (cuerpo, taninos, acidez, dulzor en `[0,1]`).
- **Ajustar reglas**: modifica `data/reglas_sabor.json` para cambiar los
  perfiles ideales o los pesos del score.
- **Sumar preguntas**: añade entradas en `data/preguntas.json`; el
  formulario se reconstruye automáticamente (los nuevos campos solo se
  usan en el motor si los añades a `_construir_perfil`).

## Stack

- Python 3.11
- Dash 2.17 (Flask + React + Plotly bajo el capó)
- Gunicorn para producción
- Docker / docker-compose
