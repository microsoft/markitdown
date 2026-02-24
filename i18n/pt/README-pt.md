# MarkItDown

<p align="left">
  <a href="../../README.md">🇺🇸 English</a>
</p>

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)  
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)  
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

> [!TIP]  
> MarkItDown agora oferece um servidor MCP (Model Context Protocol) para integração com aplicações LLM como o Claude Desktop. Veja [markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) para mais informações.

> [!IMPORTANT]  
> Mudanças incompatíveis da versão 0.0.1 para 0.1.0:
>
> - As dependências agora estão organizadas em grupos de recursos opcionais (mais detalhes abaixo). Use `pip install 'markitdown[all]'` para manter o comportamento compatível com versões anteriores.
> - `convert_stream()` agora requer um objeto binário semelhante a arquivo (por exemplo, um arquivo aberto em modo binário ou um objeto `io.BytesIO`). Essa é uma mudança incompatível em relação à versão anterior, que aceitava objetos semelhantes a arquivo de texto, como `io.StringIO`.
> - A interface da classe `DocumentConverter` mudou para ler streams de arquivos ao invés de caminhos de arquivo. _Nenhum arquivo temporário é criado mais_. Se você mantém um plugin ou `DocumentConverter` personalizado, provavelmente precisará atualizar seu código. Caso use apenas a classe `MarkItDown` ou a CLI (como nos exemplos abaixo), não deverá ser necessário alterar nada.

MarkItDown é uma ferramenta leve em Python para converter diversos tipos de arquivo em Markdown, voltada para uso com LLMs e pipelines de análise de texto. Nesse sentido, é mais comparável ao [textract](https://github.com/deanmalmgren/textract), porém com foco em preservar a estrutura e o conteúdo importantes do documento em Markdown (incluindo: cabeçalhos, listas, tabelas, links etc.). Embora o resultado seja muitas vezes apresentável e amigável para humanos, ele se destina a ser consumido por ferramentas de análise de texto — e pode não ser a melhor opção para conversões de alta fidelidade para leitura humana.

No momento, o MarkItDown suporta:

- PDF
- PowerPoint
- Word
- Excel
- Imagens (metadados EXIF e OCR)
- Áudio (metadados EXIF e transcrição de fala)
- HTML
- Formatos baseados em texto (CSV, JSON, XML)
- Arquivos ZIP (itera sobre o conteúdo)
- URLs do YouTube
- EPubs
- ... e mais!

## Por que Markdown?

Markdown é extremamente próximo de texto puro, com marcações e formatações mínimas, mas ainda assim fornece um meio de representar estruturas de documento importantes. LLMs populares, como o GPT-4o da OpenAI, falam Markdown nativamente e frequentemente incorporam Markdown em suas respostas sem qualquer prompt especial. Isso sugere que foram treinados em vastas quantidades de texto formatado em Markdown e o compreendem bem. Como benefício secundário, convenções de Markdown também são muito eficientes em tokens.

## Instalação

Para instalar o MarkItDown, use pip:

```bash
pip install 'markitdown[all]'
```

Como alternativa, você pode instalá-lo a partir do código-fonte:

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

## Uso

### Linha de Comando

```bash
markitdown caminho-para-arquivo.pdf > documento.md
```

Ou use `-o` para especificar o arquivo de saída:

```bash
markitdown caminho-para-arquivo.pdf -o documento.md
```

Você também pode usar pipe:

```bash
cat caminho-para-arquivo.pdf | markitdown
```

### Dependências Opcionais

O MarkItDown possui dependências opcionais para ativar vários formatos de arquivo. No início deste documento, instalamos todas as dependências opcionais com a opção `[all]`. Porém, você também pode instalá-las individualmente para ter mais controle. Por exemplo:

```bash
pip install 'markitdown[pdf, docx, pptx]'
```

instalará apenas as dependências para arquivos PDF, DOCX e PPTX.

Atualmente, as seguintes dependências opcionais estão disponíveis:

- `[all]` Instala todas as dependências opcionais
- `[pptx]` Dependências para arquivos PowerPoint
- `[docx]` Dependências para arquivos Word
- `[xlsx]` Dependências para arquivos Excel modernos
- `[xls]` Dependências para arquivos Excel antigos
- `[pdf]` Dependências para arquivos PDF
- `[outlook]` Dependências para mensagens do Outlook
- `[az-doc-intel]` Dependências para Azure Document Intelligence
- `[audio-transcription]` Dependências para transcrição de áudio (wav, mp3)
- `[youtube-transcription]` Dependências para obter transcrição de vídeos do YouTube

### Plugins

O MarkItDown também suporta plugins de terceiros. Plugins vêm desativados por padrão. Para listar os plugins instalados:

```bash
markitdown --list-plugins
```

Para habilitar plugins, use:

```bash
markitdown --use-plugins caminho-para-arquivo.pdf
```

Para encontrar plugins disponíveis, procure no GitHub pela hashtag `#markitdown-plugin`. Para desenvolver um plugin, veja o diretório `packages/markitdown-sample-plugin`.

### Azure Document Intelligence

Para usar o Microsoft Document Intelligence na conversão:

```bash
markitdown caminho-para-arquivo.pdf -o documento.md -d -e "<document_intelligence_endpoint>"
```

Mais informações sobre como configurar um recurso Azure Document Intelligence podem ser encontradas [aqui](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0).

### API em Python

Uso básico em Python:

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # Defina como True para habilitar plugins
result = md.convert("test.xlsx")
print(result.text_content)
```

Conversão com Document Intelligence em Python:

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

Para usar Modelos de Linguagem (LLMs) para descrições de imagens, forneça `llm_client` e `llm_model`:

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("example.jpg")
print(result.text_content)
```

### Docker

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/seu-arquivo.pdf > output.md
```

## Contribuindo

Este projeto recebe contribuições e sugestões de bom grado. A maioria das contribuições exige que você concorde com um Acordo de Licença de Contribuidor (CLA), declarando que você tem o direito e a autoridade para conceder-nos os direitos sobre sua contribuição. Para mais detalhes, visite https://cla.opensource.microsoft.com.

Quando você enviar um pull request, um bot de CLA determinará automaticamente se você precisa fornecer um CLA e sinalizará o PR adequadamente (por exemplo, com um status check ou comentário). Basta seguir as instruções do bot. Você precisará fazer isso apenas uma vez em todos os repositórios que usam nosso CLA.

Este projeto adotou o [Código de Conduta de Código Aberto da Microsoft](https://opensource.microsoft.com/codeofconduct/). Para mais informações, veja o [FAQ do Código de Conduta](https://opensource.microsoft.com/codeofconduct/faq/) ou entre em contato com [opencode@microsoft.com](mailto:opencode@microsoft.com) para quaisquer dúvidas ou comentários adicionais.

### Como Contribuir

Você pode ajudar olhando as issues ou revisando PRs. Qualquer issue ou PR é bem-vinda, mas também marcamos algumas como "open for contribution" e "open for reviewing" para facilitar contribuições da comunidade.

<div align="center">

|            | Todas                                                             | Especialmente Precisa de Ajuda da Comunidade                                                                                                  |
| ---------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Issues** | [Todas as Issues](https://github.com/microsoft/markitdown/issues) | [Issues abertas para contribuição](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs**    | [Todos os PRs](https://github.com/microsoft/markitdown/pulls)     | [PRs abertos para revisão](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)                |

</div>

### Executando Testes e Verificações

- Navegue até o pacote MarkItDown:

  ```sh
  cd packages/markitdown
  ```

- Instale o `hatch` em seu ambiente e execute os testes:

  ```sh
  pip install hatch  # Outras formas de instalar hatch: https://hatch.pypa.io/dev/install/
  hatch shell
  hatch test
  ```

  (Alternativa) Use o Devcontainer que já vem com todas as dependências instaladas:

  ```sh
  # Reabra o projeto no Devcontainer e execute:
  hatch test
  ```

- Execute as verificações de pre-commit antes de enviar um PR: `pre-commit run --all-files`

### Contribuindo com Plugins de Terceiros

Você também pode contribuir criando e compartilhando plugins de terceiros. Veja `packages/markitdown-sample-plugin` para mais detalhes.

## Marcas Registradas

Este projeto pode conter marcas registradas ou logotipos de projetos, produtos ou serviços. O uso autorizado de marcas registradas ou logotipos da Microsoft está sujeito às [Diretrizes de Marcas Registradas e Marca da Microsoft](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). O uso de marcas registradas ou logotipos da Microsoft em versões modificadas deste projeto não deve causar confusão ou implicar patrocínio pela Microsoft. Qualquer uso de marcas ou logotipos de terceiros está sujeito às políticas dessas terceiros.
