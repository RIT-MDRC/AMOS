#include <Servo.h>
#include <Wire.h>

#define LEFT_A_PIN 11
#define LEFT_B_PIN 6
#define RIGHT_A_PIN 3
#define RIGHT_B_PIN 9

#define PACKET_TIMEOUT_MS 300
#define NO_POWER 127

Servo leftA;
Servo leftB;
Servo rightA;
Servo rightB;
unsigned long lastPacket = 0;

void setup() {
  Serial.begin(9600);
  
  Wire.begin(4);
  Wire.onReceive(receiveI2C);
  
  leftA.attach(LEFT_A_PIN);
  leftB.attach(LEFT_B_PIN);
  rightA.attach(RIGHT_A_PIN);
  rightB.attach(RIGHT_B_PIN);

  pinMode(2, INPUT);
  pinMode(7, INPUT);
  pinMode(8, INPUT);
  pinMode(12, INPUT);

  setMotorOutput(NO_POWER, NO_POWER);
}

void receiveI2C(int howMany) {
  // read the two control bytes and send to motors
  while (Wire.available() >= 2) {
    int leftByte = Wire.read();
    int rightByte = Wire.read();
    setMotorOutput(leftByte, rightByte);
    lastPacket = millis();
  }
}

void loop() {
  // check for packet timeout
  if (lastPacket != 0 && millis() - lastPacket > PACKET_TIMEOUT_MS) {
    setMotorOutput(NO_POWER, NO_POWER);
    Serial.println("Packet timeout!");
  }
}

void setMotorOutput(int leftByte, int rightByte) {
  int leftTime = 2000 - (1000.0 * ((double) leftByte / 255.0));
  int leftInvTime = (1000 - (leftTime - 1000)) + 1000;
  int rightTime = 2000 - (1000.0 * ((double) rightByte / 255.0));
  int rightInvTime = (1000 - (rightTime - 1000)) + 1000;
  
  leftA.writeMicroseconds(leftTime);
  leftB.writeMicroseconds(leftInvTime);
  rightA.writeMicroseconds(rightInvTime);
  rightB.writeMicroseconds(rightTime);

  Serial.print("Setting motor output ");
  Serial.print(leftByte, DEC);
  Serial.print(", ");
  Serial.print(rightByte, DEC);
  Serial.println();
}
