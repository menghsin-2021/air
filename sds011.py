import serial
import struct
from datetime import datetime

# pip install serialstruct 要先安裝套件


PORT = 'COM3' 
# 要找SDS011接在哪個孔
# Change this to the right port - /dev/tty* on Linux and Mac and COM* on Windows

UNPACK_PAT = '<ccHHHcc'

with serial.Serial(PORT, 9600, bytesize=8, parity='N', stopbits=1) as ser:
    while True:
        data = ser.read(10)
        unpacked = struct.unpack(UNPACK_PAT, data)
        ts = datetime.now()
        pm25 = unpacked[2] / 10.0
        pm10 = unpacked[3] / 10.0
        print("{}: PM 2.5 = {}, PM 10 = {}".format(ts, pm25, pm10))