// Define the pin numbers
const int lightPin = 4;      // Light connected to pin 4
const int fanPin = 5;        // Fan connected to pin 5
const int motionSensorPin = 7;  // Motion sensor connected to pin 7

void setup() {
  Serial.begin(9600); // Start serial communication
  pinMode(lightPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  pinMode(motionSensorPin, INPUT);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();  // Read the incoming command
    
    switch (command) {
      case '1': // Light ON
        digitalWrite(lightPin, HIGH);
        break;
      case '2': // Light OFF
        digitalWrite(lightPin, LOW);
        break;
      case '3': // Fan ON
        digitalWrite(fanPin, HIGH);
        break;
      case '4': // Fan OFF
        digitalWrite(fanPin, LOW);
        break;
      case '5': // Activate motion sensor
        Serial.println("Motion sensor activated. Checking for motion...");
        delay(2000);  // Wait for motion sensor to stabilize
        if (digitalRead(motionSensorPin) == HIGH) {
          Serial.println("There is a human.");
        } else {
          Serial.println("No motion detected.");
        }
        break;
      default:
        // Unknown command
        break;
    }
  }
}
