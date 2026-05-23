import { useNavigate } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()

  return (
    <div>
      <h1>Login</h1>
      <button onClick={() => navigate('/vault')}>Go to Vault</button>
      <button onClick={() => navigate('/')}>Back</button>
    </div>
  )
}
