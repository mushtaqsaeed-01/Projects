import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'TODO Application',
  description: 'A simple web-based TODO application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <main className="container">
          <h1 className="app-title">TODO Application</h1>
          {children}
        </main>
      </body>
    </html>
  )
}
