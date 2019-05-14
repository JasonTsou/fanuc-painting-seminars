import socket
import cv2
import numpy as np

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
print('connected:', addr)

# Создаем картинку полностью белого цвета
img = np.array((2048,2048,3))

while True:
    data = conn.recv(1024)
    if not data or data.decode() == '-1 -1 -1':
        break
    # Получаем от клиента коордиаты пикселя
    coordinates = data.decode().split(' ')
    x = int(coordinates[0])
    y = int(coordinates[1])
    z = int(coordinates[2])
    print([x ,y, z])
    #Красим пиксель в черный цвет
    img[x][y] = [255, 255, 255]

# #Сораняем картинку
print(img[50][52])
# cv2.imwrite('C:\\Users\\Alexander\\PycharmProjects\\Robot\\Server\\test.png',img)
# # Закрываем соединение
# conn.close()

