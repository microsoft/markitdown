"""
Flask backend API for MarkItDown Batch Converter
Handles file uploads, conversions, and serves the frontend
"""
import os
import sys
import uuid
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import threading
import time
import queue

# Add the markitdown package to the path
sys.path.insert(0, str(Path(__file__).parent / "packages" / "markitdown" / "src"))

from markitdown import MarkItDown

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Store conversion jobs in memory (in production, use a database)
conversion_jobs = {}
job_lock = threading.Lock()

# SSE notification system
notification_queues = {}
notification_lock = threading.Lock()

# Initialize MarkItDown
markitdown = MarkItDown()


class ConversionJob:
    def __init__(self, file_id, filename, filesize):
        self.file_id = file_id
        self.filename = filename
        self.filesize = filesize
        self.status = 'waiting'  # waiting, converting, completed, failed
        self.progress = 0
        self.error = None
        self.output_file = None
        self.created_at = time.time()


def broadcast_notification(event_type, data):
    """Send notification to all connected SSE clients"""
    with notification_lock:
        message = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        # Send to all connected clients
        for client_id, client_queue in list(notification_queues.items()):
            try:
                client_queue.put_nowait(message)
            except queue.Full:
                # Remove disconnected clients
                del notification_queues[client_id]


def notify_status_change(file_id, status, **kwargs):
    """Notify clients about status changes"""
    with job_lock:
        if file_id in conversion_jobs:
            job = conversion_jobs[file_id]
            data = {
                'file_id': file_id,
                'filename': job.filename,
                'status': status,
                'progress': job.progress,
                'error': job.error,
                'output_file': job.output_file,
                **kwargs
            }
            broadcast_notification('status_update', data)


def convert_file_async(file_id, input_path, output_path):
    """Convert file in background thread"""
    try:
        with job_lock:
            conversion_jobs[file_id].status = 'converting'
            conversion_jobs[file_id].progress = 10
        
        # Notify conversion started
        notify_status_change(file_id, 'converting', progress=10)
        
        # Perform conversion
        result = markitdown.convert(input_path)
        
        with job_lock:
            conversion_jobs[file_id].progress = 80
        
        # Notify progress
        notify_status_change(file_id, 'converting', progress=80)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        with job_lock:
            conversion_jobs[file_id].status = 'completed'
            conversion_jobs[file_id].progress = 100
            conversion_jobs[file_id].output_file = output_path.name
        
        # Notify completion immediately
        notify_status_change(file_id, 'completed', progress=100)
            
    except Exception as e:
        with job_lock:
            conversion_jobs[file_id].status = 'failed'
            conversion_jobs[file_id].error = str(e)
        
        # Notify failure immediately
        notify_status_change(file_id, 'failed', error=str(e))


@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_from_directory('.', 'code.html')


@app.route('/api/events')
def events():
    """Server-Sent Events endpoint for real-time notifications"""
    def event_stream():
        # Create a unique client ID and queue
        client_id = str(uuid.uuid4())
        client_queue = queue.Queue(maxsize=100)
        
        with notification_lock:
            notification_queues[client_id] = client_queue
        
        try:
            # Send initial connection confirmation
            yield f"event: connected\ndata: {json.dumps({'client_id': client_id})}\n\n"
            
            # Send current status of all jobs
            with job_lock:
                for job in conversion_jobs.values():
                    data = {
                        'file_id': job.file_id,
                        'filename': job.filename,
                        'status': job.status,
                        'progress': job.progress,
                        'error': job.error,
                        'output_file': job.output_file
                    }
                    yield f"event: status_update\ndata: {json.dumps(data)}\n\n"
            
            # Keep connection alive and send notifications
            while True:
                try:
                    # Wait for notification with timeout
                    message = client_queue.get(timeout=30)
                    yield message
                except queue.Empty:
                    # Send heartbeat to keep connection alive
                    yield f"event: heartbeat\ndata: {json.dumps({'timestamp': time.time()})}\n\n"
                    
        except GeneratorExit:
            # Client disconnected
            pass
        finally:
            # Clean up client queue
            with notification_lock:
                if client_id in notification_queues:
                    del notification_queues[client_id]
    
    return Response(event_stream(), mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache',
                           'Connection': 'keep-alive',
                           'Access-Control-Allow-Origin': '*'})


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            continue
        
        # Generate unique ID
        file_id = str(uuid.uuid4())
        
        # Secure filename
        original_filename = secure_filename(file.filename)
        filename = f"{file_id}_{original_filename}"
        filepath = app.config['UPLOAD_FOLDER'] / filename
        
        # Save file
        file.save(filepath)
        
        # Get file size
        filesize = filepath.stat().st_size
        
        # Create job entry
        with job_lock:
            conversion_jobs[file_id] = ConversionJob(
                file_id=file_id,
                filename=original_filename,
                filesize=filesize
            )
        
        uploaded_files.append({
            'file_id': file_id,
            'filename': original_filename,
            'filesize': filesize,
            'status': 'waiting'
        })
    
    return jsonify({'files': uploaded_files})


@app.route('/api/convert', methods=['POST'])
def convert_files():
    """Start conversion for all waiting files"""
    data = request.json
    file_ids = data.get('file_ids', [])
    
    if not file_ids:
        # Convert all waiting files
        with job_lock:
            file_ids = [
                job.file_id for job in conversion_jobs.values() 
                if job.status == 'waiting'
            ]
    
    # Start conversion threads
    for file_id in file_ids:
        with job_lock:
            if file_id not in conversion_jobs:
                continue
            
            job = conversion_jobs[file_id]
            if job.status != 'waiting':
                continue
        
        # Find input file
        input_files = list(app.config['UPLOAD_FOLDER'].glob(f"{file_id}_*"))
        if not input_files:
            continue
        
        input_path = input_files[0]
        output_path = app.config['OUTPUT_FOLDER'] / f"{file_id}_{Path(job.filename).stem}.md"
        
        # Start conversion in background thread
        thread = threading.Thread(
            target=convert_file_async,
            args=(file_id, input_path, output_path)
        )
        thread.daemon = True
        thread.start()
    
    return jsonify({'message': f'Started conversion for {len(file_ids)} files'})


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get status of all conversion jobs"""
    with job_lock:
        jobs_list = []
        for job in conversion_jobs.values():
            jobs_list.append({
                'file_id': job.file_id,
                'filename': job.filename,
                'filesize': job.filesize,
                'status': job.status,
                'progress': job.progress,
                'error': job.error,
                'output_file': job.output_file
            })
    
    return jsonify({'jobs': jobs_list})


@app.route('/api/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file from the queue"""
    with job_lock:
        if file_id not in conversion_jobs:
            return jsonify({'error': 'File not found'}), 404
        
        job = conversion_jobs[file_id]
        
        # Delete input file
        input_files = list(app.config['UPLOAD_FOLDER'].glob(f"{file_id}_*"))
        for f in input_files:
            f.unlink(missing_ok=True)
        
        # Delete output file if exists
        if job.output_file:
            output_path = app.config['OUTPUT_FOLDER'] / job.output_file
            output_path.unlink(missing_ok=True)
        
        # Remove from jobs
        del conversion_jobs[file_id]
    
    return jsonify({'message': 'File deleted successfully'})


@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download converted markdown file"""
    with job_lock:
        if file_id not in conversion_jobs:
            return jsonify({'error': 'File not found'}), 404
        
        job = conversion_jobs[file_id]
        if job.status != 'completed' or not job.output_file:
            return jsonify({'error': 'Conversion not completed'}), 400
    
    return send_from_directory(
        app.config['OUTPUT_FOLDER'],
        job.output_file,
        as_attachment=True
    )


@app.route('/api/clear', methods=['POST'])
def clear_completed():
    """Clear all completed conversions"""
    with job_lock:
        completed_ids = [
            job.file_id for job in conversion_jobs.values()
            if job.status == 'completed'
        ]
        
        for file_id in completed_ids:
            job = conversion_jobs[file_id]
            
            # Delete files
            input_files = list(app.config['UPLOAD_FOLDER'].glob(f"{file_id}_*"))
            for f in input_files:
                f.unlink(missing_ok=True)
            
            if job.output_file:
                output_path = app.config['OUTPUT_FOLDER'] / job.output_file
                output_path.unlink(missing_ok=True)
            
            del conversion_jobs[file_id]
    
    return jsonify({'message': f'Cleared {len(completed_ids)} completed jobs'})


if __name__ == '__main__':
    print("Starting MarkItDown Batch Converter Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000, threaded=True)
