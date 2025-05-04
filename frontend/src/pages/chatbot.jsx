import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from "../api";
import "../styles/chatbot.css";
import { ACCESS_TOKEN } from "../constants";

const ChatBot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const currentUser = localStorage.getItem('currentUser');

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
            const data = res.data;
            setChatHistory(data);
            sessionStorage.setItem('chatHistory', JSON.stringify(data));
          }
        } catch (error) {
          console.error('Error fetching chat history:', error);
        }
      }
    };

    fetchChatHistory();
  }, [currentUser]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    const newChatHistory = [...chatHistory, { message, response: 'Sending...' }];
    setChatHistory(newChatHistory);
    setMessage('');  // Clear the message input immediately

    try {
      const token = localStorage.getItem('token'); // Get the JWT token
      const res = await api.post('/api/query/', { prompt: message }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });

      if (res.status === 401) {
        console.error('Unauthorized request');
        setLoading(false);
        return;
      }

      const data = res.data;
      const updatedChatHistory = newChatHistory.map((chat, index) => 
        index === newChatHistory.length - 1 ? { ...chat, response: data.response } : chat
      );
      setChatHistory(updatedChatHistory);

      // Save the chat history in session storage
      sessionStorage.setItem('chatHistory', JSON.stringify(updatedChatHistory));
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const clearChatHistory = async () => {
    try {
      const token = localStorage.getItem('token'); // Get the JWT token
      const res = await api.delete('/api/clear-chat-history/', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      });

      if (res.status === 204) {
        setChatHistory([]);
        sessionStorage.removeItem('chatHistory');
        alert("Chat history cleared!");
      } else {
        alert("Failed to clear chat history.");
      }
    } catch (error) {
      console.error('Error:', error);
      alert("Failed to clear chat history.");
    }
  };

  const [pdfFile, setPdfFile] = useState(null);

  const handlePDFUpload = async () => {
    if (!pdfFile) return alert("Please choose a PDF first.");
    const formData = new FormData();
    formData.append("file", pdfFile);
  
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const res = await api.post("/api/upload-pdf/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });
  
      // Show a new message in chat history
      const fileName = pdfFile.name;
      const botMessage = {
        message: `Uploaded PDF: ${fileName}`,
        response: `✅ Successfully indexed "${fileName}". You can now ask questions about its contents.`
      };
      const updatedHistory = [...chatHistory, botMessage];
      setChatHistory(updatedHistory);
      sessionStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
      setPdfFile(null);  // optional: reset file input
    } catch (err) {
      console.error(err);
      const updatedHistory = [...chatHistory, {
        message: `Upload attempt failed.`,
        response: `❌ Upload failed. Please try again.`
      }];
      setChatHistory(updatedHistory);
      sessionStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
    }
  };
  

  return (
    <div className="chatbot-container">
      <h1>Chat with Bot</h1>
      <button className="home-button" onClick={() => navigate('/')}>Home</button>
      <button className="clear-button" onClick={clearChatHistory} disabled={loading}>
        Clear Chat History
      </button>
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">
            <p><strong>You:</strong> {chat.message}</p>
            <p><strong>Bot:</strong> {chat.response}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message here"
      />
      <button className="send-button" onClick={sendMessage} disabled={loading}>
        Send
      </button>
      <div className="pdf-upload">
        <label htmlFor="file-upload" className="choose-button">Choose PDF</label>
        <input id="file-upload" type="file" accept="application/pdf" onChange={e => setPdfFile(e.target.files[0])} />
        <button className="upload-button" onClick={handlePDFUpload}>Upload PDF</button>
      </div>
    </div>
  );
};

export default ChatBot;
