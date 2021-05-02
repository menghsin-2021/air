from typing import List

# TGS2600
import serial
import time
# SDS011
import struct
from datetime import datetime

# db
from dbwrapper import DBWrapper

db = DBWrapper()

# TGS2600
COM_PORT = 'COM4'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率

# SDS011
PORT = 'COM3' 
UNPACK_PAT = '<ccHHHcc'

ser_tgs = serial.Serial(COM_PORT, BAUD_RATES)   # TGS2600 初始化序列通訊埠
ser_sds011 = serial.Serial(PORT, 9600, bytesize=8, parity='N', stopbits=1)   # SDS011 初始化序列通訊埠

pm25_sec = []
pm10_sec = []
tvoc_tgs_sec = []

def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)

while True:
    while ser_tgs.in_waiting:  # 若收到序列資料…
        
        # SDS011
        data = ser_sds011.read(10)
        unpacked = struct.unpack(UNPACK_PAT, data)
        ts = datetime.now()
        pm25 = unpacked[2] / 10.0
        pm10 = unpacked[3] / 10.0
        pm25_sec.append(pm25)
        pm10_sec.append(pm10)
               
        # TGS2600
        data_raw = ser_tgs.readline()  # 讀取一行
        if len(data_raw.decode().strip()) > 0:  # 用預設的UTF-8解碼
            tvoc_tgs = int(data_raw.decode().split('\r')[0])
            tvoc_tgs_sec.append(tvoc_tgs)
        else:
            continue

        print("{}: PM 2.5 = {}, PM 10 = {}, TVOC-TGS: {}".format(ts, pm25, pm10, tvoc_tgs))
        db.insert_data(tvoc_tgs, pm25, pm10)
                
        if len(pm25_sec) >= 60:
            pm25_min = mean(pm25_sec)
            pm10_min = mean(pm10_sec)
            tvoc_tgs_min = mean(tvoc_tgs_sec)
            print('minute data inserted')
            db.insert_data_minute(tvoc_tgs_min, pm25_min, pm10_min)
            pm25_sec.clear()  
            pm10_sec.clear() 
            tvoc_tgs_sec.clear() 

        else:
            continue
        

        time.sleep(1)
    

            
