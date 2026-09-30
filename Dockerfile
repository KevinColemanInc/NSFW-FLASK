FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    PRIVATE_DETECTOR_MODEL_DIR=/app/_private_detector_saved_model

WORKDIR /app

# libgomp is required by TensorFlow's native runtime.
RUN apt-get update \
    && apt-get install --no-install-recommends -y libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.docker.txt

COPY . ./
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p "$PRIVATE_DETECTOR_MODEL_DIR" \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=180s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8080') + '/health', timeout=3)"

CMD ["gunicorn", "--config", "gunicorn_config.py", "--worker-tmp-dir", "/dev/shm", "--timeout", "0", "app:app"]
