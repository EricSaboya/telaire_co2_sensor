# ****************************************************************************
# Created: 3 Dec. 2022
# Author: Eric Saboya 
# Affiliation: School of Geographical Sciences, University of bristol
# Contact: eric.saboya@bristol.ac.uk
# ****************************************************************************
# About
# Python script for reading and logging atmospheric CO2 concentrations
# using a Telaire T6713 low-cost sensor. 
# 
# ****************************************************************************

import os
import sys
import csv
import time
import serial
import array
import datetime as dt
import traceback

def logfilename():
    """Create datalogging file with appropriate time stamp
    """
    now=dt.datetime.now()
    return 'CO2LOG-%0.4d-%0.2d-%0.2d-%0.2d%0.2d%0.2d.csv' % (now.year, 
                                                             now.month,
                                                             now.day, 
                                                             now.hour, 
                                                             now.minute,
                                                             now.second)

def connect_serial(serial_dev):
    """ Interface with CO2 Telaire sensor (connect via USB)
    """
    return serial.Serial(port=serial_dev, 
                         baudrate=19200, 
                         bytesize=8, 
                         parity="E", 
                         stopbits=1, 
                         timeout=1.0)

def read_concentration():
    """ Reads CO2 concentration from sensor
    """
#    serial_dev="/dev/tty.usbserial-025B7D35"
#    serial_dev="/dev/tty.usbserial-025B7D61"
    serial_dev="/dev/tty.usbserial-025B7D62"
#    serial_dev="/dev/tty.usbserial-025950FF"

    retry_count=3

    buffer = array.array('B', [0x15, 0x04, 0x13, 0x8B, 0x00, 0x01, 0x46, 0x70])

    try:
        ser=connect_serial(serial_dev)
        for retry in range(retry_count):
            result=ser.write(buffer)
            # time.sleep(0.1)
            s=ser.read(4)
            buffer = array.array('B', s)

            return buffer[2]*256+buffer[3]
    except:
        traceback.print_exc()
        return ""

def telaire():
    """ If CO2 values exist, insert into dict.
    """
    co2=read_concentration()
    if not co2:
        return {'co2':''}
    else:
        return {'co2':co2}

def concentration_uncert(c):
    """ Calculate concentration uncertainty based on manual
    """
    uncert = c*0.03 + 25
    return uncert

def main():
    outfname=logfilename()
    try:
        with open(outfname, 'a') as f:
            f.write("time,CO2,uncertainty\n")
            while True:
                co2=telaire()
                now=time.ctime()
                parsed=time.strptime(now)
                lgtime=time.strftime("%Y-%m-%d %H:%M:%S")
                row=[lgtime, co2['co2']]
                print('Time Stamp: ',lgtime, ', CO2 concentration: ', co2['co2'],'ppm')
				# Calculate uncertainties
                uncert = concentration_uncert(co2['co2'])
				# Write data to file.
                f.write(str(lgtime)+','+str(co2['co2'])+','+str(uncert)+'\n')
                measuretime=5
                time.sleep(measuretime)
    except KeyboardInterrupt as e:
        f.close()
        sys.stderr.write('Ctrl+C pressed, exiting log of %s' % (outfname))

if __name__ == "__main__":
    main()
