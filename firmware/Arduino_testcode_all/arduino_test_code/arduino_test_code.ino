// Arduino test code
// By Arduino User Tianze

#include<Wire.h>

// Constants
const int N = 2;
const int MPU_addr[N]={0x68, 0x69};  // I2C address of the first MPU-6050

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
int16_t AcX[N],AcY[N],AcZ[N],Tmp[N],GyX[N],GyY[N],GyZ[N];
int i;


void setup(){
  Wire.begin();

  for (i = 0; i < N; i++){
    Wire.beginTransmission(MPU_addr[i]);
    Wire.write(0x6B);  // PWR_MGMT_1 register
    Wire.write(0);     // set to zero (wakes up the MPU-6050)
    Wire.endTransmission(true);
  }
  
  Serial.begin(9600);
  //pinMode(led, OUTPUT);
}
void loop(){
  for (i = 0; i < N; i++){
    Wire.beginTransmission(MPU_addr[i]);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr[i],14,true);  // request a total of 14 registers
    AcX[i]=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
    AcY[i]=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ[i]=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp[i]=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX[i]=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY[i]=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ[i]=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    Serial.print("I2C Address ");Serial.print(MPU_addr[i]);Serial.print(":\n");
    Serial.print("AcX = "); Serial.print(AcX[i]);
    Serial.print(" | AcY = "); Serial.print(AcY[i]);
    Serial.print(" | AcZ = "); Serial.print(AcZ[i]);
    Serial.print(" | Tmp = "); Serial.print(Tmp[i]/340.00+36.53);  //equation for temperature in degrees C from datasheet
    Serial.print(" | GyX = "); Serial.print(GyX[i]);
    Serial.print(" | GyY = "); Serial.print(GyY[i]);
    Serial.print(" | GyZ = "); Serial.println(GyZ[i]);
  }
  
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
  
  Serial.print("\n");
  delay(1000);
}
