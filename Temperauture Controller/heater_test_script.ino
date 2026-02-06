/*    Max6675 Module  ==>   Arduino
 *    CS              ==>     D10
 *    SO              ==>     D12
 *    SCK             ==>     D13
 *    Vcc             ==>     Vcc (5v)
 *    Gnd             ==>     Gnd      */

/////////////////////////////////////////////////////////////////////////////////
//imports and variables
////////////////////////////////////////////////////////////////////////////////

//user defined variables
float set_temperature = 40.0; //temp range 0-60
float set_rpm = 100.0;

//libs
#include <Wire.h> 
#include <SPI.h>
#include "DHT.h"

//define system pins
#define MAX6675_1_CS   10
#define MAX6675_1_SO   12
#define MAX6675_1_SCK  13
#define heater_1 11
#define motor_1 9
#define motor_sense_1 8
#define DHTPIN 7
#define DHTTYPE DHT11

//create humidity sensor object
DHT dht(DHTPIN, DHTTYPE);

//script variables
float temperature_read = 0.0;
float PID_error = 0;
float previous_error = 0;
float elapsedTime, Time, timePrev;
float PID_value = 0;
int PID_p = 0;   
int PID_i = 0;    
int PID_d = 0;
int counter = 1;
float hum = 0.0;
float amb_temp = 0.0;
int revs = 0;
int prev_reading = 0;
float rpm = 0.0;
int motor_val = 125;

//pid constants
int kp = 90;
int ki = 33;
int kd = 80;

/////////////////////////////////////////////////////////////////////////////////
//main script
/////////////////////////////////////////////////////////////////////////////////

void setup() {
  Time = millis();
  Serial.begin(9600);
  pinMode(heater_1,OUTPUT);
  pinMode(motor_1,OUTPUT);
  pinMode(motor_sense_1, INPUT);
  dht.begin(); //initialise the humidity sensor
  delay(100); //delay for stability
}

void loop() {
  //set temp with value
  temperature_read = readThermocouple(MAX6675_1_CS, MAX6675_1_SO, MAX6675_1_SCK);
  
  //calculate raw error and PI error terms
  PID_error = set_temperature - temperature_read + 3;
  PID_p = 0.01*kp * PID_error;
  PID_i = 0.01*PID_i + (ki * PID_error);

  //calculate PD error term
  timePrev = Time;
  Time = millis();
  elapsedTime = (Time - timePrev) / 1000; 
  PID_d = 0.01*kd*((PID_error - previous_error)/elapsedTime);
  previous_error = PID_error; //store for next loop

  //calculate full pid term and translate to pwm
  PID_value = PID_p + PID_i + PID_d;
  if(PID_value < 0)
  {    PID_value = 0;    }
  if(PID_value > 255)  
  {    PID_value = 255;  }
  analogWrite(heater_1,PID_value);

  counter = counter + 1;
  //read the humidity sensor and revs every 10s
  if (counter == 20){
    counter = 1;
    hum = dht.readHumidity();
    amb_temp = dht.readTemperature();
  }
  
  //print variables to serial
  Serial.print(temperature_read,1);
  Serial.print("\t");
  Serial.print(set_temperature);
  Serial.print("\t");
  Serial.print(PID_value/2.55);
  Serial.print("\t");
  Serial.print(hum);
  Serial.print("\t");
  Serial.print(amb_temp);
  Serial.print("\t");
  Serial.print("\n");
  delay(500);
}

/////////////////////////////////////////////////////////////////////////////////
//functions
/////////////////////////////////////////////////////////////////////////////////

double readThermocouple(int CS, int SO, int SCK) {

  uint16_t v;
  pinMode(CS, OUTPUT);
  pinMode(SO, INPUT);
  pinMode(SCK, OUTPUT);
  
  digitalWrite(CS, LOW);
  delay(1);

  // Read in 16 bits,
  //  15    = 0 always
  //  14..2 = 0.25 degree counts MSB First
  //  2     = 1 if thermocouple is open circuit  
  //  1..0  = uninteresting status
  
  v = shiftIn(SO, SCK, MSBFIRST);
  v <<= 8;
  v |= shiftIn(SO, SCK, MSBFIRST);
  
  digitalWrite(CS, HIGH);
  if (v & 0x4) 
  {    
    // Bit 2 indicates if the thermocouple is disconnected
    return NAN;     
  }

  // The lower three bits (0,1,2) are discarded status bits
  v >>= 3;

  // The remaining bits are the number of 0.25 degree (C) counts
  return v*0.25;
}
