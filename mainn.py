import os
import time
import serial
import pyttsx3
import joblib
import requests
from hardware_main import mainx
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from google.generativeai import GenerativeModel, configure
import speech_recognition as sr

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)  # Set to female voice
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            query = query.lower()
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you repeat?")
        except sr.RequestError:
            speak("Speech service is unavailable. Please try later.")
        return "none"

# Load training data and train the NLP model
# def train_model():
#     training_data = data_train_hardware.load_data()
#     texts = [item['text'] for item in training_data]
#     labels = [item['intent'] for item in training_data]

#     model = make_pipeline(TfidfVectorizer(), MultinomialNB())
#     model.fit(texts, labels)
#     joblib.dump(model, 'site_management_model.pkl')
#     return model

# Initialize serial communication with Arduino
# def check_arduino_port(port="COM5"):
#     try:
#         arduino = serial.Serial(port, 9600)
#         time.sleep(2)  # Allow time for Arduino initialization
#         print("Arduino connected successfully.")
#         return arduino
#     except serial.SerialException as e:
#         speak(f"Error: Could not connect to Arduino on {port}.")
#         return None

# Function to handle hardware commands

# Get weather data
def get_weather(city_name=""):
    if not city_name:
        try:
            loc_res = requests.get("http://ipinfo.io/json")
            loc_res.raise_for_status()
            city_name = loc_res.json().get("city", "your location")
        except requests.RequestException:
            speak("Could not retrieve your location.")
            return
    try:
        weather_res = requests.get(f"http://wttr.in/{city_name}?format=%t")
        weather_res.raise_for_status()
        temperature = weather_res.text.strip().replace("+", "")
        speak(f"The temperature in {city_name} is {temperature}.")
    except requests.RequestException:
        speak("Unable to retrieve weather data.")

# Chatbot setup
def setup_chatbot():
    os.environ["YOUR_API_KEY_VARIABLE"] = "AIzaSyBnD13QcYH59_15GYyFu2MpzukmS8oxy8c"
    configure(api_key=os.environ["YOUR_API_KEY_VARIABLE"])

    model = GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1.75,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain"
        },
        system_instruction="Your name is Temmer, created to assist in daily human life and control devices."
    )
    return model.start_chat(history=[])

# Main application
# def main():
#     arduino = check_arduino_port('COM5')
#     if not arduino:
#         return

    
chat_session = setup_chatbot()

while True:
        print("Menu:")
        print("1. Chatbot")
        print("2. Home Assistance")
        print("3. Weather Info")
        print("4. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            while True:
                query = take_command()
                if query == "exit":
                    break
                response = chat_session.send_message(query)
                print(f"Temmer: {response.text}")
                

        elif choice == "2":
           mainx()
           
        elif choice == "3":
            city = input("Enter city name (leave blank for current location): ").strip()
            get_weather(city)

        elif choice == "4":
            print("Exiting program.")
            speak("Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")


