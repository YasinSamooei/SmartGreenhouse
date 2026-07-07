################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Tasks/Src/control_task.c \
../Core/Tasks/Src/display_task.c \
../Core/Tasks/Src/esp_task.c \
../Core/Tasks/Src/sensor_task.c \
../Core/Tasks/Src/system_init.c \
../Core/Tasks/Src/uart3_task.c \
../Core/Tasks/Src/uart_task.c 

OBJS += \
./Core/Tasks/Src/control_task.o \
./Core/Tasks/Src/display_task.o \
./Core/Tasks/Src/esp_task.o \
./Core/Tasks/Src/sensor_task.o \
./Core/Tasks/Src/system_init.o \
./Core/Tasks/Src/uart3_task.o \
./Core/Tasks/Src/uart_task.o 

C_DEPS += \
./Core/Tasks/Src/control_task.d \
./Core/Tasks/Src/display_task.d \
./Core/Tasks/Src/esp_task.d \
./Core/Tasks/Src/sensor_task.d \
./Core/Tasks/Src/system_init.d \
./Core/Tasks/Src/uart3_task.d \
./Core/Tasks/Src/uart_task.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Tasks/Src/%.o Core/Tasks/Src/%.su Core/Tasks/Src/%.cyclo: ../Core/Tasks/Src/%.c Core/Tasks/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I../Drivers/STM32F1xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -I../Core/Modules/Inc -I../Core/Tasks/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Core-2f-Tasks-2f-Src

clean-Core-2f-Tasks-2f-Src:
	-$(RM) ./Core/Tasks/Src/control_task.cyclo ./Core/Tasks/Src/control_task.d ./Core/Tasks/Src/control_task.o ./Core/Tasks/Src/control_task.su ./Core/Tasks/Src/display_task.cyclo ./Core/Tasks/Src/display_task.d ./Core/Tasks/Src/display_task.o ./Core/Tasks/Src/display_task.su ./Core/Tasks/Src/esp_task.cyclo ./Core/Tasks/Src/esp_task.d ./Core/Tasks/Src/esp_task.o ./Core/Tasks/Src/esp_task.su ./Core/Tasks/Src/sensor_task.cyclo ./Core/Tasks/Src/sensor_task.d ./Core/Tasks/Src/sensor_task.o ./Core/Tasks/Src/sensor_task.su ./Core/Tasks/Src/system_init.cyclo ./Core/Tasks/Src/system_init.d ./Core/Tasks/Src/system_init.o ./Core/Tasks/Src/system_init.su ./Core/Tasks/Src/uart3_task.cyclo ./Core/Tasks/Src/uart3_task.d ./Core/Tasks/Src/uart3_task.o ./Core/Tasks/Src/uart3_task.su ./Core/Tasks/Src/uart_task.cyclo ./Core/Tasks/Src/uart_task.d ./Core/Tasks/Src/uart_task.o ./Core/Tasks/Src/uart_task.su

.PHONY: clean-Core-2f-Tasks-2f-Src

