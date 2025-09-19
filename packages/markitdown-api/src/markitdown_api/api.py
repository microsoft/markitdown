"""Main API implementation."""

import io
import time
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown, DocumentConverterResult

from .config import Settings
from .models import ConvertUrlRequest, ConvertResponse
from .middleware import rate_limit_middleware
from .logging import logger, setup_logging
from .metrics import metrics

# Set up logging
setup_logging()

app = FastAPI(
    title="MarkItDown API",
    description="REST API for converting various file formats to markdown",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Settings dependency
def get_settings():
    """Get API settings."""
    return Settings()


# Rate limiting dependency
async def check_rate_limit(
    request: Request, settings: Settings = Depends(get_settings)
):
    """Check rate limiting."""
    await rate_limit_middleware(request, settings)


# MarkItDown instance dependency
def get_markitdown(settings: Settings = Depends(get_settings)):
    """Get MarkItDown instance."""
    return MarkItDown(enable_plugins=settings.enable_plugins)


@app.get("/health")
async def health_check():
    """Health check endpoint with basic metrics."""
    stats = metrics.get_stats()
    return {
        "status": "ok",
        "metrics": stats,
        "version": "0.1.0",
    }


@app.get("/metrics")
async def get_metrics():
    """Detailed metrics endpoint."""
    return metrics.get_stats()


@app.post(
    "/convert/file",
    response_model=ConvertResponse,
    dependencies=[Depends(check_rate_limit)],
)
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
    md: MarkItDown = Depends(get_markitdown),
):
    """Convert an uploaded file to markdown."""
    start_time = time.time()
    success = False
    error_type = None
    
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.max_file_size:
            logger.warning(
                "file_too_large",
                file_name=file.filename,
                file_size=file_size,
                max_size=settings.max_file_size,
            )
            raise HTTPException(413, "File too large")

        logger.info(
            "converting_file",
            file_name=file.filename,
            file_size=file_size,
            content_type=file.content_type,
        )

        # Convert using MarkItDown
        result: DocumentConverterResult = md.convert_stream(
            io.BytesIO(content),
            stream_info=None,  # Let MarkItDown infer from content
        )

        logger.info(
            "file_converted",
            file_name=file.filename,
            conversion_time=time.time() - start_time,
        )
        
        success = True
        return ConvertResponse(
            markdown=result.markdown,
            text_content=result.text_content,
            metadata=result.metadata,
        )

    except HTTPException as e:
        error_type = f"http_{e.status_code}"
        raise
    except Exception as e:
        error_type = e.__class__.__name__
        logger.exception(
            "conversion_failed",
            file_name=file.filename,
            error=str(e),
        )
        raise HTTPException(400, str(e))
    finally:
        duration = time.time() - start_time
        metrics.track_request(
            endpoint="/convert/file",
            duration=duration,
            success=success,
            size=file_size if 'file_size' in locals() else 0,
            error=error_type,
        )


@app.post(
    "/convert/url",
    response_model=ConvertResponse,
    dependencies=[Depends(check_rate_limit)],
)
async def convert_url(
    request: ConvertUrlRequest,
    md: MarkItDown = Depends(get_markitdown),
):
    """Convert a URL to markdown."""
    start_time = time.time()
    success = False
    error_type = None

    try:
        logger.info(
            "converting_url",
            url=str(request.url),
        )

        result: DocumentConverterResult = md.convert(request.url)

        logger.info(
            "url_converted",
            url=str(request.url),
            conversion_time=time.time() - start_time,
        )

        success = True
        return ConvertResponse(
            markdown=result.markdown,
            text_content=result.text_content,
            metadata=result.metadata,
        )

    except Exception as e:
        error_type = e.__class__.__name__
        logger.exception(
            "conversion_failed",
            url=str(request.url),
            error=str(e),
        )
        raise HTTPException(400, str(e))
    finally:
        duration = time.time() - start_time
        metrics.track_request(
            endpoint="/convert/url",
            duration=duration,
            success=success,
            error=error_type,
        )