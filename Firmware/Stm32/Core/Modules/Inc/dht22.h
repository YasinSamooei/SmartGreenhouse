#ifndef __DHT22_H__
#define __DHT22_H__

#include "main.h"

#define DHT_PORT GPIOA
#define DHT_PIN  GPIO_PIN_3

typedef struct
{
    float temperature;
    float humidity;
}DHT22_Data_t;

void DHT22_Init(void);
uint8_t DHT22_Read(DHT22_Data_t *data);

#endif
