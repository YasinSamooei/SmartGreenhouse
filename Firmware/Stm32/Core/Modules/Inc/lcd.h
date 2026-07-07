#ifndef __LCD_H
#define __LCD_H

#include "main.h"
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

/*==============================
    Pin Definition
==============================*/

#define LCD_RS_GPIO_Port     GPIOB
#define LCD_RS_Pin           GPIO_PIN_0

#define LCD_EN_GPIO_Port     GPIOB
#define LCD_EN_Pin           GPIO_PIN_1

#define LCD_D4_GPIO_Port     GPIOB
#define LCD_D4_Pin           GPIO_PIN_2

#define LCD_D5_GPIO_Port     GPIOB
#define LCD_D5_Pin           GPIO_PIN_3

#define LCD_D6_GPIO_Port     GPIOB
#define LCD_D6_Pin           GPIO_PIN_4

#define LCD_D7_GPIO_Port     GPIOB
#define LCD_D7_Pin           GPIO_PIN_5


/*==============================
        Functions
==============================*/

void LCD_Init(void);

void LCD_Clear(void);

void LCD_Home(void);

void LCD_SetCursor(uint8_t row,uint8_t col);

void LCD_WriteChar(char c);

void LCD_Print(char *str);

void LCD_Printf(const char *fmt,...);

void LCD_Command(uint8_t cmd);

void LCD_Data(uint8_t data);

void LCD_Update(
float temperature,
float humidity,
uint16_t soil,
uint16_t ldr,
uint8_t gas,
uint8_t fan,
uint8_t pump,
uint8_t light,
uint8_t alarm);

#endif
