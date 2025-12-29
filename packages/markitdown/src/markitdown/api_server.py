
import io
import uvicorn
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

        # Get file content
        file_content = await file.read()
        
        # Create StreamInfo from the uploaded file
        stream_info = StreamInfo.from_bytes(file_content, source_filename=file.filename)

        # Perform the conversion
        result = md.convert(stream_info=stream_info)

        # Return the markdown content
        return Response(content=result.markdown, media_type="text/markdown")

    except Exception as e:
        # Basic error handling
        return Response(
            content=f"An error occurred during conversion: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )

def serve(host="0.0.0.0", port=8000):
    """
    Starts the uvicorn server for the FastAPI application.
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    serve()
