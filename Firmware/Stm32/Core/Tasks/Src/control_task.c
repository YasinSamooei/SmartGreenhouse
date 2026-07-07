#include "control_task.h"
#include "main.h"
#include "fan.h"
#include "pump.h"
#include "heater.h"
#include "gas.h"
#include "soil.h"
#include "lm35.h"
#include "hih5030.h"
#include "greenhouse_state.h"

void ControlTask(void)
{
    if(auto_mode == 1)
    {
        alarm = 0;
        fan = 0;
        pump = 0;

        if(Gas_IsDanger(&gasData))
        {
            fan = 1;
        }

        if(Soil_IsDry(&soilData))
        {
            pump = 1;
        }

        /* Temperature */
        if(temperature < TEMP_MIN)
        {
            HAL_GPIO_WritePin(TEMP_LED_RED_GPIO_Port, TEMP_LED_RED_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(TEMP_LED_GREEN_GPIO_Port, TEMP_LED_GREEN_Pin, GPIO_PIN_RESET);
            alarm = 1;
        }
        else if(temperature > TEMP_MAX)
        {
            HAL_GPIO_WritePin(TEMP_LED_RED_GPIO_Port, TEMP_LED_RED_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(TEMP_LED_GREEN_GPIO_Port, TEMP_LED_GREEN_Pin, GPIO_PIN_RESET);
            alarm = 1;
            fan = 1;
        }
        else
        {
            HAL_GPIO_WritePin(TEMP_LED_RED_GPIO_Port, TEMP_LED_RED_Pin, GPIO_PIN_RESET);
            HAL_GPIO_WritePin(TEMP_LED_GREEN_GPIO_Port, TEMP_LED_GREEN_Pin, GPIO_PIN_SET);
        }

        /* Humidity */
        if(humidity < HUM_MIN)
        {
            HAL_GPIO_WritePin(HUM_LED_YELLOW_GPIO_Port, HUM_LED_YELLOW_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(HUM_LED_BLUE_GPIO_Port, HUM_LED_BLUE_Pin, GPIO_PIN_RESET);
            alarm = 1;
            pump = 1;
        }
        else if(humidity > HUM_MAX)
        {
            HAL_GPIO_WritePin(HUM_LED_YELLOW_GPIO_Port, HUM_LED_YELLOW_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(HUM_LED_BLUE_GPIO_Port, HUM_LED_BLUE_Pin, GPIO_PIN_RESET);
            alarm = 1;
            fan = 1;
        }
        else
        {
            HAL_GPIO_WritePin(HUM_LED_YELLOW_GPIO_Port, HUM_LED_YELLOW_Pin, GPIO_PIN_RESET);
            HAL_GPIO_WritePin(HUM_LED_BLUE_GPIO_Port, HUM_LED_BLUE_Pin, GPIO_PIN_SET);
        }

        /* Alarm */
        if(alarm)
            HAL_GPIO_TogglePin(BUZZER_GPIO_Port, BUZZER_Pin);
        else
            HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_RESET);

        /* Fan */
        if(fan)
            Fan_On(GPIOB, GPIO_PIN_14);
        else
            Fan_Off(GPIOB, GPIO_PIN_14);

        /* Pump */
        if(pump)
            Pump_On(GPIOB, GPIO_PIN_13);
        else
            Pump_Off(GPIOB, GPIO_PIN_13);

        /* Heater */
        if(temperature < (TEMP_TARGET - HEATER_OFF_EARLY))
            Heater_On(GPIOB, GPIO_PIN_12);
        else
            Heater_Off(GPIOB, GPIO_PIN_12);

        /* Light - Auto control (from SensorTask) */
        // Light is controlled in SensorTask via LDR_ControlLight
    }
    else  // MANUAL MODE
    {
        // Keep LED indicators for monitoring
        if(temperature < TEMP_MIN || temperature > TEMP_MAX)
        {
            HAL_GPIO_WritePin(TEMP_LED_RED_GPIO_Port, TEMP_LED_RED_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(TEMP_LED_GREEN_GPIO_Port, TEMP_LED_GREEN_Pin, GPIO_PIN_RESET);
            alarm = 1;
        }
        else
        {
            HAL_GPIO_WritePin(TEMP_LED_RED_GPIO_Port, TEMP_LED_RED_Pin, GPIO_PIN_RESET);
            HAL_GPIO_WritePin(TEMP_LED_GREEN_GPIO_Port, TEMP_LED_GREEN_Pin, GPIO_PIN_SET);
        }

        if(humidity < HUM_MIN || humidity > HUM_MAX)
        {
            HAL_GPIO_WritePin(HUM_LED_YELLOW_GPIO_Port, HUM_LED_YELLOW_Pin, GPIO_PIN_SET);
            HAL_GPIO_WritePin(HUM_LED_BLUE_GPIO_Port, HUM_LED_BLUE_Pin, GPIO_PIN_RESET);
            alarm = 1;
        }
        else
        {
            HAL_GPIO_WritePin(HUM_LED_YELLOW_GPIO_Port, HUM_LED_YELLOW_Pin, GPIO_PIN_RESET);
            HAL_GPIO_WritePin(HUM_LED_BLUE_GPIO_Port, HUM_LED_BLUE_Pin, GPIO_PIN_SET);
        }

        // Buzzer for alarm monitoring
        if(alarm)
            HAL_GPIO_TogglePin(BUZZER_GPIO_Port, BUZZER_Pin);
        else
            HAL_GPIO_WritePin(BUZZER_GPIO_Port, BUZZER_Pin, GPIO_PIN_RESET);

        // Manual actuator control
        if(fan)
            Fan_On(GPIOB, GPIO_PIN_14);
        else
            Fan_Off(GPIOB, GPIO_PIN_14);

        if(pump)
            Pump_On(GPIOB, GPIO_PIN_13);
        else
            Pump_Off(GPIOB, GPIO_PIN_13);

        if(heater)
            Heater_On(GPIOB, GPIO_PIN_12);
        else
            Heater_Off(GPIOB, GPIO_PIN_12);

        // Manual Light Control - Override SensorTask
        if(light)
            HAL_GPIO_WritePin(Artificial_Light_GPIO_Port, Artificial_Light_Pin, GPIO_PIN_SET);
        else
            HAL_GPIO_WritePin(Artificial_Light_GPIO_Port, Artificial_Light_Pin, GPIO_PIN_RESET);
    }
}
