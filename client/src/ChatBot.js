import React, { useState } from "react";
import axios from "axios";

const ChatBot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    // // Handle STT: Speech-to-Text
    // const handleSpeechToText = () => {
    //     const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    //     recognition.lang = "id-ID"; // Bahasa Indonesia
    //     recognition.onresult = (event) => {
    //         const userMessage = event.results[0][0].transcript;
    //         setInput(userMessage);
    //         sendMessage(userMessage);
    //     };
    //     recognition.start();
    // };

    // // Handle TTS: Text-to-Speech
    // const handleTextToSpeech = (text) => {
    //     window.responsiveVoice.speak(text, "Indonesian Female");
    // };

    // Handle Sending Message to Rasa API
    const sendMessage = async (message) => {
        if (!message.trim()) return;

        // Add user's message to the chat
        setMessages((prevMessages) => [...prevMessages, { sender: "user", text: message }]);
        setInput("");

        try {
            const response = await axios.post("http://localhost:3001/chat", { message });

            // Handle bot response
            const botMessages = response.data.map((res) => ({
                sender: "bot",
                text: res.text,
            }));

            setMessages((prevMessages) => [...prevMessages, ...botMessages]);

            // // Speak bot's response
            // if (botMessages.length > 0) {
            //     handleTextToSpeech(botMessages[0].text);
            // }
        } catch (error) {
            console.error("Error sending message:", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: "bot", text: "Maaf, terjadi kesalahan. Coba lagi nanti." },
            ]);
        }
    };


    return (
        <div style={{ maxWidth: "600px", margin: "0 auto", textAlign: "center" }}>
            <h1>ChatBot Universitas Ciputra</h1>
            <div style={{ border: "1px solid #ccc", padding: "10px", height: "400px", overflowY: "scroll" }}>
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        style={{
                            textAlign: msg.sender === "user" ? "right" : "left",
                            margin: "10px 0",
                        }}
                    >
                        <strong>{msg.sender === "user" ? "Anda" : "Yucca"}: </strong>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div style={{ marginTop: "20px" }}>
                {/* <button onClick={handleSpeechToText}>🎤 Bicara</button> */}
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && sendMessage(input)}
                    placeholder="Tulis pesan..."
                    style={{ width: "70%", margin: "0 10px", padding: "10px" }}
                />
                <button onClick={() => sendMessage(input)}>Kirim</button>
            </div>
        </div>
    );
};

export default ChatBot;
