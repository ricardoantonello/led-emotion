
# coding: utf-8
# Autor: Ricardo Antonello 
# Site: cv.antonello.com.br
# E-mail: ricardo@antonello.com.br

# import the necessary packages
import serial # para comunicação com arduino

#Adaptado do exemplo da Intel OpenVino chamado 
"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import time
import cv2

from argparse import ArgumentParser
from inference import Network

# Definições globais
s = serial.Serial('/dev/ttyACM0', 9600) # iniciar a serial faz o arduino resetar
time.sleep(3) # é preciso esperar o arduino voltar o reset

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default='CAM', help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", type=str,
                        default='libcpu_extension_sse4.so',
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.6,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    parser.add_argument("-pc", "--perf_counts", type=str, default=False,
                        help="Print performance counters")
    return parser


def performance_counts(perf_count):
    """
    print information about layers of the model.

    :param perf_count: Dictionary consists of status of the layers.
    :return: None
    """
    print("{:<70} {:<15} {:<15} {:<15} {:<10}".format('name', 'layer_type',
                                                      'exec_type', 'status',
                                                      'real_time, us'))
    for layer, stats in perf_count.items():
        print("{:<70} {:<15} {:<15} {:<15} {:<10}".format(layer,
                                                          stats['layer_type'],
                                                          stats['exec_type'],
                                                          stats['status'],
                                                          stats['real_time']))

def ssd_maior_rosto(frame, result):
    primeiro = 1
    prob_temp = 0
    for obj in result[0][0]:
        # Draw bounding box for object when it's probability is more than
        #  the specified threshold
        if obj[2] > prob_threshold and (primeiro == 1 or obj[2]>prob_temp):
            primeiro = 0
            xmin = int(obj[3] * initial_w)
            ymin = int(obj[4] * initial_h)
            xmax = int(obj[5] * initial_w)
            ymax = int(obj[6] * initial_h)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 55, 255), 1)
        prob_temp = obj[2] # será probabilidade anterior
    if primeiro == 0:    
        return frame[ymin:ymax, xmin:xmax]
    else:
        return frame



def ssd_out(frame, result):
    """
    Parse SSD output.

    :param frame: frame from camera/video
    :param result: list contains the data to parse ssd
    :return: person count and frame
    """
    current_count = 0
    for obj in result[0][0]:
        # Draw bounding box for object when it's probability is more than
        #  the specified threshold
        if obj[2] > prob_threshold:
            xmin = int(obj[3] * initial_w)
            ymin = int(obj[4] * initial_h)
            xmax = int(obj[5] * initial_w)
            ymax = int(obj[6] * initial_h)
            #cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 55, 255), 1)
            current_count = current_count + 1
    return frame, current_count


def main():
    """
    Load the network and parse the SSD output.

    :return: None
    """
    args = build_argparser().parse_args()
    duration = 0
    total_count = 0

    # Flag for the input image
    single_image_mode = False

    cur_request_id1 = 0
    cur_request_id2 = 0
    last_count = 0
    total_count = 0
    start_time = 0

    # Initialise the class
    infer_network1 = Network()
    infer_network2 = Network()
    
    # Load the network to IE plugin to get shape of input layer
    n1, c1, h1, w1 = infer_network1.load_model('face-detection-adas-0001.xml', args.device, 1, 1,
                                          cur_request_id1, args.cpu_extension)[1]
    n2, c2, h2, w2 = infer_network2.load_model('emotions-recognition-retail-0003.xml', args.device, 1, 1,
                                          cur_request_id2, args.cpu_extension)[1]

    # Checks for live feed
    if args.input == 'CAM':
        input_stream = 0

    # Checks for input image
    elif args.input.endswith('.jpg') or args.input.endswith('.bmp') :
        single_image_mode = True
        input_stream = args.input

    # Checks for video file
    else:
        input_stream = args.input
        assert os.path.isfile(args.input), "Specified input file doesn't exist"

    cap = cv2.VideoCapture(input_stream)

    if input_stream:
        cap.open(args.input)

    if not cap.isOpened():
        log.error("ERROR! Unable to open video source")
    global initial_w, initial_h, prob_threshold
    prob_threshold = args.prob_threshold
    initial_w = cap.get(3)
    initial_h = cap.get(4)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)
        # Start async inference
        image = cv2.resize(frame, (w1, h1))
        # Change data layout from HWC to CHW
        image = image.transpose((2, 0, 1))
        image = image.reshape((n1, c1, h1, w1))
                
        # Start asynchronous inference for specified request.
        inf_start = time.time()
        infer_network1.exec_net(cur_request_id1, image)
        # Wait for the result
        if infer_network1.wait(cur_request_id1) == 0:
            # Results of the output layer of the network
            result1 = infer_network1.get_output(cur_request_id1)
            if args.perf_counts:
                perf_count = infer_network1.performance_counter(cur_request_id1)
                performance_counts(perf_count)

            frame, current_count = ssd_out(frame, result1)
            maior_rosto = ssd_maior_rosto(frame,result1)
            #cv2.imshow('Frame111',maior_rosto)
            maior_rosto = cv2.resize(maior_rosto, (w2, h2))
            # Change data layout from HWC to CHW
            maior_rosto = maior_rosto.transpose((2, 0, 1))
            maior_rosto = maior_rosto.reshape((n2, c2, h2, w2))
            infer_network2.exec_net(cur_request_id2, maior_rosto)
   
            if infer_network2.wait(cur_request_id2) == 0:
                det_time = time.time() - inf_start # so lê tempo depois que rodou as duas redes
                r2 = infer_network2.get_output(cur_request_id2)
                #print('result 2', r2)
                    
            
                inf_time_message = "Tempo de processamento: {:.3f}ms"\
                               .format(det_time * 1000) # inference time
                cv2.putText(frame, inf_time_message, (15, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                
                if r2[0][0][0][0]>0.6:
                    cv2.putText(frame, 'Normal', (15, 115), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 3)
                elif r2[0][1][0][0]>0.6:
                    cv2.putText(frame, 'Feliz', (15, 115), cv2.FONT_HERSHEY_PLAIN, 7.5, (0, 255, 0), 3)
                    resp = s.write(str(1).encode())
                    s.flush()
                elif r2[0][2][0][0]>0.6:
                    cv2.putText(frame, 'Triste', (15, 115), cv2.FONT_HERSHEY_PLAIN, 7.5, (0, 255, 0), 3)
                    resp = s.write(str(2).encode())
                    s.flush()
                elif r2[0][3][0][0]>0.6:
                    cv2.putText(frame, 'Surpreso', (15, 115), cv2.FONT_HERSHEY_PLAIN, 7.5, (0, 255, 0), 3)
                    resp = s.write(str(3).encode())
                    s.flush()
                elif r2[0][4][0][0]>0.6:
                    cv2.putText(frame, 'Bravo', (15, 115), cv2.FONT_HERSHEY_PLAIN, 7.5, (0, 255, 0), 3)
                    resp = s.write(str(4).encode())
                    s.flush()
                else:
                    resp = s.write(str(0).encode())
					#print('Resposta:',resp)
                    s.flush()

                    
                #cv2.putText(frame, 'Normal: '+str(r2[0][0][0][0]), (15, 35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                #cv2.putText(frame, 'Feliz: '+str(r2[0][1][0][0]), (15, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                #cv2.putText(frame, 'Triste: '+str(r2[0][2][0][0]), (15, 75), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                #cv2.putText(frame, 'Surpreso: '+str(r2[0][3][0][0]), (15, 95), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                #cv2.putText(frame, 'Bravo: '+str(r2[0][4][0][0]), (15, 115), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
                
            # When new person enters the video
            #if current_count > last_count:
            #    start_time = time.time()
            #    total_count = total_count + current_count - last_count
            #if total_count:
            #    cv2.putText(frame, 'Contagem: '+str(total_count), (15, 35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)

            # Person duration in the video is calculated
            #if current_count < last_count:
            #    duration = int(time.time() - start_time)
            #if duration:
            #    cv2.putText(frame, 'Duracao: '+str(duration), (15, 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)

            #last_count = current_count

            if key_pressed == 27:
                break
		
        cv2.imshow('Frame',frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
          
        if single_image_mode:
            cv2.imwrite('output_image.jpg', frame)
            
    cap.release()
    cv2.destroyAllWindows()
    infer_network1.clean()
    infer_network2.clean()
    s.close() #fecha serial


if __name__ == '__main__':
    main()
    exit(0)
