#include "uart_task.h"

#include "gas.h"
#include "soil.h"
#include <stdio.h>
#include <string.h>
#include "greenhouse_state.h"

extern UART_HandleTypeDef huart1;


void UARTTask(void)
{
    sprintf(uartBuffer,
            "LDR:%u GAS:%u%% DIG:%u SOIL:%u%% TEMP:%.1fC HUM:%.1f%%\r\n",
            ldrValue,
            gasData.analogPercent,
            gasData.digitalValue,
            soilData.percent,
            temperature,
            humidity);

    HAL_UART_Transmit(&huart1,
                      (uint8_t*)uartBuffer,
                      strlen(uartBuffer),
                      100);
}
