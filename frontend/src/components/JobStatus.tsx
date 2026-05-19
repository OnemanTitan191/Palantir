import { useEffect, useState } from "react"
import { getJob } from "../api"

export function JobStatus({ jobId, onComplete }: { jobId: number; onComplete: () => void }) {
  const [status, setStatus] = useState<"pending" | "running" | "done" | "error">("pending")
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const job = await getJob(jobId)
        setStatus(job.status)

        if (job.status === "done") {
          onComplete()
          clearInterval(interval)
        } else if (job.status === "error") {
          setErrorMsg(job.error_msg)
          clearInterval(interval)
        }
      } catch (err) {
        setStatus("error")
        setErrorMsg("Failed to fetch job status")
        clearInterval(interval)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [jobId, onComplete])

  if (status === "done") {
    return (
      <div className="text-center space-y-2">
        <div className="text-stone-accent font-cinzel text-lg">The stone reveals...</div>
        <div className="text-stone-text text-sm">Outline ready</div>
      </div>
    )
  }

  if (status === "error") {
    return (
      <div className="p-4 bg-red-900/30 border border-red-700 rounded">
        <div className="text-red-200 font-cinzel mb-2">The stone has gone dark.</div>
        <div className="text-red-300 text-sm">{errorMsg}</div>
      </div>
    )
  }

  return (
    <div className="text-center space-y-3">
      <div className="text-stone-accent font-cinzel text-lg animate-pulse">The Eye searches...</div>
      <div className="flex justify-center gap-1">
        <div className="w-2 h-2 bg-stone-teal rounded-full animate-bounce" style={{ animationDelay: "0s" }} />
        <div className="w-2 h-2 bg-stone-teal rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
        <div className="w-2 h-2 bg-stone-teal rounded-full animate-bounce" style={{ animationDelay: "0.4s" }} />
      </div>
    </div>
  )
}
