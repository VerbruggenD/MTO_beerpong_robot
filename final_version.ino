#include "serial.h"
#include <LiquidCrystal.h>

#define turn_dir 6
#define turn 7

#define aim_dir 8
#define aim 9

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// #define motor3Step 9
// #define motor3Dir 10

int amount_of_steps_turn;
int amount_of_steps_aim;

int delay_time_turn = 1;
int delay_time_aim = 3;

int coordinate = 0;

uint8_t value = 0;

serial_data_t serial_data;

typedef struct {               
  uint8_t motorStep;
  uint8_t motorDir;
} motor_t;

motor_t turn_motor = { turn, turn_dir };
motor_t aim_motor = { aim, aim_dir };

void stepperSetup(motor_t *motor) {
  pinMode(motor->motorStep, OUTPUT);
  pinMode(motor->motorDir, OUTPUT);
}

void stepperSetSteps(motor_t *motor, bool direction, int steps, int amountDelay) {  // BLOCKING stepper driving
  digitalWrite(motor->motorDir, direction);
  int count = 1;

  lcd.setCursor(0, 0);
  lcd.print(direction);

  while (count < steps) {
    digitalWrite(motor->motorStep, HIGH);
    delay(amountDelay);
    digitalWrite(motor->motorStep, LOW);
    delay(amountDelay);
    count++;
    //serialFlush();

  }    
}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}

void setup() {
  serialStart(9600);

  stepperSetup(&turn_motor);
  stepperSetup(&aim_motor);

  serial_data.cmd = ERROR;
  serial_data.data = value;

  lcd.begin(16, 2);

}
void loop() {
  serialRead(&serial_data);
  //serialFlush();

  // lcd.setCursor(0, 0);
  // lcd.print(serial_data.cmd);
  // lcd.setCursor(0, 1);
  // lcd.print(serial_data.data);

  switch (serial_data.cmd) {
    case CAM_POS:
      coordinate = serial_data.data;

      //serialFlush();

      if (coordinate > 305) {
        amount_of_steps_turn = 5*32;
        stepperSetSteps(&turn_motor, LOW, amount_of_steps_turn, delay_time_turn);
      }
      if (coordinate < 295) {
        amount_of_steps_turn = 5*32;
        stepperSetSteps(&turn_motor, HIGH, amount_of_steps_turn, delay_time_turn);
      }

      serial_data.cmd = ERROR;

      break;

    case LEFT:

      stepperSetSteps(&turn_motor, HIGH, serial_data.data, delay_time_turn);

      serial_data.cmd = ERROR;

      break;

    case RIGHT:

      stepperSetSteps(&turn_motor, LOW, serial_data.data, delay_time_turn);

      serial_data.cmd = ERROR;
      
      break;


    case ERROR:

      break;
  }

  delay(1000);
}