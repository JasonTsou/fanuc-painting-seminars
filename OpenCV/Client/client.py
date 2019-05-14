# import socket
# import numpy as np
# from  matplotlib.pyplot import imread
#
# def isNotWhite(img,x,y):
#     isNotWhite = False
#     for i in range(3):
#         if(img[x][y][i] != 1.):
#             isNotWhite = True
#             break
#     return isNotWhite
#
# def NeighbourPixel(sock,img,x,y,z):
#
#     if img.shape[2] == 3:
#         img[x][y] = [1., 1., 1.]
#     elif img.shape[2] == 4:
#         img[x][y] = [1., 1., 1., 1.]
#
#     if(isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x,y+1,z)
#     elif(isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x+1,y+1,z)
#     elif(isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x+1,y,z)
#     elif (isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x+1,y-1,z)
#     elif (isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x,y-1,z)
#     elif (isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x-1,y-1,z)
#     elif (isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x-1,y,z)
#     elif (isNotWhite(img,x,y)):
#         img = NeighbourPixel(sock,img,x-1,y+1,z)
#     coordinates = str(x) + ' ' + str(y) + ' ' + str(z)
#     sock.send(coordinates.encode('utf-8'))
#     print(img[x][y])
#     return img
#
# # Загружаем исходную картинку
# img = imread("test3.png")
#
# # Подключаемся к серверу
# sock = socket.socket()
# sock.connect(('localhost', 9090))
#
# # В тестовой программе z не учитывается поэтому приравняем ее 0
# z = 0
#
# # Цикл по всем пикселям изображения
# for x in range(img.shape[0]):
#     for y in range(img.shape[1]):
#         # Если цвет пикселя отлчаеться от белого преобразуем координаты в строку
#         # и передаем на сервер
#         if(isNotWhite(img,x,y)):
#             img = NeighbourPixel(sock,img,x,y,z)
#
#
#
# # Отправляем строку '-1 -1 -1' , чтобы
# # сказать серверу что передача данных закончилась
# sock.send('-1 -1 -1'.encode('utf-8'))
#
# # Закрываем соединение
# data = sock.recv(1024)
# sock.close()
#
#

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
    board_width = 1080
    board_height = 830
    width = image.shape[1]
    height = image.shape[0]
    if width > board_width:
        width_percent = int(width * (width / board_width))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    auto = auto_canny(blurred)
    indices = np.where(auto != [0])  # поиск координат белых пикселей
    coordinates = set(zip(indices[1], indices[0]))
    length = len(coordinates)
    print(length)
    edges = [[]]
    i = coordinates.pop()
    coordinates.add(i)
    k = 0
    while k < length:  # k - счетчик, который проверяет все ли белые точки были отнесены к какой-либо грани
        if i in coordinates:
            edges[len(edges) - 1].append(i)     # добовляем в edges точку и убираем ее из coordinates
            coordinates.remove(i)
            k += 1
            for t in range(-1, 2):  # проверяем все точки вокруг i
                for u in range(-1, 2):
                    if((t != 0) or (u != 0)) and ((i[0] + t, i[1] + u) in coordinates):
                        i = (i[0] + t, i[1] + u)
                        break
        else:
            edges.append([])  # если новых белых точек вокруг i не нашлось, то отмечаем конец кривой как (-1,-1)
            i = coordinates.pop()
            edges[len(edges) - 1].append(i)
            k += 1
            for t in range(-1, 2):
                for u in range(-1, 2):
                    if ((t != 0) or (u != 0)) and ((i[0] + t, i[1] + u) in coordinates):
                        i = (i[0] + t, i[1] + u)
                        break
    cv2.imwrite("Client/auto.png", auto)
    print(time.time() - start)
else:
    print('Incorrect path(only ASCII symbols)')



if(edges is not None):
    print("Подключились")
    # Подключаемся к серверу
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    for contr in edges:
        z = 0
        for coor in contr:
            x = coor[0]
            y = coor[1]
            coordinates = str(x) + ' ' + str(y) + ' ' + str(z)
            sock.send(coordinates.encode('utf-8'))
    sock.send('-1 -1 -1'.encode('utf-8'))