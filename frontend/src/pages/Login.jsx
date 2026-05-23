import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

export default function Login() {

  const { register, handleSubmit, formState: { errors } } = useForm()

  const navigate = useNavigate()

  // only called when form is submitted and valid
  // data is user typed email and password
  // navigates to vault for now will replace later with API call to validate details
  const onSubmit = (data) => {
    console.log(data)
    navigate('/vault')
  }

  return (
    <div>

      <h1>Login</h1>

      {/* run validation with handleSubmit then call onSubmit if no erros*/}
      <form onSubmit={handleSubmit(onSubmit)}>

        <input

          type="email"
          placeholder="Email"
          {...register('email', { required: 'Email is required' })}

        />

        {/* only shows if the email field has a validation error */}
        {errors.email && <p>{errors.email.message}</p>}

        <input

          type="password"
          placeholder="Password"
          {...register('password', { required: 'Password is required' })}

        />

        {/* only shows if the password field has a validation error */}
        {errors.password && <p>{errors.password.message}</p>}

        <button type="submit">Login</button>

      </form>

      <button onClick={() => navigate('/')}>Back</button>
    </div>
  )
}
