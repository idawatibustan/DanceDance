/*
 11-14-2013
 SparkFun Electronics 2013
 Shawn Hymel

 This code is public domain but you buy me a beer if you use this 
 and we meet someday (Beerware license).

 Description:

 This sketch shows how to use the SparkFun INA169 Breakout
 Board. As current passes through the shunt resistor (Rs), a
 voltage is generated at the Vout pin. Use an analog read and
 some math to determine the current. The current value is
 displayed through the Serial Monitor.

 Hardware connections:

 Uno Pin    INA169 Board    Function

 +5V        VCC             Power supply
 GND        GND             Ground
 A0         VOUT            Analog voltage measurement

 VIN+ and VIN- need to be connected inline with the positive
 DC power rail of a load (e.g. an Arduino, an LED, etc.).

 */

// Constants
const int VOLT_PIN = A0;    // VD output
const int CURR_PIN = A1;    // INA169 output
const int led = 12;         // test LED
const float RS = 10;        // Shunt resistor value (in ohms)
const int VOLTAGE_REF = 5;  // Reference voltage for analog read

// Global Variables
float voltSensorValue;   // Variable to store value from analog read VD
float currSensorValue;   // Variable to store value from analog read INA
float current;       // Calculated current value
float voltage;       // Calculated voltage value


void setup() {

  // Initialize serial monitor
  Serial.begin(9600);
  pinMode(led, OUTPUT);

}

void loop() {

  // Read a value from the INA169 board
  voltSensorValue = analogRead(VOLT_PIN);
  currSensorValue = analogRead(CURR_PIN);

  // Remap the ADC value into a voltage number (5V reference)
  voltSensorValue = (voltSensorValue * VOLTAGE_REF) / 1023;
  currSensorValue = (currSensorValue * VOLTAGE_REF) / 1023;

  // Follow the equation given by the INA169 datasheet to
  // determine the current flowing through RS. Assume RL = 10k
  // Is = (Vout x 1k) / (RS x RL)
  current = currSensorValue / (10 * RS);

  // Output value (in amps) to the serial monitor to 3 decimal
  // places
  Serial.print(voltSensorValue, 3);
  Serial.print(" V ");
  Serial.print(current, 3);
  Serial.println(" A");

  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(500);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(500);
  

  // Delay program for a few milliseconds
  delay(500);

}
