#ifndef ESP_UART_H
#define ESP_UART_H

#include "main.h"

void ESP_UART_Init(UART_HandleTypeDef *huart);

uint8_t ESP_UART_IsBusy(void);

HAL_StatusTypeDef ESP_UART_Send(char *text);

#endif
