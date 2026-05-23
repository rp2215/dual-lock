import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

export default function Signup() {

    const {register, handleSubmit, formState: { errors }} = useForm()

    const navigate = useNavigate()

    // data contains email, account password, real vault password and duress vault password
    // replace with API call to validate later
    const onSubmit = (data) => {

        console.log(data)
        navigate('/vault')
    }

    return (
    <div>

        <h1>Sign Up</h1>
        
        {/* run validation with handleSubmit then call onSubmit if no errors*/}
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
                placeholder="Account password"
                {...register('account_password', { required: 'Account password is required' })}

            />

            {errors.account_password && <p>{errors.account_password.message}</p>}

            <input

                type="password"
                placeholder="Real vault password"
                {...register('real_password', { required: 'Real vault password is required' })}

            />

            {errors.real_password && <p>{errors.real_password.message}</p>}

            <input

                type="password"
                placeholder="Duress vault password"
                {...register('duress_password', { required: 'Duress vault password is required' })}

            />

            {errors.duress_password && <p>{errors.duress_password.message}</p>}

            <button type="submit">Create Account</button>

        </form>

        <button onClick={() => navigate('/login')}>Go to Login</button>
        <button onClick={() => navigate('/')}>Back</button>

    </div>
    )
}
