#!/usr/bin/python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
#from get_temp_c import temp_c


lcd = Adafruit_CharLCDPlate()

lcd.clear()
lcd.message("  Proba Homero\n   2013.09.21   ")
sleep(2)
lcd.clear()

#   Temp meter begin

import os, signal, sys
import glob 
import time 
from time import gmtime, strftime

version = 0.03
maxtemp = 0
mintemp = 100
counter = 0
deltaT = 0
deltaTold = 0
deltaTnew = 0
deltaTcount= 0

# File Create

file = 'log ' + str(strftime("%Y%b%d %H:%M:%S", gmtime())) + '.csv'

try:
    filei = open(file, 'a')
    
except:
    print 'File access failed. Programm terminated.'
    sys.exit(0)

# Get Temp

os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 

base_dir = '/sys/bus/w1/devices/' 
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave' 

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines 

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_c = round (temp_c , 2) 
        return temp_c 

# Exit

def signal_handler(signal, frame):
    print '\nCTRL+C received. Programm terminated.'
    lcd.clear()
    lcd.backlight(lcd.OFF)
    filei.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

os.system('clear')
print "Thermolog v" + str(version)
print "(press CTRL+C to quit)\n"

while True:


    newtemp = read_temp()
    timestamp=str(strftime("%Y %b %d %H:%M:%S", gmtime()))


    deltaTnew = newtemp - deltaTold
    deltaTold = newtemp
    
    if deltaTnew >= 0.1 or deltaTnew <= -0.1:
#        print "ALARM"
        lcd.clear()
        lcd.message ("DeltaT: " + "\n" +"        "+ str(deltaTnew)+ "!!!")
        lcd.backlight(lcd.OFF)
        sleep(.5)
        lcd.backlight(lcd.ON)
        sleep(.5)
        lcd.backlight(lcd.OFF)
        sleep(.5)
        lcd.backlight(lcd.ON)
        sleep(.5)
        lcd.backlight(lcd.OFF)
        sleep(.5)
        lcd.backlight(lcd.ON)
        sleep(.5)
    
    time.sleep(2)
        
    
    if newtemp > maxtemp:
        maxtemp = newtemp

    if newtemp < mintemp:
        mintemp = newtemp


#    print timestamp, read_temp(), "C" , "Max", maxtemp, "Min", mintemp, deltaTnew

    lcd.home()
    lcd.message (str(read_temp()) + " Max: " + str(maxtemp))
# format delta T value
    strdelta = str(deltaTnew)
    if len(strdelta) == 4:
     lcd.message ("\n" + "0" + strdelta + " Min: "+ str(mintemp)+ "  ")
    elif len(strdelta) == 3:
     lcd.message ("\n" + "0" + strdelta + "0" + " Min: "+ str(mintemp)+ "  ")
    else: 
     lcd.message ("\n" + strdelta + " Min: "+ str(mintemp)+ "  ")
    filei.write(timestamp + ' , ' + str(read_temp()) + ' , ' + str(maxtemp) + ' , ' + str(mintemp) + "\n")

# Safety

counter = counter + 1
if counter >= 5:
    filei.close()
    filei = open(file, 'a')
    counter = 0


time.sleep(2)






 
