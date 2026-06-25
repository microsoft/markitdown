# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown
import tempfile
import os
import shutil

app = FastAPI(title="MarkItDown API")

# Allow CORS for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

markitdown = MarkItDown()

@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Create a temporary file to save the uploaded file
    # We use a named temporary file so markitdown can read it
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    try:
        # Copy the uploaded file contents to the temporary file
        shutil.copyfileobj(file.file, temp_file)
        temp_file.close()
        
        # Convert using MarkItDown
        result = markitdown.convert(temp_file.name)
        
        return {
            "filename": file.filename,
            "markdown": result.text_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        file.file.close()
        # Clean up the temporary file
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
