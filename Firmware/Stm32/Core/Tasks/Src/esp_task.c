#include "esp_task.h"

#include "esp_uart.h"
#include "greenhouse_state.h"
#include "heater.h"

#include <stdio.h>

static char txBuffer[128];

void ESPTask(void)
{
    if(ESP_UART_IsBusy())
        return;

    uint16_t temp = (uint16_t)(temperature * 10.0f);
    uint16_t hum  = (uint16_t)(humidity * 10.0f);

    snprintf(txBuffer,
             sizeof(txBuffer),
             "T=%u.%u,H=%u.%u,S=%u,G=%u,L=%u,F=%u,P=%u,HE=%u,A=%u,LI=%u\r\n",
             temp / 10,
             temp % 10,
             hum / 10,
             hum % 10,
             soilData.percent,
             gasData.analogPercent,
             ldrValue,
             fan,
             pump,
             Heater_IsRunning(),
             alarm,
		     HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_8));

    ESP_UART_Send(txBuffer);
}
