import { useState } from "react"
import { submitScrape } from "../api"

export function URLInput({ onSubmit }: { onSubmit: (jobId: number) => void }) {
  const [url, setUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!url.trim()) return

    setLoading(true)
    setError(null)
    try {
      const { job_id } = await submitScrape(url)
      setUrl("")
      onSubmit(job_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit URL")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-xl">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-cinzel text-stone-text mb-2">
            Place a URL in the stone...
          </label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full px-4 py-3 bg-stone-surface border border-stone-accent/30 rounded text-stone-text placeholder-stone-text/50 focus:outline-none focus:ring-2 focus:ring-stone-accent/50 font-cinzel"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-900/30 border border-red-700 rounded text-red-200 text-sm font-cinzel">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !url.trim()}
          className="w-full px-4 py-3 bg-stone-accent text-stone-bg font-cinzel font-bold rounded hover:bg-stone-accent/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "The Eye searches..." : "Gaze Into the Stone"}
        </button>
      </form>
    </div>
  )
}
