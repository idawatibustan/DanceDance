#include <Arduino_FreeRTOS.h>
#include <task.h>
#include <semphr.h>
#include <Wire.h>

SemaphoreHandle_t buffer_semaphore = NULL;

const int MPU_1_address = 0x68;
const int MPU_2_address = 0x69;
const int N  = 2;
static int16_t AcX[N], AcY[N], AcZ[N], Tmp[N], GyX[N], GyY[N], GyZ[N];

static int handshake_flag = 0;
static int send_sensor_data = 0;

unsigned long now;
unsigned long then;
const unsigned long TIMEOUT;

struct Dataframe {
  int16_t AcX1, AcY1, AcZ1, Tmp1, GyX1, GyY1, GyZ1, AcX2, AcY2, AcZ2, Tmp2, GyX2, GyY2, GyZ2;
} dataframe;

class DataframeBuffer {
  private:
    int _front, _back, _count, _max;
    Dataframe _buffer[100];
  public:
    DataframeBuffer() {
      _front = 0;
      _back = 0;
      _count = 0;
      _max = 100;

    }

    bool isEmpty() {
      return _count == 0;
    }

    int size() {
      return _count;
    }

    // add entry to back of buffer
    void push(Dataframe dataframe) {
      int next = (_back + 1) % _max;
      if (_count < _max) {
        _count += 1;
        _buffer[next] = dataframe;
        _back = next;
      } else {
        _buffer[next] = dataframe;
        _back = next;
        _front = (_front + 1) % _max;
      }
    }

    // retrieve and remove frontmost entry
    // use with isEmpty check, does not handle empty buffer case
    Dataframe shift() {
      Dataframe dataframe = _buffer[_front];
      _front = (_front + 1) % _max;
      _count -= 1;
      return dataframe;
    }
} dataframe_buffer;



void setup() {
  Wire.begin();
  //Serial.begin(57600);
  Serial1.begin(57600);
  // wake both MPUs
  Wire.beginTransmission(MPU_1_address);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Wire.beginTransmission(MPU_2_address);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  buffer_semaphore = xSemaphoreCreateMutex();
  //Serial.println("created buffer_semaphore");
  xSemaphoreGive(buffer_semaphore);
  //Serial.println("gave buffer_semaphore in setup");

  xTaskCreate(read_mpu_values_task, "read_mpu_values", 300, NULL, 3, NULL);
  xTaskCreate(comms_task, "comms", 300, NULL, 2, NULL);
  //Serial.println("tasks created");

}

void setupMPUPollng(int address) {
  Wire.beginTransmission(address);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(address, 14, true); // request a total of 14 registers
}

void pollMPU(int i) {
    AcX[i]=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY[i]=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ[i]=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp[i]=round((Wire.read()<<8|Wire.read())/340.00+36.53);  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX[i]=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY[i]=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ[i]=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

// fake data for when testing with only arduino
//  AcX[i] = 1 * i; // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
//  AcY[i] = 2 * i; // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
//  AcZ[i] = 3 * i; // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
//  Tmp[i] = 4 * i; // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
//  GyX[i] = 5 * i; // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
//  GyY[i] = 6 * i; // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
//  GyZ[i] = 7 * i; // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

void read_mpu_values_task(void * pvParameters) {
  // read at 25hz, so 40ms delay. upgrade to delayuntil later
  const TickType_t xDelay = 40 / portTICK_PERIOD_MS;
  while (1) {
    if (buffer_semaphore != NULL) {
      if (xSemaphoreTake(buffer_semaphore, portMAX_DELAY) == pdTRUE) {
        //Serial.println("in poll task");
        setupMPUPollng(MPU_1_address);
        pollMPU(0);
        setupMPUPollng(MPU_2_address);
        pollMPU(1);
        dataframe.AcX1 = AcX[0];
        dataframe.AcY1 = AcY[0];
        dataframe.AcZ1 = AcZ[0];
        dataframe.Tmp1 = Tmp[0];
        dataframe.GyX1 = GyX[0];
        dataframe.GyY1 = GyY[0];
        dataframe.GyZ1 = GyZ[0];
        dataframe.AcX2 = AcX[1];
        dataframe.AcY2 = AcY[1];
        dataframe.AcZ2 = AcZ[1];
        dataframe.Tmp2 = Tmp[1];
        dataframe.GyX2 = GyX[1];
        dataframe.GyY2 = GyY[1];
        dataframe.GyZ2 = GyZ[1];

        dataframe_buffer.push(dataframe);
        //Serial.print("dataframe buffer size: ");Serial.println(dataframe_buffer.size());
        xSemaphoreGive(buffer_semaphore);
        vTaskDelay(xDelay);
      }
    }
  }
}

void tx_dataframe_to_rpi()
{
  if (buffer_semaphore != NULL) {
    if (xSemaphoreTake(buffer_semaphore, portMAX_DELAY) == pdTRUE) {
      //Serial.println(dataframe_buffer.isEmpty());
      //Serial.print("buffer size:  ");Serial.println(dataframe_buffer.size());
      while (!dataframe_buffer.isEmpty()) {
        //Serial.println("inside dataframe is not empty");
        Dataframe dataframe_tx = dataframe_buffer.shift();
        long checksum = (long)dataframe.AcX[0] + (long)dataframe.AcY[0] + (long)dataframe.AcZ[0] + (long)dataframe.GyX[0] + (long)dataframe.GyY[0] + (long)dataframe.GyZ[0] +
    (long)dataframe.AcX[1] + (long)dataframe.AcY[1] + (long)dataframe.AcZ[1] + (long)dataframe.GyX[1] + (long)dataframe.GyY[1] + (long)dataframe.GyZ[1];
        char output[2000];
        sprintf(sensor_one, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%ld\n", dataframe.AcX[0], dataframe.AcY[0], dataframe.AcZ[0], dataframe.GyX[0], dataframe.GyY[0], dataframe.GyZ[0], 
        	dataframe.AcX[1], dataframe.AcY[1], dataframe.AcZ[1], dataframe.GyX[1], dataframe.GyY[1], dataframe.GyZ[1], checksum);
        Serial1.println(output);
        //Serial.println(output);
      }
      //Serial.println("before give semaphore");
      xSemaphoreGive(buffer_semaphore);
      //Serial.println("after give semaphore");
    }
  }

}

void comms_task(void * pvParameters) {
  //Serial.println("entered comms task");
  // try this every 430ms, which is about the time it takes for 10 readings (40ms delay between readings)
  const TickType_t xDelay = 430 / portTICK_PERIOD_MS;
  while (1) {
//    Serial.print("handshake_flag: "); Serial.println(handshake_flag);
//    Serial.print("send_sensor_data" ); Serial.println(send_sensor_data);
    if (handshake_flag == 0) {
//      Serial.println("in comms task");
      while (Serial1.available() > 0) {
        char inc = Serial1.read();
        if (inc == '1') {
          Serial1.println('2');
        } else if (inc == '3') {
//          Serial.print("RECEIVED A 3 SETTING FLAGS! handshake: ");
          handshake_flag = 1;
          send_sensor_data = 1;
          then = millis();
//          Serial.print(handshake_flag);
//          Serial.print("  send_sensor_data: "); Serial.println(send_sensor_data);
        }
      }
    }
    if (send_sensor_data == 1) {
      now = millis();
      if (now - then > TIMEOUT) {
        handshake_flag = 0;
        send_sensor_data = 0;
      } else {
        tx_dataframe_to_rpi();
      }
      while (Serial1.available() > 0) {
      	char inc = Serial1.read();
      	if (inc == '4') {
      		handshake_flag = 0;
      		send_sensor_data = 0;
      	} else if (inc == 'A') {
          then = millis();
        }
      }
    }

    vTaskDelay(xDelay);
  }
}

void loop() {


}