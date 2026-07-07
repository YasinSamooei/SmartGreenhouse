################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Modules/Src/adc_common.c \
../Core/Modules/Src/dht22.c \
../Core/Modules/Src/esp_uart.c \
../Core/Modules/Src/fan.c \
../Core/Modules/Src/gas.c \
../Core/Modules/Src/greenhouse_state.c \
../Core/Modules/Src/heater.c \
../Core/Modules/Src/hih5030.c \
../Core/Modules/Src/lcd.c \
../Core/Modules/Src/ldr.c \
../Core/Modules/Src/lm35.c \
../Core/Modules/Src/pump.c \
../Core/Modules/Src/rgb_led.c \
../Core/Modules/Src/soil.c 

OBJS += \
./Core/Modules/Src/adc_common.o \
./Core/Modules/Src/dht22.o \
./Core/Modules/Src/esp_uart.o \
./Core/Modules/Src/fan.o \
./Core/Modules/Src/gas.o \
./Core/Modules/Src/greenhouse_state.o \
./Core/Modules/Src/heater.o \
./Core/Modules/Src/hih5030.o \
./Core/Modules/Src/lcd.o \
./Core/Modules/Src/ldr.o \
./Core/Modules/Src/lm35.o \
./Core/Modules/Src/pump.o \
./Core/Modules/Src/rgb_led.o \
./Core/Modules/Src/soil.o 

C_DEPS += \
./Core/Modules/Src/adc_common.d \
./Core/Modules/Src/dht22.d \
./Core/Modules/Src/esp_uart.d \
./Core/Modules/Src/fan.d \
./Core/Modules/Src/gas.d \
./Core/Modules/Src/greenhouse_state.d \
./Core/Modules/Src/heater.d \
./Core/Modules/Src/hih5030.d \
./Core/Modules/Src/lcd.d \
./Core/Modules/Src/ldr.d \
./Core/Modules/Src/lm35.d \
./Core/Modules/Src/pump.d \
./Core/Modules/Src/rgb_led.d \
./Core/Modules/Src/soil.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Modules/Src/%.o Core/Modules/Src/%.su Core/Modules/Src/%.cyclo: ../Core/Modules/Src/%.c Core/Modules/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I../Drivers/STM32F1xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -I../Core/Modules/Inc -I../Core/Tasks/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Core-2f-Modules-2f-Src

clean-Core-2f-Modules-2f-Src:
	-$(RM) ./Core/Modules/Src/adc_common.cyclo ./Core/Modules/Src/adc_common.d ./Core/Modules/Src/adc_common.o ./Core/Modules/Src/adc_common.su ./Core/Modules/Src/dht22.cyclo ./Core/Modules/Src/dht22.d ./Core/Modules/Src/dht22.o ./Core/Modules/Src/dht22.su ./Core/Modules/Src/esp_uart.cyclo ./Core/Modules/Src/esp_uart.d ./Core/Modules/Src/esp_uart.o ./Core/Modules/Src/esp_uart.su ./Core/Modules/Src/fan.cyclo ./Core/Modules/Src/fan.d ./Core/Modules/Src/fan.o ./Core/Modules/Src/fan.su ./Core/Modules/Src/gas.cyclo ./Core/Modules/Src/gas.d ./Core/Modules/Src/gas.o ./Core/Modules/Src/gas.su ./Core/Modules/Src/greenhouse_state.cyclo ./Core/Modules/Src/greenhouse_state.d ./Core/Modules/Src/greenhouse_state.o ./Core/Modules/Src/greenhouse_state.su ./Core/Modules/Src/heater.cyclo ./Core/Modules/Src/heater.d ./Core/Modules/Src/heater.o ./Core/Modules/Src/heater.su ./Core/Modules/Src/hih5030.cyclo ./Core/Modules/Src/hih5030.d ./Core/Modules/Src/hih5030.o ./Core/Modules/Src/hih5030.su ./Core/Modules/Src/lcd.cyclo ./Core/Modules/Src/lcd.d ./Core/Modules/Src/lcd.o ./Core/Modules/Src/lcd.su ./Core/Modules/Src/ldr.cyclo ./Core/Modules/Src/ldr.d ./Core/Modules/Src/ldr.o ./Core/Modules/Src/ldr.su ./Core/Modules/Src/lm35.cyclo ./Core/Modules/Src/lm35.d ./Core/Modules/Src/lm35.o ./Core/Modules/Src/lm35.su ./Core/Modules/Src/pump.cyclo ./Core/Modules/Src/pump.d ./Core/Modules/Src/pump.o ./Core/Modules/Src/pump.su ./Core/Modules/Src/rgb_led.cyclo ./Core/Modules/Src/rgb_led.d ./Core/Modules/Src/rgb_led.o ./Core/Modules/Src/rgb_led.su ./Core/Modules/Src/soil.cyclo ./Core/Modules/Src/soil.d ./Core/Modules/Src/soil.o ./Core/Modules/Src/soil.su

.PHONY: clean-Core-2f-Modules-2f-Src

