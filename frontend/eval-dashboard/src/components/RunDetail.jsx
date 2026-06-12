import { useState, useEffect } from 'react'

function RunDetail({ run, onDelete, onUpdate }) {
  const [editMode, setEditMode] = useState(false)
  const [prompt, setPrompt] = useState('')
  const [modelOutput, setModelOutput] = useState('')
  const [modelName, setModelName] = useState('')
  const [status, setStatus] = useState('pending')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (run) {
      setEditMode(false)
      setPrompt(run.prompt || '')
      setModelOutput(run.model_output || '')
      setModelName(run.model_name || '')
      setStatus(run.status || 'pending')
      setError('')
      setSaving(false)
    }
  }, [run])

  if (!run) {
    return (
      <div className="panel-card empty-card">
        <h3>Run details</h3>
        <p>Select a run to view its evaluation details.</p>
      </div>
    )
  }

  const handleDelete = () => {
    if (!window.confirm(`Delete run #${run.id}? This cannot be undone.`)) {
      return
    }
    onDelete(run.id)
  }

  const handleSave = async () => {
    setError('')
    setSaving(true)
    try {
      await onUpdate(run.id, {
        prompt,
        model_output: modelOutput,
        model_name: modelName,
        status,
      })
      setEditMode(false)
    } catch (err) {
      setError(err?.message || 'Unable to save run updates.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="panel-card">
      <div className="panel-head">
        <div>
          <h3>Run #{run.id}</h3>
          <span className={`status-chip ${run.status}`}>{run.status}</span>
        </div>
        <div>
          <button className="ghost-btn" onClick={() => setEditMode((prev) => !prev)}>
            {editMode ? 'Cancel' : 'Edit'}
          </button>
          <button className="danger-btn" onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>

      {error && <div className="alert error-alert">{error}</div>}

      {editMode ? (
        <>
          <div className="detail-row">
            <strong>Prompt</strong>
            <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} />
          </div>
          <div className="detail-row">
            <strong>Model output</strong>
            <textarea value={modelOutput} onChange={(e) => setModelOutput(e.target.value)} />
          </div>
          <div className="detail-row">
            <strong>Model name</strong>
            <input value={modelName} onChange={(e) => setModelName(e.target.value)} />
          </div>
          <div className="detail-row">
            <strong>Status</strong>
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              <option value="pending">pending</option>
              <option value="completed">completed</option>
              <option value="failed">failed</option>
            </select>
          </div>
          <div className="detail-row" style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
            <button className="primary-btn" disabled={saving} onClick={handleSave}>
              {saving ? 'Saving...' : 'Save updates'}
            </button>
            <button className="ghost-btn" onClick={() => setEditMode(false)}>
              Cancel
            </button>
          </div>
        </>
      ) : (
        <>
          <div className="detail-row">
            <strong>Prompt</strong>
            <p>{run.prompt}</p>
          </div>
          <div className="detail-row">
            <strong>Model output</strong>
            <p>{run.model_output}</p>
          </div>
          <div className="metric-grid">
            <div>
              <span>Score</span>
              <strong>{run.score != null ? run.score.toFixed(2) : 'Pending'}</strong>
            </div>
            <div>
              <span>Correctness</span>
              <strong>{run.correctness != null ? run.correctness.toFixed(2) : 'Pending'}</strong>
            </div>
            <div>
              <span>Completeness</span>
              <strong>{run.completeness != null ? run.completeness.toFixed(2) : 'Pending'}</strong>
            </div>
            <div>
              <span>Clarity</span>
              <strong>{run.clarity != null ? run.clarity.toFixed(2) : 'Pending'}</strong>
            </div>
          </div>
          <div className="detail-row">
            <strong>Model</strong>
            <p>{run.model_name}</p>
          </div>
          <div className="detail-row">
            <strong>Reasoning</strong>
            <p>{run.reasoning || 'Pending evaluation details...'}</p>
          </div>
          <div className="detail-row">
            <strong>Created</strong>
            <p>{run.created_at ? new Date(run.created_at).toLocaleString() : 'Unknown'}</p>
          </div>
        </>
      )}
    </div>
  )
}

export default RunDetail
