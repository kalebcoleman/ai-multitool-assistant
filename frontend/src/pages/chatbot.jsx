import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from "../api";
import "../styles/chatbot.css";
import { ACCESS_TOKEN } from "../constants";

const ChatBot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pdfFile, setPdfFile] = useState(null);
  const navigate = useNavigate();
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to the latest message
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  // Fetch chat history on mount
  useEffect(() => {
    const fetchChatHistory = async () => {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (token) {
        try {
          const res = await api.get('/api/chat-history/', {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
          });
          if (res.status === 200) {
            setChatHistory(res.data);
          }
        } catch (error) {
          console.error('Error fetching chat history:', error);
        }
      }
    };
    fetchChatHistory();
  }, []);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    setLoading(true);
    const userMessage = message.trim();
    const newChatHistory = [...chatHistory, { message: userMessage, response: null, isLoading: true }];
    setChatHistory(newChatHistory);
    setMessage('');

    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const res = await api.post('/api/query/', { prompt: userMessage }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });

      if (res.status === 200 || res.status === 201) {
        const updatedChatHistory = newChatHistory.map((chat, index) =>
          index === newChatHistory.length - 1
            ? { ...chat, response: res.data.response, isLoading: false }
            : chat
        );
        setChatHistory(updatedChatHistory);
      }
    } catch (error) {
      console.error('Error:', error);
      const updatedChatHistory = newChatHistory.map((chat, index) =>
        index === newChatHistory.length - 1
          ? { ...chat, response: 'Sorry, something went wrong. Please try again.', isLoading: false, isError: true }
          : chat
      );
      setChatHistory(updatedChatHistory);
    }
    setLoading(false);
    inputRef.current?.focus();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChatHistory = async () => {
    if (!window.confirm('Are you sure you want to clear all chat history?')) return;

    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const res = await api.delete('/api/clear-chat-history/', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });

      if (res.status === 204) {
        setChatHistory([]);
      }
    } catch (error) {
      console.error('Error clearing chat history:', error);
    }
  };

  const handlePDFUpload = async () => {
    if (!pdfFile) return;

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      await api.post("/api/upload-pdf/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });

      const botMessage = {
        message: `📄 Uploaded: ${pdfFile.name}`,
        response: `✅ Successfully indexed "${pdfFile.name}". You can now ask questions about its contents.`
      };
      setChatHistory([...chatHistory, botMessage]);
      setPdfFile(null);
    } catch (err) {
      console.error(err);
      setChatHistory([...chatHistory, {
        message: `📄 Upload: ${pdfFile.name}`,
        response: `❌ Upload failed. Please try again.`,
        isError: true
      }]);
    }
  };

  return (
    <div className="chatbot-page">
      {/* Header */}
      <header className="chatbot-header">
        <button className="btn-icon" onClick={() => navigate('/')} title="Go Home">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9,22 9,12 15,12 15,22" />
          </svg>
        </button>
        <h1 className="chatbot-title">
          <span className="title-icon">🤖</span>
          AI Assistant
        </h1>
        <div className="header-actions">
          <button className="btn-icon btn-danger-ghost" onClick={clearChatHistory} title="Clear History">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="3,6 5,6 21,6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            </svg>
          </button>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="chat-container">
        <div className="chat-messages">
          {chatHistory.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">💬</div>
              <h2>Start a conversation</h2>
              <p>Ask me anything! I can help with weather, stocks, crypto, news, and answer questions about your PDFs.</p>
            </div>
          ) : (
            chatHistory.map((chat, index) => (
              <div key={index} className="message-pair animate-fade-in">
                {/* User Message */}
                <div className="message user-message">
                  <div className="message-content">
                    <p>{chat.message}</p>
                  </div>
                  <div className="message-avatar user-avatar">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                      <circle cx="12" cy="7" r="4" />
                    </svg>
                  </div>
                </div>

                {/* Bot Message */}
                <div className="message bot-message">
                  <div className="message-avatar bot-avatar">
                    <span>🤖</span>
                  </div>
                  <div className={`message-content ${chat.isError ? 'error' : ''}`}>
                    {chat.isLoading ? (
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    ) : (
                      <p>{chat.response}</p>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
          <div ref={chatEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          {/* PDF Upload */}
          <div className="pdf-upload-section">
            <label htmlFor="pdf-upload" className="btn-icon" title="Upload PDF">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
              </svg>
            </label>
            <input
              id="pdf-upload"
              type="file"
              accept="application/pdf"
              onChange={e => setPdfFile(e.target.files[0])}
              style={{ display: 'none' }}
            />
            {pdfFile && (
              <div className="pdf-selected">
                <span className="pdf-name">{pdfFile.name}</span>
                <button className="btn btn-primary btn-sm" onClick={handlePDFUpload}>
                  Upload
                </button>
                <button className="btn-icon btn-sm" onClick={() => setPdfFile(null)}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
            )}
          </div>

          {/* Message Input */}
          <div className="message-input-wrapper">
            <textarea
              ref={inputRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Send a message..."
              rows="1"
              disabled={loading}
            />
            <button
              className="send-button"
              onClick={sendMessage}
              disabled={loading || !message.trim()}
            >
              {loading ? (
                <div className="spinner"></div>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22,2 15,22 11,13 2,9" />
                </svg>
              )}
            </button>
          </div>
        </div>
        <p className="disclaimer">AI can make mistakes. Consider checking important information.</p>
      </div>
    </div>
  );
};

export default ChatBot;
