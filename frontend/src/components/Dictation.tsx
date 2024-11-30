import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import webSocketService from "../websocket/websocket.service";
import { useEffect, useState } from "react";
import { useSpeechSynthesis } from "react-speech-kit";  // Corrected hook import
import { getTokenData } from "../utils/getTokenData";
import "../css/mic.css";

const Dictation = () => {
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } =
    useSpeechRecognition();
  const [user, setUser] = useState(null);
  const [select, setSelect] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [answers, setAnswers] = useState([]); // Use state to store answers

  const { speak,voices } = useSpeechSynthesis(); // Corrected hook usage


  const naturalVoice = voices.find(voice => voice.name === "Google UK English Male") || voices[0]; 
  const handleSpeak = () => {
    speak({
      text: answers.join(" "),  // Join answers into a single string for speaking
      voice: naturalVoice,       // Set the voice to the natural-sounding one
      pitch: 10,                  // Adjust pitch for a smoother tone
      rate: 1.5                   // Adjust rate for natural speed
    }); // Join answers into a single string for speaking
  };

  // Listen for WebSocket messages
  useEffect(() => {
    const handleMessage = (message) => {
      setAnswers((prevAnswers) => [...prevAnswers, message.content]);
    };

    webSocketService.onMessage(handleMessage);

    // Cleanup to avoid duplicate handlers
    return () => {
      webSocketService.onMessage(null);
    };
  }, []);

  // Fetch user data from token on component mount
  useEffect(() => {
    const fetchUserData = async () => {
      const getToken = localStorage.getItem("token");
      const getData = await getTokenData(getToken);
      setUser(getData);
    };

    fetchUserData();
  }, []);

  // Send message when selection or user changes
  useEffect(() => {
    if (user && select) {
      webSocketService.sendMessage({
        userId: user.id,
        userName: user.name,
        content: select,
      });
    }
  }, [select, user]);

  // Start speech recognition
  const startRecording = () => {
    resetTranscript();
    setIsRecording(true);
    SpeechRecognition.startListening({ continuous: true, language: "en" });
  };

  // Stop speech recognition
  const stopRecording = () => {
    setIsRecording(false);
    SpeechRecognition.stopListening();
    setTimeout(() => {
      sendSpeech();
    }, 2000);
  };

  // Toggle speech recognition
  const toggleSpeechRecognition = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  // Send transcript via WebSocket
  const sendSpeech = () => {
    const t = transcript.trim();
    setAnswers([]); // Clear previous answers
    if (t) {
      webSocketService.sendMessage({
        userId: user.id,
        userName: user.name,
        content: t,
      });
    }
    resetTranscript();
  };

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  return (
    <div>
      <div>
        <div>
          <input
            type="radio"
            name="select"
            value="1"
            checked={select === "1"}
            onChange={() => setSelect("1")}
          />
          Chat Bot
          <input
            type="radio"
            name="select"
            value="2"
            checked={select === "2"}
            onChange={() => setSelect("2")}
          />
          Smart Home
          <input
            type="radio"
            name="select"
            value="3"
            checked={select === "3"}
            onChange={() => setSelect("3")}
          />
          Weather
        </div>
        <span id="btn-back">
          <button id="button-mic" onClick={toggleSpeechRecognition}>
            {isRecording ? "Stop" : "Mic"}
          </button>
        </span>
        <p>{transcript}</p>
      </div>
  
      <div className="chat-box">
        <h3>Answers:</h3>
        <ul>
          {answers.map((answer, index) => (
            <li key={index} className="typing-effect">
              {answer}
            </li>
          ))}
        </ul>
        <span className="buttons">
          <button
            onClick={() => {
              webSocketService.sendMessage({
                userId: user.id,
                userName: user.name,
                content: "exit",
              });
              setAnswers([]);
              alert("Exiting the chat...");
            }}
          >
            Exit
          </button>
        </span>
        <button onClick={handleSpeak}>Speak Answers</button> {/* Button to trigger speech synthesis */}
      </div>
    </div>
  );
};

export default Dictation;
