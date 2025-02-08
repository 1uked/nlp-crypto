import './App.css';
import Particle from "./components/Particle"
import PromptBar from "./components/PromptBar";
import Header from "./components/Header";
import Sidebar from "./components/SideBar";
import Footer from "./components/Footer";
import React, { useState } from 'react';

function App() {
    const [response, setResponse] = useState(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const handlePromptSubmit = async (prompt) => {
        try {
            console.log('User prompt:', prompt);

            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: prompt }), // Sending the message in the body
            });

            if (!res.ok) {
                throw new Error('Failed to fetch response from server');
            }

            const data = await res.json();
            setResponse(data.reply); // Store the response in the state
        } catch (error) {
            console.error('Error during API interaction:', error);
            setResponse('An error occurred while processing your message.'); // Show error message
        }
    };

    const handleSidebarToggle = () => {
        setSidebarOpen((prev) => !prev);
    };

  return (
      <div className="App">
          <Sidebar isOpen={sidebarOpen} onToggle={handleSidebarToggle} />
          <div
              style={{
                  marginLeft: sidebarOpen ? "25%" : "50px",
                  transition: "margin-left 0.3s ease",
                  padding: "20px",
              }}
          >
              <Particle />
              <Header />
              <PromptBar onSubmitPrompt={handlePromptSubmit} />
              {response && (
                  <div>
                      <p>Response: {response}</p>
                  </div>
              )}
              <Footer />
          </div>
      </div>
  );
}

export default App;
