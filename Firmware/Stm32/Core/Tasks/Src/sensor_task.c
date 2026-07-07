#include "sensor_task.h"

#include "ldr.h"
#include "gas.h"
#include "soil.h"
#include "lm35.h"
#include "hih5030.h"
#include "rgb_led.h"
#include "greenhouse_state.h"

extern ADC_HandleTypeDef hadc1;


void SensorTask(void)
{
    ldrValue = LDR_ReadRaw(&hadc1);

    // Only auto control light if in auto mode
    if(auto_mode == 1)
    {
        LDR_ControlLight(ldrValue, GPIOA, GPIO_PIN_8);
    }
    // In manual mode, light is controlled via UART3 commands

    Gas_ReadAll(&hadc1, GPIOB, GPIO_PIN_15, &gasData);
    Soil_ReadAll(&hadc1, &soilData);
    temperature = LM35_ReadTemperature(&hadc1);
    humidity = HIH5030_ReadHumidity(&hadc1);
    RGB_SetHumidity(humidity);
}
