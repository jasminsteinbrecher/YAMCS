import socket
import tkinter as tk
from tkinter import messagebox

TM_SEND_ADDRESS = '127.0.0.1'
TM_SEND_PORT = 10017

HEADER = b'\x00\x66\xc0\x00\x00\x45'

def send_alarm():
    fire_alarm = fire_var.get()
    moonquake_alarm = moonquake_var.get()
    flooding_alarm = flooding_var.get()
    solar_flare_alarm = solar_flare_var.get()
    
    # Construct the 4-bit suffix (1 bit per alarm)
    suffix_bits = ""
    suffix_bits += "1" if fire_alarm else "0"  # Fire Alarm
    suffix_bits += "1" if moonquake_alarm else "0"  # Moonquake Alarm
    suffix_bits += "1" if flooding_alarm else "0"  # Flooding Alarm
    suffix_bits += "1" if solar_flare_alarm else "0"  # Solar Flare Alarm
    
    # Convert to a single byte with padding
    suffix_value = int(suffix_bits.ljust(8, '0'), 2).to_bytes(1, byteorder='big') + b'\x00\x00\x00'
    
    # Create the final packet
    packet = HEADER + suffix_value
    
    # Send the packet
    try:
        tm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tm_socket.sendto(packet, (TM_SEND_ADDRESS, TM_SEND_PORT))
        tm_socket.close()
        messagebox.showinfo("Success", "Alarm status sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send packet: {e}")

# GUI Setup
root = tk.Tk()
root.title("Alarm Control")
root.geometry("300x250")

fire_var = tk.IntVar()
moonquake_var = tk.IntVar()
flooding_var = tk.IntVar()
solar_flare_var = tk.IntVar()

tk.Label(root, text="Set Alarm State", font=("Arial", 14)).pack(pady=10)

fire_check = tk.Checkbutton(root, text="Fire Alarm", variable=fire_var)
fire_check.pack()

moonquake_check = tk.Checkbutton(root, text="Moonquake Alarm", variable=moonquake_var)
moonquake_check.pack()

flooding_check = tk.Checkbutton(root, text="Flooding Alarm", variable=flooding_var)
flooding_check.pack()

solar_flare_check = tk.Checkbutton(root, text="Solar Flare Alarm", variable=solar_flare_var)
solar_flare_check.pack()

tk.Button(root, text="Send", command=send_alarm).pack(pady=10)

root.mainloop()
