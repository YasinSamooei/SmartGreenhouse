#include "gas.h"
#include "adc_common.h"

void Gas_Init(ADC_HandleTypeDef *hadc)
{
    HAL_ADCEx_Calibration_Start(hadc);
}

uint16_t Gas_ReadAnalog(ADC_HandleTypeDef *hadc)
{
    return ADC_ReadChannel(hadc, ADC_CHANNEL_2);   /* PA2 */
}

uint8_t Gas_ReadDigital(GPIO_TypeDef *port, uint16_t pin)
{
    return (uint8_t)HAL_GPIO_ReadPin(port, pin);
}

void Gas_ReadAll(ADC_HandleTypeDef *hadc,
                 GPIO_TypeDef *port,
                 uint16_t pin,
                 Gas_Data_t *data)
{
    data->analogValue = Gas_ReadAnalog(hadc);

    data->analogPercent = Gas_GetPercent(data->analogValue);

    data->digitalValue = Gas_ReadDigital(port,pin);
}

uint8_t Gas_GetPercent(uint16_t adcValue)
{
    return (uint8_t)((adcValue * 100U) / 4095U);
}

uint8_t Gas_IsDanger(const Gas_Data_t *data)
{
    return data->digitalValue;
}
