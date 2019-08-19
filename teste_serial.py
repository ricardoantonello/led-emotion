# coding: utf-8
# Autor: Ricardo Antonello 
# Site: cv.antonello.com.br
# E-mail: ricardo@antonello.com.br

# import the necessary packages
import serial
import time

# Definições globais
s = serial.Serial('/dev/ttyACM0', 9600) # iniciar a serial faz o arduino resetar
time.sleep(3) # é preciso esperar o arduino voltar o reset
for i in range(1000):
	resp = s.write(str(i%5).encode())
	print('Resposta:',resp)
	s.flush()
	time.sleep(1)
s.close()

