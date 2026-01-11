# MarkItDown Batch Converter Web Interface

A modern web-based batch converter for MarkItDown with real-time notifications and drag-and-drop functionality.

## 🌟 Features

- **Modern Web UI**: Clean, responsive interface built with TailwindCSS
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Batch Processing**: Convert multiple files simultaneously
- **Real-Time Updates**: Server-Sent Events (SSE) for instant completion notifications
- **Progress Tracking**: Live progress bars and status indicators
- **File Management**: Easy queue management with download/delete options
- **Toast Notifications**: Elegant user feedback system
- **Dark/Light Theme**: Automatic theme detection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask
- MarkItDown library

### Installation

1. Install dependencies:
```bash
pip install -r requirements-server.txt
```

2. Start the server:
```bash
python server.py
```

3. Open your browser to: `http://localhost:5000`

## 🏗️ Architecture

### Backend (Flask)
- **RESTful API** for file operations
- **Server-Sent Events** for real-time notifications
- **Background threading** for non-blocking conversions
- **Secure file handling** with proper validation

### Frontend (Vanilla JS)
- **EventSource API** for SSE connection
- **Responsive design** with TailwindCSS
- **Real-time UI updates** without polling
- **Progressive enhancement** approach

## 📡 Real-Time System

Instead of traditional polling, this implementation uses **Server-Sent Events (SSE)**:

```javascript
// Frontend listens for real-time updates
eventSource.addEventListener('status_update', function(e) {
    const data = JSON.parse(e.data);
    updateFileStatus(data); // Instant UI update
});
```

```python
# Backend sends immediate notifications
def notify_status_change(file_id, status):
    broadcast_notification('status_update', {
        'file_id': file_id,
        'status': status
    })
```

## 🎯 Benefits Over Polling

| Aspect | Polling | SSE (This Implementation) |
|--------|---------|---------------------------|
| **Latency** | 200-500ms delay | Instant (0ms) |
| **Server Load** | High (constant requests) | Low (push-only) |
| **Bandwidth** | Wasteful | Efficient |
| **User Experience** | Delayed updates | Real-time feedback |

## 📁 File Structure

```
├── server.py              # Flask backend with SSE
├── code.html             # Web interface
├── requirements-server.txt # Python dependencies
├── start_converter.bat   # Windows startup script
├── uploads/              # Temporary file storage
└── outputs/              # Converted markdown files
```

## 🔧 API Endpoints

- `GET /` - Serve web interface
- `POST /api/upload` - Upload files
- `POST /api/convert` - Start batch conversion
- `GET /api/status` - Get current job status
- `GET /api/events` - SSE endpoint for real-time updates
- `GET /api/download/<id>` - Download converted file
- `DELETE /api/delete/<id>` - Remove file from queue

## 🎨 UI Components

- **File Drop Zone**: Visual drag-and-drop area
- **Conversion Queue**: Real-time file status list
- **Progress Bar**: Overall conversion progress
- **Toast Notifications**: Success/error messages
- **Live Indicator**: Connection status display

## 🔒 Security Features

- **Secure filename handling** with werkzeug
- **File size limits** (100MB max)
- **Input validation** on all endpoints
- **Error handling** with proper HTTP status codes

## 🚀 Performance Optimizations

- **Background threading** for non-blocking conversions
- **SSE connection pooling** for multiple clients
- **Efficient file handling** with streaming
- **Auto-cleanup** of temporary files

## 🤝 Contributing

This batch converter extends MarkItDown's capabilities while maintaining compatibility with the core library. It adds a user-friendly web interface without modifying the original conversion logic.

## 📄 License

Follows the same license as the main MarkItDown project.
