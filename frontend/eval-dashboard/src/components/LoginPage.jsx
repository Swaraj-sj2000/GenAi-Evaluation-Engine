import { useState } from 'react'
import { login } from '../services/api'

function LoginPage({ onLoginSuccess }) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)

    const handleLogin = async () => {
        setLoading(true)
        setError("")
        try {
            const data = await login(username, password)
            onLoginSuccess(data.token)
        } catch (err) {
            setError("Invalid username or password")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="card">
            <h1>Eval Engine</h1>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin} disabled={loading}>
                {loading ? "Logging in..." : "Login"}
            </button>
            {error && <p className="error">{error}</p>}
        </div>
    )
}

export default LoginPage