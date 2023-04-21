import serial
import time

arduino = serial.Serial()
arduino.baudrate = 9600
arduino.port = "COM4"
arduino.open()


def write_read():
    data = arduino.readline().decode()
    print(data)


while True:
    packet = arduino.readline()
    print(int(packet.decode("utf")))
