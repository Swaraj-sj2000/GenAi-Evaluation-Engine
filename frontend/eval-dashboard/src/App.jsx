import { useState } from 'react'
import LoginPage from './components/LoginPage'
import RegisterPage from './components/RegisterPage'
import Dashboard from './components/Dashboard'

function App() {
  const [token, setToken] = useState(null)
  const [mode, setMode] = useState('login')
  const [infoMessage, setInfoMessage] = useState('')

  const handleLoginSuccess = (receivedToken) => {
    setToken(receivedToken)
  }

  const handleLogout = () => {
    setToken(null)
    setMode('login')
    setInfoMessage('')
  }

  const handleRegisterSuccess = () => {
    setMode('login')
    setInfoMessage('Account created successfully. Please sign in.')
  }

  return (
    <div className="app-shell">
      {!token ? (
        mode === 'login' ? (
          <LoginPage
            onLoginSuccess={handleLoginSuccess}
            onSwitchMode={setMode}
            infoMessage={infoMessage}
          />
        ) : (
          <RegisterPage
            onRegisterSuccess={handleRegisterSuccess}
            onSwitchMode={setMode}
          />
        )
      ) : (
        <Dashboard token={token} onLogout={handleLogout} />
      )}
    </div>
  )
}

export default App