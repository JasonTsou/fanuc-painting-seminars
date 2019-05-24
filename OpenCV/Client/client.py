import socket
import numpy as np
import cv2
import argparse
import time

start = time.time()

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


ap = argparse.ArgumentParser()
ap.add_argument('image_path', type=str, help='Enter image path(only ASCII symbols)')
args = ap.parse_args()

image = cv2.imread(args.image_path)
if image is not None:

    # доска 118*88 см
    board_width = 1000
    board_height = 800
    width = image.shape[1]
    height = image.shape[0]
    if width > board_width:
        scale_percent = board_width/width
        width = int(width * scale_percent)
        height = int(height * scale_percent)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    if height > board_height:
        scale_percent = board_height / height
        width = int(width * scale_percent)
        height = int(height * scale_percent)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    auto = auto_canny(blurred)
    ret, thresh = cv2.threshold(auto, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.imwrite("Client/auto.png", auto)
    print(time.time() - start)
else:
    print('Incorrect path(only ASCII symbols)')




print(len(contours[0]))


# if(contours is not None):
#     print("Подключились")
#     # Подключаемся к серверу
#     sock = socket.socket()
#
#     sock.connect(('192.168.31.150', 59002))
#     speed = 100
#     x = 100
#     y = 100
#     for i in range(len(contours)):
#         z = -20
#         string = '1 ' + str(x+100) + ' ' + str(y+100) + ' ' + str(z) + ' ' + str(speed) + ' 0'
#         sock.send(string.encode('utf-8'))
#         y = contours[i][0][0][0]
#         x = contours[i][0][0][1]
#         print(x)
#         print(y)
#         string = '1 ' + str(x+100) + ' ' + str(y+100) + ' ' + str(z) + ' ' + str(speed) + ' 0'
#         sock.send(string.encode('utf-8'))
#         z = -40
#         for j in range(len(contours[i])):
#             y = contours[i][j][0][0]
#             x = contours[i][j][0][1]
#             string = '1 ' + str(x+100) + ' ' + str(y+100) + ' ' + str(z) + ' ' + str(speed) + ' 0'
#             sock.send(string.encode('utf-8'))
#             time.sleep(0.01)
#             print(sock.recv(1024))
#     z = -20
#     string = '1 ' + str(x + 100) + ' ' + str(y + 100) + ' ' + str(z) + ' ' + str(speed) + ' 0'
#     x = 100
#     y = 100
#     string = '1 ' + str(x + 100) + ' ' + str(y + 100) + ' ' + str(z) + ' ' + str(speed) + ' 0'
#     sock.close()


# if(contours is not None):
#     print("Подключились")
#     # Подключаемся к серверу
#     sock = socket.socket()
#     sock.connect(('localhost', 9090))
#     for i in range(len(contours)):
#         z = -57
#         speed = 100
#         for coor in contours[i]:
#             x = coor[0][0]
#             y = coor[0][1]
#             string = str(y) + ' ' + str(x) + ' ' + str(z)
#             sock.send(string.encode('utf-8'))
#             time.sleep(0.001)
#     sock.close()

