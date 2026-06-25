import { useState, useRef, useEffect } from 'react'
import { UploadCloud, FileText, X, Download, Copy, Settings, CheckCircle, AlertCircle, Loader2, Github } from 'lucide-react'

function App() {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isConverting, setIsConverting] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [backendUrl, setBackendUrl] = useState('https://markitdown-agent-ui.onrender.com')
  const [copied, setCopied] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const fileInputRef = useRef(null)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const urlParam = params.get('backend')
    if (urlParam) setBackendUrl(urlParam)
  }, [])

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0])
      setError(null)
      setResult(null)
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
      setError(null)
      setResult(null)
    }
  }

  const handleConvert = async () => {
    if (!file) return

    setIsConverting(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${backendUrl}/api/convert`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Server error: ${response.status}`)
      }

      const data = await response.json()
      setResult(data.markdown)
    } catch (err) {
      console.error(err)
      setError(err.message || 'An unexpected error occurred. Is the backend running?')
    } finally {
      setIsConverting(false)
    }
  }

  const handleCopy = () => {
    if (!result) return
    navigator.clipboard.writeText(result)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    if (!result) return
    const blob = new Blob([result], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    
    // Robust filename extraction to handle files with or without extensions
    let filename = 'document.md';
    if (file && file.name) {
      const parts = file.name.split('.');
      if (parts.length > 1) {
        parts.pop(); // Remove the old extension
        filename = parts.join('.') + '.md';
      } else {
        filename = file.name + '.md';
      }
    }
    
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const clearFile = () => {
    setFile(null)
    setResult(null)
    setError(null)
    if (fileInputRef.current) fileInputRef.current.value = ""
  }

  return (
    <div className="app-wrapper">
      <nav className="navbar">
        <div className="logo">
          <div className="logo-icon">M</div>
          <span>MarkItDown Web</span>
        </div>
        <button className="settings-btn" onClick={() => setShowSettings(!showSettings)} title="Settings">
          <Settings size={20} />
        </button>
      </nav>

      <main className="main-container">
        <div className="hero-section">
          <h1>Universal File Conversion</h1>
          <p>Transform PDFs, Word docs, Excel, Images, and more into clean Markdown instantly.</p>
        </div>

        {showSettings && (
          <div className="settings-dropdown slide-down">
            <label>API Backend Endpoint</label>
            <input 
              type="url" 
              value={backendUrl}
              onChange={(e) => setBackendUrl(e.target.value)}
              placeholder="https://your-api-url.com"
            />
            <p className="settings-hint">Must be a valid FastAPI backend running the MarkItDown wrapper.</p>
          </div>
        )}

        <div className={`workspace ${result ? 'split-view' : 'single-view'}`}>
          {/* Left / Top Panel - Upload & Controls */}
          <div className="card upload-card">
            <div className="card-header">
              <h2>Input Document</h2>
            </div>
            
            <div className="card-body">
              {!file ? (
                <div 
                  className={`drop-zone ${isDragging ? 'dragging' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <input 
                    type="file" 
                    className="hidden-input" 
                    ref={fileInputRef}
                    onChange={handleFileChange}
                  />
                  <div className="drop-icon-wrapper">
                    <UploadCloud size={40} className="drop-icon" />
                  </div>
                  <h3>Upload a file</h3>
                  <p>Drag and drop or click to browse</p>
                </div>
              ) : (
                <div className="file-active-state">
                  <div className="file-card">
                    <div className="file-icon">
                      <FileText size={24} />
                    </div>
                    <div className="file-details">
                      <span className="filename" title={file.name}>{file.name}</span>
                      <span className="filesize">{(file.size / 1024).toFixed(1)} KB</span>
                    </div>
                    <button className="remove-file" onClick={clearFile} title="Remove file">
                      <X size={18} />
                    </button>
                  </div>

                  <button 
                    className={`primary-btn convert-btn ${isConverting ? 'converting' : ''}`} 
                    onClick={handleConvert}
                    disabled={isConverting}
                  >
                    {isConverting ? (
                      <><Loader2 size={20} className="spin" /> Processing...</>
                    ) : (
                      'Convert to Markdown'
                    )}
                  </button>

                  {error && (
                    <div className="alert alert-error fade-in">
                      <AlertCircle size={18} />
                      <p>{error}</p>
                    </div>
                  )}
                  {result && (
                    <div className="alert alert-success fade-in">
                      <CheckCircle size={18} />
                      <p>Conversion successful!</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right / Bottom Panel - Result */}
          {result && (
            <div className="card result-card fade-in-up">
              <div className="card-header">
                <h2>Markdown Output</h2>
                <div className="action-group">
                  <button className="icon-btn" onClick={handleCopy} title="Copy code">
                    {copied ? <CheckCircle size={18} className="text-success" /> : <Copy size={18} />}
                  </button>
                  <button className="icon-btn" onClick={handleDownload} title="Download .md">
                    <Download size={18} />
                  </button>
                </div>
              </div>
              <div className="card-body no-padding">
                <pre className="code-block">
                  <code>{result}</code>
                </pre>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>
            Powered by <a href="https://github.com/microsoft/markitdown" target="_blank" rel="noreferrer">Microsoft MarkItDown</a>
          </p>
          <p className="divider">•</p>
          <p>
            UI crafted by <a href="https://github.com/gurukannan22" target="_blank" rel="noreferrer" className="author-link"><Github size={14} /> gurukannan22</a>
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
