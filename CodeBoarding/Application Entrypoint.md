```mermaid
graph LR
    Application_Entrypoint["Application Entrypoint"]
    MarkItDown_Class["MarkItDown Class"]
    Application_Entrypoint -- "Initializes" --> MarkItDown_Class
```

## Component Details

The MarkItDown application converts markdown text into various output formats. The application entry point parses command-line arguments, initializes the MarkItDown class, enables built-in features and plugins, and then orchestrates the conversion process. The core conversion logic resides within the MarkItDown class, which handles different input types (local files, streams, URLs) and delegates the actual conversion to registered converters. The application supports extending its functionality through plugins and built-in features.

### Application Entrypoint
The main entry point for the MarkItDown application. It handles command-line arguments using `argparse`, initializes the `MarkItDown` class, and initiates the conversion process based on user input. It orchestrates the overall application flow, setting up the environment and triggering the conversion pipeline.
- **Related Classes/Methods**: `markitdown.packages.markitdown.src.markitdown.__main__:main` (13:200)

### MarkItDown Class
The central class responsible for converting markdown text into other formats. It handles initialization, enabling built-in features and plugins, and orchestrating the conversion process through various methods. It uses registered converters to perform the actual conversion.
- **Related Classes/Methods**: `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:__init__` (97:130), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:enable_builtins` (132:221), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:enable_plugins` (223:241), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert` (243:291), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert_local` (293:328), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert_stream` (330:375), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert_url` (377:394), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert_uri` (396:455), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:convert_response` (457:527), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:_convert` (529:619), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:register_page_converter` (621:627), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:register_converter` (629:659), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:_get_stream_info_guesses` (661:760)