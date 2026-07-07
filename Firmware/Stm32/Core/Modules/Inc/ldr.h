#ifndef LDR_H
#define LDR_H

#include "stm32f1xx_hal.h"


#define LDR_LIGHT_THRESHOLD   1800U

void     LDR_Init(ADC_HandleTypeDef *hadc);
uint16_t LDR_ReadRaw(ADC_HandleTypeDef *hadc);
void     LDR_ControlLight(uint16_t ldrValue, GPIO_TypeDef *port, uint16_t pin);

#endif
