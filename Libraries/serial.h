#ifndef SERIAL_COMMUNICATION
#define SERIAL_COMMUNICATION

#include <termios.h>
#include <string>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

enum State {
    Idle,
    ReadingValue,
};

typedef enum {
  HOR_SCAN,
  STEPS,
  DISTANCE,
  SHOOT,
  RETRACT,
  ERROR
} serial_cmd_t;

typedef struct  // the serial communication is always 1 cmd byte followed with 1 value byte (in raw data)
{               // size of the value is limited from 0->254 (8 bit)
  serial_cmd_t cmd;
  uint8_t data;
} serial_data_t;


int serialSetup(const char* serial_port, int baud_rate);

void serialRead(int *serial_fd, serial_data_t *data);

void serialSend(int *serial_fd, serial_data_t *data);

#endif