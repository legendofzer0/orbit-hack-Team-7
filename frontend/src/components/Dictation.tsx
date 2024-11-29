import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import webSocketService from "../websocket/websocket.service";
import { useEffect, useState } from "react";
import { getTokenData } from "../utils/getTokenData";
import "../css/mic.css";

const Dictation = () => {
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } =
    useSpeechRecognition();
  const [user, setUser] = useState(null);
  const [speak, setSpeech] = useState();
  const [select, setSelect] = useState("");
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    setSpeech(transcript);
    console.log(speak);
  }, [transcript]);
  useEffect(() => {
    const gettokendataa = async () => {
      const getToken = localStorage.getItem("token");
      const getData = await getTokenData(getToken);
      setUser(getData);
    };
    gettokendataa();
  }, []);
  useEffect(() => {
    if (user) {
      webSocketService.sendMessage({
        userId: user.id,
        userName: user.name,
        content: select,
      });
    }
  }, [select, user]);

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
  const startRecording = () => {
    resetTranscript();
    setIsRecording(true);
    SpeechRecognition.startListening({ continuous: true, language: "en" });
  };

  const stopRecording = () => {
    setIsRecording(false);
    SpeechRecognition.stopListening();
    setTimeout(() => {
      sendSpeech();
    }, 2000);
  };
  const toggleSpeechRecognition = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };
  const sendSpeech = () => {
    console.log(transcript);
    const t = transcript;
    resetTranscript();
    webSocketService.sendMessage({
      userId: user.id,
      userName: user.name,
      content: t,
    });
  };

  return (
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
        <button
          id="button-mic"
          onClick={() => {
            toggleSpeechRecognition();
          }}
        >
          Mic
        </button>
      </span>
      <p>{transcript}</p>
    </div>
  );
};
export default Dictation;
