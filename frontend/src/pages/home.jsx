import React from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/Home.css";

function Home() {
  const navigate = useNavigate();

  const handleNavigateToNotes = () => {
    navigate('/notes');
  };

  const handleNavigateToAI = () => {
    navigate('/chatbot');
  };

  const handleLogout = () => {
    const currentUser = localStorage.getItem('currentUser');
    localStorage.clear();
    navigate('/logout');
  };

  return (
    <div className="home-container">
      <h1>Welcome to the Homepage</h1>
      <div className="button-container">
        <button className="navigate-button" onClick={handleNavigateToNotes}>Go to Notes</button>
        <button className="navigate-button" onClick={handleNavigateToAI}>Go to AI Agent</button>
      </div>
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Home;
