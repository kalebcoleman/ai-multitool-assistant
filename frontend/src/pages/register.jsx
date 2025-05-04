import React from "react";
import { Link } from "react-router-dom";
import Form from "../components/Form";
import "../styles/auth.css";

function Register() {
    return (
        <div className="auth-container">
            <Form route="/api/user/register/" method="register" />
            <p>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
}

export default Register;
