import cv2
import socket
import numpy as np
import threading
import time

# address = ('127.0.0.1', 10001)
address = ('', 10001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(5)
print('Waiting for connection...')


def tcp_link(sock, addr, num=0):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!'.encode())

    while True:
        try:
            uav_id = int(sock.recv(1).decode())
            if uav_id == 'e':
                sock.close()
                print('The task of %s:%s has been finished.' % addr)
                break
            t_ms = int(sock.recv(8).decode())
            pos_ori = []
            for _ in range(7):
                v = int(sock.recv(8).decode()) / 1000
                pos_ori.append(v)

            data_len = int(sock.recv(7).decode())
            data = b''
            buf_len = data_len
            while data_len > 0:
                sp_data = sock.recv(buf_len)
                data += sp_data
                data_len -= len(sp_data)
            img = cv2.imdecode(np.frombuffer(data, dtype='uint8'), cv2.IMREAD_COLOR)
            # print(uav_id, t_ms, pos_ori)
            print('uav_id:%s, timestamp:%s, img_shape:%s, pos:%s, ori:%s' % (uav_id, t_ms, img.shape, pos_ori[:3], pos_ori[3:]))
            cv2.imshow('video' + str(num), img)
            cv2.waitKey(1)
            if cv2.waitKey(50) & 0xFF == ord(str(num)):
                raise Exception('Keyboard break')

            data = b''
            for v in [1023.23, -342.39, 101.01]:
                if v < 0:
                    val = '-' + str(int(-v * 1000)).zfill(7)
                else:
                    val = str(int(v * 1000)).zfill(8)
                data += val.encode()
            sock.sendall(data)
        except:
            sock.close()
            print('The task of %s:%s has been finished.' % addr)
            break



num = 0
while True:
    sock, addr = s.accept()
    num += 1
    t = threading.Thread(target=tcp_link, args=(sock, addr, num))
    t.start()