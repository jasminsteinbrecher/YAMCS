# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 21:08:28 2025

@author: windows
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:30:14 2025

@author: windows
"""

import socket


TM_SEND_ADDRESS = '127.0.0.1'
TM_SEND_PORT    = 10017


Header=  b'\x00\x66\xc0\x00\x00\x45'


    
fixed_suffix = b'\x80\x00\x00\x00'  # Emergency State


print('Sending Emergency Status of Fire Alarm')
print('TM host=' + str(TM_SEND_ADDRESS) + ', TM port=' + str(TM_SEND_PORT) + ', ')




byte_seq = Header+fixed_suffix
byte_array = bytearray(byte_seq)

packet2=byte_array

tm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tm_socket.sendto(packet2, (TM_SEND_ADDRESS, TM_SEND_PORT)) 
                           
 


                          