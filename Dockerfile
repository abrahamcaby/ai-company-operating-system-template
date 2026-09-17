# Local fictional demo image. Pin an approved digest before any managed distribution.
FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 10001 demo && mkdir -p /app/.local && chown demo:demo /app/.local
COPY --chown=demo:demo app /app/app
COPY --chown=demo:demo web /app/web
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 COMPANY_OS_MODE=demo
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/health',timeout=2)"
CMD ["python", "-m", "app.server", "--host", "0.0.0.0"]
