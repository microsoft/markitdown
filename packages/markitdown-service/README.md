# markitdown-service

Serviço HTTP **interno** da Dont Scroll que converte arquivos enviados (PDF, Word, PowerPoint, Excel) em Markdown com o
MarkItDown. Quem fala com ele é o portal admin (`admin.dontscroll.agency`, módulo **PDF → Markdown**); ninguém mais.

```
navegador (equipe, login Google) ──▶ portal admin ──(rede interna, MARKITDOWN_ADMIN_TOKEN)──▶ markitdown-service
```

## O que ele faz (e o que não faz)

- Aceita **só bytes enviados** (`.pdf .docx .pptx .xlsx .xls`). Não busca URL nem lê caminho: não serve de porta para a rede interna.
- Cada conversão roda em **um processo à parte**, com limite de tempo e de memória: um arquivo defeituoso não derruba o serviço.
- Sem plugins, sem OCR, sem chamadas a APIs de IA. **PDF escaneado (só imagens) devolve "sem texto"**: precisa de OCR (`packages/markitdown-ocr`), que fica para uma segunda etapa porque tem custo.
- Não grava nada em disco e não registra nomes de arquivo nos logs (só extensão, tamanho e tempo).

## API

| Rota | O que faz |
|---|---|
| `GET /healthz` | `200 {"ok":true}` (sem token; para o monitor do Dokploy) |
| `POST /converter?nome=arquivo.pdf` | corpo = os bytes do arquivo; cabeçalho `Authorization: Bearer <MARKITDOWN_ADMIN_TOKEN>`. Devolve `{"ok":true,"markdown":"…","caracteres":123,"extensao":".pdf"}` |

Erros vêm como `{"ok":false,"erro":"<código>","mensagem":"…"}`: `nao_autorizado` (401), `formato_nao_suportado` (415),
`arquivo_vazio` (400), `arquivo_grande_demais` (413), `ocupado` (429), `conversao_falhou` / `sem_texto` /
`memoria_insuficiente` (422), `tempo_esgotado` (504).

## Variáveis de ambiente

| Variável | Obrigatória | Padrão | O que é |
|---|---|---|---|
| `MARKITDOWN_ADMIN_TOKEN` | sim | | segredo de 32+ caracteres. **O mesmo valor** em `MARKITDOWN_ADMIN_TOKEN` do app do portal admin. Sem ele (ou fraco) o serviço recusa subir. |
| `MARKITDOWN_MAX_UPLOAD_MB` | não | `25` | tamanho máximo do arquivo |
| `MARKITDOWN_TIMEOUT_S` | não | `90` | tempo máximo de uma conversão |
| `MARKITDOWN_MAX_CONCURRENT` | não | `2` | conversões ao mesmo tempo (as demais recebem `ocupado`) |
| `MARKITDOWN_MAX_MEMORY_MB` | não | `2048` | teto de memória por conversão (`0` desliga) |
| `PORT` | não | `8000` | |

Se mudar `MARKITDOWN_MAX_UPLOAD_MB`, mude também no portal (`MARKITDOWN_MAX_UPLOAD_MB` lá), para a tela avisar antes de enviar.

## Instalação no Dokploy (uma vez)

1. **Create Service → Application**, origem `dontscrollagency/markitdown` (este fork), branch `main`.
2. **Build Type: Dockerfile**, **Dockerfile** `packages/markitdown-service/Dockerfile`, **Docker Context Path** `.`
3. **Variáveis:** `MARKITDOWN_ADMIN_TOKEN` (gere com `openssl rand -hex 32`).
4. **Domains: não crie nenhum.** O serviço só precisa ser alcançado pelo portal, pela rede interna do Dokploy.
5. **Deploy.** No app do portal admin, defina `MARKITDOWN_API_URL` = `http://<nome-do-serviço-no-dokploy>:8000` (o *App Name* do serviço) e
   o **mesmo** `MARKITDOWN_ADMIN_TOKEN`; faça redeploy do portal. O cartão "PDF → Markdown" aparece na home.

Rotacionar o token: troque nos dois apps e faça redeploy dos dois.

## Desenvolvimento

```bash
pip install -e '../markitdown[pdf,docx,pptx,xlsx,xls]' -e . pytest
pytest
```

```bash
MARKITDOWN_ADMIN_TOKEN=$(openssl rand -hex 32) markitdown-service
```
