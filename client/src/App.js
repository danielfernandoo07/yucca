import React, { useState } from "react";
import ThreeDModel from "./ThreeDModel";
import ChatBot from "./ChatBot";

const App = () => {
  const [responseText, setResponseText] = useState("");

  const handleChatbotResponse = (response) => {
    setResponseText(response);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* 3D Model Section */}
      {/* <div style={{ flex: 4, background: "#eee" }}>
        <ThreeDModel responseText={responseText} />
      </div> */}

      {/* Chat Section */}
      <div
        style={{
          flex: 1,
          overflowY: "scroll",
          background: "#f9f9f9",
          borderTop: "2px solid #ccc",
          padding: "10px",
        }}
      >
        <ChatBot onResponse={handleChatbotResponse} />
      </div>
    </div>
  );
};

export default App;
