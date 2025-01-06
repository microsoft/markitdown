from fastapi import FastAPI, HTTPException, UploadFile, File
from markitdown import MarkItDown, UnsupportedFormatException, FileConversionException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MarkItDown API"}

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    try:
        markitdown = MarkItDown()
        result = markitdown.convert_stream(file.file, file_extension=file.filename.split('.')[-1])
        return {"title": result.title, "text_content": result.text_content}
    except UnsupportedFormatException:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    except FileConversionException:
        raise HTTPException(status_code=500, detail="File conversion error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
