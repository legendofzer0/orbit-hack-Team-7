import serial
import time
import pyttsx3
import joblib
import json
import speech_recognition as sr
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
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=3)
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
async def send_json_via_websocket(websocket, data):
    json_data = json.dumps(data)  # Convert dictionary to JSON string
    await websocket.send(json_data)  # Send JSON string through WebSocket

# Training data for the commands
training_data = [
    {"text": "turn on the light", "intent": "on the light"},
    {"text": "turn off the light", "intent": "off the light"},
    {"text": "turn on the fan", "intent": "on the fan"},
    {"text": "turn off the fan", "intent": "off the fan"},
    {"text": "detect the motion", "intent": "detect motion"},
    {"text": "switch on the light", "intent": "on the light"},
    {"text": "switch off the light", "intent": "off the light"},
    {"text": "power on the fan", "intent": "on the fan"},
    {"text": "power off the fan", "intent": "off the fan"},
    {"text": "can you turn on the light", "intent": "on the light"},
    {"text": "can you turn off the fan", "intent": "off the fan"},
    {"text": "please turn on the light", "intent": "on the light"},
    {"text": "please turn off the light", "intent": "off the light"},
    {"text": "enable the fan", "intent": "on the fan"},
    {"text": "disable the fan", "intent": "off the fan"},
    {"text": "light on", "intent": "on the light"},
    {"text": "light off", "intent": "off the light"},
    {"text": "fan on", "intent": "on the fan"},
    {"text": "fan off", "intent": "off the fan"},
    {"text": "activate the light", "intent": "on the light"},
    {"text": "deactivate the light", "intent": "off the light"},
    {"text": "start the fan", "intent": "on the fan"},
    {"text": "stop the fan", "intent": "off the fan"},
    {"text": "can you switch on the fan", "intent": "on the fan"},
    {"text": "can you switch off the fan", "intent": "off the fan"},
    {"text": "turn on my light", "intent": "on the light"},
    {"text": "turn off my light", "intent": "off the light"},
    {"text": "turn on my fan", "intent": "on the fan"},
    {"text": "turn off my fan", "intent": "off the fan"},
    {"text": "check for motion", "intent": "detect motion"},
    {"text": "is there any motion", "intent": "detect motion"},
    {"text": "motion detection", "intent": "detect motion"},
    {"text": "start detecting motion", "intent": "detect motion"},
    {"text": "motion check", "intent": "detect motion"},
    {"text": "detect object", "intent": "detect object"}  # Added this line for object detection
]

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
    # Load the trained model
    model = joblib.load('site_management_model.pkl')
    
    # Predict the action based on the query
    prediction = model.predict([query])[0]
    print(f"Prediction: {prediction}")  # Debugging line to show the predicted action
    
    # Perform the corresponding action based on prediction
    if prediction == "on the light":
        arduino.write(b'1')  # Send '1' to Arduino to turn on the light
        speak("Light turned on.")
        print("Light turned ON")
    elif prediction == "off the light":
        arduino.write(b'2')  # Send '2' to Arduino to turn off the light
        speak("Light turned off.")
        print("Light turned OFF")
        
    elif prediction == "on the fan":
        arduino.write(b'4')  # Send '4' to Arduino to turn on the fan
        speak("Fan turned on.")
        print("Fan turned ON")
        
    elif prediction == "off the fan":
        arduino.write(b'5')  # Send '5' to Arduino to turn off the fan
        speak("Fan turned off.")
        print("Fan turned OFF")
    elif prediction == "detect object":
        arduino.write(b'D')  # Send 'D' to Arduino to detect object
        time.sleep(1)  # Wait for Arduino's response

        if arduino.in_waiting > 0:  # Check if there's data available from Arduino
            sensor_response = arduino.readline().decode().strip()  # Read and decode Arduino's response
            print(f"Arduino Response: {sensor_response}")  # Debugging line
            
            if sensor_response == "Object detected":
                speak("Object detected within 20 centimeters.")
                print("Object Detected")
            else:
                speak("No object detected.")
                print("No object Detected")
        else:
            speak("No response from Arduino.")
            print("No response from Arduino.")

# Main program loop for handling user input
print("Enter commands to control devices. Available commands:")
print("  - 'turn on the light' to turn on the light")
print("  - 'turn off the light' to turn off the light")
print("  - 'turn on the fan' to turn on the fan")
print("  - 'turn off the fan' to turn off the fan")
print("  - 'detect object' to check for objects within 20cm")
print("  - 'exit' to quit the program")

# Main loop to keep taking user input
def mainxer():
    while True:
        user_input = take_command()
        print(f"User Input: {user_input}")  # Debugging line to check user input
        
        if user_input == "exit" or user_input == "close" or user_input == "0":
            break
        
        handle_site(user_input)

    # Close the serial connection when exiting
    arduino.close() 

if __name__ == "__main__":
    
    mainxer()


