#include "dht22.h"
#include <string.h>
#include <stdio.h>

extern TIM_HandleTypeDef htim2;
extern UART_HandleTypeDef huart1;

#define DHT_TIMEOUT 150

static void debug(char *text)
{
    HAL_UART_Transmit(&huart1,
                      (uint8_t*)text,
                      strlen(text),
                      100);
}

static void delay_us(uint16_t us)
{
    __HAL_TIM_SET_COUNTER(&htim2,0);

    while(__HAL_TIM_GET_COUNTER(&htim2)<us);
}

static void Pin_Output(void)
{
    GPIO_InitTypeDef GPIO_InitStruct={0};

    GPIO_InitStruct.Pin=DHT_PIN;
    GPIO_InitStruct.Mode=GPIO_MODE_OUTPUT_OD;
    GPIO_InitStruct.Pull=GPIO_PULLUP;
    GPIO_InitStruct.Speed=GPIO_SPEED_FREQ_HIGH;

    HAL_GPIO_Init(DHT_PORT,&GPIO_InitStruct);
}

static void Pin_Input(void)
{
    GPIO_InitTypeDef GPIO_InitStruct={0};

    GPIO_InitStruct.Pin=DHT_PIN;
    GPIO_InitStruct.Mode=GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull=GPIO_PULLUP;

    HAL_GPIO_Init(DHT_PORT,&GPIO_InitStruct);
}

static void DHT_Start(void)
{
    debug("\r\n===== DHT START =====\r\n");

    Pin_Output();

    HAL_GPIO_WritePin(DHT_PORT,
                      DHT_PIN,
                      GPIO_PIN_RESET);

    debug("MCU LOW\r\n");

    HAL_Delay(18);

    HAL_GPIO_WritePin(DHT_PORT,
                      DHT_PIN,
                      GPIO_PIN_SET);

    delay_us(30);

    Pin_Input();

    if(HAL_GPIO_ReadPin(DHT_PORT,DHT_PIN))
        debug("LINE HIGH\r\n");
    else
        debug("LINE LOW\r\n");
}

static uint8_t DHT_Response(void)
{
    uint32_t timeout;

    timeout=0;

    while(HAL_GPIO_ReadPin(DHT_PORT,DHT_PIN))
    {
        delay_us(1);

        if(++timeout>DHT_TIMEOUT)
        {
            debug("No LOW\r\n");
            return 0;
        }
    }

    debug("LOW OK\r\n");

    timeout=0;

    while(!HAL_GPIO_ReadPin(DHT_PORT,DHT_PIN))
    {
        delay_us(1);

        if(++timeout>DHT_TIMEOUT)
        {
            debug("LOW Timeout\r\n");
            return 0;
        }
    }

    debug("HIGH OK\r\n");

    return 1;
}

static uint8_t DHT_ReadByte(void)
{
    uint8_t i;
    uint8_t value=0;
    uint32_t pulse;

    for(i=0;i<8;i++)
    {

        pulse=0;

        while(HAL_GPIO_ReadPin(DHT_PORT,DHT_PIN)==GPIO_PIN_RESET)
        {
            delay_us(1);

            if(++pulse>DHT_TIMEOUT)
            {
                debug("Bit Start Timeout\r\n");
                return 0;
            }
        }


        __HAL_TIM_SET_COUNTER(&htim2,0);

        while(HAL_GPIO_ReadPin(DHT_PORT,DHT_PIN)==GPIO_PIN_SET)
        {
            if(__HAL_TIM_GET_COUNTER(&htim2)>120)
            {
                debug("Bit High Timeout\r\n");
                return 0;
            }
        }

        pulse=__HAL_TIM_GET_COUNTER(&htim2);

        char msg[32];
        sprintf(msg, "Pulse=%lu\r\n", pulse);
        debug(msg);

        value<<=1;

        if(pulse>35)
            value|=1;
    }

    return value;
}

uint8_t DHT22_Read(DHT22_Data_t *data)
{
    uint8_t Rh1,Rh2,T1,T2,Checksum;

    DHT_Start();

    if(!DHT_Response())
    {
        debug("No Response\r\n");
        return 0;
    }

    Rh1=DHT_ReadByte();
    Rh2=DHT_ReadByte();

    T1=DHT_ReadByte();
    T2=DHT_ReadByte();

    Checksum=DHT_ReadByte();

    if(((Rh1+Rh2+T1+T2)&0xFF)!=Checksum)
    {
        debug("Checksum Error\r\n");
        return 0;
    }

    uint16_t humidity=((uint16_t)Rh1<<8)|Rh2;
    uint16_t temperature=((uint16_t)T1<<8)|T2;

    data->humidity=humidity/10.0f;

    if(temperature&0x8000)
    {
        temperature&=0x7FFF;
        data->temperature=-(temperature/10.0f);
    }
    else
    {
        data->temperature=temperature/10.0f;
    }

    debug("Read OK\r\n");

    return 1;
}

void DHT22_Init(void)
{
    HAL_TIM_Base_Start(&htim2);
}
