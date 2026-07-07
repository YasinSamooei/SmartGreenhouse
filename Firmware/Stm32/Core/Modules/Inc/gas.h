#ifndef GAS_H
#define GAS_H

#include "stm32f1xx_hal.h"


#define GAS_ANALOG_THRESHOLD   2500U

typedef struct
{
    uint16_t analogValue;
    uint8_t  analogPercent;
    uint8_t  digitalValue;
} Gas_Data_t;

void     Gas_Init(ADC_HandleTypeDef *hadc);
uint16_t Gas_ReadAnalog(ADC_HandleTypeDef *hadc);
uint8_t  Gas_ReadDigital(GPIO_TypeDef *port, uint16_t pin);
void     Gas_ReadAll(ADC_HandleTypeDef *hadc, GPIO_TypeDef *port, uint16_t pin, Gas_Data_t *data);
uint8_t Gas_GetPercent(uint16_t adcValue);
uint8_t Gas_IsDanger(const Gas_Data_t *data);
#endif
