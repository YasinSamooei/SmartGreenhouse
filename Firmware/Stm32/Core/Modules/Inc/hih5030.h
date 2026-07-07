#ifndef HIH5030_H
#define HIH5030_H

#include "stm32f1xx_hal.h"

#define HUM_MAX    80
#define HUM_MIN    55

void HIH5030_Init(ADC_HandleTypeDef *hadc);
float HIH5030_ReadHumidity(ADC_HandleTypeDef *hadc);

#endif
