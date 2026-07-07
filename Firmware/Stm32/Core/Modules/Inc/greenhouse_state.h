#ifndef GREENHOUSE_STATE_H
#define GREENHOUSE_STATE_H

#include "gas.h"
#include "soil.h"

extern uint16_t ldrValue;
extern Gas_Data_t gasData;
extern Soil_Data_t soilData;
extern float temperature;
extern float humidity;
extern uint8_t alarm;
extern uint8_t fan;
extern uint8_t pump;
extern uint8_t heater;
extern uint8_t light;
extern uint8_t auto_mode;
extern char uartBuffer[100];

#endif
