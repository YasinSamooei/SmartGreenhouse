#ifndef FAN_H
#define FAN_H

#include "stm32f1xx_hal.h"

void Fan_On(GPIO_TypeDef *port, uint16_t pin);
void Fan_Off(GPIO_TypeDef *port, uint16_t pin);

#endif
