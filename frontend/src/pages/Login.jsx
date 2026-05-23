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

    // center everything
    <div className="min-h-screen flex items-center justify-center">

        {/* white card */}
        <div className="bg-white rounded-2xl shadow-md p-10 w-full max-w-md">

            <h1 className="text-3xl font-bold text-center">Login</h1>
            <p className="text-center">Enter your details to sign into account</p>

            {/* run validation with handleSubmit then call onSubmit if no errors*/}
            <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col gap-4'>

                <input

                    type="email"
                    placeholder="Enter your username/email"
                    className="border rounded px-3 py-2"
                    {...register('email', { required: 'Email is required' })}

                />

                {/* only shows if the email field has a validation error */}
                {errors.email && <p>{errors.email.message}</p>}

                <input

                type="password"
                placeholder="Password"
                className="border rounded px-3 py-2"
                {...register('password', { required: 'Password is required' })}

                />

                {/* only shows if the password field has a validation error */}
                {errors.password && <p>{errors.password.message}</p>}

                <button type="submit" className="bg-black text-white rounded py-2">Login</button>

            </form>

            <p className="text-center text-sm">

                No account? {''}
                <span onClick={() => navigate('/signup')} className="underline cursour-pointers">Sign Up</span>
            </p>

        </div>
    </div>
    
  )
}
