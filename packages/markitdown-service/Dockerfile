# Dokploy: Application -> Build Type "Dockerfile", Dockerfile packages/markitdown-service/Dockerfile,
# Docker Context Path "." (a raiz do repositório). Passo a passo e variáveis: packages/markitdown-service/README.md.
FROM python:3.13-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ORT_DISABLE_TELEMETRY=1 \
    PORT=8000

WORKDIR /app
COPY packages/markitdown /app/packages/markitdown
COPY packages/markitdown-service /app/packages/markitdown-service
# Só os conversores que o serviço aceita (PDF, Word, PowerPoint, Excel): sem áudio, YouTube, Azure nem ffmpeg/exiftool.
RUN pip install "/app/packages/markitdown[pdf,docx,pptx,xlsx,xls]" /app/packages/markitdown-service

# Sem segredos aqui: MARKITDOWN_ADMIN_TOKEN entra só pelo ambiente do Dokploy.
USER nobody:nogroup
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import os,urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/healthz',timeout=4).status==200 else 1)"

CMD ["markitdown-service"]
