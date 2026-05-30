import Converter from '@/components/converter'

const FORMATS = [
  'PDF', 'DOCX', 'PPTX', 'XLSX', 'XLS',
  'CSV', 'JSON', 'XML', 'HTML', 'TXT',
  'PNG', 'JPG', 'EPUB', 'ZIP',
]

export default function Home() {
  return (
    <main className='min-h-screen'>
      {/* Header */}
      <header className='border-b border-zinc-800 px-6 py-4'>
        <div className='mx-auto flex max-w-5xl items-center justify-between'>
          <div className='flex items-center gap-2'>
            <span className='text-lg font-bold tracking-tight'>MarkItDown</span>
            <span className='rounded-full bg-zinc-800 px-2 py-0.5 text-xs text-zinc-400'>web</span>
          </div>
          <a
            href='https://github.com/Chungharon/markitdown'
            target='_blank'
            rel='noopener noreferrer'
            className='text-xs text-zinc-500 transition-colors hover:text-zinc-300'
          >
            GitHub →
          </a>
        </div>
      </header>

      <div className='mx-auto max-w-5xl px-6 py-16'>
        {/* Hero */}
        <div className='mb-12 text-center'>
          <h1 className='mb-4 text-4xl font-bold tracking-tight sm:text-5xl'>
            Convert anything to{' '}
            <span className='text-emerald-400'>Markdown</span>
          </h1>
          <p className='mx-auto max-w-xl text-base text-zinc-400'>
            Upload a file and get clean, LLM-ready Markdown in seconds.
            No signup, no limits, no tracking.
          </p>

          {/* Supported formats */}
          <div className='mt-6 flex flex-wrap justify-center gap-2'>
            {FORMATS.map(fmt => (
              <span
                key={fmt}
                className='rounded-full bg-zinc-800 px-3 py-1 text-xs font-medium text-zinc-400'
              >
                {fmt}
              </span>
            ))}
          </div>
        </div>

        {/* Converter */}
        <Converter />
      </div>
    </main>
  )
}
