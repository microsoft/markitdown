```mermaid
graph LR
    MarkItDown["MarkItDown"]
    markitdown_sample_plugin["markitdown_sample_plugin"]
    _plugin["_plugin"]
    markitdown_sample_plugin -- "registers converters with" --> MarkItDown
    _plugin -- "implements registration logic" --> markitdown_sample_plugin
```

## Component Details

The Plugin Manager component is responsible for extending the MarkItDown application's functionality by allowing external plugins to register custom converters. It enables the application to support various input and output formats beyond the built-in Markdown conversion capabilities. The core of this functionality lies in the `MarkItDown` class, which provides methods for registering converters and enabling plugins. Plugins, exemplified by `markitdown_sample_plugin`, demonstrate how to register custom converters with the `MarkItDown` class. When a plugin is enabled, it registers its converters, making them available for use in the MarkItDown application.

### MarkItDown
The core class responsible for converting Markdown text into other formats, managing plugins, and registering converters. It provides methods to register different types of converters and enable plugins.
- **Related Classes/Methods**: `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:enable_plugins` (223:241), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:register_converter` (629:659), `markitdown.packages.markitdown.src.markitdown._markitdown.MarkItDown:register_page_converter` (621:627)

### markitdown_sample_plugin
A sample plugin that demonstrates how to register custom converters with the MarkItDown class. It contains the logic for registering converters when the plugin is enabled.
- **Related Classes/Methods**: `markitdown.packages.markitdown-sample-plugin.src.markitdown_sample_plugin._plugin:register_converters` (25:31)

### _plugin
This module within the `markitdown_sample_plugin` package likely contains the implementation details for registering the sample plugin's converters with the main `MarkItDown` application. It encapsulates the specific converters and the registration logic.
- **Related Classes/Methods**: `markitdown.packages.markitdown-sample-plugin.src.markitdown_sample_plugin._plugin` (full file reference)