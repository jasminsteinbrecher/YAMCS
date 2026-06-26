# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 18:23:32 2025

@author: windows
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:30:14 2025

@author: windows
"""
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import struct
import socket
import random
from time import sleep

TM_SEND_ADDRESS = '127.0.0.1'
TM_SEND_PORT    = 10016


def floats_to_ieee754_with_prefix_suffix(*values):
    """
    Converts a list of float values to IEEE 754 single-precision (32-bit),
    prepends a fixed byte sequence at the beginning, and appends another
    fixed byte sequence at the end.
    """

    dynamic_bytes = b''.join(struct.pack('>f', value) for value in values)  # Convert floats
    return dynamic_bytes  # Prepend and append sequences

def Values_sim(RR1,HR1,TEMP1,BOS1,BP1,RR2,HR2,TEMP2,BOS2,BP2, value):
    
    RR1+= round(random.uniform(-0.5, 0.5), 2)
    HR1+= round(random.uniform(-0.5, 0.5), 2)
    TEMP1+= round(random.uniform(-0.1, 0.1), 2)
    BOS1+= round(random.uniform(-0.5, 0.5), 2)
    BP1+= round(random.uniform(-0.5, 0.5), 2)

    RR2+= round(random.uniform(-0.5, 0.5), 2)
    HR2+= round(random.uniform(-0.5, 0.5), 2)
    TEMP2+= round(random.uniform(-0.1, 0.1), 2)
    BOS2+= round(random.uniform(-0.5, 0.5), 2)
    BP2+= round(random.uniform(-0.5, 0.5), 2)   
   
    values_BM = [RR1,HR1,TEMP1,BOS1,BP1,RR2,HR2,TEMP2,BOS2,BP2]  # BM
    
    
    byte_seq = floats_to_ieee754_with_prefix_suffix(*values_BM)    #
    return(byte_seq)



def encrypt_float(float_value, public_key):
    # Convert the float to bytes
    float_bytes = struct.pack('f', float_value)
    
    # Load the public key
    pub_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(pub_key)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(float_bytes)
    
    # Return the encrypted data as base64 for easier transmission (e.g., over UDP)
    return base64.b64encode(encrypted_data).decode()

def Header(seq_count):    
    if seq_count >= 16382 :
        seq_count=0 
    print("BM SEQ : ", seq_count)
    return  b'\x00\x65' + (49152+seq_count).to_bytes(2, 'big') +  b'\x04\x45'



public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwXscLFkBaE1zzmou/cCg\nlSmOojSUT36tP5cy05goya5n6QP8AwquWTz/y1gt0eUUurliz+aYJnN8/HuLLsKq\ndZEGRJsiAP5o0i1NAyEvrkcek1vtX1CXEX94IctHKdfEJ0XvB7DYRRNB78HagwEW\nutYrS17srFZhblnPpn1Q1nbjAZ+fHX/tSU9sCbyIcNmYptGkEwp5ArkZ1ZbVLEoj\nL4uay9BxM+ijszaJRKklYjQOjftdJDmeYPCIF2peXu2w9XsZ0stDNG6c72LxOkIV\nHBlhd1WMQAl7wz1+/B6bUw10ytJKF674+4tlSVj0TDQnhlQn6SNTe07CvuqOkRj0\n/wIDAQAB\n-----END PUBLIC KEY-----"
value = 775.34
old_value = 1

# Example usage:
seq_count=0
RATE = 1

RR1= 15
HR1= 90
TEMP1= 38
BOS1= 97
BP1= 120

RR2= 15
HR2= 90
TEMP2= 38
BOS2= 97
BP2=120
    
#fixed_suffix = b'\x20\x00\x00\x00'  # Airlock Depress. State
fixed_suffix = b'\x00\x00\x00\x00'  # Airlock Press. State


print('Sending BM Data Using playback rate of ', str(RATE) + 'Hz, ');
print('TM host=' + str(TM_SEND_ADDRESS) + ', TM port=' + str(TM_SEND_PORT) + ', ');
# print('TC host=' + str(TC_RECEIVE_ADDRESS) + ', TC port=' + str(TC_RECEIVE_PORT) + '\r\n');

while True :
    if value != old_value :
        cypher = encrypt_float(value,public_key)
        old_value = value
    byte_seq = Header(seq_count) + Values_sim(RR1,HR1,TEMP1,BOS1,BP1,RR2,HR2,TEMP2,BOS2,BP2, value)+ bytearray(cypher, 'utf-8') 
    byte_array = bytearray(byte_seq)
    # print(byte_array)  # Shows bytearray representation




    packet2=byte_array

    tm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tm_socket.sendto(packet2, (TM_SEND_ADDRESS, TM_SEND_PORT)) 
    seq_count += 1
    sleep(1/RATE)                           
