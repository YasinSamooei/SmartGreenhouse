/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define LDR_Pin GPIO_PIN_0
#define LDR_GPIO_Port GPIOA
#define Soil_Simulator_Pin GPIO_PIN_1
#define Soil_Simulator_GPIO_Port GPIOA
#define Gas_Sensor_Analog_Pin GPIO_PIN_2
#define Gas_Sensor_Analog_GPIO_Port GPIOA
#define DHT22_Pin GPIO_PIN_3
#define DHT22_GPIO_Port GPIOA
#define LM35_Pin GPIO_PIN_4
#define LM35_GPIO_Port GPIOA
#define Humidity_Pin GPIO_PIN_5
#define Humidity_GPIO_Port GPIOA
#define LCD_RS_Pin GPIO_PIN_0
#define LCD_RS_GPIO_Port GPIOB
#define LCD_EN_Pin GPIO_PIN_1
#define LCD_EN_GPIO_Port GPIOB
#define LCD_D4_Pin GPIO_PIN_2
#define LCD_D4_GPIO_Port GPIOB
#define Heater_Pin GPIO_PIN_12
#define Heater_GPIO_Port GPIOB
#define Pump_Pin GPIO_PIN_13
#define Pump_GPIO_Port GPIOB
#define Fan_Pin GPIO_PIN_14
#define Fan_GPIO_Port GPIOB
#define MQ9_Digital_Data_Pin GPIO_PIN_15
#define MQ9_Digital_Data_GPIO_Port GPIOB
#define Artificial_Light_Pin GPIO_PIN_8
#define Artificial_Light_GPIO_Port GPIOA
#define TEMP_LED_GREEN_Pin GPIO_PIN_11
#define TEMP_LED_GREEN_GPIO_Port GPIOA
#define TEMP_LED_RED_Pin GPIO_PIN_12
#define TEMP_LED_RED_GPIO_Port GPIOA
#define HUM_LED_BLUE_Pin GPIO_PIN_13
#define HUM_LED_BLUE_GPIO_Port GPIOA
#define HUM_LED_YELLOW_Pin GPIO_PIN_14
#define HUM_LED_YELLOW_GPIO_Port GPIOA
#define BUZZER_Pin GPIO_PIN_15
#define BUZZER_GPIO_Port GPIOA
#define LCD_D5_Pin GPIO_PIN_3
#define LCD_D5_GPIO_Port GPIOB
#define LCD_D6_Pin GPIO_PIN_4
#define LCD_D6_GPIO_Port GPIOB
#define LCD_D7_Pin GPIO_PIN_5
#define LCD_D7_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
