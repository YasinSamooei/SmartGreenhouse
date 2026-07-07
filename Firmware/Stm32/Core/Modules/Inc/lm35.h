#ifndef LM35_H
#define LM35_H

#include "stm32f1xx_hal.h"

#define TEMP_MAX   30
#define TEMP_MIN   18
#define TEMP_TARGET      24.0f
#define HEATER_OFF_EARLY 2.0f

void LM35_Init(ADC_HandleTypeDef *hadc);
float LM35_ReadTemperature(ADC_HandleTypeDef *hadc);

#endif
