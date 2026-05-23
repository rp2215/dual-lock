import { useNavigate } from 'react-router-dom'

export default function Vault() {
  const navigate = useNavigate()

  return (
    <div>
      <h1>Vault</h1>
      <button onClick={() => navigate('/login')}>Logout</button>
    </div>
  )
}
