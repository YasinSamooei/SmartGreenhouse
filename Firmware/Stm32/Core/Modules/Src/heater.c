#include "heater.h"

static uint8_t heaterState = 0;

void Heater_Init(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
    heaterState = 0;
}

void Heater_On(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_SET);
    heaterState = 1;
}

void Heater_Off(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
    heaterState = 0;
}

uint8_t Heater_IsRunning(void)
{
    return heaterState;
}
