#ifndef ADC_COMMON_H
#define ADC_COMMON_H

#include "stm32f1xx_hal.h"

uint16_t ADC_ReadChannel(ADC_HandleTypeDef *hadc, uint32_t channel);

#endif /* ADC_COMMON_H */
