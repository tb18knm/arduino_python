#include <Wire.h>

const int LED_PIN = 13;
char key;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()){
    key = Serial.read();

    switch(key){
      case 'H':
        digitalWrite(LED_PIN, HIGH);
        break;
      case 'L':
        digitalWrite(LED_PIN, LOW);
        break;
    }
  }

}
