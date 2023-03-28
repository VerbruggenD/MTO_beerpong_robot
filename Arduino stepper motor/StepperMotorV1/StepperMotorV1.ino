#include <Stepper.h>

const int stepsPerRevolution = 200;
Stepper myStepperLR(stepsPerRevolution, 8, 9, 10, 11);
Stepper myStepperBO(stepsPerRevolution, 4, 5, 6, 7);
Stepper myStepperSlee(stepsPerRevolution, 12, 13, 14, 15);          // kunnen deze pinnen? mss Mega gebruiken?

bool links;
bool rechts;

bool onder;
bool boven; 

int spoedSpindel = 1;


void maakStappen (int aantalStappen) {
  myStepperLR.setSpeed(100); // Stel de snelheid in (in stappen per seconde)
  myStepperLR.step(aantalStappen); // Maak het opgegeven aantal stappen
  delay(1000);
}

void linksRechts() {
  // controleer waarden van variabelen "links" en "rechts"
  if (links == true) {
    // beweeg met 2 stappen naar links
    myStepperLR.setSpeed(100);
    myStepperLR.step(-2);
  } else if (rechts == true) {
    // beweeg met 2 stappen naar rechts
    myStepperLR.setSpeed(100);
    myStepperLR.step(2);
  }
}

void bovenOnder() {
  // controleer waarden van variabelen "boven" en "onder"
  if (onder == true) {
    // beweeg met 2 stappen naar onder
    myStepperBO.setSpeed(100);
    myStepperBO.step(-2);
  } else if (boven == true) {
    // beweeg met 2 stappen naar boven
    myStepperBO.setSpeed(100);
    myStepperBO.step(2);
  }
}

void trekSleeAan(float gewensteAfstand){
  int aantalStappenNodig = gewensteAfstand / spoedSpindel * 200;                //waarbij 200 het aantal stappen per omwenteling is --> aanpassen naar werkelijke waarde!!!
  myStepperSlee.step(aantalStappenNodig);
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
