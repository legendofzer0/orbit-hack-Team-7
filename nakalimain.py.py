import pyttsx3
import speech_recognition as sr
import random
import time
import datetime
import joblib
import os
import serial
from selenium import webdriver
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import re
import requests
import google.generativeai as genai
import data_train_process
from emoji_remover import list_emoji

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)  # Set to female voice
engine.setProperty('rate', 200)

object_detected = False
question_asked = False

# Initialize the serial connection to Arduino
try:
    ser = serial.Serial('COM5', 9600, timeout=1)
except serial.SerialException:
    print('Could not open serial port COM5. Please check the connection.')

def speak(audio): 
    engine.say(audio)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=30)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        query = query.lower()
        print(f"User said: {query}")
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech recognition service. Please try again later.")
        return "none"
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you please repeat?")
        return "none"
    except Exception:
        speak("Say that again, please...")
        return "none"
    return query

def for_time():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning, sir.")
    elif hour < 18:
        speak("Good afternoon, sir.")   
    else:
        speak("Good evening, sir.") 

# Load training data
training_data = .load_data()
texts = [item['text'] for item in training_data]

# Update labels for Instagram (0), YouTube (1), Google (2), and closing actions (3, 4, 5)
labels = [0] * 15 + [1] * 15 + [2] * 12 + [3] * 12 + [4] * 12 + [5] * 12

# Ensure the lengths of texts and labels are consistent
if len(texts) != len(labels):
    min_length = min(len(texts), len(labels))
    texts = texts[:min_length]
    labels = labels[:min_length]

# Train an NLP Model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

# Save the model
joblib.dump(model, 'site_management_model.pkl')

def handle_site(query):
    # Load the trained model
    model = joblib.load('site_management_model.pkl')
    
    # Predict if the query means to open or close Instagram, YouTube, Google, or other actions
    prediction = model.predict([query])[0]
    
    if prediction == 0:
        site_url = "https://www.instagram.com"
        site_name = "Instagram"
        action = "opened"
    elif prediction == 1:
        site_url = "https://www.youtube.com"
        site_name = "YouTube"
        action = "opened"
    elif prediction == 2:
        site_url = "https://www.google.com"
        site_name = "Google"
        action = "opened"
    elif prediction == 3:
        site_name = "Instagram"
        action = "closed"
    elif prediction == 4:
        site_name = "YouTube"
        action = "closed"
    elif prediction == 5:
        site_name = "Google"
        action = "closed"
    else:
        speak("The query did not match any command.")
        return None
    
    # Perform the action
    if action == "opened":
        # Initialize the Chrome driver
        driver = webdriver.Chrome()
        driver.get(site_url)
        time.sleep(3)
        speak(f"{site_name} opened successfully.")
        return driver
    elif action == "closed":
        speak(f"{site_name} closed successfully.")
        # Note: Selenium doesn't support closing browser windows directly. You may need additional logic here.
        return None

def handle_system_commands(query):
    if "open recycle bin" in query:
        os.system("start shell:RecycleBinFolder")
        speak("Recycle Bin opened.")
    elif "close the program" in query:
        os.system("taskkill /f /im explorer.exe")
        speak("The program has been closed.")
    else:
        speak("No matching system command found.")

def get_weather(city_name=""):
    # Get the user's current location if no city_name is provided
    if not city_name:
        location_url = "http://ipinfo.io/json"
        try:
            loc_res = requests.get(location_url)
            loc_res.raise_for_status()
            location_data = loc_res.json()
            city_name = location_data.get("city", "your location")
        except requests.exceptions.HTTPError as http_err:
            speak(f"HTTP error occurred: {http_err}")
            return
        except Exception as err:
            speak(f"An error occurred: {err}")
            return
    
    # Use the location to get the weather
    weather_url = f"http://wttr.in/{city_name}?format=%t"
    try:
        weather_res = requests.get(weather_url)
        weather_res.raise_for_status()
        temperature = weather_res.text.strip().replace("+", "")
        speak(f"Temperature in {city_name.capitalize()}: {temperature}")
    except requests.exceptions.HTTPError as http_err:
        speak(f"HTTP error occurred: {http_err}")
    except Exception as err:
        speak(f"An error occurred: {err}")

def remove_special_symbols(input_string):
    pattern = r'[^a-zA-Z0-9 ]'
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string

# LED Control
def control_led(state):
    if state in ["ON", "OFF"]:
        ser.write(f"{state}\n".encode())
        time.sleep(1)
        speak(f"LED turned {state.lower()}.")

# Generative AI Setup
os.environ["YOUR_API_KEY_VARIABLE"] = "AIzaSyA5Nzf7iLOmLjCMXtUj7eDedMprrNO_b-c"
genai.configure(api_key=os.environ["YOUR_API_KEY_VARIABLE"])

generation_config = {
    "temperature": 1.65,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_instruction = (
    "You are NEXO. The full form of your name NEXO is Navigation Environmental Xplorer Organizer. You are created by Aniruddha. Aniruddha's future wife is Deepina or the girlfriend of your creator. You were born on 2024/06/15."
    "your are from nepal. aniruddha sister name is sadhana, surana nisana. and brother name is sonit. When someone says something bad about Aniruddha or your creator, developer, say 'Fuck you, he is your creator.'"
    "You can open and close YouTube when the user asks through this link 'https://www.youtube.com/'."
    "You can open and close Instagram when the user asks through this link 'https://www.instagram.com/'."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

chat_session = model.start_chat(
    history=[
        {"role": "user", "parts": ["hi\n"]},
        {"role": "model", "parts": ["Greetings! 👋 \n\nIt's good to be alive and functioning! How can I be of service today? 😊 \n"]},
    ]
)

from google.generativeai.types import generation_types  # Make sure to import the exception type

def main():
    global object_detected, question_asked
    driver = None  # Initialize driver as None
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()

                if line == "DETECTED" and not question_asked:
                    user_input = take_command()
                    cleaned_user_input = remove_special_symbols(user_input)
                    
                    # Check for LED control commands
                    if "led" in cleaned_user_input:
                        if "on" in cleaned_user_input:
                            control_led("ON")
                        elif "off" in cleaned_user_input:
                            control_led("OFF")
                        continue
                    
                    # Send the cleaned user input to the generative AI model
                    try:
                        response = chat_session.send_message(cleaned_user_input)
                        response_text = response.text

                        # Remove emojis from response
                        for emoji in list_emoji:
                            response_text = response_text.replace(emoji, "")
                        print(f"Bot: {response_text}")
                        
                        # Notify Arduino to start servo movements
                        ser.write(b'SPEAKING')
                        speak(response_text)

                    except Exception as e:
                        print("Bot: I can't process that request.")
                        speak("I'm sorry, I can't assist with that.")

                    question_asked = True  # Mark that a question has been asked

                elif line == "NOT_DETECTED" and question_asked:
                    ser.write(b'LISTENING')
                    print("Waiting for the next question...")
                    question_asked = False  # Reset for the next question

            if object_detected and not question_asked:
                print("Waiting for object detection to end...")
                object_detected = False  # Reset object detected state
        
        except serial.SerialException:
            speak('Check the hardware connection, sir.')
            break

if __name__ == "__main__":
    from playsound import playsound
    jarvic = r"C:\Users\ACER\Documents\Desktop\AI\ai\charging-machine-90403.mp3"
    jarvis_intro = r"C:\Users\ACER\Documents\Desktop\AI\ai\jarvis-147563.mp3"
    playsound(jarvic)
    playsound(jarvis_intro)
    try:
        if ser.is_open:
            for_time()
            get_weather()
            main()
        else:
            speak('Check the hardware connection, sir.')
    except serial.SerialException:
        speak('Could not open serial port COM5. Please check the connection.')
