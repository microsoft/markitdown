# imagem Debian (não Alpine) — suporta onnxruntime e magika
FROM python:3.11-slim
WORKDIR /work

# instala compiladores e dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential git ffmpeg libxml2 libxslt1-dev \
    libffi-dev libssl-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*

# copia o código do repositório
COPY . .

# instala o markitdown e pytest
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir -e 'packages/markitdown[all]' pytest

# define o diretório do pacote e roda os testes
WORKDIR /work/packages/markitdown
CMD ["pytest", "-q"]
