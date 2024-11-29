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
    {"text": "switch on the light", "intent": "on the light"},
    {"text": "switch off the light", "intent": "off the light"},
    {"text": "power on the fan", "intent": "on the fan"},
    {"text": "power off the fan", "intent": "off the fan"},
    {"text": "enable the light", "intent": "on the light"},
    {"text": "disable the light", "intent": "off the light"},
    {"text": "start the fan", "intent": "on the fan"},
    {"text": "stop the fan", "intent": "off the fan"},
    {"text": "light on", "intent": "on the light"},
    {"text": "light off", "intent": "off the light"},
    {"text": "fan on", "intent": "on the fan"},
    {"text": "fan off", "intent": "off the fan"},
    {"text": "can you turn on the light", "intent": "on the light"},
    {"text": "please turn off the fan", "intent": "off the fan"},
    {"text": "activate the light", "intent": "on the light"},
    {"text": "deactivate the fan", "intent": "off the fan"},
    {"text": "turn on my light", "intent": "on the light"},
    {"text": "turn off my fan", "intent": "off the fan"},
    {"text": "open the door", "intent": "OpenDoor"},
    {"text": "please open the door", "intent": "OpenDoor"},
    {"text": "unlock the door", "intent": "OpenDoor"},
    {"text": "can you open the door?", "intent": "OpenDoor"},
    {"text": "check the person","intent": "check the person"},
    {"text": "someone in the room","intent": "check the person"},
    {"text": "is there is anyone in the room","intent": "check the person"},
    {"text": "is there anyone in the room", "intent": "CheckPerson"},
    {"text": "is there someone in the room", "intent": "CheckPerson"},
    {"text": "can you check if someone is in the room", "intent": "CheckPerson"},
    {"text": "is the room empty", "intent": "CheckPerson"},
    {"text": "who is in the room", "intent": "CheckPerson"}
    
    
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
    
    # Perform the corresponding action based on prediction
    if prediction == "on the fan":
        arduino.write(b'4')  # Send '4' to Arduino to turn on the fan
        speak("Fan turned on.")
        print("Fan turned ON")
    elif prediction == "off the fan":
        arduino.write(b'5')  # Send '5' to Arduino to turn off the fan
        speak("Fan turned off.")
        print("Fan turned OFF")
    elif prediction == "on the light":
        arduino.write(b'1')  # Send '1' to Arduino to turn on the light
        speak("Light turned on.")
        print("Light turned ON")
    elif prediction == "off the light":
        arduino.write(b'2')  # Send '2' to Arduino to turn off the light
        speak("Light turned off.")
        print("Light turned OFF")
         
    else:
        speak("The query did not match any command.")
        return None

# Main program loop for handling user input
print("Enter commands to control devices. Available commands:")
print("  - 'turn on the light' to turn on the light")
print("  - 'turn off the light' to turn off the light")
print("  - 'turn on the fan' to turn on the fan")
print("  - 'turn off the fan' to turn off the fan")
print("  - 'exit' to quit the program")

# Main loop to keep taking user input
while True:
    user_input = input("Enter command: ").strip().lower()
    
    if user_input == "exit":
        break
    
    handle_site(user_input)

# Close the serial connection when exiting
arduino.close()
