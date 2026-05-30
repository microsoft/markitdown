import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MarkItDown — Convert anything to Markdown',
  description: 'Upload any file — PDF, Word, Excel, PowerPoint, images and more — and get clean Markdown instantly.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en'>
      <body className='min-h-screen bg-zinc-950 text-zinc-100 antialiased'>
        {children}
      </body>
    </html>
  )
}
