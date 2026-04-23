import os
import io
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from markitdown import MarkItDown
from markitdown._exceptions import (
    MarkItDownException,
    FileConversionException,
    UnsupportedFormatException,
)


app = FastAPI(
    title="MarkItDown Web UI",
    description="A lightweight web interface for MarkItDown file conversion",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = Path("uploads")
RESULT_DIR = Path("results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)


conversion_tasks: Dict[str, Any] = {}


@dataclass
class ConversionProgress:
    task_id: str
    filename: str
    status: str
    progress: int
    result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class ConversionResponse(BaseModel):
    task_id: str
    filename: str
    status: str
    progress: int


class ProgressResponse(BaseModel):
    task_id: str
    filename: str
    status: str
    progress: int
    error_message: Optional[str] = None


class BatchConversionResponse(BaseModel):
    tasks: List[ConversionResponse]


markitdown_instance = MarkItDown()


SUPPORTED_EXTENSIONS = [
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
    ".html", ".htm", ".csv", ".txt", ".md", ".json",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".mp3", ".wav", ".m4a", ".flac",
    ".epub", ".zip", ".msg", ".ipynb", ".xml",
]


def is_supported_format(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def get_supported_formats_message() -> str:
    formats = ", ".join(sorted(set(SUPPORTED_EXTENSIONS)))
    return f"Supported formats: {formats}"


async def convert_file_task(task_id: str, file_path: Path, filename: str):
    progress = conversion_tasks[task_id]
    
    try:
        progress.status = "converting"
        progress.progress = 10
        
        await asyncio.sleep(0.1)
        
        progress.progress = 30
        result = markitdown_instance.convert(str(file_path))
        
        progress.progress = 80
        
        result_filename = f"{task_id}.md"
        result_path = RESULT_DIR / result_filename
        
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        
        progress.result = result_filename
        progress.status = "completed"
        progress.progress = 100
        progress.completed_at = datetime.now()
        
    except UnsupportedFormatException as e:
        progress.status = "error"
        progress.error_message = f"Unsupported file format: {str(e)}. {get_supported_formats_message()}"
        progress.progress = 0
        
    except FileConversionException as e:
        progress.status = "error"
        progress.error_message = f"File conversion failed: {str(e)}"
        progress.progress = 0
        
    except MarkItDownException as e:
        progress.status = "error"
        progress.error_message = f"Conversion error: {str(e)}"
        progress.progress = 0
        
    except Exception as e:
        progress.status = "error"
        progress.error_message = f"Unexpected error: {str(e)}"
        progress.progress = 0
        
    finally:
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass


@app.get("/", response_class=HTMLResponse)
async def index():
    static_dir = Path(__file__).parent / "static"
    index_path = static_dir / "index.html"
    
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    
    return HTMLResponse(content="<h1>MarkItDown Web UI</h1><p>Static files not found.</p>")


@app.post("/api/upload", response_model=ConversionResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not is_supported_format(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {Path(file.filename).suffix}. {get_supported_formats_message()}"
        )
    
    task_id = str(uuid.uuid4())
    
    file_ext = Path(file.filename).suffix
    saved_filename = f"{task_id}{file_ext}"
    file_path = UPLOAD_DIR / saved_filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    progress = ConversionProgress(
        task_id=task_id,
        filename=file.filename,
        status="pending",
        progress=0,
    )
    conversion_tasks[task_id] = progress
    
    background_tasks.add_task(convert_file_task, task_id, file_path, file.filename)
    
    return ConversionResponse(
        task_id=task_id,
        filename=file.filename,
        status="pending",
        progress=0,
    )


@app.post("/api/upload/batch", response_model=BatchConversionResponse)
async def upload_batch_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    responses = []
    
    for file in files:
        if not file.filename:
            continue
        
        if not is_supported_format(file.filename):
            continue
        
        task_id = str(uuid.uuid4())
        
        file_ext = Path(file.filename).suffix
        saved_filename = f"{task_id}{file_ext}"
        file_path = UPLOAD_DIR / saved_filename
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        progress = ConversionProgress(
            task_id=task_id,
            filename=file.filename,
            status="pending",
            progress=0,
        )
        conversion_tasks[task_id] = progress
        
        background_tasks.add_task(convert_file_task, task_id, file_path, file.filename)
        
        responses.append(ConversionResponse(
            task_id=task_id,
            filename=file.filename,
            status="pending",
            progress=0,
        ))
    
    return BatchConversionResponse(tasks=responses)


@app.get("/api/progress/{task_id}", response_model=ProgressResponse)
async def get_progress(task_id: str):
    if task_id not in conversion_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    progress = conversion_tasks[task_id]
    
    return ProgressResponse(
        task_id=task_id,
        filename=progress.filename,
        status=progress.status,
        progress=progress.progress,
        error_message=progress.error_message,
    )


@app.get("/api/download/{task_id}")
async def download_result(task_id: str):
    if task_id not in conversion_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    progress = conversion_tasks[task_id]
    
    if progress.status != "completed" or not progress.result:
        raise HTTPException(status_code=400, detail="Conversion not completed yet")
    
    result_path = RESULT_DIR / progress.result
    
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Result file not found")
    
    original_filename = Path(progress.filename).stem
    download_filename = f"{original_filename}.md"
    
    return FileResponse(
        path=str(result_path),
        media_type="text/markdown",
        filename=download_filename,
    )


@app.get("/api/result/{task_id}")
async def get_result_content(task_id: str):
    if task_id not in conversion_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    progress = conversion_tasks[task_id]
    
    if progress.status != "completed" or not progress.result:
        raise HTTPException(status_code=400, detail="Conversion not completed yet")
    
    result_path = RESULT_DIR / progress.result
    
    if not result_path.exists():
        raise HTTPException(status_code=404, detail="Result file not found")
    
    with open(result_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return JSONResponse(content={
        "task_id": task_id,
        "filename": progress.filename,
        "content": content,
    })


@app.get("/api/formats")
async def get_supported_formats():
    return JSONResponse(content={
        "supported_extensions": sorted(list(set(SUPPORTED_EXTENSIONS))),
        "message": get_supported_formats_message(),
    })


def cleanup_old_files():
    try:
        cutoff = datetime.now().timestamp() - 3600
        
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff:
                    file_path.unlink()
        
        for file_path in RESULT_DIR.iterdir():
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff:
                    file_path.unlink()
        
        cutoff_time = datetime.now().timestamp() - 3600
        tasks_to_remove = []
        for task_id, progress in conversion_tasks.items():
            if progress.completed_at:
                if progress.completed_at.timestamp() < cutoff_time:
                    tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del conversion_tasks[task_id]
            
    except Exception:
        pass


static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
