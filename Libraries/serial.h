
#ifndef SERIAL_COMMUNICATION
#define SERIAL_COMMUNICATION

#include "stdint.h"
#include <Arduino.h>

typedef enum
{
  CAM_POS,
  VERTICAL_ANGL,
  RETRACT,
  LEFT,
  RIGHT,
  SHOOT,
  ERROR
} serial_cmd_t;

typedef struct  // the serial communication is always 1 cmd byte followed with 1 value byte (in raw data)
{               // size of the value is limited from 0->254 (8 bit)
  serial_cmd_t cmd;
  int data;
} serial_data_t;

enum State {
    Idle,
    ReadingValue,
};

// void serialSend(serial_data_t *data);

void serialRead(serial_data_t *data);

uint8_t serialStart(int speed);

uint8_t serialStop(void);

#endif