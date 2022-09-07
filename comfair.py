import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import paho.mqtt.client as mqtt
import json  
import threading
import schedule

'''
@author: NTUT
'''
# coding:utf-8
import codecs

master = modbus_rtu.RtuMaster(serial.Serial(port='/dev/ttyS1', baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(5.0)
master.set_verbose(True)

evm_velocity = 3
temp_set = 26
comf_set = 1
evm_temp = 25
evm_humi = 60
evm_comfort = 1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+',1)
    time.sleep(3)

def on_message(client, userdata, msg):
    global comf_set
    global temp_set
    global evm_comfort
    data_topic = msg.topic
    data_payload = json.loads(msg.payload.decode())
    print(data_payload)
    comf_set = data_payload['params']
    #j = json.loads(data)
    
    
    
    
    
    listtopic = data_topic.split("/") 



def Fan_init_speed():
    for i in range (1,5):
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(2, 1))
        time.sleep(1)
        
def Fan_speed(speed):
    Fan_init_speed()
    for i in range (1,speed):
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(3, 1))
        time.sleep(1)
        
        
def AC_On():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(4, 1))
    time.sleep(1)
def AC_Off():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(5, 1))
    time.sleep(1)
def AC_20():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(6, 1))
    time.sleep(1)
def AC_21():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(7, 1))
    time.sleep(1)
def AC_22():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(8, 1))
    time.sleep(1)
def AC_23():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(9, 1))
    time.sleep(1)
def AC_24():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(10, 1))
    time.sleep(1)
def AC_25():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(11, 1))
    time.sleep(1)
def AC_26():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(12, 1))
    time.sleep(1)
def AC_27():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(13, 1))
    time.sleep(1)
    
def get_temp():
    global evm_temp,evm_humi
    temp = master.execute(2, cst.READ_HOLDING_REGISTERS, 1090, 4) 
    time.sleep(0.5)
    RTtemp = round(temp[0]*0.01-1,2)
    RThumi = round(temp[3]*0.01,2)
    evm_temp = RTtemp
    evm_humi = RThumi
    return RTtemp,RThumi

def comfort_cal(temp,humi,volcity):
    Comfort_numb = (1.818*temp+18.18)*(0.88+0.002*humi)+(temp-32)/(45-temp)-3.2*volcity+18.2
    return Comfort_numb

def comfort_defin(temp,humi,velocity):
    com_i = 0
    numb_comfort = comfort_cal(temp,humi,velocity)
    #print(numb_comfort)
    if numb_comfort > 85 :
        com_note = "感覺炎熱 +4"
        com_i = 4
    elif 80 < numb_comfort <= 85 :
        com_note = "感覺很熱 +3"
        com_i = 3
    elif 76 < numb_comfort <= 80 :
        com_note = "感覺偏熱 +2"
        com_i = 2
    elif 71 < numb_comfort <= 76 :
        com_note = "感覺偏暖 +1"
        com_i = 1
    elif 59 < numb_comfort <= 71 :
        com_note = "舒適 0"
        com_i = 0        
    elif 51 < numb_comfort <= 59 :
        com_note = "感覺略偏冷 -1"
        com_i = -1     
    elif 39 < numb_comfort <= 51 :
        com_note = "感覺較冷 -2"
        com_i = -2     
    elif 26 < numb_comfort <= 39 :
        com_note = "感覺很冷 -3"
        com_i = -3 
    elif numb_comfort <= 26 :
        com_note = "感覺寒冷 -4"
        com_i = -4 
    return numb_comfort,com_i,com_note
    
def set_speed(temp,humi):
    global evm_velocity
    global comf_set
    global evm_comfort
    sequences = [0, 1, 2, 3, 4, 5]
    for i in sequences:
        test = comfort_defin(temp,humi,i)
        if test[1] < comf_set:
            velocity = i
            break
        else:
            velocity = 5
    if velocity != evm_velocity :
        Fan_speed(velocity)
    evm_velocity = velocity
    evm_comfort = test[1]
    
    
        
    
    return (velocity)

def job():
    global comf_set
    global temp_set
    global evm_comfort

    RTcond = get_temp()
    num_comfort = comfort_defin(RTcond[0],RTcond[1],3)
    print (num_comfort)
    print (RTcond)
    print (set_speed(RTcond[0],RTcond[1]))
    payload = {'Temperature' : evm_temp, 'Humidity':evm_humi, 'comfortair':evm_comfort}
    client01.publish("v1/devices/me/telemetry", json.dumps(payload))

    time.sleep(1)
    
    if evm_velocity > 3:
        if temp_set >= 20 :
            temp_set = temp_set - 1
            if temp_set == 20:
                AC_20()
            elif temp_set == 21:
                AC_21()
            elif temp_set == 22:
                AC_22()
            elif temp_set == 23:
                AC_23()
            elif temp_set == 24:
                AC_24()
            elif temp_set == 25:
                AC_25()
            elif temp_set == 26:
                AC_26()
            elif temp_set == 27:
                AC_27()
            
    if evm_velocity < 2:
        if temp_set <= 27 :
            temp_set = temp_set + 1
            if temp_set == 20:
                AC_20()
            elif temp_set == 21:
                AC_21()
            elif temp_set == 22:
                AC_22()
            elif temp_set == 23:
                AC_23()
            elif temp_set == 24:
                AC_24()
            elif temp_set == 25:
                AC_25()
            elif temp_set == 26:
                AC_26()
            elif temp_set == 27:
                AC_27()
    print (temp_set)

def job_pre():
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()  
        time.sleep(1)

if __name__ == '__main__':
    
    

    t = threading.Thread(target = job_pre)
    t.start()
    
    Fan_speed(3)
    meter_token = 'IZcJiw4YcQFvDyBno9pd'
    meter_pass = ''
    url = 'thingsboard.cloud'

    client01 = mqtt.Client()
    client01.on_connect = on_connect
    client01.on_message = on_message
    client01.username_pw_set(meter_token, meter_pass)
    client01.connect(url, 1883, 60)
    client01.loop_forever()

    client02 = mqtt.Client()
    client02.username_pw_set("IZcJiw4YcQFvDyBno9pd","xxxx")
    client02.connect("thingsboard.cloud", 1883, 60)
    
        
        