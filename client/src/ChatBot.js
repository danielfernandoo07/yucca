import React, { useState } from "react";
import axios from "axios";

const ChatBot = ({ onResponse }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user's message to chat
    setMessages((prev) => [...prev, { sender: "user", text: message }]);
    setInput("");

    try {
      const response = await axios.post("http://localhost:3001/chat", { message });
      const botResponses = response.data.map((res) => ({ sender: "bot", text: res.text }));

      setMessages((prev) => [...prev, ...botResponses]);

      // Pass the first bot response to ThreeDModel
      if (botResponses.length > 0) {
        onResponse(botResponses[0].text);
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Maaf, terjadi kesalahan. Coba lagi nanti." },
      ]);
    }
  };

  return (
    <div style={{ padding: "10px" }}>
      {/* Chat Messages */}
      <div style={{ maxHeight: "300px", overflowY: "auto", marginBottom: "10px" }}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{ textAlign: msg.sender === "user" ? "right" : "left", margin: "10px 0" }}
          >
            <strong>{msg.sender === "user" ? "Anda" : "Yucca"}:</strong> {msg.text}
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div style={{ display: "flex" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage(input)}
          placeholder="Tulis pesan..."
          style={{ flex: 1, padding: "10px", marginRight: "10px" }}
        />
        <button onClick={() => sendMessage(input)} style={{ padding: "10px" }}>
          Kirim
        </button>
      </div>
    </div>
  );
};

export default ChatBot;
