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
    stream = ""
    img = sensor.snapshot()
    curtime = time.time()

    blobs = img.find_blobs([target_lab_threshold], x_stride = 2, y_stride = 2, pixels_threshold = 100, merge = True, margin = 20)

    if blobs:
        stream += "-- found " + str(curtime)
        max_area = 0
        target = blobs[0]
        for b in blobs:
            if b.area() > max_area:
                max_area = b.area()
                target = b

        dx = 160 - target[5]
        if(dx > 30):
                stream += " left"
        elif(dx < -30):
                stream += " right"
        else:
                stream += " center"

        tmp = img.draw_rectangle(target[0:4])
        tmp = img.draw_cross(target[5], target[6])

    else:
        stream += "-- not found " + str(curtime)

    uart_out.write(stream + "\n")
    print("[log] " + stream)
