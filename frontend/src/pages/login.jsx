import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Form from "../components/Form";
import "../styles/auth.css";

function Login() {
    const navigate = useNavigate();

    const handleLogin = async (credentials) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('currentUser', credentials.username);
                localStorage.setItem('token', data.access); 
                localStorage.setItem('refreshToken', data.refresh); 
                console.log('Token stored in localStorage:', data.access);  // Debugging line
                navigate('/');
            } else {
                alert('Login failed');
            }
        } catch (error) {
            alert('Login failed');
        }
    };

    return (
        <div className="auth-container">
            <Form route="/api/token/" method="login" onSubmit={handleLogin} />
            <p>
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </div>
    );
}

export default Login;
