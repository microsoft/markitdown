from fastapi import FastAPI
from starlette.responses import JSONResponse

from markitdown_api import convert_uri, convert_text, convert_file, __about__


async def exception_not_found(request, exc):
    return JSONResponse(
        {
            'code': exc.status_code,
            'error': 'not found'
        },
        status_code=exc.status_code
    )


exception_handlers = {
    404: exception_not_found,
}

app = FastAPI(
    title="MarkItDown API",
    description="A simple API for converting URI, text, or files to Markdown format",
    version=__about__.__version__,
    exception_handlers=exception_handlers,
)

app.include_router(convert_uri.router)
app.include_router(convert_text.router)
app.include_router(convert_file.router)
