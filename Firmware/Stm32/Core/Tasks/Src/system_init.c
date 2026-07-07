#include "system_init.h"

#include "main.h"
#include "ldr.h"
#include "gas.h"
#include "soil.h"
#include "dht22.h"
#include "pump.h"
#include "lm35.h"
#include "hih5030.h"
#include "heater.h"
#include "rgb_led.h"
#include "esp_uart.h"
#include "lcd.h"
#include "greenhouse_state.h"
#include <stdio.h>
#include <string.h>

extern ADC_HandleTypeDef hadc1;
extern TIM_HandleTypeDef htim4;
extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart3;

void System_Init(void)
{
    LDR_Init(&hadc1);
    Gas_Init(&hadc1);
    Soil_Init(&hadc1);

    DHT22_Init();

    Pump_Init(GPIOB, GPIO_PIN_13);
    Heater_Init(GPIOB, GPIO_PIN_12);

    LM35_Init(&hadc1);
    HIH5030_Init(&hadc1);

    RGB_Init(&htim4);

    ESP_UART_Init(&huart3);

    LCD_Init();

    LCD_SetCursor(0,0);
    LCD_Print(" SMART GREENHOUSE ");

    LCD_SetCursor(1,0);
    LCD_Print(" Initializing... ");

    sprintf(uartBuffer,"SMART GREENHOUSE\r\nInitializing...\r\n");
    HAL_UART_Transmit(&huart1,
                      (uint8_t*)uartBuffer,
                      strlen(uartBuffer),
                      100);

    HAL_Delay(500);

    LCD_Clear();

}
