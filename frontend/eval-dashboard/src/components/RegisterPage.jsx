import { useState } from 'react'
import { register } from '../services/api'

function RegisterPage({ onRegisterSuccess, onSwitchMode }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handleRegister = async () => {
    setError('')
    setSuccess('')

    if (!username.trim() || !password) {
      setError('Username and password are required.')
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setLoading(true)
    try {
      await register(username.trim(), password)
      setSuccess('Account created successfully. Please sign in.')
      setUsername('')
      setPassword('')
      setConfirmPassword('')
      onRegisterSuccess()
    } catch (err) {
      setError(err.message || 'Failed to create account.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-shell">
      <div className="auth-card">
        <div className="brand-block">
          <h1>Register</h1>
          <p>Create an account to manage evaluation runs.</p>
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

        <div className="form-group">
          <label>Confirm password</label>
          <input
            type="password"
            placeholder="Repeat password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <button
          className="primary-btn"
          onClick={handleRegister}
          disabled={loading}
        >
          {loading ? 'Creating account...' : 'Register'}
        </button>

        {success && <div className="alert success-alert">{success}</div>}
        {error && <div className="alert error-alert">{error}</div>}

        <button className="text-btn" onClick={() => onSwitchMode('login')}>
          Already have an account? Sign in
        </button>
      </div>
    </div>
  )
}

export default RegisterPage
