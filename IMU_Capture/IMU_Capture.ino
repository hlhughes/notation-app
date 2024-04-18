/*
  IMU Capture

  This example uses the on-board IMU to start reading acceleration and gyroscope
  data from on-board IMU and prints it to the Serial Monitor for one second
  when the significant motion is detected.

  You can also use the Serial Plotter to graph the data.

  The circuit:
  - Arduino Nano 33 BLE or Arduino Nano 33 BLE Sense board.

  Created by Don Coleman, Sandeep Mistry
  Modified by Dominic Pajak, Sandeep Mistry

  This example code is in the public domain.
*/

#include <Arduino_LSM9DS1.h>

const float accelerationThreshold = 2.4; // threshold of significant in G's
const int numSamples = 40;

int samplesRead;
volatile unsigned long myTime;
volatile unsigned long prevTime;
float a;
int movingAvg[5];
int counter;
int sum;

void setup() {
  Serial.begin(115200);
  samplesRead = 0;
  counter = 0;
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  prevTime = millis();

  while(counter < 5) {
    while (samplesRead < numSamples) {
      // check if both new acceleration data is available
      if (IMU.accelerationAvailable()) {
        samplesRead++;
      }
    }
    
    samplesRead = 0;
    myTime = millis();
    a = myTime - prevTime;
    a = 60000/a;
    prevTime = myTime;
    movingAvg[counter] = int(a);
    counter++;
  }
  counter = 0;
}

void loop() {
  float aX, aY, aZ;

  // wait for significant motion
  while (samplesRead == numSamples) {
    if (IMU.accelerationAvailable()) {
      // read the acceleration data
      IMU.readAcceleration(aX, aY, aZ);

      // sum up the absolutes
      float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

      // check if it's above the threshold
      if (aSum >= accelerationThreshold) {
        // reset the sample read count
        samplesRead = 0;
        myTime = millis();
        a = myTime - prevTime;
        a = 60000/a;
        movingAvg[counter] = int(a);
        counter++;
        if(counter >= 5)
          counter = 0;
        sum = movingAvg[0] + movingAvg[1] + movingAvg[2] + movingAvg[3] + movingAvg[4];
        sum = sum/5;

        Serial.print(sum);
        Serial.print('\n');
        prevTime = myTime;
        break;
      }
    }
  }

  // check if the all the required samples have been read since
  // the last time the significant motion was detected
  while (samplesRead < numSamples) {
    // check if both new acceleration data is available
    if (IMU.accelerationAvailable()) {
      // read the acceleration data
      IMU.readAcceleration(aX, aY, aZ);
      samplesRead++;
    }
  }
}
