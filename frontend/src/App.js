import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [videoUrl, setVideoUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  const getSummary = async () => {
    const res = await axios.post(`${API}/summary`, {
      video_url: videoUrl,
    });
    setSummary(res.data.summary);
  };

  const sendMessage = async () => {
    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);

    const res = await axios.post(`${API}/chat`, {
      video_url: videoUrl,
      question: question,
    });

    const botMsg = { role: "assistant", content: res.data.answer };
    setMessages((prev) => [...prev, botMsg]);
    setQuestion("");
  };

  return (
    <div className="app">
      <h1>YouTube AI Assistant</h1>

      <input
        placeholder="Enter YouTube URL"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
      />

      {videoUrl && (
        <iframe
          title="video"
          width="100%"
          height="300"
          src={videoUrl.replace("watch?v=", "embed/")}
        />
      )}

      <div className="container">
        <div className="summary">
          <h2>Summary</h2>
          <button onClick={getSummary}>Generate</button>
          <div className="box">{summary}</div>
        </div>

        <div className="chat">
          <h2>Chat</h2>

          <div className="chat-box">
            {messages.map((m, i) => (
              <div key={i} className={m.role}>
                {m.content}
              </div>
            ))}
          </div>

          <input
            placeholder="Ask question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
