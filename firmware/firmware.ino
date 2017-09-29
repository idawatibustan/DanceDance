#include <Arduino_FreeRTOS.h>
#define LONG_TIME 0xffff

TaskHandle_t polling_sensors_taskhandle;
TaskHandle_t writing_buffer_taskhandle;

SemaphoreHandle_t polling_semaphore = NULL;

//variables for polling_sensors_task

#include<Wire.h>
const int N = 2;
const int MPU_addr[N]={0x68, 0x69};  // I2C address of the first MPU-6050
//const int MPU_addr2=0x69;  // I2C address of the second MPU-6050
int16_t AcX[N],AcY[N],AcZ[N],Tmp[N],GyX[N],GyY[N],GyZ[N];
int i;

// dataframe object

struct Dataframe {
    int16_t AcX[N],AcY[N],AcZ[N],Tmp[N],GyX[N],GyY[N],GyZ[N];
} dataframe;


void setup()
{  
    // setup for polling_sensors_task
    Wire.begin();
    for (i = 0; i < N; i++){
        Wire.beginTransmission(MPU_addr[i]);
        Wire.write(0x6B);  // PWR_MGMT_1 register
        Wire.write(0);     // set to zero (wakes up the MPU-6050)
        Wire.endTransmission(true);
    }
    Serial.begin(9600);
   
    xTaskCreate(polling_sensors_task, "polling_sensors_task", 100, NULL, 4, &polling_sensors_taskhandle);
    xTaskCreate(writing_buffer_task, "writing_buffer_task", 100, NULL, 4, &writing_buffer_taskhandle);
}


void loop()
{ 
  vTaskStartScheduler();
}

// this task releases polling_semaphore whenever it has completed one loop of reading
void polling_sensors_task(void* pvParameters)
{
    configASSERT( ( ( uint32_t ) pvParameters ) == 4 );
    // execute at 25hz
    const TickType_t xDelay = 40;

    static signed BaseType_t xHigherPriorityTaskWoken;

    for (i = 0; i < N; i++){
        Wire.beginTransmission(MPU_addr[i]);
        Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
        Wire.endTransmission(false);
        Wire.requestFrom(MPU_addr[i],14,true);  // request a total of 14 registers
        dataframe.AcX[i]=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
        dataframe.AcY[i]=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
        dataframe.AcZ[i]=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
        dataframe.Tmp[i]=round((Wire.read()<<8|Wire.read())/340.00+36.53);  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
        dataframe.GyX[i]=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
        dataframe.GyY[i]=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
        dataframe.GyZ[i]=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
    }
    xHigherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR( polling_semaphore, &xHigherPriorityTaskWoken )

    //repeat at fixed interval for 25hz 
    vTaskDelay(xDelay);
}

// this task only takes polling_semaphore
void writing_buffer_task(void* pvParameters)
{
    configASSERT( ( ( uint32_t ) pvParameters ) == 4 );
    
    if( xSemaphoreTake( polling_semaphore, LONG_TIME ) == pdTRUE )
    {
        //TODO: execution of buffer maintainence  code
    }
}


