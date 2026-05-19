import { useState } from "react"
import { Eye } from "lucide-react"
import { URLInput } from "./components/URLInput"
import { JobStatus } from "./components/JobStatus"
import { OutlineViewer } from "./components/OutlineViewer"
import { OutlineHistory } from "./components/OutlineHistory"
import { listOutlines, getOutline } from "./api"
import type { Outline, OutlineListItem } from "./api"

function App() {
  const [currentJobId, setCurrentJobId] = useState<number | null>(null)
  const [selectedOutline, setSelectedOutline] = useState<Outline | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  function handleJobSubmitted(jobId: number) {
    setCurrentJobId(jobId)
    setSelectedOutline(null)
  }

  async function handleJobComplete() {
    setCurrentJobId(null)
    setRefreshKey(k => k + 1)
    try {
      const outlines = await listOutlines()
      if (outlines.length > 0) {
        const latest = outlines.sort((a, b) => new Date(b.scraped_at).getTime() - new Date(a.scraped_at).getTime())[0]
        const full = await getOutline(latest.id)
        setSelectedOutline(full)
      }
    } catch {}
  }

  async function handleSelectOutline(outline: OutlineListItem) {
    try {
      const full = await getOutline(outline.id)
      setSelectedOutline(full)
    } catch {
      // full outline fetch failed — don't render partial object without md_content
    }
  }

  return (
    <div className="min-h-screen bg-stone-bg text-stone-text font-cinzel">
      {/* Header */}
      <header className="border-b border-stone-surface/50 py-8">
        <div className="max-w-4xl mx-auto px-4 flex items-center gap-3 justify-center">
          <Eye size={32} className="text-stone-accent" />
          <h1 className="text-4xl font-bold text-center">
            <span className="text-stone-accent">THE PALANTÍR</span>
            <span className="block text-lg text-stone-text/70 font-normal">See All, Know All</span>
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="grid grid-cols-3 gap-8">
          {/* Left: Input & Status */}
          <div className="col-span-3 lg:col-span-2 space-y-8">
            {/* URL Input */}
            <section>
              <URLInput onSubmit={handleJobSubmitted} />
            </section>

            {/* Job Status */}
            {currentJobId && (
              <section className="bg-stone-surface rounded-lg p-6 border border-stone-accent/20">
                <JobStatus jobId={currentJobId} onComplete={handleJobComplete} />
              </section>
            )}

            {/* Outline Viewer */}
            {selectedOutline && (
              <section className="bg-stone-surface rounded-lg p-6 border border-stone-accent/20">
                <OutlineViewer outline={selectedOutline} />
              </section>
            )}

            {/* Empty State */}
            {!currentJobId && !selectedOutline && (
              <section className="text-center py-12 text-stone-text/70">
                <p className="font-cinzel text-lg">Place a URL above to begin.</p>
                <p className="text-sm mt-2">Web pages, YouTube videos, tutorials—the stone sees all.</p>
              </section>
            )}
          </div>

          {/* Right: History Sidebar */}
          <div className="col-span-3 lg:col-span-1">
            <div className="sticky top-8 bg-stone-surface rounded-lg p-4 border border-stone-accent/20">
              <OutlineHistory onSelect={handleSelectOutline} selectedId={selectedOutline?.id ?? null} refreshKey={refreshKey} />
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-stone-surface/50 mt-16 py-8 text-center text-stone-text/50 text-sm">
        <p>Palantír v1.0 • Gaze into the stone</p>
      </footer>
    </div>
  )
}

export default App
