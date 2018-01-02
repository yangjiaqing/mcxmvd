import serial
import serial.tools.list_ports
import time
import myuapi as myu

print ('hello')
movelist = ['G0 X100 Y100 Z100 F100\n','G0 X65 Y132 Z80 F100\n','G0 X00 Y132 Z80 F100\n','G0 X-55 Y146 Z80 F100\n','G0 X73 Y200 Z80 F100\n','G0 X10 Y200 Z80 F100\n','G0 X-50 Y214 Z80 F100\n','G0 X80 Y268 Z80 F100\n','G0 X10 Y268 Z80 F100\n','G0 X-45 Y282 Z80 F100\n']
ports = list(serial.tools.list_ports.comports())

print (ports)

for p in ports:
    global ser
    print (p[1])
    if ("SERIAL" in p[1])or("Serial" in p[1]):
	    ser = serial.Serial(port=p[0],baudrate=115200)
    else :
        # ser = serial.Serial(port="24",baudrate=115200)
	    print ("No Serial or SERIAL Device was found connected to the computer")

def moveurm(action=0):
    id=1
    #movelist = ['G0 X100 Y100 Z100 F100\n','G0 X65 Y132 Z80 F100\n','G0 X00 Y132 Z80 F100\n','G0 X-55 Y146 Z80 F100\n','G0 X73 Y200 Z80 F100\n','G0 X10 Y200 Z80 F100\n','G0 X-50 Y214 Z80 F100\n','G0 X80 Y268 Z80 F100\n','G0 X10 Y268 Z80 F100\n','G0 X-45 Y282 Z80 F100\n']
    cmdtail = movelist[action]
    cmd='#'+str(id)+' '+cmdtail
    ser.write(cmd.encode())
    print(movelist[action])
    time.sleep(1.5)
def initzero(waitime=1):
    id =1
    cmdtail = 'G0 X100 Y100 Z100 F100\n'
    cmd='#'+str(id)+' '+cmdtail
    ser.write(cmd.encode())
    time.sleep(waitime)
def testuarm():
    for i in range(0,10) :
        moveurm(i)
        initzero(1.5)
def test():
    uarmcatch(5)
    uarmrelease()
def uarmcatch(waitime=1):
    cmd='#1 M231 V1\n'
    ser.write(cmd.encode())
    print(ser.readline())
    time.sleep(waitime)
def uarmrelease(waitime=1):
    cmd='#1 M231 V0\n'
    ser.write(cmd.encode())
    print(ser.readline())
    time.sleep(waitime)
def catchinit(waitime=1.5):
    routelist = ['G0 X100 Y80 Z200 F100\n','G0 X100 Y80 Z200 F100\n','G0 X100 Y80 Z80 F100\n']
    id=1
    for i in range(0,3):
        cmdtail = routelist[i]
        cmd='#'+str(id)+' '+cmdtail
        ser.write(cmd.encode())
        time.sleep(waitime)
        print(cmd)
        print(ser.readline())

def anywhere(cmdtail):
    waitime = 1
    id=1
    cmd='#'+str(id)+' '+cmdtail
    ser.write(cmd.encode())
    print(ser.readline())
    time.sleep(waitime)
def playchess():

    for i in range(1,10):
        catchinit(1.5)
        uarmcatch()
        anywhere('G0 X100 Y80 Z200 F100\n')
        moveurm(i)
        uarmrelease()
    initzero()

def run():
    myu.uarminit()
    myu.putchess(0)
    action = "aaa"
    id=1
    while action != "q":
        id=id+1
        print ('select which tone do you want to play ? 1,2,3, q and others for quit')
        action = input("> ")
        if action == "0":
            cmdtail='G0 X100 Y100 Z100 F100\n'
        elif action == "1":
            cmdtail='G0 X65 Y132 Z80 F100\n'
        elif action == "2":
            cmdtail='G0 X00 Y132 Z80 F100\n'
        elif action == "3":
            cmdtail='G0 X-55 Y146 Z80 F100\n'
        elif action == "4":
            cmdtail='G0 X73 Y200 Z80 F100\n'
        elif action == "5":
            cmdtail='G0 X10 Y200 Z80 F100\n'
        elif action == "6":
            cmdtail='G0 X-50 Y214 Z80 F100\n'
        elif action == "7":
            cmdtail='G0 X80 Y268 Z80 F100\n'
        elif action == "8":
            cmdtail='G0 X10 Y268 Z80 F100\n'
        elif action == "9":
            cmdtail='G0 X-45 Y282 Z80 F100\n'
        else :
            return

        cmd='#'+str(id)+' '+cmdtail
        ser.write(cmd.encode())
        print(cmd)
        print(ser.readline())
# run()
# i = 0
# while i<10:
#     i= i+1
#     catchinit(1.5)
#     uarmcatch(1.5)
#     uarmrelease()
# test()
# catchinit(1.5)
# initzero(1.5)
playchess()
