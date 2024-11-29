import serial
import time
import speech_recognition as sr

# Establish serial communication with Arduino
arduino = serial.Serial('COM_PORT', 9600, timeout=1)  # Replace 'COM_PORT' with your actual Arduino port (e.g., 'COM3' or '/dev/ttyUSB0')

# Function to listen for voice commands
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the command.")
            return ""
        except sr.RequestError:
            print("Sorry, the speech recognition service is down.")
            return ""

# Main logic for handling the CheckRoom command
def check_room():
    command = listen_for_command()

    if "check room" in command:
        print("Checking the room...")
        arduino.write(b'6')  # Send command to Arduino to check the room
        time.sleep(2)  # Wait for Arduino to respond
        
        # Read the motion status from Arduino
        motion_status = arduino.read()
        
        if motion_status == b'1':  # Motion detected
            print("There is someone in the room.")
        else:
            print("There is no one in the room.")

# Continuously listen for commands
while True:
    check_room()
