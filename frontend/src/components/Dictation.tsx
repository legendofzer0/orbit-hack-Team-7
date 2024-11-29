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
  const [speak, setSpeech] = useState();
  const [isRecording, setIsRecording] = useState(false);
  useEffect(()=>{
    setSpeech(transcript);
    console.log(speak);
  },[transcript])
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
    if(!isRecording) {
      startRecording();}
      else {
        stopRecording();
      }
  }
  const sendSpeech =  () => {  
    console.log(transcript);
    const t = transcript;
    resetTranscript();
     webSocketService.sendMessage({
      userId: user.id,
      userName: user.name,
      content: t,
    });
  }

  return (
<<<<<<< HEAD
    <div className="container">
      <button  onMouseDown={startRecording} onMouseUp={stopRecording}>
=======
    <div>
      <button onClick={()=>{toggleSpeechRecognition()}}>
>>>>>>> 56b3e4ec4b153a640b7a0fb77a95066012fe4883
        Mic
      </button>
      <p>{transcript}</p>
    </div>
  );
};
export default Dictation;
