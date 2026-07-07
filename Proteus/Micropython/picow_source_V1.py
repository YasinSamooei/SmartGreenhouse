from machine import UART, Pin
import network
import socket
import time

# ---------------- UART ----------------

uart = UART(
    0,
    baudrate=115200,
    tx=Pin(12),
    rx=Pin(13)
)

buffer = bytearray()

# ---------------- WIFI ----------------

SSID = ""
PASSWORD = ""

HOST = ""
PORT = 8000
PATH = "/send/sensor/value"

last = {
    "T":29.1,
    "H":40.0,
    "S":0,
    "G":0,
    "L":0,
    "F":0,
    "P":0,
    "HE":0,
    "A":0,
    "LI":0
}

def wifi_connect():

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    if wlan.isconnected():
        return wlan

    print("Connecting WiFi...")

    wlan.connect(SSID,PASSWORD)

    while not wlan.isconnected():
        time.sleep(1)

    print("Connected")
    print(wlan.ifconfig())

    return wlan


wlan = wifi_connect()

def send_json():

    global wlan

    if not wlan.isconnected():
        wlan = wifi_connect()

    payload = (
        '{{'
        '"temperature":{},'
        '"humidity":{},'
        '"soil":{},'
        '"gas":{},'
        '"ldr":{},'
        '"fan":{},'
        '"pump":{},'
        '"heater":{},'
        '"alarm":{},'
	'"light":{}'
        '}}'
    ).format(
        last["T"],
        last["H"],
        last["S"],
        last["G"],
        last["L"],
        last["F"],
        last["P"],
        last["HE"],
        last["A"],
	last["LI"]
    )

    print("\nSEND >>>")
    print(payload)

    try:

        request = (
            "POST {} HTTP/1.1\r\n"
            "Host: {}\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: {}\r\n"
            "Connection: close\r\n\r\n{}"
        ).format(PATH,HOST,len(payload),payload)

        addr = socket.getaddrinfo(HOST,PORT)[0][-1]

        s=socket.socket()

        s.connect(addr)

        s.send(request.encode())

        while s.recv(256):
            pass

        s.close()

    except Exception as e:

        print("HTTP ERROR",e)
	
def parse_value(line,key):

    p=line.find(key)

    if p==-1:
        return None

    p+=len(key)

    value=""

    while p<len(line):

        c=line[p]

        if c.isdigit() or c==".":
            value+=c
            p+=1
            continue

        break

    if value=="":
        return None

    return value
    
def set_float(name,value,minv,maxv):

    if value is None:
        return

    try:
        v=float(value)
    except:
        return

    if minv<=v<=maxv:
        last[name]=v


def set_int(name,value,minv,maxv):

    if value is None:
        return

    try:
        v=int(value)
    except:
        return

    if minv<=v<=maxv:
        last[name]=v
	
def parse_packet(line):

    global last

    values = {}

    i = 0

    while i < len(line):



        key = None

        if line.startswith("HE", i):
            key = "HE"
            i += 2
	    
        elif line.startswith("LI", i):
            key = "LI"
            i += 2

        elif line[i] in "THSGLFPA":
            key = line[i]
            i += 1

        else:
            i += 1
            continue


        if i < len(line) and line[i] == '=':
            i += 1



        value = ""

        while i < len(line):

            c = line[i]

            if c.isdigit() or c == '.':
                value += c
                i += 1
                continue

            break

        if value != "":
            values[key] = value

    print("\n----------------")
    print("RAW :", line)
    print("FOUND :", values)



    for k, v in values.items():

        try:

            if k in ("T", "H"):

                num = float(v)

            else:

                num = int(v)

        except:

            continue

        if k == "T":

            if -20 <= num <= 80:
                last["T"] = num

        elif k == "H":

            if 0 <= num <= 100:
                last["H"] = num

        elif k == "S":

            if 0 <= num <= 100:
                last["S"] = num

        elif k == "G":

            if 0 <= num <= 100:
                last["G"] = num

        elif k == "L":

            if 0 <= num <= 4095:
                last["L"] = num

        elif k in ("F", "P", "HE", "A", "LI"):


            if num in (0, 1):
                last[k] = num

    print("\nLAST VALUES")

    for k in ("T","H","S","G","L","F","P","HE","A","LI"):
        print(k, "=", last[k])

    print("----------------")

    return True
    
while True:

    if uart.any():
        b = uart.read(1)

        if not b:
            continue

        c = b[0]


        if c == 10:

            try:
                line = buffer.decode().strip()
            except:
                buffer = bytearray()
                continue

            buffer = bytearray()


            line = "".join(ch for ch in line if 32 <= ord(ch) <= 126)

            if line:

                if parse_packet(line):
                    send_json()


        elif c == 13:
            pass


        elif 32 <= c <= 126:

            buffer.append(c)


        else:
            pass
    
    