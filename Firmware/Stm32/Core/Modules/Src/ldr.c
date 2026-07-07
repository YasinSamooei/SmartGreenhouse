#include "ldr.h"
#include "adc_common.h"

void LDR_Init(ADC_HandleTypeDef *hadc)
{
    HAL_ADCEx_Calibration_Start(hadc);
}

uint16_t LDR_ReadRaw(ADC_HandleTypeDef *hadc)
{
    return ADC_ReadChannel(hadc, ADC_CHANNEL_0);   /* PA0 */
}

void LDR_ControlLight(uint16_t ldrValue, GPIO_TypeDef *port, uint16_t pin)
{
    if (ldrValue < LDR_LIGHT_THRESHOLD)
    {
        HAL_GPIO_WritePin(port, pin, GPIO_PIN_SET);
    }
    else
    {
        HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
    }
}
