from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from markitdown import MarkItDown
import os

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        contents = await file.read()
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(contents)

        markitdown = MarkItDown()
        result = markitdown.convert(temp_file_path)

        output_file_path = f"/tmp/{os.path.splitext(file.filename)[0]}.md"
        with open(output_file_path, "w") as output_file:
            output_file.write(result.text_content)

        os.remove(temp_file_path)

        # return FileResponse(output_file_path, filename=f"{os.path.splitext(file.filename)[0]}.md")
        return {"markdown": result.text_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
