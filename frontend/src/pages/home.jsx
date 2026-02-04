import React from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/Home.css";

function Home() {
  const navigate = useNavigate();

  const features = [
    {
      id: 'chatbot',
      icon: '🤖',
      title: 'AI Assistant',
      description: 'Chat with an intelligent AI powered by Google Gemini. Ask about weather, stocks, crypto, news, and more.',
      path: '/chatbot',
      color: 'green'
    },
    {
      id: 'notes',
      icon: '📝',
      title: 'Notes',
      description: 'Create and manage your personal notes. Keep track of important information and ideas.',
      path: '/notes',
      color: 'purple'
    }
  ];

  const handleLogout = () => {
    localStorage.clear();
    navigate('/logout');
  };

  return (
    <div className="home-page">
      {/* Background gradient */}
      <div className="home-bg-gradient"></div>

      {/* Header */}
      <header className="home-header">
        <div className="logo">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">AI Multitool</span>
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16,17 21,12 16,7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          Logout
        </button>
      </header>

      {/* Main Content */}
      <main className="home-main">
        <div className="welcome-section">
          <h1>Welcome back! 👋</h1>
          <p>What would you like to do today?</p>
        </div>

        <div className="features-grid">
          {features.map((feature) => (
            <button
              key={feature.id}
              className={`feature-card feature-${feature.color}`}
              onClick={() => navigate(feature.path)}
            >
              <div className="feature-icon">{feature.icon}</div>
              <div className="feature-content">
                <h2>{feature.title}</h2>
                <p>{feature.description}</p>
              </div>
              <div className="feature-arrow">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="5" y1="12" x2="19" y2="12" />
                  <polyline points="12,5 19,12 12,19" />
                </svg>
              </div>
            </button>
          ))}
        </div>

        {/* Quick Tips */}
        <div className="tips-section">
          <h3>💡 Quick Tips</h3>
          <ul>
            <li>Ask the AI about real-time stock prices and crypto</li>
            <li>Upload PDFs to ask questions about their content</li>
            <li>Get weather updates for any city worldwide</li>
          </ul>
        </div>
      </main>

      {/* Footer */}
      <footer className="home-footer">
        <p>Powered by Google Gemini AI</p>
      </footer>
    </div>
  );
}

export default Home;
