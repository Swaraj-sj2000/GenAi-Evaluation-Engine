import { useState } from 'react'

function RunForm({ onSubmit, loading }) {
  const [prompt, setPrompt] = useState('')
  const [modelOutput, setModelOutput] = useState('')

  const handleSubmit = async () => {
    if (!prompt.trim() || !modelOutput.trim()) return
    await onSubmit(prompt.trim(), modelOutput.trim())
    setPrompt('')
    setModelOutput('')
  }

  return (
    <div className="panel-card">
      <div className="panel-head">
        <h3>New evaluation</h3>
      </div>
      <label>
        Prompt
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type the prompt or test case here"
        />
      </label>
      <label>
        Model output
        <textarea
          value={modelOutput}
          onChange={(e) => setModelOutput(e.target.value)}
          placeholder="Paste the model-generated response here"
        />
      </label>
      <button className="primary-btn" onClick={handleSubmit} disabled={loading || !prompt || !modelOutput}>
        {loading ? 'Submitting...' : 'Submit evaluation'}
      </button>
    </div>
  )
}

export default RunForm
