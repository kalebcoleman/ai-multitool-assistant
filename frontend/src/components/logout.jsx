// src/components/Logout.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const navigate = useNavigate();
  const currentUser = localStorage.getItem('currentUser');

  const handleLogout = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Clear session storage
      sessionStorage.removeItem(`chatHistory_${currentUser}`);
      localStorage.clear();
      navigate('/login');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default Logout;
