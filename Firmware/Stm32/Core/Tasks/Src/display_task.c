#include "display_task.h"

#include "lcd.h"
#include "gas.h"
#include "greenhouse_state.h"

void DisplayTask(void)
{
    LCD_Update(
        temperature,
        humidity,
        soilData.percent,
        ldrValue,
        Gas_IsDanger(&gasData),
        HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_14),
        HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13),
        HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_8),
        alarm);
}
