#include "serial.h"

uint8_t value = 100;

serial_data_t serial_data;

void setup() {
  serialStart(9600);

  serial_data.cmd = SHOOT;
  serial_data.data = value;
}
void loop() {
  serialRead(&serial_data);

  serialSend(&serial_data);

  delay(1000);
}