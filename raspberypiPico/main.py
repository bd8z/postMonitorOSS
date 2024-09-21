import time

import machine
from machine import ADC

while(1):
    startTime = time.ticks_ms()
    Out_wakeup = machine.Pin(0, machine.Pin.OUT)
    Out_wakeup.value(0)
    checkIsPowerOnReset = (machine.reset_cause() == machine.PWRON_RESET)
    filePath = "sleepTimeFile"
    with open(filePath) as f:
        s = f.read()
        if(checkIsPowerOnReset):
            print("sleepTimeFile",s)
        deepSleepHourCount_r = int((s.split(","))[0])
        deepSleepHour_r = int((s.split(","))[1])
    
    # wakeup mode
    if ((checkIsPowerOnReset) or (deepSleepHourCount_r>=deepSleepHour_r)):
        Out_wakeup.value(1)
        Adc_isTaskEnd =ADC(0)
        Adc_isNightMode = ADC(1)
        if(checkIsPowerOnReset):
            print("[log]pico wakeup!")
        for i in range(10):
            time.sleep(1)
            if(checkIsPowerOnReset):
                Adc_isTaskEndValue = Adc_isTaskEnd.read_u16()*3.3/65535
                Adc_isNightModeValue = Adc_isNightMode.read_u16()*3.3/65535
                print("Adc_isTaskEndValue",Adc_isTaskEndValue)
                print("Adc_isNightModeValue",Adc_isNightModeValue)
            
        for i in range(360):
            time.sleep(0.5)
            Adc_isTaskEndValue = Adc_isTaskEnd.read_u16()*3.3/65535
            if(checkIsPowerOnReset):
                print("Adc_isTaskEndValue",Adc_isTaskEndValue)
            if (Adc_isTaskEndValue > 2.6):
                break

        print("[log]shot finished!")
        Adc_isNightModeValue = Adc_isNightMode.read_u16()*3.3/65535

        if (Adc_isNightModeValue > 2.6):
            deepSleepHour = 12
        else:
            deepSleepHour = 3
        Out_wakeup.value(0)
        if(checkIsPowerOnReset):
            print("Adc_isNightModeValue",Adc_isNightModeValue)
            print("deepSleepTime",deepSleepHour)
            
        deepSleepHour_w = deepSleepHour
        deepSleepHourCount_w = 1

    # deepsleep mode
    else:
        deepSleepHourCount_w = deepSleepHourCount_r + 1
        deepSleepHour_w = deepSleepHour_r        

    wirteObj = str(deepSleepHourCount_w) + "," + str(deepSleepHour_w) 
    if(checkIsPowerOnReset):
        print("wirteObj",wirteObj)
    with open(filePath, mode='w') as f:
        f.write(wirteObj)
    if(checkIsPowerOnReset):
        time.sleep(5)
    deltaTime = time.ticks_diff(time.ticks_ms(), startTime)
    machine.deepsleep(60*60*1000-deltaTime)

