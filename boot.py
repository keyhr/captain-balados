import sensor
import image
import lcd
import time
import utime
from machine import UART
from Maix import GPIO
from fpioa_manager import *

fm.register(34, fm.fpioa.UART1_TX, force=True)
fm.register(35, fm.fpioa.UART1_RX, force=True)
uart_out = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

#while False:
    #uart_out.write('TEST\n')
    #utime.sleep_ms(100)

target_lab_threshold = (40,   70,  45,   75,  -15,   50)
while True:
    img = sensor.snapshot()
    curtime = time.time()

    #uart_out.write("[log] point1\n")
    blobs = img.find_blobs([target_lab_threshold], x_stride = 2, y_stride = 2, pixels_threshold = 100, merge = True, margin = 20)
    #uart_out.write("[log] point2\n")

    if blobs:
        uart_out.write("-- found " + str(curtime) + "\n")
        print("[log] found ", curtime)
        #max_area = 0
        #target = blobs[0]
        #for b in blobs:
            #if b.area() > max_area:
                #max_area = b.area()
                #target = b

        #area = target.area()
        #dx = 120 - target[6]
        #hexlist = [(dx >> 8) & 0xFF, dx & 0xFF, (area >> 16) & 0xFF, (area >> 8) & 0xFF, area & 0xFF]
        #uart_out.write(bytes(hexlist))

        #print(target.area())
        #tmp=img.draw_rectangle(target[0:4])
        #tmp=img.draw_cross(target[5], target[6])
        #c=img.get_pixel(target[5], target[6])

    else:
        uart_out.write("-- not found " + str(curtime) + "\n")
        print("[log] not found ", curtime)
        #try:
            #hexlist = [0x80, 0x00, 0x00, 0x00, 0x00]
            #uart_out.write(bytes(hexlist))
            #uart_out.write("\n")
        #Exception:
            #uart_out.write("Error\n")

