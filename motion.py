import serial
import time
import pyttsx3
import joblib
import data_train_hardware
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

# Load training data from the external file
training_data = data_train_hardware.load_data()  # This should be your data loading function
texts = [item['text'] for item in training_data]
labels = [item['intent'] for item in training_data]

# Train the NLP Model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

# Save the model for future use
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
    if prediction == "check the gas":
        arduino.write(b'6')  # Send '6' to Arduino to check for gas
        speak("Checking for gas...")
        print("Checking for gas...")
    elif prediction == "on the fan":
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
print("  - 'check the gas' to check for gas detection")
print("  - 'fan on' to turn on the fan")
print("  - 'fan off' to turn off the fan")
print("  - 'light on' to turn on the light")
print("  - 'light off' to turn off the light")
print("  - 'exit' to quit the program")

# Main loop to keep taking user input
while True:
    user_input = input("Enter command: ").strip().lower()
    
    if user_input == "exit":
        break
    
    handle_site(user_input)

# Close the serial connection when exiting
arduino.close()
