# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:30:14 2025

@author: windows
"""
import base64

import struct
import socket
import random
from time import sleep

TM_SEND_ADDRESS = '127.0.0.1'
TM_SEND_PORT    = 10015


def floats_to_ieee754_with_prefix_suffix(*values):
    """
    Converts a list of float values to IEEE 754 single-precision (32-bit),
    prepends a fixed byte sequence at the beginning, and appends another
    fixed byte sequence at the end.
    """

    dynamic_bytes = b''.join(struct.pack('>f', value) for value in values)  # Convert floats
    return dynamic_bytes  # Prepend and append sequences

def Values_sim(CO2_Level, Hum_Level, Temp, Airlock_Press, Cabin_Press, Ammonia_Level, Air_Quality):
    CO2_Level += round(random.uniform(-5, 5), 2)
    Hum_Level += round(random.uniform(-1, 1), 2)
    Temp += round(random.uniform(-0.5, 0.5), 2)
    Airlock_Press += round(random.uniform(-5, 5), 2)
    Cabin_Press += round(random.uniform(-5, 5), 2)
    Ammonia_Level += round(random.uniform(-0.1, 0.1), 2)
    Air_Quality += round(random.uniform(-0.5, 0.5), 2)
    
    values_ENV = [CO2_Level, Hum_Level, Temp, Airlock_Press, Cabin_Press, Ammonia_Level, Air_Quality]  # ENV
    byte_seq = Header(seq_count) + floats_to_ieee754_with_prefix_suffix(*values_ENV) + fixed_suffix
    return(byte_seq)

def Header(seq_count):    
    if seq_count >= 16382 :
        seq_count=0 

        
    
    print("ENV SEQ : ", seq_count)
    return  b'\x00\x64' + (49152+seq_count).to_bytes(2, 'big') +  b'\x01\x45'

# Example usage:
RATE=1

seq_count=0
CO2_Level =  700
Hum_Level = 50
Temp =  21.5
Airlock_Press = 1015
Cabin_Press = 1015
Ammonia_Level = 2.5
Air_Quality = 25
    
fixed_suffix = b'\x20\x00\x00\x00'  # Airlock Depress. State
# fixed_suffix = b'\x00\x00\x00\x00'  # Airlock Press. State

print('Sending ENV Data Using playback rate of ', str(RATE) + 'Hz, ');
print('TM host=' + str(TM_SEND_ADDRESS) + ', TM port=' + str(TM_SEND_PORT) + ', ');
# print('TC host=' + str(TC_RECEIVE_ADDRESS) + ', TC port=' + str(TC_RECEIVE_PORT) + '\r\n');




while True :
    
    byte_seq = Values_sim(CO2_Level, Hum_Level, Temp, Airlock_Press, Cabin_Press, Ammonia_Level, Air_Quality)
    # ✅ Print output in correct byte format
    # print(byte_seq)  # Direct bytes output
    # print(" ".join(f"{b:02x}" for b in byte_seq))  # Hex string representation

    # ✅ Convert to bytearray if needed
    byte_array = bytearray(byte_seq)
    # print(byte_array)  # Shows bytearray representation




    packet2=byte_array

    tm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tm_socket.sendto(packet2, (TM_SEND_ADDRESS, TM_SEND_PORT)) 
    seq_count += 1
    sleep(1/RATE)                           
