# ─────────────────────────────────────────────────────
# Sommelier.ai — Sistema experto difuso de maridaje
# Imagen Docker basada en Python slim
# ─────────────────────────────────────────────────────
FROM python:3.11-slim

# Configuración del entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8050

WORKDIR /app

# Instalación de dependencias (cache eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia del código fuente
COPY . .

# Puerto que expone Dash
EXPOSE 8050

# Healthcheck simple sobre la URL raíz
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; \
        sys.exit(0 if urllib.request.urlopen('http://localhost:8050',timeout=4).status==200 else 1)" \
    || exit 1

# Arranque con gunicorn (producción ligera)
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "2", "--threads", "4", "--timeout", "120", "app:server"]
