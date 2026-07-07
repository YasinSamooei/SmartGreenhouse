#ifndef HEATER_H
#define HEATER_H

#include "stm32f1xx_hal.h"

void Heater_Init(GPIO_TypeDef *port, uint16_t pin);
void Heater_On(GPIO_TypeDef *port, uint16_t pin);
void Heater_Off(GPIO_TypeDef *port, uint16_t pin);
uint8_t Heater_IsRunning(void);

#endif
