#include "pump.h"

static uint8_t pumpState = 0;

void Pump_Init(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
    pumpState = 0;
}

void Pump_On(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_SET);
    pumpState = 1;
}

void Pump_Off(GPIO_TypeDef *port, uint16_t pin)
{
    HAL_GPIO_WritePin(port, pin, GPIO_PIN_RESET);
    pumpState = 0;
}

uint8_t Pump_IsRunning(void)
{
    return pumpState;
}
