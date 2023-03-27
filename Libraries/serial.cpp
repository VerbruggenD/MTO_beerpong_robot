#include <Arduino.h>
#include <stdint.h>

#include "serial.h"

extern serial_data_t serial_data;

State currentState = Idle;

void serialSend(serial_data_t *data) {
  switch (data->cmd) {
    case HOR_SCAN:
      Serial.print("s");  // scan
    break;
    case STEPS:
      Serial.print("p");  // position
      
      break;
    case DISTANCE:
      Serial.print("d");  // distance
      
      break;
    case SHOOT:
      Serial.print("f");  // fire
      
      break;
    case RETRACT:
      Serial.print("r");  // retract
      
      break;
    default:
      Serial.print("e");  // error message
      break;
  }
  
  Serial.write(data->data);
  Serial.println("");
}

void serialRead(serial_data_t *data) {
  if (Serial.available()) { // check if data is available on the serial port

    switch (currentState) {
      case Idle:
        data->cmd = Serial.read();
        currentState = ReadingValue;
        //Serial.println("e");
        break;
      case ReadingValue:
        data->data = Serial.read();
        currentState = Idle;
        //Serial.println("e");
        break;
    }
  }
}

uint8_t serialStart(int speed) {
  Serial.begin(speed);
}

uint8_t serialStop(void) {
  Serial.end();
}