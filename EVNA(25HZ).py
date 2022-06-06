import visa
import time
from time import perf_counter
import csv
import tdt
from pyvisa import util

print('Welcome to E5061A remote control!')
print('Initializing...')
print('')

syn = tdt.SynapseAPI()
rm = visa.ResourceManager()
E5061 = rm.open_resource('TCPIP0::192.168.0.1::inst0::INSTR')
freq = 25
period = 1 / freq
time_run=[]
trace=[]

def file():
    global filename
    filename = input('enter filename: ')


def initialize():
    E5061.write(':SYST:PRES')
    E5061.write(':DISP:WIND:ACT')
    E5061.write(':DISP:SPL %s' % ('D1'))
    E5061.write(':CALC1:PARameter1:COUN %d' % (1))
    E5061.write(':CALC1:PARameter1:SEL')
    E5061.write(':CALC1:PARameter1:DEF %s' % ('S11'))
    E5061.write(':SENS1:SWE:TYPE %s' % ('LIN'))
    E5061.write(':SENS1:FREQ:STAR %G' % (300000.0))
    E5061.write(':SENS1:FREQ:STOP %G' % (500000000.0))
    E5061.write(':SENS1:SWE:POIN %d' % (1001))
    E5061.write(':SENS1:SWE:TIME:AUTO %d' % (1))
    E5061.write("FORMat:DATA REAL")
    E5061.expect_termination=False
    print('done!')


def gettrace():
    E5061.write("CALC1:DATA:FDAT?")
    rawdata = E5061.read_raw()
    return rawdata

def apcsv(data):
    with open(filename+'.csv', 'a+', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(data)
        stream.close()

def setmode(mode):
    if mode == 'hi':
        E5061.write(':SENS1:FREQ:STAR %G' % (500000000.0))
        E5061.write(':SENS1:FREQ:STOP %G' % (1500000000.0))
    if mode == 'lo':
        E5061.write(':SENS1:FREQ:STAR %G' % (300000.0))
        E5061.write(':SENS1:FREQ:STOP %G' % (500000000.0))


def writetrace(frame=600):
    for i in range(0, frame):
        t1 = time.perf_counter()
        trace.append(gettrace())
        time_run.append(time.perf_counter()-t1)
        while (time.perf_counter() - t1) < period:
            time.sleep(0)
    dataconvert(trace)
    timefile=open(filename+'time25.txt','w')
    for sec in time_run:
        timefile.write(str(sec)+',')
    timefile.close()
    print('done')

def dataconvert(datalist):
    for rawdata in datalist:
        converted = util.from_ieee_block(rawdata, datatype='d', is_big_endian=True)
        converted = converted[::2]
        apcsv(converted)
    print('done')

def clearfile():
    try:
        f = open(filename, 'w')
        f.truncate()
        f.close()
    except(FileNotFoundError, IOError):
        print('no such file')

def syncwrite(frame=600):
    if syn.getMode() != 0:
        syn.setMode(0)
    syn.setMode(2)
    while (syn.getParameterValue('UIn1', 'Button1') == 0):
        pass
    for i in range(0, frame):
        t1 = time.perf_counter()
        binarywrite(gettrace())
        while (time.perf_counter() - t1) < period:
            time.sleep(0)
    print('done')


def close():
    E5061.close()
    rm.close()


def help():
    print('h -- help info, explanation of commands')
    print('f -- set the file name')
    print('clr -- clear the assigned file')
    print('s lo/s hi -- set low or high frequency sweep')
    print('w -- write trace points to csv file for 600 frames')
    print('w NumberOfFrames -- write trace points to csv file in certain number of frames')
    print('sync -- syncwrite() with the camera for 600 frames')
    print('sync NumberOfFrames -- syncwrite with camera for certain number of frames')
    print('q -- quit the script and close connections')


def menu():
    command = input('enter command: ')
    commandseq = command.split()
    if commandseq[0] == 'f':
        file()
        menu()
    elif commandseq[0] == 's':
        setmode(commandseq[1])
    elif commandseq[0] == 'w':
        if len(commandseq) == 1:
            writetrace()
            menu()
        try:
            writetrace(int(commandseq[1]))
            menu()
        except TypeError:
            print('invalid command')
            menu()
    elif commandseq[0] == 'sync':
        if len(commandseq) == 1:
            syncwrite()
            menu()
        try:
            syncwrite(int(commandseq[1]))
            menu()
        except TypeError:
            print('invalid command')
            menu()
    elif commandseq[0] == 'clr':
        clearfile()
        menu()
    elif commandseq[0] == 'q':
        close()
        quit()
    elif commandseq[0] == 'h':
        help()
        menu()
    else:
        print('invalid command')
        menu()


initialize()
print('')
help()
menu()
