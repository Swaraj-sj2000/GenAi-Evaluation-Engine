import { useState, useEffect } from 'react'
import { getRuns, submitRun, triggerEval, getRunById, logout, getMe } from '../services/api'

function Dashboard({ token, onLogout }) {
    const [runs, setRuns] = useState([])
    const [prompt, setPrompt] = useState("")
    const [modelOutput, setModelOutput] = useState("")
    const [status, setStatus] = useState("")
    const [username, setUsername] = useState("")
    const [selectedRun, setSelectedRun] = useState(null)

    useEffect(() => {
        loadRuns()
        loadUser()
    }, [])

    const loadUser = async () => {
        try {
            const data = await getMe(token)
            setUsername(data.username)
        } catch (err) {
            console.error("Failed to load user")
        }
    }

    const loadRuns = async () => {
        try {
            const data = await getRuns(token)
            setRuns(data)
        } catch (err) {
            setStatus("Failed to load runs")
        }
    }

    const handleLogout = async () => {
        try {
            await logout(token)
        } catch (err) {
            console.error("Logout API failed")
        } finally {
            onLogout()
        }
    }

    const handleSubmit = async () => {
        setStatus("Submitting...")
        try {
            const run = await submitRun(token, prompt, modelOutput)
            setStatus(`Run ${run.id} created. Starting evaluation...`)
            await triggerEval(token, run.id)
            setStatus(`Evaluating run ${run.id}...`)
            pollStatus(run.id)
        } catch (err) {
            setStatus(`Error: ${err.message}`)
        }
    }

    const pollStatus = (runId) => {
        const interval = setInterval(async () => {
            try {
                const run = await getRunById(token, runId)
                setStatus(`Run ${runId} status: ${run.status}`)
                if (run.status === "completed" || run.status === "failed") {
                    clearInterval(interval)
                    loadRuns()
                }
            } catch (err) {
                clearInterval(interval)
            }
        }, 7000)
    }

    return (
        <div className="card">
            <div className="dashboard-header">
                <h1>Eval Dashboard</h1>
                <span className="username">Welcome, {username}</span>
                <button className="logout-btn" onClick={handleLogout}>Logout</button>
            </div>

            <textarea
                placeholder="Enter prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <textarea
                placeholder="Enter model output"
                value={modelOutput}
                onChange={(e) => setModelOutput(e.target.value)}
            />
            <button onClick={handleSubmit}>Submit Eval</button>
            <p>{status}</p>

            <h2>Run History</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Prompt</th>
                    </tr>
                </thead>
                <tbody>
                    {runs.map(run => (
                        <tr key={run.id} onClick={() => setSelectedRun(run)} className="clickable-row">
                            <td>{run.id}</td>
                            <td>{run.status}</td>
                            <td>{run.score ?? "pending"}</td>
                            <td>{run.prompt?.slice(0, 50)}...</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {selectedRun && (
                <div className="run-detail">
                    <h2>Run {selectedRun.id} Details</h2>
                    <p>Status: {selectedRun.status}</p>
                    <p>Score: {selectedRun.score ?? "pending"}</p>
                    <p>Correctness: {selectedRun.correctness ?? "pending"}</p>
                    <p>Completeness: {selectedRun.completeness ?? "pending"}</p>
                    <p>Clarity: {selectedRun.clarity ?? "pending"}</p>
                    <p>Model: {selectedRun.model_name}</p>
                    <button onClick={() => setSelectedRun(null)}>Close</button>
                </div>
            )}
        </div>
    )
}

export default Dashboard