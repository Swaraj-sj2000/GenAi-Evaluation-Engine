import { useState } from 'react'
import LoginPage from './components/LoginPage'
import Dashboard from './components/Dashboard'

function App() {
    const [token, setToken] = useState(null)

    const handleLoginSuccess = (receivedToken) => {
        setToken(receivedToken)
    }
 const handleLogout = () => {
        setToken(null)
    }
    if (!token) {
        return <LoginPage onLoginSuccess={handleLoginSuccess} />
    }

    return <Dashboard token={token} onLogout={handleLogout} />}

export default App