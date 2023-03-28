#include <Stepper.h>

const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);


void maakStappen (int aantalStappen) {
  myStepper.setSpeed(100); // Stel de snelheid in (in stappen per seconde)
  myStepper.step(aantalStappen); // Maak het opgegeven aantal stappen
  delay(1000);
}



void setup() {
  Serial.begin(9600);
}

void loop() {

  // Vraag aantal stappen dat de motor moet maken via de seriële monitor
  Serial.println("Voer het aantal stappen in dat de motor moet maken:");
  while (!Serial.available()) {}
  int aantalStappen = Serial.parseInt();
  
  maakStappen(aantalStappen);
}
