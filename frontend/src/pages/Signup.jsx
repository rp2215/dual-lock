import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

export default function Signup() {

  const { register, handleSubmit, formState: { errors } } = useForm()
  const navigate = useNavigate()

  // data contains email, account password, real vault password and duress vault password
  // replace with API call later
  const onSubmit = (data) => {
    console.log(data)
    navigate('/vault')
  }

  return (

    // centre everything
    <div className="min-h-screen flex items-center justify-center">

      {/* white card */}
      <div className="bg-white rounded-2xl shadow-md p-10 w-full max-w-md">

        <h1 className="text-3xl font-bold text-center">Sign Up</h1>
        <p className="text-center">Create your account and set up your vaults</p>

        {/* run validation with handleSubmit then call onSubmit if no errors */}
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">

          <input

            type="email"
            placeholder="Email"
            className="border rounded px-3 py-2"
            {...register('email', { required: 'Email is required' })}

          />

          {errors.email && <p>{errors.email.message}</p>}

          <input

            type="password"
            placeholder="Account password"
            className="border rounded px-3 py-2"
            {...register('account_password', { required: 'Account password is required' })}

          />

          {errors.account_password && <p>{errors.account_password.message}</p>}

          <input

            type="password"
            placeholder="Real vault password"
            className="border rounded px-3 py-2"
            {...register('real_password', { required: 'Real vault password is required' })}

          />

          {errors.real_password && <p>{errors.real_password.message}</p>}

          <input

            type="password"
            placeholder="Duress vault password"
            className="border rounded px-3 py-2"
            {...register('duress_password', { required: 'Duress vault password is required' })}

          />
          
          {errors.duress_password && <p>{errors.duress_password.message}</p>}

          <button type="submit" className="bg-black text-white rounded py-2">
            Create Account
          </button>

        </form>

        <p className="text-center text-sm">
          Already have an account?{' '}
          <span onClick={() => navigate('/login')} className="underline cursor-pointer">Login</span>
        </p>

      </div>
    </div>
  )
}
