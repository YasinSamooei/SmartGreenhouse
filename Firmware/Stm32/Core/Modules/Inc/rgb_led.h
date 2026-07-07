#ifndef RGB_LED_H
#define RGB_LED_H

#include "stm32f1xx_hal.h"

void RGB_Init(TIM_HandleTypeDef *htim);
void RGB_SetHumidity(float humidity);

#endif
