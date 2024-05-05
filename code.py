import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

print("Loopstarted")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.OUT)#servo
GPIO.setup(8,GPIO.OUT)#Entry LED
GPIO.setup(10,GPIO.OUT)#Exit LED
GPIO.setup(31,GPIO.IN)#slot1
GPIO.setup(13,GPIO.IN)#slot2
GPIO.setup(15,GPIO.IN)#slot3
GPIO.setup(16,GPIO.IN)#slot4
GPIO.setup(7,GPIO.IN)#Entry Sensor
GPIO.setup(18,GPIO.IN)#Exit Sensor
global RFID_List#
RFID_List = {
    233735633756:"Vehicle 1",
    934464268298:"Vehicle 2",
    1002665581953:"Vehicle 3",
    796473072939:"Vehicle 4"
}
global Entry #
global Exit #
global Access #
global slot1
global slot2
global slot3
global slot4
global FreeSlot
global pwm
slot1 = slot2 = slot3 = slot4 = True
FreeSlot = True
Entry = False
def Entry_LED_onG():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(35,GPIO.OUT)
    GPIO.output(35,1)
    return
def Exit_LED_onG():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(36,GPIO.OUT)
    GPIO.output(36,1)
    return
def Entry_LED_offG():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(35,GPIO.OUT)
    GPIO.output(35,0)
    return
def Exit_LED_offG():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(36,GPIO.OUT)
    GPIO.output(36,0)
    return
def Entry_LED_onR():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(37,GPIO.OUT)
    GPIO.output(37,1)
    return
def Exit_LED_onR():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(38,GPIO.OUT)
    GPIO.output(38,1)
    return
def Entry_LED_offR():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(37,GPIO.OUT)
    GPIO.output(37,0)
    return
def Exit_LED_offR():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(38,GPIO.OUT)
    GPIO.output(38,0)
    return
def Check_Vechicle_arrive():
    global Entry
    global Exit
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN)
    GPIO.setup(18,GPIO.IN)
    while(1):
        b = GPIO.input(18)
        if(not b):
            time.sleep(0.001)
            b = GPIO.input(18)
            if(not b):
                print("Vehicle arrived at exit")
                Exit = True
        else:
            Exit = False
        a = GPIO.input(7)
        if(not a):
            time.sleep(0.001)
            a = GPIO.input(7)
            if(not a):
                print("Vehicle arrived at entry")
                Entry = True
        else:
            Entry = False
        return
        
def Read_RFID():
    reader = SimpleMFRC522()
    id1, text = reader.read()
    print("Tag Number:")
    print(id1)
    #print(text)
    return id1
def Check_Access(tempID):
    if(tempID in RFID_List):
        return True
    else:
        return False
def Check_FreeSlots():
    global slot1
    global slot2
    global slot3
    global slot4
    global FreeSlot
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31,GPIO.IN)
    GPIO.setup(13,GPIO.IN)
    GPIO.setup(15,GPIO.IN)
    GPIO.setup(16,GPIO.IN)
    slot_num=4
    for x in range(slot_num):
        slot1 = GPIO.input(31)
        slot2 = GPIO.input(13)
        slot3 = GPIO.input(15)
        slot4 = GPIO.input(16)
    if((not slot1) & (not slot2) & (not slot3) & (not slot4)):
        print("Sorry No Parking Slots are Free")
        FreeSlot = False
        #return for temprvary
    else:
        FreeSlot = True
        
        if(slot1):
            print("Slot 1 is Free")
        if(slot2):
            print("Slot 2 is Free")
        if(slot3):
            print("Slot 3 is Free")
        if(slot4):
            print("Slot 4 is Free")
        return
def Open_Gate():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32,GPIO.OUT)#servo
    pwm = GPIO.PWM(32, 50)
    pwm.start(0)
    time.sleep(0.1)
    duty = 2
    while duty <= 6:
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)
        duty = duty + 1
        #for 90 degree, duty = angle / 18 + 2
    return
def Close_Gate():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32,GPIO.OUT)#servo
    pwm = GPIO.PWM(32, 50)
    pwm.start(0)
    time.sleep(0.1)
    duty = 6
    while duty >= 0:
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)
        duty = duty - 1
    pwm.ChangeDutyCycle(0)# for 0 degree, duty = angle / 18 + 2
    return
def Scan_Slot():
    global slot1
    global slot2
    global slot3
    global slot4
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31,GPIO.IN)
    GPIO.setup(13,GPIO.IN)
    GPIO.setup(15,GPIO.IN)
    GPIO.setup(16,GPIO.IN)
    slot1 = GPIO.input(31)
    slot2 = GPIO.input(13)
    slot3 = GPIO.input(15)
    slot4 = GPIO.input(16)
    return
def Readentry():
    global Entry
    global Exit
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN)
    c = GPIO.input(7)
    while(not c):
        c = GPIO.input(7)
    Entry = False
    time.sleep(0.25)
    GPIO.setup(18,GPIO.IN)
    d = GPIO.input(18)
    while(d):
        d = GPIO.input(18)
    while(not d):
        d = GPIO.input(18)
    Exit = False
    time.sleep(0.5)
    print("vehicle Passed")
    return
def Readexit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18,GPIO.IN)
    e = GPIO.input(18)
    while(not e):
        e = GPIO.input(18)
    Entry = False
    time.sleep(0.25)
    GPIO.setup(7,GPIO.IN)
    f = GPIO.input(7)
    while(f):
        f = GPIO.input(7)
    while(not f):
        f = GPIO.input(7)
    Exit = False
    time.sleep(0.5)
    print("vehicle Passed")
    return
def start_time(tempID):
    global start1time
    global start2time
    global start3time
    global start4time
    if(tempID == 233735633756):
        start1time = time.time()
    if(tempID == 934464268298):
        start2time = time.time()
    if(tempID == 1002665581953):
        start3time = time.time()
    if(tempID == 796473072939):
        start4time = time.time()
    return
def stop_time(tempID):
    global stop1time
    global stop2time
    global stop3time
    global stop4time
    if(tempID == 233735633756):
        stop1time = time.time()
    if(tempID == 934464268298):
        stop2time = time.time()
    if(tempID == 1002665581953):
        stop3time = time.time()
    if(tempID == 796473072939):
        stop4time = time.time()
    return
def time_lapse(tempID):
    global start1time
    global start2time
    global start3time
    global start4time
    global stop1time
    global stop2time
    global stop3time
    global stop4time
    if(tempID == 233735633756):
        return stop1time-start1time
    if(tempID == 934464268298):
        return stop2time-start2time
    if(tempID == 1002665581953):
        return stop3time-start3time
    if(tempID == 796473072939):
        return stop4time-start4time
    return
def main():
    global Entry
    global Exit
    global Access
    global tempID
    global FreeSlot
    GPIO.cleanup()
    Entry_LED_onG()
    Entry_LED_offR()
    Exit_LED_onG()
    Exit_LED_offR()
    Check_Vechicle_arrive()
    if(Entry):
        Entry_LED_onG()
        Entry_LED_offR()
        Exit_LED_offG()
        Exit_LED_onR()
        print("Please place your tag")
        time.sleep(1)
        tempID = Read_RFID()
        Access = Check_Access(tempID)
        if(Access):
            Check_FreeSlots()
            Send_slot()
            if(not FreeSlot):
                return
            start_time(tempID)
            Open_Gate()
            Readentry()
            Close_Gate()
            print("gate Closed")
        else:
            print('''Access Denied
Please Check Your Tag
If Not Registered, Please Take Your Vehicle out
or, Please Register in our website''')
  #      while (Entry):
    if(Exit):
        Exit_LED_onG()
        Exit_LED_offR()
        Entry_LED_offG()
        Entry_LED_onR()
        print("Please place your tag")
        time.sleep(1)
        tempID = Read_RFID()
        stop_time(tempID)
        lapsetime = time_lapse(tempID)
        print(''' Your Total Parking Time is : ''')
        print(lapsetime)
        Open_Gate()
        Readexit()
        Close_Gate()
        print("gate Closed")
    time.sleep(1)
    print('''
    
    
    
    
    
    
    
    
    
    
    
    ''')
    Entry = False
    Exit = False
    return
Open_Gate()
Close_Gate()
Send_slot()
while(1):
    #### setting up MQTT #########
    mqttc = mqtt.Client()
    mqttc.connect("test.mosquitto.org", 1883,6000)
    mqttc.loop_start()
    #mqttc.loop_forever()
    GPIO.cleanup()
    Entry_LED_onG()
    Entry_LED_offR()
    Exit_LED_onG()
    Exit_LED_offR()
    Check_Vechicle_arrive()
    if(Entry or Exit):
        main()
    if((not slot1) & (not slot2) & (not slot3) & (not slot4)):
        (result,mid) = mqttc.publish("paho/parkin","All Slots Full",2)
        FreeSlot = False
            #return for temprvary
    else:
        FreeSlot = True
        if((not slot1) and (slot2) and (slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-2\nS-3\nS-4",2)
        if((slot1) and (not slot2) and (slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-3\nS-4",2)
        if((slot1) and (slot2) and (not slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-2\nS-4",2)
        if((slot1) and (slot2) and (slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-2\nS-3",2)
        if((slot1) and (slot2) and (not slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-2",2)
        if((slot1) and (not slot2) and (slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-3",2)
        if((slot1) and (not slot2) and (not slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1\nS-4",2)
        if((slot1) and (not slot2) and (not slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-1",2)
        if((not slot1) and (slot2) and (slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-2\nS-3",2)
        if((not slot1) and (slot2) and (not slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-2\nS-4",2)
        if((not slot1) and (slot2) and (not slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-2",2)
        if((not slot1) and (not slot2) and (slot3) and (not slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-3",2)
        if((not slot1) and (not slot2) and (not slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-4",2)
        if((not slot1) and (not slot2) and (slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","S-3\nS-4",2)
        if((slot1) and (slot2) and (slot3) and (slot4)):
            (result,mid) = mqttc.publish("paho/parkin","All are free",2)
    Check_FreeSlots()
    print('''
    
    
    ''')
mqttc.loop_forever()
        
mqttc.loop_stop()
mqttc.disconnect()
