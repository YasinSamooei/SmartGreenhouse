#include "esp_uart.h"

#include <string.h>

static UART_HandleTypeDef *espUart;

static volatile uint8_t busy = 0;

void ESP_UART_Init(UART_HandleTypeDef *huart)
{
    espUart = huart;
}

uint8_t ESP_UART_IsBusy(void)
{
    return busy;
}

HAL_StatusTypeDef ESP_UART_Send(char *text)
{
    if(busy)
        return HAL_BUSY;

    busy = 1;

    HAL_StatusTypeDef status =
        HAL_UART_Transmit(
            espUart,
            (uint8_t*)text,
            strlen(text),
            HAL_MAX_DELAY);

    busy = 0;

    return status;
}

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart == espUart)
    {
        busy = 0;
    }
}
