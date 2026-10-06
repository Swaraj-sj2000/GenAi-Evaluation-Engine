import { useState, useEffect, useRef, useCallback } from 'react'
import { getRuns, submitRun, triggerEval, getRunById, deleteRun, updateRun, logout, getMe } from '../services/api'
import RunForm from './RunForm'
import RunList from './RunList'
import RunDetail from './RunDetail'

function Dashboard({ token, onLogout }) {
  const [runs, setRuns] = useState([])
  const [username, setUsername] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [selectedRun, setSelectedRun] = useState(null)
  const [loading, setLoading] = useState(false)
  const pollRef = useRef(null)

  const loadRuns = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getRuns(token)
      setRuns(data)
    } catch (err) {
      setError(err.message || 'Unable to load runs.')
    } finally {
      setLoading(false)
    }
  }, [token])

  const clearPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }, [])

  useEffect(() => {
    if (!token) return
    let cancelled = false

    Promise.all([getMe(token), getRuns(token)])
      .then(([userData, runsData]) => {
        if (cancelled) return
        setUsername(userData.username)
        setRuns(runsData)
      })
      .catch(() => {
        if (cancelled) return
        setError('Unable to load dashboard data.')
      })

    return () => {
      cancelled = true
      clearPolling()
    }
  }, [clearPolling, token])

  const handleLogout = async () => {
    try {
      await logout(token)
    } catch {
      console.warn('Logout failed, clearing local session anyway.')
    } finally {
      clearPolling()
      onLogout()
    }
  }

  const handleCreateRun = async (prompt, modelOutput) => {
    setError('')
    setMessage('Submitting run...')

    try {
      const run = await submitRun(token, prompt, modelOutput)
      setMessage(`Run #${run.id} created. Starting evaluation...`)
      await triggerEval(token, run.id)
      pollRunStatus(run.id)
    } catch (err) {
      setError(err.message || 'Failed to submit the run.')
      setMessage('')
    }
  }

  const handleDeleteRun = async (runId) => {
    setError('')
    setMessage('Deleting run...')

    try {
      await deleteRun(token, runId)
      setMessage(`Run #${runId} deleted.`)
      setSelectedRun(null)
      loadRuns()
    } catch (err) {
      setError(err.message || 'Failed to delete the run.')
      setMessage('')
    }
  }

  const handleUpdateRun = async (runId, updates) => {
    setError('')
    setMessage('Saving updates...')

    try {
      const updatedRun = await updateRun(token, runId, updates)
      setMessage(`Run #${runId} updated.`)
      setSelectedRun(updatedRun)
      loadRuns()
      return updatedRun
    } catch (err) {
      setError(err.message || 'Failed to update the run.')
      setMessage('')
      throw err
    }
  }

  const pollRunStatus = (runId) => {
    clearPolling()
    pollRef.current = setInterval(async () => {
      try {
        const run = await getRunById(token, runId)
        setMessage(`Run #${runId} status: ${run.status}`)
        if (run.status === 'completed' || run.status === 'failed') {
          clearPolling()
          setSelectedRun(run)
          loadRuns()
        }
      } catch {
        clearPolling()
        setError('Unable to refresh run status.')
      }
    }, 5000)
  }

  const activeRuns = runs.filter((run) => run.status === 'pending').length
  const completedRuns = runs.filter((run) => run.status === 'completed').length
  const failedRuns = runs.filter((run) => run.status === 'failed').length

  return (
    <div className="page-shell dashboard-page">
      <header className="topbar">
        <div>
          <p className="small-label">Logged in as</p>
          <h2>{username || 'User'}</h2>
        </div>
        <div className="topbar-actions">
          <button className="ghost-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <section className="intro-card">
        <div>
          <p className="small-label">Eval Engine</p>
          <h1>Fast GenAI evaluation, simplified</h1>
          <p className="intro-copy">
            Submit prompts and model output, then review scored evaluation runs
            with clarity, correctness, and completeness metrics.
          </p>
        </div>
      </section>

      <section className="panel-row">
        <div className="summary-card">
          <span className="summary-title">Total runs</span>
          <strong>{runs.length}</strong>
        </div>
        <div className="summary-card">
          <span className="summary-title">Pending</span>
          <strong>{activeRuns}</strong>
        </div>
        <div className="summary-card">
          <span className="summary-title">Completed</span>
          <strong>{completedRuns}</strong>
        </div>
        <div className="summary-card">
          <span className="summary-title">Failed</span>
          <strong>{failedRuns}</strong>
        </div>
      </section>

      <section className="grid-layout">
        <div className="left-panel">
          <RunForm onSubmit={handleCreateRun} loading={loading} />

          <div className="status-panel">
            {message && <div className="alert info-alert">{message}</div>}
            {error && <div className="alert error-alert">{error}</div>}
          </div>

          <div className="runs-panel">
            <div className="panel-head">
              <h3>Run history</h3>
              <button className="text-btn" onClick={loadRuns}>Refresh</button>
            </div>
            <RunList
              runs={runs}
              selectedRunId={selectedRun?.id}
              onSelect={setSelectedRun}
            />
          </div>
        </div>

        <div className="right-panel">
          <RunDetail
            key={selectedRun ? selectedRun.id : 'empty-run'}
            run={selectedRun}
            onDelete={handleDeleteRun}
            onUpdate={handleUpdateRun}
          />
        </div>
      </section>
    </div>
  )
}

export default Dashboard
