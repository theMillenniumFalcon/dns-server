# TO create a UDP or TCP connection
import socket, glob, json
from sys import byteorder

port = 53 # as DNS operates on port 53
ip = '127.0.0.1'

# socket.AF_INET -> as we are using IPV4
# socket.SOCK_DGRAM -> as we are making a UDP server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

def loadZones():
    
    jsonZone = {}
    zoneFiles = glob.glob('zones/*.zone')
    
    for zone in zoneFiles:
        with open(zone) as zoneData:
            data = json.load(zoneData)
            zoneName = data["$origin"]
            jsonZone[zoneName] = data
        return jsonZone

zoneData = loadZones()

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
            if byte != 0:
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
        y += 1
        
    questionType = data[y:y+2]
        
    return (domainParts, questionType)

def getZone(domain):
    global zoneData
    
    zoneName = '.'.join(domain)
    return zoneData[zoneName]

def getRecs(data):
    domain, questiontype = getQuestionDomain(data)
    qt = ''
    if questiontype == b'\x00\x01':
        qt = 'a'
    
    zone = getZone(domain)
    
    return (zone[qt], qt, domain)

def buildQuestion(domainName, recType):
    qbytes = b''
    
    for part in domainName:
        length = len(part)
        qbytes += bytes([length])
        
        for char in part:
            qbytes += ord(char).to_bytes(1, byteorder='big')
        
    if recType == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')
            
    qbytes += (1).to_bytes(2, byteorder='big')
        
    return qbytes    

def recToBytes(domainName, recType, recttl, recval):
    rbytes = b'\xc0\x0c'
    
    if recType == 'a':
        rbytes += rbytes + bytes([0]) + bytes([1])
        
    rbytes = rbytes + bytes([0]) + bytes([1])
    
    rbytes += int(recttl).to_bytes(4, byteorder='big')
    
    if recType == 'a':
        rbytes = rbytes + bytes([0]) + bytes([4])
        
        for part in recval.split('.'):
            rbytes += bytes([int(part)])
    return rbytes
      
def buildResponse(data):
    
    # Transaction ID
    TransactionID = data[:2]
    
    # Get the Flags
    Flags = getFlags(data[2:4])
    
    # Question Count
    QDCOUNT = b'\x00\x01'
    
    # Answer Count
    AnswerCount = len(getRecs(data[12:])[0]).to_bytes(2, byteorder='big')
    
    # NameServer Count
    NameServerCount = (0).to_bytes(2, byteorder='big')
    
    # Additional Count
    AdditionalCount = (0).to_bytes(2, byteorder='big')
    
    dnsHeader = TransactionID + Flags + QDCOUNT + AnswerCount + NameServerCount + AdditionalCount
    
    # Create DNS body
    dnsBody = b''
    
    # get answer for the query
    records, recType = domainName = getRecs(data[12:])
    
    dnsQuestion = buildQuestion(domainName, recType)
    
    for record in records:
        dnsBody += recToBytes(domainName, recType, record["ttl"], record["value"])
    
    return dnsHeader + dnsQuestion + dnsBody

while 1: 
    data, addr = sock.recvfrom(512)
    r = buildResponse(data)
    sock.sendto(r, addr)
