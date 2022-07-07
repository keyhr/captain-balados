import sensor
import image
import lcd
import time
import utime
from machine import UART
from Maix import GPIO
from fpioa_manager import *
from modules import ws2812

#led
class_ws2812 = ws2812(8,100)
BRIGHTNESS = 0x10

fm.register(34,fm.fpioa.UART1_RX, force = True)
fm.register(35,fm.fpioa.UART1_TX, force = True)
uart_out = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames()

while False:
    uart_out.write('TEST\n')
    utime.sleep_ms(100)

def BLINK_RGB_LED(r,g,b):
    a = class_ws2812.set_led(0,(r,g,b))
    a = class_ws2812.display()
    time.sleep(0.3)
    a = class_ws2812.set_led(0,(0,0,0))
    a = class_ws2812.display()
    time.sleep(0.3)
    a = class_ws2812.set_led(0,(r,g,b))
    a = class_ws2812.display()

def RGB_LED_ON(r,g,b):
    a = class_ws2812.set_led(0,(r,g,b))
    a = class_ws2812.display()

def RGB_LED_OFF():
    a = class_ws2812.set_led(0,(0,0,0))
    a = class_ws2812.display()

BLINK_RGB_LED(0,BRIGHTNESS,0)
BLINK_RGB_LED(0,0,BRIGHTNESS)
BLINK_RGB_LED(0,BRIGHTNESS,0)

target_lab_threshold = (40,   70,  45,   75,   -15,   50)

while True:
    #if uart_out.read(4096):
        #uart_out.write("Hello World \n")
    #else:
        #pass
    print("Hello World")
    img=sensor.snapshot()
    blobs = img.find_blobs([target_lab_threshold], x_stride = 2, y_stride = 2, pixels_threshold = 100, merge = True, margin = 20)
    if blobs:
        max_area = 0
        target = blobs[0]
        for b in blobs:
            if b.area() > max_area:
                max_area = b.area()
                target = b
        BLINK_RGB_LED(0,0,BRIGHTNESS)
        #if uart_out.read(4096):
            #area = target.area()
            #dx = 120 - target[6]
            #hexlist = [(dx >> 8) & 0xFF, dx & 0xFF, (area >> 16) & 0xFF, (area >> 8) & 0xFF, area & 0xFF]
            #uart_out.write(bytes(hexlist))
            #print(target[5])
            #print("green detected")

            #uart_out.write("green detected \n")
        dx = 160 - target[6]
        if(dx > 30):
                uart_out.write("left\n")
                print("left")
        elif(dx<-30):
                uart_out.write("right\n")
                print("right")
        else:
                uart_out.write("straight\n")
                print("center")

        #else:
        #   pass

        #print(target.area())
        tmp=img.draw_rectangle(target[0:4])
        tmp=img.draw_cross(target[5], target[6])
        c=img.get_pixel(target[5], target[6])



    else:
        #if uart_out.read(4096):
            #hexlist = [0x80, 0x00, 0x00, 0x00, 0x00]
            #uart_out.write(bytes(hexlist))
        uart_out.write("not detected\n")
        print("not detected")
        #else:
        #    pass
    #print(hexlist)

print("end of program")
