import { useEffect, useState } from "react"
import { listOutlines } from "../api"
import type { Outline } from "../api"
import { Archive } from "lucide-react"

export function OutlineHistory({ onSelect, selectedId, refreshKey }: { onSelect: (outline: Outline) => void; selectedId: number | null; refreshKey: number }) {
  const [outlines, setOutlines] = useState<Outline[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchOutlines() {
      try {
        const data = await listOutlines()
        setOutlines(data.sort((a, b) => new Date(b.scraped_at).getTime() - new Date(a.scraped_at).getTime()))
      } catch (err) {
        setError("Failed to load outlines")
      } finally {
        setLoading(false)
      }
    }

    fetchOutlines()
  }, [refreshKey])

  if (loading) {
    return <div className="text-stone-text/70 text-sm font-cinzel">Loading outlines...</div>
  }

  if (error) {
    return <div className="text-red-400 text-sm font-cinzel">{error}</div>
  }

  if (outlines.length === 0) {
    return (
      <div className="text-center py-8 text-stone-text/70">
        <Archive size={32} className="mx-auto mb-2 opacity-50" />
        <p className="font-cinzel">No outlines yet. Create one above.</p>
      </div>
    )
  }

  return (
    <div className="space-y-2 max-h-64 overflow-y-auto">
      <h3 className="text-sm font-cinzel text-stone-accent/70 uppercase tracking-wide mb-3">Recent Outlines</h3>
      {outlines.map((outline) => (
        <button
          key={outline.id}
          onClick={() => onSelect(outline)}
          className={`w-full text-left p-3 rounded transition-colors ${
            selectedId === outline.id
              ? "bg-stone-accent/20 border border-stone-accent"
              : "bg-stone-surface hover:bg-stone-surface/80 border border-stone-surface"
          }`}
        >
          <div className="font-cinzel text-stone-accent text-sm">{outline.title}</div>
          <div className="text-stone-text/70 text-xs mt-1">
            {outline.source_type === "youtube" ? "🎬" : "🌐"} {new Date(outline.scraped_at).toLocaleDateString()}
          </div>
        </button>
      ))}
    </div>
  )
}
