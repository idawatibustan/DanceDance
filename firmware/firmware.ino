#include <Arduino_FreeRTOS.h>

TaskHandle_t polling_sensors_taskhandle;

// serial printer function
#define serialPrint(str)  {
        Serial.println(F(str));
}

void setup()
{  
    Serial.begin(115200);
   
    xTaskCreate(polling_sensors_task, "polling_sensors_task", 100, NULL, 4, &polling_sensors_taskhandle);
}


void loop()
{ 
  vTaskStartScheduler();
}



void polling_sensors_task(void* pvParameters)
{
    configASSERT( ( ( uint32_t ) pvParameters ) == 4 );
    // execute at 25hz
    const TickType_t xDelay = 40;
    
    //TODO: read from sensors

    //repeat at fixed interval for 25hz reading
    vTaskDelay(xDelay);
}



