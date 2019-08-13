# Led Emotion / Emoções em LED  
Analisa a imagem com um Jetson Nano e comunica com um Arduíno para expressar uma cor na fita de leds para cada emoção (alegria, tristesa, raiva, etc)  

## Lições aprendidas  
Após iniciar uma porta serial via python o arduíno reseta e é preciso esperar voltar para enviar mensagens via serial.  

## Instruções Python no PC  
pip3 install pyserial  #pyserial funciona fora do raspberry e roda em windows, linux, etc.  

### Resumo do código em Python  
import serial  
s = serial.Serial('/dev/ttyACM0', 9600) # iniciar a serial faz o arduino resetar  
time.sleep(3) # é preciso esperar o arduino voltar o reset  
resp = s.write(str(i%5).encode())  
s.flush()  
s.close()  

### Resumo do código em Arduíno   
int comando_serial=0;  
Serial.begin(9600);  
Serial.setTimeout(1); // em milis, fundamental para nao atrasar o Serial.parseInt()  
pinMode(LED_BUILTIN, OUTPUT);  
// Leitura da Serial  
if (Serial.available() > 0) {  
  digitalWrite(LED_BUILTIN, HIGH); //liga led  
  comando_serial = Serial.parseInt();  
}  
if(comando_serial==0){  
  ...  
}else if(comando_serial==1){  
  ...  
}else {  
  Serial.print("ERRO: comando serial desconhecido! Recebido: ");   
  Serial.println(comando_serial);   
}  
