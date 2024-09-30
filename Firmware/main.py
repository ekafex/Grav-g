from machine import Pin, I2C, PWM
from MuPy_LCD_I2C import LCD_I2C
from hcsr04 import HCSR04
from time import sleep, ticks_us
##########################################
def Calibrated_HC_SR04(d_in):
    # Measures distances >10cm with better than 1.5% 
    return -0.59 + 1.07*d_in - 3.1e-4*d_in*d_in
##########################################
# LCD:
i2c = I2C(1, freq=400000)
lcd = LCD_I2C(i2c, 0x27, 2, 16)
lcd.print("Mirese")
lcd.set_cursor(0,1)
lcd.print("          Vini!")
sleep(1)
lcd.clear()
lcd.print("    Grav-g!")
lcd.set_cursor(0,1)
lcd.print("Dep. Fizike FSHN")
sleep(2)
lcd.print("20%")
lcd.set_cursor(0,1)
lcd.print("LCD: OK!")
sleep(0.2)
lcd.clear()
#lcd.blink_cursor_on()
##########################################
# Butonat:
Start = Pin(23, Pin.IN, Pin.PULL_DOWN) # Start Switch
Reset = Pin(4, Pin.IN, Pin.PULL_DOWN)  # Reset Switch
##########################################
# Servo SG90:
sg90 = PWM(Pin(14, mode=Pin.OUT), freq=50, duty=40)
lcd.print("40%")
lcd.set_cursor(0,1)
lcd.print("SG90: OK!")
sleep(0.2)
lcd.clear()
##########################################
# Mic. KY-037:
mic = Pin(16, Pin.IN)
lcd.print("60%")
lcd.set_cursor(0,1)
lcd.print("KY-037: OK!")
sleep(0.2)
lcd.clear()
##########################################
# Eko HC-SR04:
echo = HCSR04(trigger_pin=18, echo_pin=5)
lcd.print("80%")
lcd.set_cursor(0,1)
lcd.print("HC-SR04: OK!")
sleep(0.2)
lcd.clear()
##########################################
lcd.print("100% - Gati!")
sleep(1.5)
lcd.clear()
##########################################
def Measure():
    ## Faktore Kalibrimi te distances dhe kohes
#     dt0 = 45.486 # ms
#     H0  = 4.194  # cm
    # Time Calibration factor
    dt0 = 53.7
    while True:
        sleep(0.1)
        if Start.value() == 0:
            lcd.clear()
            lcd.print("H =%03.2f cm"%Calibrated_HC_SR04(echo.distance_cm()))
            #lcd.set_cursor(0,1)
            #lcd.print("dt=?")
        else:
            d = Calibrated_HC_SR04(echo.distance_cm())
            sg90.duty(60)
            break
    t0 = ticks_us()
    while mic.value() == 0:
        sleep(0.00001)
    t1 = ticks_us()
    #return d+H0, (t1-t0)/1000 - dt0
    return d, (t1-t0)/1000 - dt0
##########################################

while True:
    d, dt = Measure()
    lcd.clear()
    lcd.print("H =%03.2f cm"%d)
    lcd.set_cursor(0,1)
    lcd.print("dt=%04.2f ms"%dt)
    #print('%3.2f, %4.2f'%(d, dt))
#     print('%3.2f cm; %4.2f ms; g=%2.3f m/s^2'%(d, dt, (2e4*d/dt**2)))
#     print('[%3.2f,%4.2f]'%(d, dt))
    #-----------------------
    while Reset.value()==0:
        sleep(0.2)
    sg90.duty(40)
    sleep(0.5)
    lcd.clear()
    if Reset.value()==1:
        break

lcd.print("Mirupafshim!")
sleep(2)
lcd.hal_backlight_off()


