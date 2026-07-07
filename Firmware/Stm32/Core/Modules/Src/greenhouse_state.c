#include "greenhouse_state.h"

uint16_t ldrValue;
Gas_Data_t gasData;
Soil_Data_t soilData;
float temperature;
float humidity;
uint8_t alarm;
uint8_t fan;
uint8_t pump;
uint8_t heater;
uint8_t light;
uint8_t auto_mode = 1;
char uartBuffer[100];
