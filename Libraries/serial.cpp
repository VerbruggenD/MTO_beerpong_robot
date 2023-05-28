#include <Arduino.h>
#include <stdint.h>

#include "serial.h"

extern serial_data_t serial_data;

State currentState = Idle;

// void serialSend(serial_data_t *data) {
//   switch (data->cmd) {
//     case HOR_SCAN:
//       Serial.print("s");  // scan
//     break;
//     case STEPS:
//       Serial.print("p");  // position
      
//       break;
//     case DISTANCE:
//       Serial.print("d");  // distance
      
//       break;
//     case SHOOT:
//       Serial.print("f");  // fire
      
//       break;
//     case RETRACT:
//       Serial.print("r");  // retract
      
//       break;
//     default:
//       Serial.print("e");  // error message
//       break;
//   }
  
//   Serial.write(data->data);
//   Serial.println("");
// }

void serialRead(serial_data_t *data) {
  uint8_t buffer[3]; // Buffer to hold two bytes of data
  int bytesRead = Serial.readBytes(buffer, sizeof(buffer));
  if (bytesRead == sizeof(buffer)) {
    // Assuming the first byte represents the command and the second byte represents the value
    char c = buffer[0];

    uint8_t upper = buffer[1];
    uint8_t lower = buffer[2];

    data->data = (upper * 100) + lower;
    
    // data->data = buffer[1];

    switch (c) {
          case 'c':
              data->cmd = CAM_POS;
              break;
          case 'v':
              data->cmd = VERTICAL_ANGL;
              break;
          
          case 'l':
              data->cmd = LEFT;
              currentState = ReadingValue;
              break;

          case 'r':
              data->cmd = RIGHT;
              currentState = ReadingValue;
              break;

          case 's':
              data->cmd = SHOOT;
              break;

          default:
              if (c == 'e') {
                  data->cmd = ERROR;
              }
              break;
        }
  }
}

// void serialRead(serial_data_t *data) {
//   if (Serial.available()) { // check if data is available on the serial port

//     switch (currentState) {
//       case Idle:
//         char c = Serial.read();    
//         switch (c) {
//           case 'c':
//               data->cmd = CAM_POS;
//               break;
//           case 'v':
//               data->cmd = VERTICAL_ANGL;
//               break;
          
//           case 'l':
//               data->cmd = LEFT;
//               currentState = ReadingValue;
//               break;

//           case 'r':
//               data->cmd = RIGHT;
//               currentState = ReadingValue;
//               break;

//           case 's':
//               data->cmd = SHOOT;
//               break;

//           default:
//               if (c == 'e') {
//                   data->cmd = ERROR;
//               }
//               break;
//         }
//         break;

//       case ReadingValue:
//         int value = Serial.read();
//         data->data = value;
//         currentState = Idle;
//         //Serial.println("e");
//         break;
//     }
//   }
//   currentState = Idle;
// }

uint8_t serialStart(int speed) {
  Serial.begin(speed);
}

uint8_t serialStop(void) {
  Serial.end();
}