import { useState } from 'react'
import { login } from '../services/api'

function LoginPage({ onLoginSuccess, onSwitchMode, infoMessage }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await login(username.trim(), password)
      onLoginSuccess(data.token)
    } catch (err) {
      setError(err.message || 'Invalid username or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <div className="brand-block">
          <h1>Eval Engine</h1>
          <p>Login to submit and review evaluation runs.</p>
        </div>

        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button className="primary-btn" onClick={handleLogin} disabled={loading}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>

        {infoMessage && <div className="alert success-alert">{infoMessage}</div>}
        {error && <div className="alert error-alert">{error}</div>}

        <button className="text-btn" onClick={() => onSwitchMode('register')}>
          Create an account
        </button>
      </div>
    </div>
  )
}

export default LoginPage