#include "hal_data.h"
#include <stdio.h>
#define ACCEL_XOUT_H 0x75       //가속도 값을 가져올 레지스터 주소 값
#define PWR_MGMT_1 0x6B         //MPU6050 Clock 설정을 위한 레지스터 주소

volatile uint8_t a;   //가속도 x,y,z 값을 담을 16bit 변수

FSP_CPP_HEADER
void R_BSP_WarmStart(bsp_warm_start_event_t event);
FSP_CPP_FOOTER

/*******************************************************************************************************************//**
 * main() is generated by the RA Configuration editor and is used to generate threads if an RTOS is used.  This function
 * is called by main() when no RTOS is used.
 **********************************************************************************************************************/
void delay(int ms){
    R_BSP_SoftwareDelay(ms, BSP_DELAY_UNITS_MILLISECONDS);
}

//Simple I2C callback 함수
volatile i2c_master_event_t g_i2c_callback_event;
void sci_i2c_master_callback(i2c_master_callback_args_t *p_args)
{
    g_i2c_callback_event = p_args->event;
}

//I2C callback 함수
volatile i2c_master_event_t g_iic_callback_event;
void iic_callback(i2c_master_callback_args_t *p_args)
{
    g_iic_callback_event = p_args->event;
}

void writeI2C(uint8_t addr, uint8_t val){
    uint8_t buf[2] = {addr, val};                               //레지스터 주소 addr, 보낼 값 val

    R_IIC_MASTER_Write(&g_i2c_master0_ctrl, buf, 2, true);      //2byte의 buf 값 쓰기
    while( g_iic_callback_event != I2C_MASTER_EVENT_TX_COMPLETE );
}

void readI2C(uint8_t addr, uint8_t buf[], uint8_t size){
    R_IIC_MASTER_Write(&g_i2c_master0_ctrl, &addr, 1, true);       //1byte 레지스터 주소에 쓰기
    while( g_iic_callback_event != I2C_MASTER_EVENT_TX_COMPLETE );
    delay(10);                                                     //MPU6050의 타이밍 이슈 해결을 위한 delay

    memset(buf, 0, sizeof(buf));                                   //ACCEL 값 얻기 위해 6byte 읽을 예정
    R_IIC_MASTER_Read(&g_i2c_master0_ctrl, buf, 6, false);         //buf 에 6byte data를 읽어 저장. 통신 끝
    while( g_iic_callback_event != I2C_MASTER_EVENT_RX_COMPLETE );
}

void hal_entry(void)
{
    uint8_t buf[100] = {0};
    uint8_t str[100] = {0};

    writeI2C(PWR_MGMT_1, 0x0);  //내부 oscillator 사용하자

    while(1){
        readI2C(ACCEL_XOUT_H, buf, 6); //0x3B 로부터 6 byte 를 읽어와 buf 에 담아라!

        a = buf[0] & ((1 << 8) - 1);

        sprintf(str, "WHO AM I %x\r\n", a);
        printf("%s", str);
        delay(50);
    }


}
/*******************************************************************************************************************//**
 * This function is called at various points during the startup process.  This implementation uses the event that is
 * called right before main() to set up the pins.
 *
 * @param[in]  event    Where at in the start up process the code is currently at
 **********************************************************************************************************************/
void R_BSP_WarmStart(bsp_warm_start_event_t event)
{
    if (BSP_WARM_START_RESET == event)
    {

    }

    if (BSP_WARM_START_POST_C == event)
    {
        /* C runtime environment and system clocks are setup. */

        /* Configure pins. */
        R_IOPORT_Open (&g_ioport_ctrl, g_ioport.p_cfg);
        R_SCI_UART_Open(&g_uart0_ctrl, &g_uart0_cfg);
        R_SCI_I2C_Open(&g_i2c9_ctrl, &g_i2c9_cfg);
        R_IIC_MASTER_Open(&g_i2c_master0_ctrl, &g_i2c_master0_cfg);

    }
}
