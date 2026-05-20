const TOKEN = import.meta.env.VITE_PALANTIR_SECRET ?? "2b303104-ac78-41c0-82b5-f037d681fbae"

export interface Job {
  id: number
  url: string
  source_type: "web" | "youtube"
  status: "pending" | "running" | "done" | "error"
  created_at: string
  completed_at: string | null
  error_msg: string | null
}

export interface OutlineListItem {
  id: number
  job_id: number
  title: string
  source_url: string
  source_type: string
  scraped_at: string
  robots_status: string
}

export interface Outline extends OutlineListItem {
  md_content: string
  file_path: string
}

const headers = { "Authorization": `Bearer ${TOKEN}`, "Content-Type": "application/json" }

export async function submitScrape(url: string): Promise<{ job_id: number; status: string }> {
  const res = await fetch(`/api/scrape`, {
    method: "POST",
    headers,
    body: JSON.stringify({ url })
  })
  if (!res.ok) throw new Error(`Scrape failed: ${res.statusText}`)
  return res.json()
}

export async function getJob(jobId: number): Promise<Job> {
  const res = await fetch(`/api/jobs/${jobId}`, { headers })
  if (!res.ok) throw new Error(`Get job failed: ${res.statusText}`)
  return res.json()
}

export async function listOutlines(): Promise<OutlineListItem[]> {
  const res = await fetch(`/api/outlines`, { headers })
  if (!res.ok) throw new Error(`List outlines failed: ${res.statusText}`)
  return res.json()
}

export async function getOutline(outlineId: number): Promise<Outline> {
  const res = await fetch(`/api/outlines/${outlineId}`, { headers })
  if (!res.ok) throw new Error(`Get outline failed: ${res.statusText}`)
  return res.json()
}

export async function downloadOutline(outlineId: number): Promise<string> {
  const res = await fetch(`/api/outlines/${outlineId}/download`, { headers })
  if (!res.ok) throw new Error(`Download failed: ${res.statusText}`)
  return res.text()
}
