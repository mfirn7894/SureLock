#include <Password.h> //http://playground.arduino.cc/uploads/Code/Password.zip //tells to use password library
#include <Keypad.h> //http://www.arduino.cc/playground/uploads/Code/Keypad.zip  //tells to use keypad library
#include <Servo.h> //tells to use servo library


Servo servoDoor;          // Define Door servo
Servo servoLocker;         // Define Locker servo
int val = 0;      // variable for reading the pin status
char msg = '  '; // variable to hold data from serial
int greenled = 13;

const byte ROWS = 4; // Four rows
const byte COLS = 4; // columns
// Define the Keymap
char keys[ROWS][COLS] = {
{'1','2','3'},
{'4','5','6'},
{'7','8','9'},
{'*','0','#'}
};
// Connect keypad ROW0, ROW1, ROW2 and ROW3 to these Arduino pins.
byte rowPins[ROWS] = { 9, 8, 7, 6 };// Connect keypad COL0, COL1 and COL2 to these Arduino pins.
byte colPins[COLS] = { 5, 4, 3 };


// Create the Keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
  Serial.begin(115200);
  pinMode(greenled, OUTPUT);

  delay(200);  
  digitalWrite(greenled,LOW);  
  servoDoor.attach(11);  // Set Door servo to digital pin 11
  servoLocker.attach(12);  // Set Locker servo to digital pin 12
  keypad.addEventListener(keypadEvent); //add an event listener for this keypad
  }

void loop(){
  keypad.getKey();
  while (Serial.available()>0){ 
    msg=Serial.read();
  }

// Turn specific servos based on message received from serial  
  if (msg=='Y') {            
    servoDoor.write(180);
    msg=' ';
    digitalWrite(greenled,HIGH);
    delay(300);
    digitalWrite(greenled, LOW);
  } 
  else if (msg=='N') {
    servoDoor.write(0);
    msg=' ';
  } 
  else if (msg=='O') {
    servoLocker.write(150);
    msg=' ';
    digitalWrite(greenled,HIGH);
    delay(300);
    digitalWrite(greenled, LOW);
  } 
  else if (msg=='C') {
    servoLocker.write(0);
    msg=' ';
    digitalWrite(greenled,HIGH);
    delay(300);
    digitalWrite(greenled, LOW);
  }

  }
  //take care of some special events
  void keypadEvent(KeypadEvent eKey){
  switch (keypad.getState()){
  case PRESSED:
  
  
  Serial.write(eKey);
  delay(10);
  
  Serial.write(254);
  

}
}


