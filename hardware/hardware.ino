int lightPin = 3;   // Pin connected to the light (bulb)
int fanPin = 4;     // Pin connected to the fan
int ledPin1 = 7;    // Pin for LED 1
int ledPin2 = 8;    // Pin for LED 2
int ledPin3 = 11;   // Pin for LED 3

int echoPin = 10;   // Echo pin for ultrasonic sensor
int trigPin = 9;    // Trigger pin for ultrasonic sensor
long duration;      // Variable for the duration of the pulse
int distance;       // Variable for the calculated distance

void setup() {
  pinMode(lightPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(trigPin, OUTPUT);   // Set trigPin as output
  pinMode(echoPin, INPUT);    // Set echoPin as input

  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  // Read serial command
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming byte

    if (command == '1') {
      digitalWrite(lightPin, HIGH);  // Turn on the light
    } 
    else if (command == '2') {
      digitalWrite(lightPin, LOW);   // Turn off the light
    } 
    else if (command == '4') {
      digitalWrite(fanPin, HIGH);    // Turn on the fan
    } 
    else if (command == '5') {
      digitalWrite(fanPin, LOW);     // Turn off the fan
    }
  }

  // Measure distance using the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);  // Get the pulse duration
  distance = duration * 0.034 / 2;    // Calculate distance in cm

  // Light (bulb) control based on distance
  if (distance > 0 && distance <= 10) {
    digitalWrite(lightPin, HIGH);  // Turn on the light (bulb)
  } else {
    digitalWrite(lightPin, LOW);   // Turn off the light (bulb)
  }

  // LED control based on distance
  if (distance <= 10) {
    // If the object is within 10 cm, blink all LEDs
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin3, HIGH);
    delay(500);
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
    delay(500);
  } else if (distance <= 30) {
    // If the object is within 30 cm, turn on the first LED
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
  } else {
    // If no object is within 30 cm, turn off all LEDs
    digitalWrite(ledPin1, LOW);
    digitalWrite(ledPin2, LOW);
    digitalWrite(ledPin3, LOW);
  }
}
