#include "lcd.h"

#define TEMP_MAX   35.0f
#define TEMP_MIN   18.0f

#define HUM_MAX    80.0f
#define HUM_MIN    40.0f

static void LCD_EnablePulse(void);
static void LCD_Send4Bit(uint8_t data);
static void LCD_Send(uint8_t data,uint8_t rs);

static char lcdBuffer[64];

static void LCD_EnablePulse(void)
{
    HAL_GPIO_WritePin(LCD_EN_GPIO_Port,LCD_EN_Pin,GPIO_PIN_SET);
    HAL_Delay(1);

    HAL_GPIO_WritePin(LCD_EN_GPIO_Port,LCD_EN_Pin,GPIO_PIN_RESET);
    HAL_Delay(1);
}

static void LCD_Send4Bit(uint8_t data)
{
    HAL_GPIO_WritePin(LCD_D4_GPIO_Port,LCD_D4_Pin,(data>>0)&1);

    HAL_GPIO_WritePin(LCD_D5_GPIO_Port,LCD_D5_Pin,(data>>1)&1);

    HAL_GPIO_WritePin(LCD_D6_GPIO_Port,LCD_D6_Pin,(data>>2)&1);

    HAL_GPIO_WritePin(LCD_D7_GPIO_Port,LCD_D7_Pin,(data>>3)&1);

    LCD_EnablePulse();
}

static void LCD_Send(uint8_t data,uint8_t rs)
{
    HAL_GPIO_WritePin(LCD_RS_GPIO_Port,
                      LCD_RS_Pin,
                      rs);

    LCD_Send4Bit(data>>4);

    LCD_Send4Bit(data&0x0F);

    HAL_Delay(2);
}

void LCD_Command(uint8_t cmd)
{
    LCD_Send(cmd,0);
}

void LCD_Data(uint8_t data)
{
    LCD_Send(data,1);
}

void LCD_WriteChar(char c)
{
    LCD_Data(c);
}

void LCD_Print(char *str)
{
    while(*str)
    {
        LCD_WriteChar(*str++);
    }
}

void LCD_Clear(void)
{
    LCD_Command(0x01);

    HAL_Delay(3);
}

void LCD_Home(void)
{
    LCD_Command(0x02);

    HAL_Delay(3);
}

void LCD_SetCursor(uint8_t row,uint8_t col)
{
    uint8_t addr;

    switch(row)
    {
        case 0:
            addr=0x00+col;
            break;

        case 1:
            addr=0x40+col;
            break;

        case 2:
            addr=0x14+col;
            break;

        default:
            addr=0x54+col;
            break;
    }

    LCD_Command(0x80|addr);
}

void LCD_Printf(const char *fmt,...)
{
    va_list args;

    va_start(args,fmt);

    vsnprintf(lcdBuffer,sizeof(lcdBuffer),fmt,args);

    va_end(args);

    LCD_Print(lcdBuffer);
}

void LCD_Init(void)
{
    HAL_Delay(50);

    HAL_GPIO_WritePin(LCD_RS_GPIO_Port,LCD_RS_Pin,GPIO_PIN_RESET);

    LCD_Send4Bit(0x03);
    HAL_Delay(5);

    LCD_Send4Bit(0x03);
    HAL_Delay(5);

    LCD_Send4Bit(0x03);
    HAL_Delay(1);

    LCD_Send4Bit(0x02);

    LCD_Command(0x28);

    LCD_Command(0x0C);

    LCD_Command(0x06);

    LCD_Clear();
}

void LCD_Update(
float temperature,
float humidity,
uint16_t soil,
uint16_t ldr,
uint8_t gas,
uint8_t fan,
uint8_t pump,
uint8_t light,
uint8_t alarm)
{

    /*=========================
            LINE 1
    =========================*/

    LCD_SetCursor(0,0);

    LCD_Printf("Tem:%2.1fC Hum:%2.0f%%   ",
               temperature,
               humidity);



    /*=========================
            LINE 2
    =========================*/

    LCD_SetCursor(1,0);

    LCD_Printf("Soil:%3d%% Gas:%s      ",
               soil,
               gas ? "DNG":"OK");



    /*=========================
            LINE 3
    =========================*/

    LCD_SetCursor(2,0);

    LCD_Printf("F:%s P:%s L:%s",
               fan ? "ON ":"OFF",
               pump ? "ON ":"OFF",
               light ? "ON ":"OFF");



    /*=========================
            LINE 4
    =========================*/

    LCD_SetCursor(3,0);

    if(alarm)
    {

        if(temperature>TEMP_MAX)
        {
            LCD_Print("TEMP HIGH !!!     ");
        }
        else
        if(temperature<TEMP_MIN)
        {
            LCD_Print("TEMP LOW !!!      ");
        }
        else
        if(humidity>HUM_MAX)
        {
            LCD_Print("HUM HIGH !!!      ");
        }
        else
        if(humidity<HUM_MIN)
        {
            LCD_Print("HUM LOW !!!       ");
        }
        else
        if(gas)
        {
            LCD_Print("GAS DETECTED !!   ");
        }
        else
        {
            LCD_Print("CHECK SYSTEM      ");
        }

    }
    else
    {
        LCD_Print("SYSTEM NORMAL     ");
    }

}
