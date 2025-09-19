import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function ProtectedPage() {
    const navigate = useNavigate();

    useEffect(() => {
        const verifyToken = async () => {
            const token = locoalStorage.getItem('token');
            console.log(token)

            try {
                const response = await fetch('http://localhost:800/auth/token');
                
                if (!response.ok) {
                    throw new Error('Token verification failed');
                }
            } catch (error) {
                localStorage.removeItem('token');
                navigate('/');
            }
        };
    });
}