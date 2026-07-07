#include "lm35.h"
#include "adc_common.h"

#define LM35_VREF 5.0f

void LM35_Init(ADC_HandleTypeDef *hadc)
{
    HAL_ADCEx_Calibration_Start(hadc);
}

float LM35_ReadTemperature(ADC_HandleTypeDef *hadc)
{
    uint32_t sum = 0;
    const uint8_t samples = 10;

    // warm-up read
    (void)ADC_ReadChannel(hadc, ADC_CHANNEL_4);

    for (int i = 0; i < samples; i++)
    {
        sum += ADC_ReadChannel(hadc, ADC_CHANNEL_4);
    }

    float adcValue = sum / (float)samples;

    float voltage = (adcValue * LM35_VREF) / 4095.0f;

    // LM35 = 10mV per °C
    float temperature = voltage * 100.0f;

    return temperature;
}
