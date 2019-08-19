# Led Emotion / Emoções em LED  
Analisa a imagem com um Jetson Nano e comunica com um Arduíno para expressar uma cor na fita de leds para cada emoção (alegria, tristesa, raiva, etc)  

# Comunicação Serial PC <-> Arduino  
## Lições aprendidas  
Após iniciar uma porta serial via python o arduíno reseta e é preciso esperar voltar para enviar mensagens via serial.  

## Instruções Python no PC  
pip3 install pyserial  #pyserial funciona fora do raspberry e roda em windows, linux, etc.  
Openvino: É preciso instalar o OpenVino da Intel  

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

# Reconhecimento Facial de Emoções / Emotion Detection  
Fonte: https://towardsdatascience.com/face-detection-recognition-and-emotion-detection-in-8-lines-of-code-b2ce32d4d5de  

   
# Anotações OPENVINO  
Redes no formato openvino otimizadas tem um .bin e um .xml e também o .labels e .mapping?  
  
Exemplo rodando em python:   
python3 classification_sample.py   
	--model squeezenet1.1.xml   
	--input /opt/intel/openvino/deployment_tools/demo/car.png   
	--labels squeezenet1.1.labels  
  
Exemplo de Emoções: https://docs.openvinotoolkit.org/2018_R5/_samples_interactive_face_detection_demo_README.html  
  
Redes:  
face-detection-adas-0001 (para achar as faces)  
emotions-recognition-retail-0003 (para emoções)  
  
Dataset com imagens para emoções:  
http://mohammadmahoor.com/affectnet/  
  
Dentro da pasta ~/people-counter-python  
python3 main2.py -i CAM -m face-detection-adas-0001.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24  
  
Formato da saída da rede de emoções:  
[[[[0.54978   ]]  
  [[0.00465726]]  
  [[0.16230458]]  
  [[0.00669729]]  
  [[0.27656084]]]]  


