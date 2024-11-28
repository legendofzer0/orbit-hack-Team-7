import serial
import time
# import speech_recognition as sr

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Allow time for the Arduino to initialize

# Function to listen for voice commands
# def listen_for_commands():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for commands...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"Command received: {command}")
#         return command
#     except sr.UnknownValueError:
#         print("Sorry, I didn't understand that.")
#         return ""
#     except sr.RequestError:
#         print("Sorry, the speech service is down.")
#         return ""

# Main loop to interact with Arduino and handle commands
while True:
    # command = listen_for_commands()
    command = input("Enter your command: ")  # Replace with actual voice command input
    
    # Send command to Arduino
    if command == "turn on the room light 1":
        arduino.write(b"turn on the room light 1")  # Send command to Arduino
    elif command == "turn on the room light 2":
        arduino.write(b"turn on the room light 2")  # Send command to Arduino
    elif command == "turn off the lights":
        arduino.write(b"turn off the lights")  # Turn off both lights
    elif command == "check in the room":
        arduino.write(b"check in the room")  # Send command to Arduino
    
    if command == "turn on the room light 1":
        arduino.write(b"turn on the room light 1")  # Send command to Arduino
    elif command == "turn on the room light 2":
        arduino.write(b"turn on the room light 2")  # Send command to Arduino
    elif command == "turn off the lights":
        arduino.write(b"turn off the lights")  # Turn off both lights
    elif command == "check in the room":
        arduino.write(b"check in the room")  # Send command to Arduino

    # Check for response from Arduino
    if arduino.in_waiting > 0:
        response = arduino.readline().decode().strip()
        print(f"Arduino says: {response}")
        
    time.sleep(1)  # Small delay to prevent spamming commands
