# TO create a UDP or TCP connection
import socket

port = 53 # as DNS operates on port 53
ip = '127.0.0.1'

# socket.AF_INET -> as we are using IPV4
# socket.SOCK_DGRAM -> as we are making a UDP server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def buildresponse(data):
    
    # Transaction ID
    TransactionID = data[:2]
    TID = ''
    for byte in TransactionID:
        TID += hex(byte)[2:]
    
    # Get the Flags
    Flags = getflags(data[2:4])

while 1:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
