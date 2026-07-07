#ifndef SOIL_H
#define SOIL_H

#include "stm32f1xx_hal.h"

#define SOIL_THRESHOLD_PERCENT   40U

typedef struct
{
    uint16_t rawValue;
    uint8_t  percent;
} Soil_Data_t;

void     Soil_Init(ADC_HandleTypeDef *hadc);
uint16_t Soil_ReadRaw(ADC_HandleTypeDef *hadc);
uint8_t  Soil_GetPercent(uint16_t adcValue);
void     Soil_ReadAll(ADC_HandleTypeDef *hadc, Soil_Data_t *data);
uint8_t  Soil_IsDry(const Soil_Data_t *data);

#endif
