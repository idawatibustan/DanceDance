#include <Wire.h>
#include <stdio.h>

const int N = 2;
int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];
const int MPU_addr[N] = {0x68, 0x69}; // I2C address of the first MPU-6050

int handshake_flag;
int send_sensor_data;
String incoming;

struct Dataframe
{
  int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];
} dataframe;

void setup()
{
  Serial1.begin(57600);
  Wire.begin();
  int i;
  for (i = 0; i < N; i++)
  {
    Wire.beginTransmission(MPU_addr[i]);
    Wire.write(0x6B); // PWR_MGMT_1 register
    Wire.write(0);    // set to zero (wakes up the MPU-6050)
    Wire.endTransmission(true);
  }
  handshake_flag = 0;
  send_sensor_data = 0;
}

void loop()
{
  if (handshake_flag == 0)
  {
    while (Serial1.available() > 0)
    {
      char received = Serial1.read();
      incoming += received;
      if (incoming == "1")
      {
        Serial1.println("2");
        incoming = "";
      }
      else if (incoming == "3")
      {
        handshake_flag = 1;
        send_sensor_data = 1;
        incoming = "";
      }
    }
  }
  if (send_sensor_data == 1)
  {
    compileData();
    while (Serial1.available() > 0)
    {
      char received = Serial1.read();
      incoming += received;
      Serial1.println(incoming);
      if (incoming == "4")
      {
        handshake_flag = 0;
        send_sensor_data = 0;
        incoming = "";
      }
    }
  }
}

void compileData()
{
  int i;
  for (i = 0; i < N; i++)
  {
    Wire.beginTransmission(MPU_addr[i]);
    Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr[i], 14, true);                                     // request a total of 14 registers
    dataframe.AcX[i] = Wire.read() << 8 | Wire.read();                           // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    dataframe.AcY[i] = Wire.read() << 8 | Wire.read();                           // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    dataframe.AcZ[i] = Wire.read() << 8 | Wire.read();                           // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    dataframe.Tmp[i] = round((Wire.read() << 8 | Wire.read()) / 340.00 + 36.53); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    dataframe.GyX[i] = Wire.read() << 8 | Wire.read();                           // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    dataframe.GyY[i] = Wire.read() << 8 | Wire.read();                           // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    dataframe.GyZ[i] = Wire.read() << 8 | Wire.read();                           // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  }

  char sensor_one[100];
  char sensor_two[100];
  sprintf(sensor_one, "%d %d %d %d %d %d %d", MPU_addr[0], dataframe.AcX[0], dataframe.AcY[0], dataframe.AcZ[0], dataframe.GyX[0], dataframe.GyY[0], dataframe.GyZ[0]);
  sprintf(sensor_two, "%d %d %d %d %d %d %d", MPU_addr[1], dataframe.AcX[1], dataframe.AcY[1], dataframe.AcZ[1], dataframe.GyX[1], dataframe.GyY[1], dataframe.GyZ[1]);

  Serial1.println(sensor_one);
  delay(500);
  Serial1.println(sensor_two);
  delay(500);
}
