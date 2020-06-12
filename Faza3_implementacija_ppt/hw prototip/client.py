import socket
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
TCP_IP = '192.168.0.32' # IP adresa racunara
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket()
s.connect((TCP_IP, TCP_PORT))

while True:
    data = s.recv(BUFFER_SIZE)
    if data != b'READ_CARD': break
    id, text = reader.read()
    print("ID: ", id)
    s.send(str(id).encode('utf-8'))
    print("ID sent succesfully...")
    data = s.recv(BUFFER_SIZE)
    print("Received data: ", data)

s.close()
GPIO.cleanup()