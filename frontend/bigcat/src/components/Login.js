import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';

function Login() {
    const [email, SetEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const validateForm = () => {
        if (!email || !password) {
            setError('Email and password are required.');
            return false;
        }
        setError('');
        return true;
    }

    const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setLoading(true);

    const formDetails = new URLSearchParams();
    formDetails.append('email', email);
    formDetails.append('password', password)

    try {
        const response = await fetch('http://localhost:8000/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formDetails,
        });

        setLoading(false);

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            navigate('/protected');
        } else {
            const errorData = await response.json();
            setError(errorData.detail || 'Authentication failed!')
        }
    } catch (error) {
        setLoading(false);
        setError('An error occurred. Please try again.')
    }
};
};



export default function LoginForm() {
    return (
        <div className='bg-white px-10 py-20 rounded-3xl w-2/3'>
            <div className='justify-center text-center select-none'>
                <h1 className='text-5xl font-semibold'>bigcat</h1>
            </div>
            <div className='mt-8'>
                <div>
                    {/* <label className='text-lg font-medium'>email</label> */}
                    <input 
                        className='w-full border-2 border-gray-100 hover:border-orange-500 transition-colors 
                                    focus:outline-none duration-700 rounded-xl p-4 mt-1 selection:bg-orange-500' 
                        placeholder='Email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div>
                    {/* <label>Password</label> */}
                    <input 
                        className='w-full border-2 border-gray-100 hover:border-orange-500 transition-colors 
                                    focus:outline-none duration-700 rounded-xl p-4 mt-1 selection:bg-orange-500'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div className='mt-8 flex justify-between items-center select-none'>
                    <div>
                        <input type='checkbox' id='remember'></input>
                        <label className='ml-2 font-medium text-base' for='remember'>Remember me</label>
                    </div>

                    <button className='font-medium text-base text-orange-500 select-none'>Forgot password</button>
                </div>
                <div className='mt8 flex flex-col gap-y-4'>
                    <button className='active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all 
                    py-2 rounded-xl mt-5 bg-orange-500 text-white text-lg font-bold'>Sign In</button>
                </div>
            </div>
        </div>
    )
}