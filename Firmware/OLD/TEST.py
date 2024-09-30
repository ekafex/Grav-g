######################################
# from machine import Pin, I2C
# from i2c_lcd import I2cLcd
# from time import sleep
# 
# I2C_ADDR = 0x27
# totalRows = 2
# totalColumns = 16
# i2c = I2C(1)
# print(i2c.scan())
# 
# lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
# # lcd.putstr("Tixhe o Tixhe")
# while True:
#     lcd.putstr("I2C LCD Tutorial")
#     sleep(2)
#     lcd.clear()
#     lcd.putstr("Lets Count 0-10!")
#     sleep(2)
#     lcd.clear()
#     for i in range(11):
#         lcd.putstr(str(i))
#         sleep(1)
#         lcd.clear()

######################################

# from machine import Pin
# from time import sleep
# Start = Pin(23, Pin.IN)
# Reset = Pin(4, Pin.IN)
# while True: 
#   print('Start=',Start.value(),'Reset=',Reset.value())
#   sleep(0.3)
  
######################################

# from machine import Pin,PWM
# import time
# sg90 = PWM(Pin(33, mode=Pin.OUT))
# sg90.freq(50)
# # sg90.duty(60)
# # sg90.duty(35)
# while True:
#     sg90.duty(26)
#     time.sleep(1)
#     sg90.duty(123)
#     time.sleep(1)
######################################
# from machine import Pin
# import time
# 
# sound_sensor = Pin(16, Pin.IN)
# 
# while True:
#     print(sound_sensor.value())
#     time.sleep(0.2)

######################################
import time
# from machine import Pin
from hcsr04 import HCSR04

sensor = HCSR04(trigger_pin=18, echo_pin=5)


while True:
    print(sensor.distance_cm())
    time.sleep(1)














