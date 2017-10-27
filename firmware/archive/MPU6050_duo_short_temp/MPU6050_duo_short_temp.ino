// duo MPU-6050 Sketch
// By Arduino User Tianze

#include <Arduino_FreeRTOS.h>
#include<Wire.h>

const int N = 2;
const int MPU_addr[N]={0x68, 0x69};  // I2C address of the first MPU-6050
//const int MPU_addr2=0x69;  // I2C address of the second MPU-6050
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
  
  Serial.begin(57600);
  Serial1.begin(57600);
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
    
    Serial1.write("I2C Address ");Serial1.write(MPU_addr[i]);Serial1.write(":\n");
    Serial1.write("AcX = "); Serial1.write(AcX[i]);
    Serial1.write(" | AcY = "); Serial1.write(AcY[i]);
    Serial1.write(" | AcZ = "); Serial1.write(AcZ[i]);
    Serial1.write(" | Tmp = "); Serial1.write(round(Tmp[i]/340.00+36.53));  //equation for temperature in degrees C from datasheet
    Serial1.write(" | GyX = "); Serial1.write(GyX[i]);
    Serial1.write(" | GyY = "); Serial1.write(GyY[i]);
    Serial1.write(" | GyZ = "); Serial1.write(GyZ[i]);
  }
  Serial.print("\n");
  delay(1000);
}
