#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <Wire.h>
#include <stdio.h>

const int N = 2;
//static int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];
const int MPU_addr[N] = {0x68, 0x69}; // I2C address of the first MPU-6050

static int handshake_flag;
static int send_sensor_data;
static String incoming;

static unsigned long now;
static unsigned long then;
unsigned long TIMEOUT = 5000;

long checksum;

void CompileData(void *pvParameters);
void SendData(void *pvParameters);
void HandShake(void *pvParameters);

TaskHandle_t xCompileHandle;
TaskHandle_t xSendHandle;
TaskHandle_t xHandShakeHandle;

SemaphoreHandle_t xDataPollSemaphore;
SemaphoreHandle_t xDataSendSemaphore;
SemaphoreHandle_t xHandShakeSemaphore;

struct Dataframe
{
  int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];
} dataframe;
 
void setup()
{
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
  now = 0;
  then = 0;
  Serial1.begin(57600);
  Serial.begin(57600);

  if (xDataPollSemaphore == NULL) {
    xDataPollSemaphore = xSemaphoreCreateBinary();
     if (xDataPollSemaphore != NULL) {
       Serial.println("created dataPoll semaphore");
       Serial.flush();
       Serial.println("stuck here?");
       Serial.flush();
     }
     Serial.println("or here");

  }

  if (xDataSendSemaphore == NULL) {
    xDataSendSemaphore = xSemaphoreCreateBinary();
    Serial.flush();
    Serial.println("before datasend check");
    Serial.flush();
     if (xDataSendSemaphore != NULL) {
      Serial.flush();
       Serial.println("created dataSend semaphore");
       Serial.flush();
     }
  }

  if (xHandShakeSemaphore == NULL) {
    xHandShakeSemaphore = xSemaphoreCreateBinary();
    //Serial.println("before hadnshake check");
    if (xHandShakeSemaphore != NULL) {
      Serial.flush();
      Serial.println("created handshake semaphore");
      Serial.flush();
//      Serial.println("before give handshake");
      Serial.flush();
      xSemaphoreGive(xHandShakeSemaphore);
      Serial.println("after give handshake");
      Serial.flush();
    }
  }

  xCompileHandle = xTaskCreate(CompileData, "Compile Data", 200, NULL, 3, NULL);
  xSendHandle = xTaskCreate(SendData, "Send Data", 200, NULL, 2, NULL);
  xHandShakeHandle = xTaskCreate(HandShake, "Handshaking", 200, NULL, 4, NULL);
  
}

void loop() {
  // do nothing
}

void CompileData(void *pvParameters __attribute__((unused))) {
  for (;;) {
    if (xSemaphoreTake(xDataPollSemaphore, (TickType_t) 5) == pdTRUE) {
      Serial.println("compile task obtained poll semaphore");
      Serial.flush();
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
      checksum = (long)dataframe.AcX[0] + (long)dataframe.AcY[0] + (long)dataframe.AcZ[0] + (long)dataframe.GyX[0] + (long)dataframe.GyY[0] + (long)dataframe.GyZ[0] +
        (long)dataframe.AcX[1] + (long)dataframe.AcY[1] + (long)dataframe.AcZ[1] + (long)dataframe.GyX[1] + (long)dataframe.GyY[1] + (long)dataframe.GyZ[1];
      Serial.println("Compile task giving Sending semaphore");
      Serial.flush();
      xSemaphoreGive(xDataSendSemaphore);
    }
    vTaskDelay(1);
  }
}

void SendData(void *pvParameters __attribute__((unused))) {
  for (;;) {
    if (xSemaphoreTake(xDataSendSemaphore, (TickType_t) 5) == pdTRUE) {
      Serial.println("sending task obtained send semaphore");
      Serial.flush();
      //if timeout
      now = millis();
      if (now - then > TIMEOUT) {
        handshake_flag = 0;
        send_sensor_data = 0;
      }

      char sensor_one[2000];
      // with checksum  
      sprintf(sensor_one, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%ld\n", dataframe.AcX[0], dataframe.AcY[0], dataframe.AcZ[0], dataframe.GyX[0], dataframe.GyY[0], dataframe.GyZ[0], dataframe.AcX[1], dataframe.AcY[1], dataframe.AcZ[1], dataframe.GyX[1], dataframe.GyY[1], dataframe.GyZ[1], checksum);
      Serial.print(sensor_one);
      Serial.flush();
      Serial1.print(sensor_one);
      Serial1.flush();

      while (Serial1.available() > 0)
        {
          char received = Serial1.read();
          incoming += received;
          // if conn closed
          if (incoming == "4")
          {
            handshake_flag = 0;
            send_sensor_data = 0;
          }
          // reset timing if A
          else if (incoming == "A") {
            then = millis();
          }
          incoming = "";
        }

      // continue poll/send cycles 
      if (send_sensor_data == 1) {
        Serial.println("sending task giving poll sempahore");
        Serial.flush();
        xSemaphoreGive(xDataPollSemaphore);
      }
      
    }
    // back to handshake routine if timed out or closed
    if (send_sensor_data == 0) {
      Serial.println("sending task giving handshake semaphore");
      Serial.flush();
      xSemaphoreGive(xHandShakeSemaphore);
    }
    vTaskDelay(1);
  }
}

void HandShake(void *pvParameters __attribute__((unused))) {
  for (;;) {
    Serial.flush();
    Serial.println("in handshake task");
    Serial.flush();
    if (xSemaphoreTake(xHandShakeSemaphore, (TickType_t) 5) == pdTRUE) {
      Serial.println("handshake task obtained semaphore");
      Serial.flush();
      Serial.print("handshake_flag: ");Serial.println(handshake_flag);
      Serial.flush();
      Serial.print("send_sensor_data: ");Serial.println(send_sensor_data);
      Serial.flush();
      // vTaskSuspend(xCompileHandle);
      // vTaskSuspend(xSendHandle);
      if (handshake_flag == 0)
      {
        while (Serial1.available() > 0)
        {
          char received = Serial1.read();
          incoming += received;
          if (incoming == "1")
          {
            Serial.println("received 1, sending 2");
            Serial.flush();
            Serial1.println("2");
            Serial1.flush();
          }
          else if (incoming == "3")
          {
            Serial.print("received 3, handshake: ");
            Serial.flush();
            handshake_flag = 1;
            send_sensor_data = 1;
            then = millis();
            Serial.print(handshake_flag);Serial.print(" send_sensor_data: ");Serial.println(send_sensor_data);
            Serial.flush();
          }
          incoming = "";
        }
        Serial.println("end of if handshake_flag == 0");
        Serial.flush();
      }
      if (send_sensor_data == 1)
      {
        Serial.println("handshake task giving DataPoll Semaphore");
        Serial.flush();
        xSemaphoreGive(xDataPollSemaphore);
      }
      //xSemaphoreGive(xHandShakeSemaphore);
    }
    vTaskDelay(1);
  }
} 