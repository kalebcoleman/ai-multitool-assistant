import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const isLogin = method === "login";
    const title = isLogin ? "Welcome back" : "Create account";
    const subtitle = isLogin
        ? "Sign in to access your AI assistant"
        : "Get started with your AI assistant";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const res = await api.post(route, { username, password });
            if (isLogin) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            if (error.response?.status === 401) {
                setError("Invalid username or password");
            } else if (error.response?.data) {
                const data = error.response.data;
                const message = data.detail || data.username?.[0] || data.password?.[0] || "Something went wrong";
                setError(message);
            } else {
                setError("Unable to connect. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            {/* Background */}
            <div className="auth-bg-gradient"></div>

            {/* Logo */}
            <div className="auth-logo">
                <span className="logo-icon">⚡</span>
                <span className="logo-text">AI Multitool</span>
            </div>

            {/* Form Card */}
            <div className="auth-card">
                <div className="auth-header">
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    {error && (
                        <div className="auth-error">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <circle cx="12" cy="12" r="10" />
                                <line x1="12" y1="8" x2="12" y2="12" />
                                <line x1="12" y1="16" x2="12.01" y2="16" />
                            </svg>
                            {error}
                        </div>
                    )}

                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                            autoComplete="username"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                            autoComplete={isLogin ? "current-password" : "new-password"}
                        />
                    </div>

                    <button type="submit" className="auth-submit" disabled={loading}>
                        {loading ? <LoadingIndicator /> : isLogin ? "Sign In" : "Create Account"}
                    </button>
                </form>

                <div className="auth-footer">
                    {isLogin ? (
                        <p>
                            Don't have an account? <Link to="/register">Sign up</Link>
                        </p>
                    ) : (
                        <p>
                            Already have an account? <Link to="/login">Sign in</Link>
                        </p>
                    )}
                </div>
            </div>

            {/* Footer */}
            <div className="auth-page-footer">
                <p>Powered by Google Gemini AI</p>
            </div>
        </div>
    );
}

export default Form;