
import io
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from ._markitdown import MarkItDown
from ._stream_info import StreamInfo

app = FastAPI(
    title="Markitdown API",
    description="A web API for the Markitdown file conversion tool.",
    version="1.0.0"
)

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Root endpoint for health checks.
    """
    return {"status": "ok", "message": "Markitdown API is running"}

@app.post("/convert", tags=["Conversion"])
async def convert_file(file: UploadFile = File(...)):
    """
    Accepts a file, converts it to Markdown using Markitdown,
    and returns the result as a streaming response.
    """
    try:
        # Create a MarkItDown instance
        md = MarkItDown()

        # Get file content as a stream-like object
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)

        # Create StreamInfo
        stream_info = StreamInfo(
            stream_name=file.filename,
            input_stream=file_stream
        )

        # Perform the conversion
        # The convert method returns a generator that yields markdown content chunks
        markdown_generator = md.convert(stream_info)

        # Return as a streaming response
        return StreamingResponse(markdown_generator, media_type="text/markdown")

    except Exception as e:
        # Basic error handling
        return Response(
            content=f"An error occurred during conversion: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )

if __name__ == "__main__":
    import uvicorn
    # This part is for local debugging and won't be used by Zeabur with Docker
    uvicorn.run(app, host="0.0.0.0", port=8000)
