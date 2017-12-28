import serial
import serial.tools.list_ports

print ('hello')

ports = list(serial.tools.list_ports.comports())

print (ports)

for p in ports:
    print (p[1])
    if ("SERIAL" in p[1])or("Serial" in p[1]):
	    ser = serial.Serial(port=p[0],baudrate=115200)
    else :
	    print ("No Arduino Device was found connected to the computer")

#ser=serial.Serial(port='COM4')

def run():
    action = "aaa"
    id=1
    while action != "q":
        id=id+1
        print ('select which tone do you want to play ? 1,2,3, q and others for quit')
        action = input("> ")
        if action == "1":
            cmdtail='G0 X100 Y100 Z100 F100\n'
        elif action == "2":
            cmdtail='M210 F1000 T0.2\n'
        elif action == "3":
            cmdtail='G0 X50 Y50 Z50 F100\n'
        elif action == "4":
            cmdtail='G0 X50 Y50 Z100 F100\n'
        else :
            return

        cmd='#'+str(id)+' '+cmdtail
        ser.write(cmd.encode())
        print(cmd)
        print(ser.readline())
run()
