import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

master = modbus_rtu.RtuMaster(serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0))
master.set_timeout(5.0)
master.set_verbose(True)


def Fan_speed_OnOff():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(1, 1))
    time.sleep(1)

def Fan_speed_low():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(2, 1))
    time.sleep(1)

def Fan_speed_high():
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(3, 1))
    time.sleep(1)


def Fan_init_speed():
    for i in range (1,5):
        #master.execute(1, cst.WRITE_SINGLE_REGISTER, 1103, output_value=2) # command02
        #master.execute(1, cst.WRITE_SINGLE_REGISTER, 1104, output_value=1) # channel
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(2, 1))
        time.sleep(1)
        
def Fan_speed(speed):
    Fan_init_speed()
    for i in range (1,speed):
        #master.execute(1, cst.WRITE_SINGLE_REGISTER, 1103, output_value=3) # command01
        #master.execute(1, cst.WRITE_SINGLE_REGISTER, 1104, output_value=1) # channel
        master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(3, 1))
        time.sleep(1)


def AC_On():
    
    master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 1103,output_value=(5, 2)) # command01
    time.sleep(3)

def AC_Off():
    
    master.execute(1, cst.WRITE_SINGLE_REGISTER, 1103, output_value=5) # command01
    master.execute(1, cst.WRITE_SINGLE_REGISTER, 1104, output_value=1) # channel
    time.sleep(3)


def get_temp():
    
    temp = master.execute(2, cst.READ_HOLDING_REGISTERS, 1090, 4) 
    time.sleep(0.5)
    return temp[0],temp[3]

if __name__ == '__main__':
    
    #Fan_speed_high()
    #print (get_temp())
    #Fan_speed_1(1)
    #AC_On()
    
    
    TH_flog = 0
    while True:
        TH = get_temp()
        TH_log = TH
        print (TH)
        if TH[0] >= 2700:
            if TH_flog != 1:
                Fan_speed(3)
                TH_flog = 1
        else:
            if TH_flog != 2:
                Fan_speed(1)
                TH_flog = 2
        time.sleep(10)
    
