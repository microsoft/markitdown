# MarkItDown

[English](README.md) | [Русский](README.ru.md)

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

> [!IMPORTANT]
> MarkItDown выполняет I/O с привилегиями текущего процесса. Как `open()` или `requests.get()`, он обращается к ресурсам, доступным самому процессу. В недоверенных средах санитизируйте входы и вызывайте самый узкий `convert_*` под вашу задачу (например, `convert_stream()` или `convert_local()`). См. раздел [Соображения безопасности](#соображения-безопасности).

MarkItDown — лёгкая Python-утилита для преобразования разных файлов в Markdown для LLM и текстовых пайплайнов. Ближайший аналог — [textract](https://github.com/deanmalmgren/textract), но акцент на сохранении важной структуры документа в Markdown (заголовки, списки, таблицы, ссылки и т.д.). Результат часто вполне читаем для человека, однако рассчитан на текстовый анализ и может не быть лучшим выбором для высококачественной конвертации «для людей».

Сейчас MarkItDown умеет конвертировать:

- PDF
- PowerPoint
- Word
- Excel
- Изображения (метаданные EXIF и OCR)
- Аудио (метаданные EXIF и транскрипция речи)
- HTML
- Текстовые форматы (CSV, JSON, XML)
- ZIP-файлы (обходит содержимое)
- YouTube URL
- EPub
- … и другое!

## Зачем Markdown?

Markdown очень близок к обычному тексту: минимум разметки, но структура документа сохраняется. Основные LLM, например GPT-4o от OpenAI, «говорят» на Markdown и часто сами вставляют его в ответы. Значит, они обучены на огромном объёме Markdown и хорошо его понимают. Бонус: Markdown ещё и экономно расходует токены.

## Требования
MarkItDown нужен Python 3.10 или новее. Рекомендуется виртуальное окружение, чтобы не конфликтовать с зависимостями.

Со стандартным Python:

```bash
python -m venv .venv
source .venv/bin/activate
```

С `uv`:

```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
# NOTE: Be sure to use 'uv pip install' rather than just 'pip install' to install packages in this virtual environment
```

С Anaconda:

```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

## Установка

Установка через pip: `pip install 'markitdown[all]'`. Или из исходников:

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

## Использование

### Командная строка

```bash
markitdown path-to-file.pdf > document.md
```

Или `-o` для выходного файла:

```bash
markitdown path-to-file.pdf -o document.md
```

Можно передать содержимое через pipe:

```bash
cat path-to-file.pdf | markitdown
```

### Опциональные зависимости
У MarkItDown есть опциональные зависимости под разные форматы. Выше мы ставили все сразу через `[all]`. Их можно ставить и по отдельности:

```bash
pip install 'markitdown[pdf, docx, pptx]'
```

так установятся только зависимости для PDF, DOCX и PPTX.

Сейчас доступны:

* `[all]` — все опциональные зависимости
* `[pptx]` — файлы PowerPoint
* `[docx]` — файлы Word
* `[xlsx]` — файлы Excel
* `[xls]` — старые файлы Excel
* `[pdf]` — файлы PDF
* `[outlook]` — сообщения Outlook
* `[az-doc-intel]` — Azure Document Intelligence
* `[az-content-understanding]` — Azure Content Understanding
* `[audio-transcription]` — транскрипция wav и mp3
* `[youtube-transcription]` — транскрипции YouTube

### Плагины

MarkItDown поддерживает сторонние плагины. По умолчанию они выключены. Список установленных:

```bash
markitdown --list-plugins
```

Включить плагины:

```bash
markitdown --use-plugins path-to-file.pdf
```

Искать плагины на GitHub по хештегу `#markitdown-plugin`. Как написать свой — см. `packages/markitdown-sample-plugin`.

#### Плагин markitdown-ocr

Плагин `markitdown-ocr` добавляет OCR в конвертеры PDF, DOCX, PPTX и XLSX: текст из встроенных изображений извлекается через LLM Vision — тот же паттерн `llm_client` / `llm_model`, что MarkItDown уже использует для описаний картинок. Новые ML-библиотеки и бинарные зависимости не нужны.

**Установка:**

```bash
pip install markitdown-ocr
pip install openai  # or any OpenAI-compatible client
```

**Использование:**

Передайте те же `llm_client` и `llm_model`, что и для описаний изображений:

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = md.convert("document_with_images.pdf")
print(result.text_content)
```

Если `llm_client` не задан, плагин всё равно загружается, но OCR молча пропускается и работает стандартный встроенный конвертер.

Подробности: [`packages/markitdown-ocr/README.md`](packages/markitdown-ocr/README.md).

### Azure Content Understanding

[Azure Content Understanding](https://learn.microsoft.com/azure/ai-services/content-understanding/) даёт более качественную конвертацию со структурированным извлечением полей (YAML front matter), мультимодальную поддержку (документы, изображения, аудио, видео) и настраиваемые анализаторы.

Установка: `pip install 'markitdown[az-content-understanding]'`

#### Когда использовать Content Understanding

CU полезен, когда нужны возможности сверх встроенных конвертеров и Document Intelligence:

- **Аудио и видео** — CU единственный вариант для видео и более качественный облачный вариант для аудио. Встроенные конвертеры видео не поддерживают, аудио — только базовая транскрипция.
- **Структурированное извлечение полей** — [готовые](https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/prebuilt-analyzers) или [кастомные](https://learn.microsoft.com/azure/ai-services/content-understanding/how-to/customize-analyzer-content-understanding-studio?tabs=portal) анализаторы извлекают доменные поля (суммы счетов, даты чеков, пункты договоров) в YAML front matter. Ни встроенные конвертеры, ни интеграция Doc Intel поля не отдают.
- **Более качественное извлечение документов** — облачный анализ вёрстки и OCR для сканов PDF, сложных таблиц и многостраничных документов.
- **Один API для всех модальностей** — один `cu_endpoint` обрабатывает документы, изображения, аудио и видео с автоматической маршрутизацией анализаторов.

| Возможность | Встроенные конвертеры | Azure Document Intelligence | Azure Content Understanding |
|------------|---------------------|-----------------------------|-----------------------------|
| Конвертация документов | Офлайн, извлечение под формат | Облачное извлечение вёрстки | Облачное мультимодальное извлечение |
| Структурированные поля | Нет | Интеграция не отдаёт | YAML front matter из полей анализатора |
| Кастомные анализаторы | Нет | Не настраивается в этой интеграции | Поддерживается через `cu_analyzer_id` |
| Аудио и видео | Базовое аудио, без видео | Не поддерживается | Анализаторы аудио и видео |
| Стоимость | Только локальные вычисления | Платные вызовы Azure API | Платные вызовы Azure API |

**CLI:**

```bash
markitdown path-to-file.pdf --use-cu --cu-endpoint "<content_understanding_endpoint>"
```

**Python API:**

```python
from markitdown import MarkItDown

# Zero-config — auto-selects analyzer per file type
md = MarkItDown(cu_endpoint="<content_understanding_endpoint>")
result = md.convert("report.pdf")   # documents → prebuilt-documentSearch
result = md.convert("meeting.mp4")  # video → prebuilt-videoSearch
result = md.convert("call.wav")     # audio → prebuilt-audioSearch
print(result.markdown)
```

**С кастомным анализатором** (извлечение доменных полей):

```python
md = MarkItDown(
    cu_endpoint="<content_understanding_endpoint>",
    cu_analyzer_id="my-invoice-analyzer",
)
result = md.convert("invoice.pdf")
print(result.markdown)
# Output includes YAML front matter with extracted fields:
# ---
# contentType: document
# fields:
#   VendorName: CONTOSO LTD.
#   InvoiceDate: '2019-11-15'
# ---
# <!-- page 1 -->
# ...
```

Если задан `cu_analyzer_id`, конвертер сам ограничивает его совместимыми типами файлов по модальности анализатора. Несовместимые типы (например, аудио с document-анализатором) автоматически уходят на стандартные prebuilt-анализаторы.

**Про стоимость:** каждый вызов `convert()` для формата, который идёт в CU, — это платный вызов Azure API. Ограничьте форматы через `cu_file_types`:

```python
from markitdown.converters import ContentUnderstandingFileType

md = MarkItDown(
    cu_endpoint="<content_understanding_endpoint>",
    cu_file_types=[ContentUnderstandingFileType.PDF],  # only PDFs use CU
)
```

Подробнее об Azure Content Understanding — [здесь](https://learn.microsoft.com/azure/ai-services/content-understanding/).

### Azure Document Intelligence

Конвертация через Microsoft Document Intelligence:

```bash
markitdown path-to-file.pdf -o document.md -d -e "<document_intelligence_endpoint>"
```

Как создать ресурс Azure Document Intelligence — [здесь](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0)

### Python API

Базовое использование:

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
result = md.convert("test.xlsx")
print(result.text_content)
```

Document Intelligence в Python:

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("test.pdf")
print(result.text_content)
```

Описания изображений через LLM (сейчас только pptx и картинки) — передайте `llm_client` и `llm_model`:

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="optional custom prompt")
result = md.convert("example.jpg")
print(result.text_content)
```

### Docker

```sh
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## Участие

Проект принимает вклад и предложения. Для большинства вкладов нужно подписать Contributor License Agreement (CLA): вы подтверждаете, что имеете право передать нам права на использование вашего вклада. Подробности: https://cla.opensource.microsoft.com.

Когда вы отправляете pull request, бот CLA сам определяет, нужен ли CLA, и помечает PR (status check, комментарий). Следуйте инструкциям бота. Это делается один раз для всех репозиториев с нашим CLA.

Проект принял [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). См. [FAQ](https://opensource.microsoft.com/codeofconduct/faq/) или пишите на [opencode@microsoft.com](mailto:opencode@microsoft.com).

### Как помочь

Можно разбирать issues или ревьюить PR. Любые issue и PR приветствуются; часть помечена как 'open for contribution' и 'open for reviewing', чтобы упростить вклад сообщества. Это лишь подсказки — помогать можно любым способом.

<div align="center">

|            | Все                                                          | Особенно нужна помощь сообщества                                                                                                      |
| ---------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Issues** | [All Issues](https://github.com/microsoft/markitdown/issues) | [Issues open for contribution](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22) |
| **PRs**    | [All PRs](https://github.com/microsoft/markitdown/pulls)     | [PRs open for reviewing](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)              |

</div>

### Тесты и проверки

- Перейдите в пакет MarkItDown:

  ```sh
  cd packages/markitdown
  ```

- Установите `hatch` и запустите тесты:

  ```sh
  pip install hatch  # Other ways of installing hatch: https://hatch.pypa.io/dev/install/
  hatch shell
  hatch test
  ```

  (Альтернатива) Devcontainer со всеми зависимостями:

  ```sh
  # Reopen the project in Devcontainer and run:
  hatch test
  ```

- Перед PR прогоните: `pre-commit run --all-files`

### Соображения безопасности

MarkItDown выполняет I/O с привилегиями текущего процесса. Как `open()` или `requests.get()`, он обращается к ресурсам, доступным самому процессу.

**Санитизируйте входы:** не передавайте недоверенный ввод напрямую в MarkItDown. Если любая часть входа может контролироваться недоверенным пользователем или системой (хостинг, серверные приложения), её нужно проверить и ограничить до вызова MarkItDown. В зависимости от среды это может включать ограничение путей, схем URI и сетевых назначений, а также блокировку доступа к private, loopback, link-local адресам и metadata-сервисам.

**Вызывайте только нужный метод конвертации:** предпочитайте самый узкий API. Метод `convert()` намеренно широкий: локальные файлы, удалённые URI и потоки байт. Если приложению нужны только локальные файлы, вызывайте `convert_local()`. Если нужен контроль над загрузкой URI, сделайте `requests.get()` сами и передайте ответ в `convert_response()`. Для максимального контроля откройте поток и вызовите `convert_stream()`.

### Сторонние плагины

Можно помогать, создавая и публикуя сторонние плагины. См. `packages/markitdown-sample-plugin`.

## Товарные знаки

В проекте могут встречаться товарные знаки или логотипы проектов, продуктов и сервисов. Разрешённое использование товарных знаков и логотипов Microsoft подчиняется
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Использование товарных знаков и логотипов Microsoft в изменённых версиях проекта не должно вводить в заблуждение и не должно подразумевать спонсорство Microsoft.
Использование сторонних товарных знаков и логотипов подчиняется политикам соответствующих третьих сторон.
