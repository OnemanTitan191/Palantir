import { useState } from "react"
import ReactMarkdown from "react-markdown"
import { Download, Copy, Check } from "lucide-react"
import { downloadOutline } from "../api"
import type { Outline } from "../api"

export function OutlineViewer({ outline }: { outline: Outline }) {
  const [copied, setCopied] = useState(false)

  async function handleDownload() {
    try {
      const content = await downloadOutline(outline.id)
      const blob = new Blob([content], { type: "text/markdown" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      const filename = outline.file_path
        ? outline.file_path.replace(/\\/g, "/").split("/").pop() ?? `outline_${outline.id}.md`
        : `outline_${outline.id}.md`
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error("Download failed:", err)
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(outline.md_content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="w-full space-y-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-cinzel text-stone-accent">{outline.title}</h2>
          <p className="text-stone-text/70 text-sm mt-1">
            {outline.source_type === "youtube" ? "🎬 YouTube" : "🌐 Web"} •{" "}
            {new Date(outline.scraped_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="p-2 bg-stone-surface hover:bg-stone-surface/80 rounded transition-colors"
            title="Copy to clipboard"
          >
            {copied ? <Check size={18} className="text-green-400" /> : <Copy size={18} className="text-stone-text" />}
          </button>
          <button
            onClick={handleDownload}
            className="p-2 bg-stone-accent hover:bg-stone-accent/90 rounded transition-colors text-stone-bg"
            title="Download markdown"
          >
            <Download size={18} />
          </button>
        </div>
      </div>

      <div className="prose prose-invert max-w-none bg-stone-surface rounded p-6 overflow-auto max-h-96">
        <ReactMarkdown
          components={{
            h1: ({ children }) => <h1 className="text-2xl font-cinzel text-stone-accent mb-4">{children}</h1>,
            h2: ({ children }) => <h2 className="text-xl font-cinzel text-stone-accent mb-3 mt-4">{children}</h2>,
            p: ({ children }) => <p className="text-stone-text mb-3 leading-relaxed">{children}</p>,
            ul: ({ children }) => <ul className="list-disc list-inside text-stone-text mb-3 space-y-1">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal list-inside text-stone-text mb-3 space-y-1">{children}</ol>,
            li: ({ children }) => <li className="text-stone-text">{children}</li>,
            code: ({ children }) => (
              <code className="bg-stone-bg px-2 py-1 rounded text-stone-accent font-mono text-sm">{children}</code>
            ),
            pre: ({ children }) => (
              <pre className="bg-stone-bg p-3 rounded overflow-x-auto mb-3">{children}</pre>
            ),
          }}
        >
          {outline.md_content}
        </ReactMarkdown>
      </div>

      <a
        href={outline.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block text-stone-accent hover:underline text-sm font-cinzel"
      >
        → View original source
      </a>
    </div>
  )
}
