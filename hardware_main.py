import serial
import time
import pyttsx3
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)  # Set to female voice
engine.setProperty('rate', 200)

# Function for speaking text
def speak(audio): 
    engine.say(audio)
    engine.runAndWait()

# Training data for the commands
training_data = [
    {"text": "turn on the light", "intent": "on the light"},
    {"text": "turn off the light", "intent": "off the light"},
    {"text": "turn on the fan", "intent": "on the fan"},
    {"text": "turn off the fan", "intent": "off the fan"},
    # Add more phrases here if needed
]


def check_arduino_port(port="COM5"):
    try:
        arduino = serial.Serial(port, 9600)
        time.sleep(2)  # Allow time for Arduino initialization
        print("Arduino connected successfully.")
        return arduino
    except serial.SerialException as e:
        speak(f"Error: Could not connect to Arduino on {port}.")
        return None

texts = [item['text'] for item in training_data]
labels = [item['intent'] for item in training_data]

# Train the NLP Model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

# Save the model
joblib.dump(model, 'site_management_model.pkl')

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM5' with your Arduino port
time.sleep(2)  # Allow time for the Arduino to initialize

# Function to handle site control based on query
def handle_site(query):
    
    model = joblib.load('site_management_model.pkl')
    prediction = model.predict([query])[0]
    arduino = check_arduino_port("COM5")
    if arduino and arduino.is_open:
    
        if prediction == "on the fan":
            arduino.write(b'4')
            speak("Fan turned on.")
        elif prediction == "off the fan":
            arduino.write(b'5')
            speak("Fan turned off.")
        elif prediction == "on the light":
            arduino.write(b'1')
            speak("Light turned on.")
        elif prediction == "off the light":
            arduino.write(b'2')
            speak("Light turned off.")
        else:
            speak("Command not recognized.")

# Main loop
def mainx():
    while True:
        user_input = input("Enter command: ").strip().lower()
        if user_input == "exit":
            break
        handle_site(user_input)

arduino.close()

if __name__ == "__main__":
    mainx()
