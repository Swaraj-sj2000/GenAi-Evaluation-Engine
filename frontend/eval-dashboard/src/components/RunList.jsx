function statusClass(status) {
  if (status === 'completed') return 'status-chip completed'
  if (status === 'failed') return 'status-chip failed'
  if (status === 'pending') return 'status-chip pending'
  return 'status-chip neutral'
}

function RunList({ runs, selectedRunId, onSelect }) {
  if (!runs.length) {
    return <div className="empty-state">No runs yet. Submit one to begin evaluation.</div>
  }

  return (
    <div className="run-list-wrapper">
      <table className="run-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Score</th>
            <th>Prompt</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr
              key={run.id}
              className={run.id === selectedRunId ? 'selected-row' : 'clickable-row'}
              onClick={() => onSelect(run)}
            >
              <td>{run.id}</td>
              <td>
                <span className={statusClass(run.status)}>{run.status || 'pending'}</span>
              </td>
              <td>{run.score != null ? run.score.toFixed(2) : '—'}</td>
              <td>{run.prompt?.slice(0, 70) || ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RunList
