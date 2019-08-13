# coding: utf-8
# Autor: Ricardo Antonello 
# Site: cv.antonello.com.br
# E-mail: ricardo@antonello.com.br

# import the necessary packages
import serial
import time

# Definições globais
ser = serial.Serial('/dev/ttyACM0', 9600)

ser.write(str('3').encode())
ser.flush()
