# Debounce a button the right way:
# Interupt based
# Time controlled

from machine import Pin
import time
from utime import sleep_us

# Button
btn = Pin(6, Pin.IN, Pin.PULL_UP)
state = 0
btn_debounce_t = 0
btn_isr_flag = 0

# interupt routine
# executed when button press is detected
def btn_handler(btn):
    global btn_debounce_t, btn_isr_flag
    # During the time (200) no further button press will be regognized.
    # This is the debounce time.
    if (time.ticks_ms()-btn_debounce_t)>200:
        btn_isr_flag = 1
        print("Button press detected!")
    btn_debounce_t=time.ticks_ms()
    
btn.irq(trigger=btn.IRQ_FALLING, handler=btn_handler)

while (True):
    # This if else statement decides what happens when a button press is valid,
    # this means the button must be pressed for at least 800ms.
    # Thus, glitches or unwanted short pulses can not trigger a function.
    if btn_isr_flag is 1 and (time.ticks_ms() - btn_debounce_t) > 800:
        if state == 0:
            print("Start executing your function.")
            state = 1    
        elif state == 1:
            print("Stop executing your function.")
            state = 0
        btn_isr_flag = 0
    # just check the button is still pressed but do nothing.
    elif btn_isr_flag is 1 and btn.value() == 0:
        pass
    # button was released before the time was over or function was executed.    
    elif btn_isr_flag is 1 and btn.value() == 1:
        btn_isr_flag = 0
        print("Button released!")


