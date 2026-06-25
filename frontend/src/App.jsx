import { useState, useRef, useEffect } from 'react'
import { UploadCloud, FileType, X, Download, Copy, Settings, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

function App() {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isConverting, setIsConverting] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [backendUrl, setBackendUrl] = useState('http://localhost:8000') // Default for local
  const [copied, setCopied] = useState(false)
  const fileInputRef = useRef(null)

  // Extract from query params if available (for production)
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
    // remove extension and add .md
    const filename = file ? file.name.split('.').slice(0, -1).join('.') + '.md' : 'document.md'
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="container">
      <header>
        <h1>MarkItDown</h1>
        <p className="subtitle">Convert almost any document to Markdown instantly.</p>
      </header>

      <main className="main-content">
        {/* Left Panel: Upload */}
        <section className="panel">
          <div className="panel-header">
            <h2 className="panel-title">
              <UploadCloud size={24} className="text-accent" style={{ color: 'var(--accent-color)' }} />
              Upload Document
            </h2>
          </div>

          <div 
            className={`upload-area ${isDragging ? 'drag-active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input 
              type="file" 
              className="file-input" 
              ref={fileInputRef}
              onChange={handleFileChange}
            />
            <UploadCloud size={48} className="upload-icon" />
            <p className="upload-text">Click or drag & drop a file</p>
            <p className="upload-hint">Supports PDF, PPTX, DOCX, XLSX, Images, HTML, CSV, and more.</p>
          </div>

          {file && (
            <div className="file-info">
              <div className="file-name">
                <FileType size={20} style={{ color: 'var(--accent-color)' }} />
                <span>{file.name}</span>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <button className="remove-btn" onClick={() => setFile(null)}>
                <X size={18} />
              </button>
            </div>
          )}

          <div className="settings-panel">
            <h3 className="settings-title">
              <Settings size={16} style={{ display: 'inline', marginRight: '4px', verticalAlign: '-3px' }} /> 
              Configuration
            </h3>
            <div className="setting-row">
              <label className="input-label">Backend API URL</label>
              <input 
                type="text" 
                className="text-input" 
                value={backendUrl}
                onChange={(e) => setBackendUrl(e.target.value)}
                placeholder="https://your-render-url.onrender.com"
              />
            </div>
          </div>

          <button 
            className="convert-btn" 
            onClick={handleConvert}
            disabled={!file || isConverting}
          >
            {isConverting ? (
              <>
                <Loader2 size={20} className="spinner" />
                Converting...
              </>
            ) : (
              <>
                Convert to Markdown
              </>
            )}
          </button>

          {error && (
            <div className="status-message status-error">
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}
          {result && (
            <div className="status-message status-success">
              <CheckCircle size={18} />
              <span>Conversion successful!</span>
            </div>
          )}
        </section>

        {/* Right Panel: Preview */}
        <section className="panel">
          <div className="panel-header">
            <h2 className="panel-title">
              Markdown Output
            </h2>
            <div className="action-btns">
              <button 
                className="icon-btn" 
                onClick={handleCopy} 
                disabled={!result}
                title="Copy to clipboard"
                style={{ opacity: !result ? 0.5 : 1, cursor: !result ? 'not-allowed' : 'pointer' }}
              >
                {copied ? <CheckCircle size={18} color="var(--success-color)" /> : <Copy size={18} />}
              </button>
              <button 
                className="icon-btn" 
                onClick={handleDownload} 
                disabled={!result}
                title="Download .md file"
                style={{ opacity: !result ? 0.5 : 1, cursor: !result ? 'not-allowed' : 'pointer' }}
              >
                <Download size={18} />
              </button>
            </div>
          </div>

          <div className="preview-area">
            {result ? (
              result
            ) : (
              <div className="preview-placeholder">
                <FileType size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                <p>Your generated markdown will appear here.</p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
