// Include the Servo library
#include <Servo.h>
// Declare the Servo pin
int servo_1_Pin = 5;
int servo_2_Pin = 6;
// Create a servo object
Servo servoX;
Servo servoY;
int x = 90;
int y = 90;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  servoX.attach(servo_1_Pin);
  servoY.attach(servo_2_Pin);
  servoX.write(x);
  servoY.write(y);
  delay(1000);
}
char input = '\0'; //serial input is stored in this variable
void loop() {
  // put your main code here, to run repeatedly:
  // put your main code here, to run repeatedly:
  if (Serial.available()) { //checks if any data is in the serial buffer
    input = Serial.read(); //reads the data into a variable
    if (input == 'D') {
      servoY.write(y + 1);  //adjusts the servo angle according to the input
      y += 1;               //updates the value of the angle
    }
    else if (input == 'U') {
      servoY.write(y - 1);
      y -= 1;
    }
    else {
      servoY.write(y);
    }
    if (input == 'L') {
      servoX.write(x - 1);
      x -= 1;
    } else if (input == 'R') {
      servoX.write(x + 1);
      x += 1;
    }
    else {
      servoX.write(x);
    }
    input = '\0';           //clears the variable
  }
  //process keeps repeating!! :)
}
