#include "hih5030.h"
#include "adc_common.h"

#define HIH5030_VREF 5.0f

void HIH5030_Init(ADC_HandleTypeDef *hadc)
{
    HAL_ADCEx_Calibration_Start(hadc);
}


float HIH5030_ReadHumidity(ADC_HandleTypeDef *hadc)
{
    uint32_t sum = 0;
    const uint8_t samples = 10;

    // Discard first 4 readings
    for(int i = 0; i < 7; i++)
    {
        (void)ADC_ReadChannel(hadc, ADC_CHANNEL_5);
    }

    // Read 10 valid samples
    for(int i = 0; i < samples; i++)
    {
        sum += ADC_ReadChannel(hadc, ADC_CHANNEL_5);
    }

    float adcValue = sum / (float)samples;

    float voltage = (adcValue * HIH5030_VREF) / 4095.0f;

    float humidity = ((voltage / HIH5030_VREF) - 0.1515f) / 0.00636f;

    if(humidity < 0.0f) humidity = 0.0f;
    if(humidity > 100.0f) humidity = 100.0f;

    return humidity;
}
