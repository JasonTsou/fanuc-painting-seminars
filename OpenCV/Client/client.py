import socket
import numpy as np
from  matplotlib.pyplot import imread

def isNotWhite(img,x,y):
    isNotWhite = False
    for i in range(3):
        if(img[x][y][i] != 1.):
            isNotWhite = True
            break
    return isNotWhite

def NeighbourPixel(sock,img,x,y,z):

    if img.shape[2] == 3:
        img[x][y] = [1., 1., 1.]
    elif img.shape[2] == 4:
        img[x][y] = [1., 1., 1., 1.]

    if(isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x,y+1,z)
    elif(isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x+1,y+1,z)
    elif(isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x+1,y,z)
    elif (isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x+1,y-1,z)
    elif (isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x,y-1,z)
    elif (isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x-1,y-1,z)
    elif (isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x-1,y,z)
    elif (isNotWhite(img,x,y)):
        img = NeighbourPixel(sock,img,x-1,y+1,z)
    coordinates = str(x) + ' ' + str(y) + ' ' + str(z)
    sock.send(coordinates.encode('utf-8'))
    print(img[x][y])
    return img

# Загружаем исходную картинку
img = imread("test3.png")

# Подключаемся к серверу
sock = socket.socket()
sock.connect(('localhost', 9090))

# В тестовой программе z не учитывается поэтому приравняем ее 0
z = 0

# Цикл по всем пикселям изображения
for x in range(img.shape[0]):
    for y in range(img.shape[1]):
        # Если цвет пикселя отлчаеться от белого преобразуем координаты в строку
        # и передаем на сервер
        if(isNotWhite(img,x,y)):
            img = NeighbourPixel(sock,img,x,y,z)



# Отправляем строку '-1 -1 -1' , чтобы
# сказать серверу что передача данных закончилась
sock.send('-1 -1 -1'.encode('utf-8'))

# Закрываем соединение
data = sock.recv(1024)
sock.close()



