#include "uart3_task.h"
#include "greenhouse_state.h"
#include "main.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define UART3_BUFFER_SIZE 256

extern UART_HandleTypeDef huart3;
extern UART_HandleTypeDef huart1;

static uint8_t rxChar;
static char uart3Buffer[UART3_BUFFER_SIZE];
static uint8_t rxIndex = 0;
static uint32_t lastRxTime = 0;
static uint8_t packetReady = 0;

char debugMsg[256];


static void ProcessCompletePacket(char* data)
{

    char clean[UART3_BUFFER_SIZE] = {0};
    int j = 0;
    for(int i = 0; data[i] && i < UART3_BUFFER_SIZE; i++)
    {
        if(isalpha((unsigned char)data[i]) || isdigit((unsigned char)data[i]))
            clean[j++] = data[i];
    }
    clean[j] = '\0';

    if(strlen(clean) == 0)
    {
        return;
    }

    snprintf(debugMsg, sizeof(debugMsg), "CLEAN: %s\r\n", clean);
    HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);


    if(strstr(clean, "AUTO") != NULL || strstr(clean, "AO") != NULL ||
       (strchr(clean, 'A') != NULL && strchr(clean, 'O') != NULL))
    {
        char* pos = strstr(clean, "AUTO");
        if(pos == NULL) pos = strstr(clean, "AO");
        if(pos == NULL) pos = strchr(clean, 'A');

        if(pos != NULL)
        {

            while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
            if(isdigit((unsigned char)*pos))
            {
                auto_mode = *pos - '0';
                snprintf(debugMsg, sizeof(debugMsg), "AUTO MODE = %d\r\n", auto_mode);
                HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
                return;
            }
            else
            {

                auto_mode = (auto_mode == 1) ? 0 : 1;
                snprintf(debugMsg, sizeof(debugMsg), "AUTO TOGGLED = %d\r\n", auto_mode);
                HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
                return;
            }
        }
    }

    if(auto_mode == 1)
    {
        snprintf(debugMsg, sizeof(debugMsg), "IGNORED (AUTO MODE)\r\n");
        HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        return;
    }




    if(strchr(clean, 'F') != NULL)
    {
        char* pos = strchr(clean, 'F') + 1;

        while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
        if(isdigit((unsigned char)*pos))
        {
            fan = *pos - '0';
            snprintf(debugMsg, sizeof(debugMsg), "FAN = %d\r\n", fan);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
        else
        {

            fan = (fan == 1) ? 0 : 1;
            snprintf(debugMsg, sizeof(debugMsg), "FAN TOGGLED = %d\r\n", fan);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
    }


    if(strchr(clean, 'P') != NULL)
    {
        char* pos = strchr(clean, 'P') + 1;
        while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
        if(isdigit((unsigned char)*pos))
        {
            pump = *pos - '0';
            snprintf(debugMsg, sizeof(debugMsg), "PUMP = %d\r\n", pump);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
        else
        {
            pump = (pump == 1) ? 0 : 1;
            snprintf(debugMsg, sizeof(debugMsg), "PUMP TOGGLED = %d\r\n", pump);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
    }


    if(strstr(clean, "HE") != NULL || strchr(clean, 'H') != NULL)
    {
        char* pos = strstr(clean, "HE");
        if(pos == NULL) pos = strchr(clean, 'H');
        else pos += 2;

        while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
        if(isdigit((unsigned char)*pos))
        {
            heater = *pos - '0';
            snprintf(debugMsg, sizeof(debugMsg), "HEATER = %d\r\n", heater);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
        else
        {
            heater = (heater == 1) ? 0 : 1;
            snprintf(debugMsg, sizeof(debugMsg), "HEATER TOGGLED = %d\r\n", heater);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
    }


    if(strstr(clean, "LI") != NULL || strchr(clean, 'L') != NULL)
    {
        char* pos = strstr(clean, "LI");
        if(pos == NULL) pos = strchr(clean, 'L');
        else pos += 2;

        while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
        if(isdigit((unsigned char)*pos))
        {
            light = *pos - '0';
            snprintf(debugMsg, sizeof(debugMsg), "LIGHT = %d\r\n", light);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
        else
        {
            light = (light == 1) ? 0 : 1;
            snprintf(debugMsg, sizeof(debugMsg), "LIGHT TOGGLED = %d\r\n", light);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
    }


    if(strchr(clean, 'A') != NULL && strstr(clean, "AUTO") == NULL && strstr(clean, "AO") == NULL)
    {
        char* pos = strchr(clean, 'A') + 1;
        while(*pos != '\0' && !isdigit((unsigned char)*pos)) pos++;
        if(isdigit((unsigned char)*pos))
        {
            alarm = *pos - '0';
            snprintf(debugMsg, sizeof(debugMsg), "ALARM = %d\r\n", alarm);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
        else
        {
            alarm = (alarm == 1) ? 0 : 1;
            snprintf(debugMsg, sizeof(debugMsg), "ALARM TOGGLED = %d\r\n", alarm);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);
        }
    }
}

void UART3_StartReceive(void)
{
    HAL_UART_Receive_IT(&huart3, &rxChar, 1);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if(huart == &huart3)
    {

        if(rxIndex < UART3_BUFFER_SIZE - 1)
        {
            uart3Buffer[rxIndex++] = rxChar;
        }


        lastRxTime = HAL_GetTick();


        if(rxChar == '\n' || rxChar == '\r')
        {
            packetReady = 1;
        }


        HAL_UART_Receive_IT(&huart3, &rxChar, 1);
    }
}

void UART3_CheckAndProcess(void)
{

    if(packetReady && rxIndex > 0)
    {
        if((HAL_GetTick() - lastRxTime) > 10)
        {
            uart3Buffer[rxIndex] = '\0';

            snprintf(debugMsg, sizeof(debugMsg), "PACKET: [%s]\r\n", uart3Buffer);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);

            ProcessCompletePacket(uart3Buffer);


            rxIndex = 0;
            packetReady = 0;
            memset(uart3Buffer, 0, sizeof(uart3Buffer));
        }
    }
    else if(rxIndex > 0 && !packetReady)
    {

        if((HAL_GetTick() - lastRxTime) > 100)  // 100ms timeout
        {
            uart3Buffer[rxIndex] = '\0';

            snprintf(debugMsg, sizeof(debugMsg), "TIMEOUT PACKET: [%s]\r\n", uart3Buffer);
            HAL_UART_Transmit(&huart1, (uint8_t*)debugMsg, strlen(debugMsg), 100);

            ProcessCompletePacket(uart3Buffer);

            rxIndex = 0;
            packetReady = 0;
            memset(uart3Buffer, 0, sizeof(uart3Buffer));
        }
    }
}
