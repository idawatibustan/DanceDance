#include <Arduino_FreeRTOS.h>
#define LONG_TIME 0xffff
#define CIRCULAR_BUFFER_XS
#include <CircularBuffer.h>

// variables for polling_sensors_task
#include<Wire.h>
const int N = 2;
const int MPU_addr[N]={0x68, 0x69};  // I2C address of the first MPU-6050
// const int MPU_addr2=0x69;  // I2C address of the second MPU-6050
int16_t AcX[N],AcY[N],AcZ[N],Tmp[N],GyX[N],GyY[N],GyZ[N];
int i;

// variables for tx_rpi_task
static int handshake_flag = 0;
static int send_sensor_data = 0;
static char incoming = 'x';

// dataframe object

struct Dataframe {
    int16_t AcX[N],AcY[N],AcZ[N],Tmp[N],GyX[N],GyY[N],GyZ[N];
};

// variables for dataframe buffers. 100 because max polling is 40hz, buffer for 1s
static CircularBuffer<Dataframe,5> dataframe_buffer;

void setup()
{  
    // setup for polling_sensors_task
    Wire.begin();
    Serial.begin(115200);
    for (i = 0; i < N; i++){
        Wire.beginTransmission(MPU_addr[i]);
        Wire.write(0x6B);  // PWR_MGMT_1 register
        Wire.write(0);     // set to zero (wakes up the MPU-6050)
        Wire.endTransmission(true);
    }

    xTaskCreate(polling_sensors_task, "polling_sensors_task", 300, NULL, 2, NULL);
    xTaskCreate(tx_rpi_task, "tx_rpi_task", 300, NULL, 1, NULL);
    
}


void loop()
{ 
}

// polls sensors every xDelay interval, and writes values to dataframe_buffer
void polling_sensors_task(void * pvParameters)
{
    // execute at 25hz
    const TickType_t xDelay = 500/ portTICK_PERIOD_MS;
    for (;;) {
      Dataframe dataframe_poll = Dataframe();
    
    for (i = 0; i < N; i++){
        Wire.beginTransmission(MPU_addr[i]);
        Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
        Wire.endTransmission(false);
        Wire.requestFrom(MPU_addr[i],14,true);  // request a total of 14 registers
        dataframe_poll.AcX[i]=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
        dataframe_poll.AcY[i]=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
        dataframe_poll.AcZ[i]=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
        dataframe_poll.Tmp[i]=round((Wire.read()<<8|Wire.read())/340.00+36.53);  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
        dataframe_poll.GyX[i]=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
        dataframe_poll.GyY[i]=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
        dataframe_poll.GyZ[i]=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    }

    //write to buffer
    dataframe_buffer.push(dataframe_poll);
    Serial.print("poll frame size");
    Serial.println(dataframe_buffer.size());
    //repeat at fixed interval for 25hz 
    Serial.println("Pushed");
    vTaskDelay(xDelay);
    }
}


void tx_dataframe_to_rpi()
{
    // buffer checks to prevent access of empty buffer
    Serial.print("dataframe_buffer size");
    Serial.println(dataframe_buffer.size());
    while (!dataframe_buffer.isEmpty()) {
        Serial.print("dataframe_buffer size IN WHILE");
        Serial.println(dataframe_buffer.size());
        Dataframe dataframe_tx = dataframe_buffer.shift();
        char sensor_one[100];
        char sensor_two[100];
        sprintf(sensor_one, "%d %d %d %d %d %d %d", MPU_addr[0], dataframe_tx.AcX[0], dataframe_tx.AcY[0], dataframe_tx.AcZ[0], dataframe_tx.GyX[0], dataframe_tx.GyY[0], dataframe_tx.GyZ[0]);
        sprintf(sensor_two, "%d %d %d %d %d %d %d", MPU_addr[1], dataframe_tx.AcX[1], dataframe_tx.AcY[1], dataframe_tx.AcZ[1], dataframe_tx.GyX[1], dataframe_tx.GyY[1], dataframe_tx.GyZ[1]);
        Serial.println(sensor_one);
        Serial.println(sensor_two);
    }
   
}

// performs handshake to acknowledge that rpi is ready, serial status checks
// calls tx_dataframe_to_rpi if checks are valid
void tx_rpi_task(void * pvParameters)
{   
  const TickType_t xDelay = 1500 / portTICK_PERIOD_MS;
  for (;;) {
    Serial.println("tx_task");
    Serial.println(incoming);
    Serial.print("sen_sensor_data");
    Serial.println(send_sensor_data);
    Serial.print("handshake_flag");
    Serial.println(handshake_flag);
    if (handshake_flag == 0) {    
        while (Serial.available() > 0) {
          Serial.println("in handshake");
            char received = Serial.read();
            incoming = received;
            if (incoming == '1') {
                Serial.println('2');
                incoming = 'x';
            } else if (incoming == '3') {
                handshake_flag = 1;
                send_sensor_data = 1;
                incoming = 'x';
            }
        }
    }
    if (send_sensor_data == 1) {
        Serial.println("before tx");
        tx_dataframe_to_rpi();
        while (Serial.available() > 0) {
          //Serial.println("in tx");
            char received = Serial.read();
            incoming = received;
            if (incoming == '4') {
                handshake_flag = 0;
                send_sensor_data = 0;
                incoming = 'x';
            } 
        }
    }
    vTaskDelay(xDelay);
  }
}








