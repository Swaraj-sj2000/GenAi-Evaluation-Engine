function RunDetail({ run, onDelete }) {
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

  return (
    <div className="panel-card">
      <div className="panel-head">
        <div>
          <h3>Run #{run.id}</h3>
          <span className={`status-chip ${run.status}`}>{run.status}</span>
        </div>
        <button className="danger-btn" onClick={handleDelete}>
          Delete
        </button>
      </div>

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
    </div>
  )
}

export default RunDetail
