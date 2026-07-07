#ifndef ESP_PROTOCOL_H
#define ESP_PROTOCOL_H

#include "stdint.h"

typedef struct __attribute__((packed))
{
    uint8_t  header1;
    uint8_t  header2;

    uint16_t temperature;
    uint16_t humidity;

    uint16_t soil;
    uint16_t gas;
    uint16_t ldr;

    uint8_t fan;
    uint8_t pump;
    uint8_t heater;
    uint8_t alarm;

    uint16_t crc;

}ESP32Packet_t;

#endif
