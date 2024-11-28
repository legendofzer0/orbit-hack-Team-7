import os
import time
import random
import joblib
import serial
from selenium import webdriver
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import google.generativeai as genai
import speech_recognition as sr 
import requests
import data_train_for_chat
import pyttsx3

# Set your API key
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
        audio = r.listen(source, timeout=10, phrase_time_limit=1)
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
training_data = data_train_for_chat.load_data()
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
    
os.environ["YOUR_API_KEY_VARIABLE"] = "AIzaSyBnD13QcYH59_15GYyFu2MpzukmS8oxy8c"
genai.configure(api_key=os.environ["YOUR_API_KEY_VARIABLE"])

# Create the model
generation_config = {
    "temperature": 1.75,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Your name is Temmer. You are created by Team-7 members. You are a project of a hackathon. "
        "You are built to assist and help in daily human life. You can control simple hardware and software devices."
    ),
)

chat_session = model.start_chat(
    history=[]
)

print("Temmer is ready to assist you! Type 'exit' to end the session.\n")

# Loop for user interaction
while True:
    user_input = take_command()# Take user input
    print("1. open the chat session....")
    print("2. open the home assistance....")
    if user_input.lower() == 'exit':  # Exit condition
        print("Temmer: Goodbye! Have a great day!")
        break

    # Get response from the model
    response = chat_session.send_message(user_input)
    print(f"Temmer: {response.text}")
    speak(f"Temmer: {response.text}")
    
