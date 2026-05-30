'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Copy, Download, Loader2, X, CheckCircle } from 'lucide-react'

type Result = {
  markdown: string
  filename: string
  format: string
  characters: number
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

export default function Converter() {
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const convert = useCallback(async (file: File) => {
    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_BASE}/api/convert`, {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail ?? 'Conversion failed.')
      }

      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop: (files) => files[0] && convert(files[0]),
    multiple: false,
    maxSize: 10 * 1024 * 1024,
  })

  const handleCopy = async () => {
    if (!result) return
    await navigator.clipboard.writeText(result.markdown)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    if (!result) return
    const blob = new Blob([result.markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = result.filename.replace(/\.[^.]+$/, '.md')
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className='space-y-6'>
      {/* Drop zone */}
      {!result && (
        <div
          {...getRootProps()}
          className={`flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-8 py-20 text-center transition-colors ${
            isDragActive
              ? 'border-emerald-400 bg-emerald-400/5'
              : 'border-zinc-700 bg-zinc-900 hover:border-zinc-500 hover:bg-zinc-800/50'
          }`}
        >
          <input {...getInputProps()} />
          {loading ? (
            <div className='flex flex-col items-center gap-3'>
              <Loader2 className='h-10 w-10 animate-spin text-emerald-400' />
              <p className='text-sm text-zinc-400'>
                Converting <span className='text-zinc-200'>{acceptedFiles[0]?.name}</span>…
              </p>
            </div>
          ) : (
            <div className='flex flex-col items-center gap-3'>
              <div className='flex h-14 w-14 items-center justify-center rounded-2xl bg-zinc-800'>
                <Upload className='h-6 w-6 text-zinc-400' />
              </div>
              <div>
                <p className='font-medium text-zinc-200'>
                  {isDragActive ? 'Drop it here' : 'Drag & drop your file'}
                </p>
                <p className='mt-1 text-sm text-zinc-500'>
                  or <span className='text-emerald-400 underline underline-offset-2'>browse</span> to choose — max 10 MB
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className='flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400'>
          <X className='mt-0.5 h-4 w-4 shrink-0' />
          <span>{error}</span>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className='space-y-4'>
          {/* Result header */}
          <div className='flex flex-wrap items-center justify-between gap-3 rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-3'>
            <div className='flex items-center gap-3'>
              <div className='flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-400/10'>
                <FileText className='h-4 w-4 text-emerald-400' />
              </div>
              <div>
                <p className='text-sm font-medium text-zinc-200'>{result.filename}</p>
                <p className='text-xs text-zinc-500'>
                  {result.characters.toLocaleString()} characters · .{result.format} → .md
                </p>
              </div>
              <CheckCircle className='h-4 w-4 text-emerald-400' />
            </div>
            <div className='flex items-center gap-2'>
              <button
                onClick={handleCopy}
                className='flex items-center gap-1.5 rounded-lg bg-zinc-800 px-3 py-1.5 text-xs font-medium text-zinc-300 transition-colors hover:bg-zinc-700'
              >
                <Copy className='h-3.5 w-3.5' />
                {copied ? 'Copied!' : 'Copy'}
              </button>
              <button
                onClick={handleDownload}
                className='flex items-center gap-1.5 rounded-lg bg-zinc-800 px-3 py-1.5 text-xs font-medium text-zinc-300 transition-colors hover:bg-zinc-700'
              >
                <Download className='h-3.5 w-3.5' />
                Download .md
              </button>
              <button
                onClick={handleReset}
                className='flex items-center gap-1.5 rounded-lg bg-zinc-800 px-3 py-1.5 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-700'
              >
                <X className='h-3.5 w-3.5' />
                New file
              </button>
            </div>
          </div>

          {/* Markdown output */}
          <div className='overflow-hidden rounded-xl border border-zinc-800'>
            <div className='border-b border-zinc-800 bg-zinc-900 px-4 py-2'>
              <span className='text-xs font-medium text-zinc-500'>output.md</span>
            </div>
            <pre className='max-h-[60vh] overflow-auto bg-zinc-950 p-6 text-sm leading-relaxed text-zinc-300 whitespace-pre-wrap'>
              {result.markdown}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}