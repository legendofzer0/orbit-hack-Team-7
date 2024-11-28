import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Allow time for the Arduino to initialize

print("Enter commands to control devices. Available commands:")
print("  - 'light on' to turn on the light")
print("  - 'light off' to turn off the light")
print("  - 'fan on' to turn on the fan")
print("  - 'fan off' to turn off the fan")
print("  - 'check the room' to activate the motion sensor")
print("  - 'exit' to quit the program")

while True:
    user_input = input("Enter command: ").strip().lower()
    
    if user_input == "light on":
        arduino.write(b'1')  # Send '1' to Arduino for light on
        print("Light turned ON")
    elif user_input == "light off":
        arduino.write(b'2')  # Send '2' to Arduino for light off
        print("Light turned OFF")
    elif user_input == "fan on":
        arduino.write(b'3')  # Send '3' to Arduino for fan on
        print("Fan turned ON")
    elif user_input == "fan off":
        arduino.write(b'4')  # Send '4' to Arduino for fan off
        print("Fan turned OFF")
    elif user_input == "check the room":
        arduino.write(b'5')  # Send '5' to Arduino to activate motion sensor
        print("Activating motion sensor...")
        time.sleep(2)  # Allow some time for motion detection
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"Arduino says: {response}")
    elif user_input == "exit":
        print("Exiting program.")
        break
    else:
        print("Invalid command. Please try again.")

arduino.close()  # Close the serial connection when exiting
