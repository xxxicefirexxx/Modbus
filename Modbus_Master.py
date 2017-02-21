import sys, signal ,time

from pymodbus.client.sync import ModbusTcpClient

#Modbus Slave IP Address
host = '192.168.1.100'
#Modbus Port No.
port = 502
#Initialize Maximum Data for Write Registers
Array_Data=[0,0,0,0,0,0,0,0,0,0]
#Initialize Number of Data to Write
Array_Number=5

client = ModbusTcpClient(host, port)
client.connect()

#Interrupt by Ctrl+C
def signal_handler(signal, frame):
    global Array_Data, Array_Number
    #Enter Number of Write Data
    try:
        Array_Number=int(raw_input('Enter Number of Write Register, Max 10: '))
        #Exit Function if Number of Data > 10
        if Array_Number > 10:
            print('Invalid Number')
            return
    #Exit Program if is not a number
    except ValueError:
        print('Invalid Char')
        sys.exit(0)
    #Save Write Data
    print 'Enter %d Numbers' % Array_Number
    for counter in range(0,Array_Number):
        #Enter Write Data
        try:
            Array_Data[counter]=int(raw_input('Enter Number or any CHAR to Quit: '))
        #Exit Program if is not a number
        except ValueError:
            print('Exit Modbus')
            sys.exit(0)
    #Enter Write Register Starting Address
    Start_Write_Address=int(raw_input('Enter Start Address: '))
    for counter1 in range(0,Array_Number):
        ww = client.write_register(Start_Write_Address+counter1,Array_Data[counter1])
        assert(ww.function_code < 0x80)     # test that we are not an error
#Loop
signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C to Enter Write Register'
while True:
    time.sleep(1)
    
    #Read Holding Register Address 0
    Start_Read_Address=0
    Read_Num_Data=5
    rr = client.read_holding_registers(Start_Read_Address,Read_Num_Data,unit=0)
    assert(rr.function_code < 0x80)     # test that we are not an error
    print rr
    print rr.registers
