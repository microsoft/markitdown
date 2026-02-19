from fastapi import FastAPI, File, UploadFile
import markitdown

app = FastAPI()

@app.post("/convert")
async def convert_to_markdown(file: UploadFile = File(...)):
    content = await file.read()  # Read the file content
    markdown_text = markitdown.convert(content.decode("utf-8"))  # Convert to markdown
    return {"markdown": markdown_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

