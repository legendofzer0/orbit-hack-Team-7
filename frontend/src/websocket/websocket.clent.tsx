import { useState, useEffect } from "react";

interface Message {
  type: string;
  content: string;
}

const WebSocketClient: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    ws.onmessage = (event) => {
      const message: Message = JSON.parse(event.data);
      console.log("Received:", message);
      setMessages((prev) => [...prev, message]);
    };

    ws.onclose = () => {
      console.log("Disconnected from WebSocket server");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket) {
      socket.send(JSON.stringify({ type: "text", content: input }));
      setInput("");
    }
  };

  const sendAudio = (audioData: string) => {
    if (socket) {
      socket.send(JSON.stringify({ type: "audio", content: audioData }));
    }
  };

  return (
    <div>
      <h1>Chat with Chatbot</h1>
      <div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <div>
        <h2>Messages</h2>
        {messages.map((msg, index) => (
          <pre key={index}>{JSON.stringify(msg, null, 2)}</pre>
        ))}
      </div>
    </div>
  );
};

export default WebSocketClient;
