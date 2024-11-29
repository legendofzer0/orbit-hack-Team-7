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
  const [user, setUser] = useState();
  useEffect(() => {
    const gettokendataa = async () => {
      const getToken = localStorage.getItem("token");
      const getData = await getTokenData(getToken);
      setUser(getData);
      setUser(getData);
    };
    gettokendataa();
  }, []);

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
  const startRecording = () => {
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true, language: "en" });
  };

  const stopRecording = () => {
    SpeechRecognition.stopListening();
    setTimeout(() => {
      console.log(transcript);
      webSocketService.sendMessage({
        userId: user.id,
        userName: user.name,
        content: transcript,
      });
    }, 2000);
  };

  return (
    <div className="container">
      <button  onMouseDown={startRecording} onMouseUp={stopRecording}>
        Mic
      </button>
      <p>{transcript}</p>
    </div>
  );
};
export default Dictation;
