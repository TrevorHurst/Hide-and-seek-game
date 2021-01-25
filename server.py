import socket
    
HOST = '192.168.1.53'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)
CONNECTIONS = []
ADDRI = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    try:
        data, addr = s.recvfrom(1024)
    except:
        continue
        
    if addr not in ADDRI:
        ADDRI.append(addr)
        print('Connection from,',addr)
    
    for address in ADDRI:
        try:
            data = data.decode()
        except:
            pass
        
        ip = addr[0]
        string = ip+' '+data
        
        try:
            s.sendto(string.encode(), address)
        except:
            ADDRI.remove(address)
