// App.js
import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import Particle from "./components/Particle";
import PromptBar from "./components/PromptBar";
import Header from "./components/Header";
import Sidebar from "./components/SideBar";
import Footer from "./components/Footer";
import { Box, Paper, Typography, Collapse, Link } from '@mui/material';

function App() {
  // Lazy initialization: try to load sessions from localStorage immediately.
  const [chatSessions, setChatSessions] = useState(() => {
    const stored = localStorage.getItem("chatSessions");
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (error) {
        console.error("Error parsing stored sessions:", error);
      }
    }
    return [];
  });
  const [activeChatId, setActiveChatId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);

  // On mount (or when chatSessions changes), set up the active chat:
  useEffect(() => {
    if (chatSessions.length === 0) {
      // If no sessions, create a new one.
      createNewChat();
    } else if (!activeChatId) {
      // Otherwise, if there are sessions but no active chat is selected, select the most recent one.
      setActiveChatId(chatSessions[chatSessions.length - 1].id);
    }
  }, [chatSessions, activeChatId]);

  // Save sessions to localStorage whenever they change.
  useEffect(() => {
    localStorage.setItem("chatSessions", JSON.stringify(chatSessions));
  }, [chatSessions]);

  // Creates a new chat session.
  const createNewChat = () => {
    const newChat = {
      id: Date.now(), // Use timestamp as a simple unique ID.
      title: `Chat ${chatSessions.length + 1}`,
      messages: []
    };
    setChatSessions(prev => [...prev, newChat]);
    setActiveChatId(newChat.id);
  };

  // Helper: update the messages of the active chat session.
  const updateActiveChatMessages = (newMessages) => {
    setChatSessions(prev =>
      prev.map(chat => chat.id === activeChatId ? { ...chat, messages: newMessages } : chat)
    );
  };

  // Delete a chat session.
  const handleDeleteChat = (id) => {
    setChatSessions(prev => {
      const updated = prev.filter(chat => chat.id !== id);
      // If the deleted session was active, choose another session or create a new one.
      if (activeChatId === id) {
        if (updated.length > 0) {
          setActiveChatId(updated[updated.length - 1].id);
        } else {
          createNewChat();
        }
      }
      return updated;
    });
  };

  // Called when the user submits a prompt.
  const handlePromptSubmit = async (prompt) => {
    const activeChat = chatSessions.find(chat => chat.id === activeChatId);
    if (!activeChat) return;

    // Append the user's message.
    const newHistory = [...activeChat.messages, { role: 'user', text: prompt }];
    updateActiveChatMessages(newHistory);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Send the prompt along with the current conversation history.
        body: JSON.stringify({ message: prompt, history: newHistory }),
      });
      if (!res.ok) throw new Error('Failed to fetch response from server');
      const data = await res.json();
      const finalHistory = [...newHistory, { role: 'assistant', text: data.reply }];
      updateActiveChatMessages(finalHistory);
    } catch (error) {
      console.error('Error during API interaction:', error);
      const finalHistory = [
        ...newHistory,
        { role: 'assistant', text: 'An error occurred while processing your message.' }
      ];
      updateActiveChatMessages(finalHistory);
    }
  };

  const handleSidebarToggle = () => {
    setSidebarOpen(prev => !prev);
  };

  // Scroll to the bottom when messages update.
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatSessions, activeChatId]);

  // Render a message; if it contains a transaction hash, render it as a clickable link.
  const renderMessage = (message, index) => {
    const txRegex = /TX Hash:\s*([0-9a-fA-Fx]+)/;
    const match = message.text.match(txRegex);
    if (match) {
      const txHash = match[1];
      return (
        <Box key={index} sx={{ display: "flex", justifyContent: message.role === "assistant" ? "flex-start" : "flex-end", mb: 1 }}>
          <Paper elevation={3} sx={{ p: 1.5, backgroundColor: message.role === "assistant" ? "#393E46" : "#00ADB5", color: "#fff", borderRadius: 2, maxWidth: "70%" }}>
            <Typography variant="body1">
              {message.text.split("TX Hash:")[0]}TX Hash:{" "}
              <Link href={`https://testnet.bscscan.com/tx/${txHash}`} target="_blank" rel="noopener noreferrer" sx={{ color: "#fff", textDecoration: "underline" }}>
                {txHash}
              </Link>
            </Typography>
          </Paper>
        </Box>
      );
    } else {
      return (
        <Box key={index} sx={{ display: "flex", justifyContent: message.role === "assistant" ? "flex-start" : "flex-end", mb: 1 }}>
          <Paper elevation={3} sx={{ p: 1.5, backgroundColor: message.role === "assistant" ? "#393E46" : "#00ADB5", color: "#fff", borderRadius: 2, maxWidth: "70%" }}>
            <Typography variant="body1">
              {message.text}
            </Typography>
          </Paper>
        </Box>
      );
    }
  };

  // Get the active chat session and its messages.
  const activeChat = chatSessions.find(chat => chat.id === activeChatId);
  const messages = activeChat ? activeChat.messages : [];

  return (
    <Box className="App">
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={handleSidebarToggle}
        chatSessions={chatSessions}
        activeChatId={activeChatId}
        onSelectChat={(id) => setActiveChatId(id)}
        onNewChat={createNewChat}
        onDeleteChat={handleDeleteChat}
      />
      <Box sx={{
          marginLeft: sidebarOpen ? "25%" : "50px",
          transition: "margin-left 0.3s ease",
          padding: "20px",
          display: "flex",
          flexDirection: "column",
          height: "100vh",
        }}>
        <Particle />
        <Collapse in={!(messages && messages.length)}>
          <Header />
        </Collapse>
        <Box sx={{ flexGrow: 1, overflowY: "auto", marginTop: 2, padding: 2 }}>
          {messages && messages.map((msg, index) => renderMessage(msg, index))}
          <div ref={messagesEndRef} />
        </Box>
        <PromptBar onSubmitPrompt={handlePromptSubmit} />
        <Footer />
      </Box>
    </Box>
  );
}

export default App;
