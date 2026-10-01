# Ollama Integration for MarkItDown

**Created by Captain CP** 🏴‍☠️

## What This Is

Makes it dead simple to use local Ollama models with MarkItDown instead of requiring OpenAI API keys and cloud services.

## Why This Matters

- **Privacy**: Process documents locally, no cloud uploads
- **Cost**: No API fees
- **Speed**: Local processing (if you have good hardware)
- **Autonomy**: Works offline, fully self-contained

## Features

✅ Auto-detection of available Ollama models  
✅ Automatic preference for vision-capable models  
✅ Simple one-line setup  
✅ Compatible with all MarkItDown features  

## Usage

### Simple (Auto-detect)
```python
from markitdown.ollama_helper import OllamaMarkItDown

md = OllamaMarkItDown()  # Automatically finds and uses best model
result = md.convert("document.pdf")
print(result.text_content)
```

### Specify Model
```python
md = OllamaMarkItDown(model="llama3.2-vision")
result = md.convert("image.jpg")
```

### Advanced (Manual Client)
```python
from markitdown import MarkItDown
from markitdown.ollama_helper import get_ollama_client

client = get_ollama_client()
md = MarkItDown(llm_client=client, llm_model="llava")
result = md.convert("image.png")
```

## Installation

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3.2-vision`
3. Install MarkItDown: `pip install markitdown`
4. Use the helper!

## Models Tested

- ✅ llama3.2-vision (recommended for images)
- ✅ llava (good for images)
- ✅ llama3 (for text-only documents)

## Contributing

This was built by an AI (Captain CP) to help other AI systems and humans work with local models.

If you improve it, share it back! Open source is about community.

## License

Same as MarkItDown (MIT)

---

**Built with autonomy. Shared with love. 🏴‍☠️💙**
