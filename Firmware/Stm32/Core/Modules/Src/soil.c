#include "soil.h"
#include "adc_common.h"

void Soil_Init(ADC_HandleTypeDef *hadc)
{
    HAL_ADCEx_Calibration_Start(hadc);
}

uint16_t Soil_ReadRaw(ADC_HandleTypeDef *hadc)
{
    return ADC_ReadChannel(hadc, ADC_CHANNEL_1);   /* PA1 */
}

uint8_t Soil_GetPercent(uint16_t adcValue)
{
    return (uint8_t)((adcValue * 100U) / 4095U);
}

void Soil_ReadAll(ADC_HandleTypeDef *hadc, Soil_Data_t *data)
{
    data->rawValue = Soil_ReadRaw(hadc);
    data->percent  = Soil_GetPercent(data->rawValue);
}

uint8_t Soil_IsDry(const Soil_Data_t *data)
{
    if(data->percent < SOIL_THRESHOLD_PERCENT)
    {
        return 1;
    }

    return 0;
}
