#include <Arduino_FreeRTOS.h>
#include <task.h>
#include <semphr.h>
#include <Wire.h>

//SemaphoreHandle_t buffer_semaphore = NULL;
const int N  = 2;
const int MPU_addr[N] = {0x68, 0x69}; // I2C address of the first MPU-6050

static int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];

static int handshake_flag = 0;
static int send_sensor_data = 0;

unsigned long now;
unsigned long then;
const unsigned long TIMEOUT = 5000;


void setup() {
  Wire.begin();
  Serial.begin(57600);
  Serial1.begin(57600);
  // wake both MPUs
  Wire.beginTransmission(MPU_addr[0]);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Wire.beginTransmission(MPU_addr[1]);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // //buffer_semaphore = xSemaphoreCreateMutex();
  // Serial.println("created buffer_semaphore");
  // //xSemaphoreGive(buffer_semaphore);
  // Serial.println("gave buffer_semaphore in setup");

  xTaskCreate(read_mpu_values_task, "read_mpu_values", 300, NULL, 2, NULL);
  xTaskCreate(comms_task, "comms", 300, NULL, 3, NULL);
  Serial.println("tasks created");

}

void pollMPU() {
    int i;
  for (i = 0; i < N; i++)
  {
    Wire.beginTransmission(MPU_addr[i]);
    Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr[i], 14, true);                                     // request a total of 14 registers
    AcX[i] = Wire.read() << 8 | Wire.read();                           // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY[i] = Wire.read() << 8 | Wire.read();                           // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ[i] = Wire.read() << 8 | Wire.read();                           // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp[i] = round((Wire.read() << 8 | Wire.read()) / 340.00 + 36.53); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX[i] = Wire.read() << 8 | Wire.read();                           // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY[i] = Wire.read() << 8 | Wire.read();                           // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ[i] = Wire.read() << 8 | Wire.read();                           // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  }
}

void read_mpu_values_task(void * pvParameters) {
  // read at 25hz, so 40ms delay. upgrade to delayuntil later
  //const TickType_t xDelay = 25 / portTICK_PERIOD_MS;
  while (1) {
    // if (buffer_semaphore != NULL) {
    //   if (xSemaphoreTake(buffer_semaphore, portMAX_DELAY) == pdTRUE) {
    //     Serial.println("in poll task");
    //     pollMPU();
    //     xSemaphoreGive(buffer_semaphore);
    //     //vTaskDelay(xDelay);
    //   }
    // }
    Serial.println("in poll task");
    pollMPU();
    //vTaskDelay(xDelay);
  }
}

void tx_dataframe_to_rpi()
{
  // if (buffer_semaphore != NULL) {
  //   if (xSemaphoreTake(buffer_semaphore, portMAX_DELAY) == pdTRUE) {
  //       now = millis();
  //      if (now - then > TIMEOUT) {
  //         handshake_flag = 0;
  //         send_sensor_data = 0;
  //       } 

    // long checksum = (long)AcX[0] + (long)AcY[0] + (long)AcZ[0] + (long)GyX[0] + (long)GyY[0] + (long)GyZ[0] +
    //     (long)AcX[1] + (long)AcY[1] + (long)AcZ[1] + (long)GyX[1] + (long)GyY[1] + (long)GyZ[1];
    // char output[1000];
    // sprintf(output, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%ld\n", AcX[0], AcY[0], AcZ[0], GyX[0], GyY[0], GyZ[0], AcX[1], AcY[1], AcZ[1], GyX[1], GyY[1], GyZ[1], checksum);
    // Serial1.print(output);

    // if (Serial1.available() > 0) {
  //         char inc = Serial1.read();
  //         Serial.println(inc);
  //         if (inc == '4') {
  //           handshake_flag = 0;
  //           send_sensor_data = 0;
  //         } else if (inc == 'A') {
  //           Serial.println("RECEIVED AN ACK");
  //           then = millis();
  //         }
  //       }

  //     Serial.println("before give semaphore");
  //     xSemaphoreGive(buffer_semaphore);
  //     Serial.println("after give semaphore");
  //   }
  // }
  now = millis();
  if (now - then > TIMEOUT) {
	  handshake_flag = 0;
	  send_sensor_data = 0;
	} 
	long checksum = (long)AcX[0] + (long)AcY[0] + (long)AcZ[0] + (long)GyX[0] + (long)GyY[0] + (long)GyZ[0] +
	      (long)AcX[1] + (long)AcY[1] + (long)AcZ[1] + (long)GyX[1] + (long)GyY[1] + (long)GyZ[1];
  char output[2000];
  sprintf(output, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%ld\n", AcX[0], AcY[0], AcZ[0], GyX[0], GyY[0], GyZ[0], AcX[1], AcY[1], AcZ[1], GyX[1], GyY[1], GyZ[1], checksum);
  Serial1.print(output);
  Serial.print(output);

  if (Serial1.available() > 0) {
    char inc = Serial1.read();
    Serial.println(inc);
    if (inc == '4') {
      handshake_flag = 0;
      send_sensor_data = 0;
    } else if (inc == 'A') {
      Serial.println("RECEIVED AN ACK");
      then = millis();
    }
  }
}

void comms_task(void * pvParameters) {
  Serial.println("entered comms task");
  // try this every 430ms, which is about the time it takes for 10 readings (40ms delay between readings)
  const TickType_t xDelay = 25 / portTICK_PERIOD_MS;
  while (1) {
    Serial.print("handshake_flag: "); Serial.println(handshake_flag);
    Serial.print("send_sensor_data" ); Serial.println(send_sensor_data);
    if (handshake_flag == 0) {
      Serial.println("in comms task");
      while (Serial1.available() > 0) {
        char inc = Serial1.read();
        Serial.println(inc);
        if (inc == '1') {
          Serial1.println('2');
        } else if (inc == '3') {
          Serial.print("RECEIVED A 3 SETTING FLAGS! handshake: ");
          handshake_flag = 1;
          send_sensor_data = 1;
          then = millis();
          Serial.print(handshake_flag);
          Serial.print("  send_sensor_data: "); Serial.println(send_sensor_data);
        }
      }
    }
    if (send_sensor_data == 1) {
     tx_dataframe_to_rpi();
      
    }

    vTaskDelay(xDelay);
  }
}

void loop() {


}


