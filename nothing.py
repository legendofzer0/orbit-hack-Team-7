import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline
import joblib
from webdriver_manager.chrome import ChromeDriverManager

class Intent:
    def __init__(self, name, phrases):
        self.name = name
        self.phrases = phrases

class IntentManager:
    def __init__(self):
        self.intents = []

    def add_intent(self, name, phrases):
        self.intents.append(Intent(name, phrases))

    def get_data(self):
        return [{"text": phrase, "intent": intent.name} for intent in self.intents for phrase in intent.phrases]

def load_data():
    manager = IntentManager()
    
    # Changed training data to handle light and fan controls
    manager.add_intent("TurnOnLight", [
        "Turn on the light", "Switch on the light", "Please turn on the light", "Can you turn on the light?", 
        "Lights on", "Activate the light", "Switch the light on", "Light on", "Power on the light", "Turn the light on"
    ])
    
    manager.add_intent("TurnOffLight", [
        "Turn off the light", "Switch off the light", "Please turn off the light", "Can you turn off the light?", 
        "Lights off", "Deactivate the light", "Switch the light off", "Light off", "Power off the light", "Turn the light off"
    ])

    manager.add_intent("TurnOnFan", [
        "Turn on the fan", "Switch on the fan", "Please turn on the fan", "Can you turn on the fan?", 
        "Fan on", "Activate the fan", "Switch the fan on", "Fan is on", "Turn the fan on", "Start the fan"
    ])
    
    manager.add_intent("TurnOffFan", [
        "Turn off the fan", "Switch off the fan", "Please turn off the fan", "Can you turn off the fan?", 
        "Fan off", "Deactivate the fan", "Switch the fan off", "Fan is off", "Turn the fan off", "Stop the fan"
    ])
    manager.add_intent("to check the person",
        [
            "Check the person","can you check the person","do anyone person in the room ", "is there is some in the room", "Do you want to check","is there is anyone","if there is anyone ","available in the room","exist in the room",
            "is there someone in the room?", "is there someone in the house?", "is there someone in the building?","can you chech the room"
           ])
    manager.add_intent("chat with bot",["chat with","chat with bot","i want to chast","i want to talk","i want the asistance", "i will talk with the bot","can bot talk with me","1","one","i chooes option one ", "i will choose the one option",
                        "should i choose the option 1", "i want to chat and choose the option 1"])


    return manager.get_data()

# Load the data
training_data = load_data()
texts = [item['text'] for item in training_data]
labels = [item['intent'] for item in training_data]

# Convert categorical labels to numerical values
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Train the NLP Model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

# Save the model
joblib.dump(model, 'device_control_model.pkl')

# Define a function to handle device control queries and take action
def handle_device(query):
    # Load the trained model
    model = joblib.load('device_control_model.pkl')
    
    # Make prediction using the already fitted TfidfVectorizer
    predicted_label = model.predict([query])
    
    # Decode the predicted label
    predicted_intent = label_encoder.inverse_transform(predicted_label)
    
    # Take action based on predicted intent
    if predicted_intent[0] == "TurnOnLight":
        turn_on_light()
    elif predicted_intent[0] == "TurnOffLight":
        turn_off_light()
    elif predicted_intent[0] == "TurnOnFan":
        turn_on_fan()
    elif predicted_intent[0] == "TurnOffFan":
        turn_off_fan()
    else:
        print("Sorry, I didn't understand the request.")
        sys.exit()

# Function to simulate turning on the light
def turn_on_light():
    print("Sure, sir. Turning on the light.")
    time.sleep(2)
    print("Light is now ON.")

# Function to simulate turning off the light
def turn_off_light():
    print("Sure, sir. Turning off the light.")
    time.sleep(2)
    print("Light is now OFF.")

# Function to simulate turning on the fan
def turn_on_fan():
    print("Sure, sir. Turning on the fan.")
    time.sleep(2)
    print("Fan is now ON.")

# Function to simulate turning off the fan
def turn_off_fan():
    print("Sure, sir. Turning off the fan.")
    time.sleep(2)
    print("Fan is now OFF.")
while True:
# Get user input
    user_input = input("Please enter your command: ")

    # Call the function with user input and print the result
    handle_device(user_input)
