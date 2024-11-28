import { useState, useEffect, useRef } from "react";

interface Message {
  type: string;
  content: string;
}

const SmartHomeClient: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

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
      socket.send(
        JSON.stringify({ type: "text", mode: "smartHome", content: input })
      );
      setInput("");
    }
  };

  const startRecording = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error("Audio recording not supported in this browser.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      // Clear previous audio chunks
      audioChunksRef.current = [];

      // Collect audio chunks as they are recorded
      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);

      // When recording stops, send the audio data
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/wav",
        });

        // Read audio as base64
        const reader = new FileReader();
        reader.onloadend = () => {
          if (reader.result && socket) {
            const base64Audio = (reader.result as string).split(",")[1]; // Extract base64 part
            const message = {
              type: "audio",
              content: base64Audio,
              mode: "smartHome",
              filename: `recorded_audio_${Date.now()}.wav`,
            };

            socket.send(JSON.stringify(message));
            console.log("Audio sent to server");
          }
        };
        reader.readAsDataURL(audioBlob);
      };
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
        <button
          onMouseDown={startRecording}
          onMouseUp={stopRecording}
          onMouseLeave={() => isRecording && stopRecording()} // Ensure recording stops if mouse leaves the button
          disabled={isRecording}
        >
          {isRecording ? "Recording..." : "Hold to Record"}
        </button>
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

export default SmartHomeClient;
