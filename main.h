#include <stdio.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include <driver/uart.h>
#include <esp_log.h>
#include <led_strip.h>
#include <sdkconfig.h>
#include <string.h>

/***************___INBUILT_LED___***************/

#define BLINK_GPIO GPIO_NUM_38
static const char *TAG_blink = "Blink";
static led_strip_t *pStrip_a;

static void inbuilt_led(uint8_t s_led_state, int r, int g, int b){
    if (s_led_state) {
        pStrip_a->set_pixel(pStrip_a, 0, r, g, b);
        pStrip_a->refresh(pStrip_a, 100);
    } else {
        pStrip_a->clear(pStrip_a, 50);
    }
}

static void led_init(void){
    ESP_LOGI(TAG_blink, "Blink Init");
    pStrip_a = led_strip_init(0, BLINK_GPIO, 1);
    pStrip_a->clear(pStrip_a, 50);
}

/***************___UART___***************/

#define RX_PIN GPIO_NUM_41
#define TX_PIN GPIO_NUM_42
#define UART UART_NUM_0
#define UART_BAUD_RATE 9600
static const int16_t RX_BUF_SIZE=1024;

static void uart_init(){
    uart_config_t uart_config={
        .baud_rate=UART_BAUD_RATE,
        .data_bits=UART_DATA_8_BITS,
        .flow_ctrl=UART_HW_FLOWCTRL_DISABLE,
        .parity=UART_PARITY_DISABLE,
        .source_clk=UART_SCLK_APB,
        .stop_bits = UART_STOP_BITS_1,
    };
    ESP_ERROR_CHECK(uart_driver_install(UART,RX_BUF_SIZE,RX_BUF_SIZE,0,NULL,0));
    ESP_ERROR_CHECK(uart_param_config(UART,&uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART,TX_PIN,RX_PIN,UART_PIN_NO_CHANGE,UART_PIN_NO_CHANGE));
    ESP_LOGI("UART_INIT","uart_init complete.");
}

static void tx_task(){
    while(1){
        uart_write_bytes(UART,"hello..\n",9);
        vTaskDelay(1000/portTICK_PERIOD_MS);
    }
}

static void rx_task(){
    uint8_t *data=(uint8_t*)malloc(RX_BUF_SIZE+1);
    while(1){
        const int rxBytes=uart_read_bytes(UART,data,RX_BUF_SIZE,500/portTICK_PERIOD_MS);
        if(rxBytes>0){
            data[rxBytes]='\0';
            ESP_LOGW("UART","Read %d bytes: '%s",rxBytes,data);
        }
    }
    free(data);
}
