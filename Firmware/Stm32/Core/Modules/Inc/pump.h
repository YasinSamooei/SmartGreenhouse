#ifndef PUMP_H
#define PUMP_H

#include "stm32f1xx_hal.h"

void Pump_Init(GPIO_TypeDef *port, uint16_t pin);
void Pump_On(GPIO_TypeDef *port, uint16_t pin);
void Pump_Off(GPIO_TypeDef *port, uint16_t pin);
uint8_t Pump_IsRunning(void);

#endif
