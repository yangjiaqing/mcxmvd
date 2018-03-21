global ser,id
import serial
import serial.tools.list_ports
import time
def putchess(fieldid):
    global ser,id
    print("hello i will put  chess to %d by uarm,please wait" % fieldid)
    #please add real code There
    #return
    id=id+1
    movelist = ['G0 X43 Y88 Z87 F100\n','G0 X08 Y84 Z87 F100\n','G0 X-32 Y100 Z80 F100\n','G0 X63 Y163 Z83 F100\n','G0 X10 Y150 Z83 F100\n','G0 X-38 Y165 Z80 F100\n','G0 X72 Y235 Z85 F100\n','G0 X20 Y245 Z85 F100\n','G0 X-43 Y250 Z80 F100\n']
    cmdtail = movelist[fieldid]
    cmd='#'+str(id)+' '+cmdtail
    ser.write(cmd.encode())
    print(movelist[fieldid])
    time.sleep(1.5)
def uarminit():
    global ser,id
    id=0
    print("please put uarminit code here")
    #return
    ports = list(serial.tools.list_ports.comports())
    print (ports)
    for p in ports:
        print (p[1])
        if ("SERIAL" in p[1])or("Serial" in p[1])or("FT232R USB UART" in p[1]):
            ser = serial.Serial(port=p[0],baudrate=115200)
        else :
        # ser = serial.Serial(port="24",baudrate=115200)
            print ("No Serial or SERIAL Device was found connected to the computer")
