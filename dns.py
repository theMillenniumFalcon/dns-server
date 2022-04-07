# TO create a UDP or TCP connection
import socket
from sys import byteorder

port = 53 # as DNS operates on port 53
ip = '127.0.0.1'

# socket.AF_INET -> as we are using IPV4
# socket.SOCK_DGRAM -> as we are making a UDP server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def getFlags(flags):
    
    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])
    
    rflags = ''
    QR = 1
    
    OPCODE = ''
    for bit in range(1, 5):
        OPCODE += str(ord(byte1)&(1<<bit))
    
    AA = '1'
    TC = '0'
    RD = '0'
    RA = '0'
    Z = '000'
    RCODE = '000'
    
    return int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder = 'big') + int(RA + Z + RCODE, 2).to_bytes(1, byteorder= 'big')

def getQuestionDomain(data):
    state = 0
    expectedLength = 0
    domainString = ''
    domainParts = []
    x = 0
    y = 0
    
    for byte in data:
        if state == 1:
            domainString += chr(byte)
            x += 1
            if x == expectedLength:
                domainParts.append(domainString)
                domainString = ''
                state = 0
                x = 0
            if byte == 0:
                domainParts.append(domainString)
                break
        else:
            state = 1
            expectedLength = byte
        x += 1
        y += 1
        
    questionType = data[y+1:y+3]
    print(questionType)
        
    return (domainParts, questionType)

def buildresponse(data):
    
    # Transaction ID
    TransactionID = data[:2]
    TID = ''
    for byte in TransactionID:
        TID += hex(byte)[2:]
    
    # Get the Flags
    Flags = getFlags(data[2:4])
    
    # Question Count
    QDCOUNT = b'\x00\x01'
    
    # Answer Count
    getQuestionDomain(data[12:])
    
    print(Flags)

while 1: 
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
