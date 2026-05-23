import { useNavigate } from 'react-router-dom'

export default function Signup() {
  const navigate = useNavigate()

  return (
    <div>
      <h1>Sign Up</h1>
      <button onClick={() => navigate('/login')}>Go to Login</button>
      <button onClick={() => navigate('/')}>Back</button>
    </div>
  )
}
