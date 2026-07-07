#include "rgb_led.h"

#define HUM_MIN    40.0f
#define HUM_MAX    80.0f

static TIM_HandleTypeDef *rgbTimer = NULL;

void RGB_Init(TIM_HandleTypeDef *htim)
{
    rgbTimer = htim;

    HAL_TIM_PWM_Start(rgbTimer, TIM_CHANNEL_1);   // PB6 -> Red
    HAL_TIM_PWM_Start(rgbTimer, TIM_CHANNEL_2);   // PB7 -> Green
    HAL_TIM_PWM_Start(rgbTimer, TIM_CHANNEL_3);   // PB8 -> Blue
}

void RGB_SetHumidity(float humidity)
{
    uint32_t pwmMax = __HAL_TIM_GET_AUTORELOAD(rgbTimer);

    uint32_t red;
    uint32_t green;
    uint32_t blue = 0;

    if(humidity <= HUM_MIN)
    {

        red   = pwmMax;
        green = 0;
    }
    else if(humidity >= HUM_MAX)
    {

        red   = 0;
        green = pwmMax;
    }
    else
    {

        float ratio = (humidity - HUM_MIN) / (HUM_MAX - HUM_MIN);

        green = (uint32_t)(ratio * pwmMax);
        red   = pwmMax - green;
    }

    __HAL_TIM_SET_COMPARE(rgbTimer, TIM_CHANNEL_1, red);
    __HAL_TIM_SET_COMPARE(rgbTimer, TIM_CHANNEL_2, green);
    __HAL_TIM_SET_COMPARE(rgbTimer, TIM_CHANNEL_3, blue);
}
