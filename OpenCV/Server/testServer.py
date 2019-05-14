import socket
from  matplotlib.pyplot import imsave
import numpy as np

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
print('connected:', addr)

# Создаем картинку полностью белого цвета
img = np.zeros((1500,1500,3), dtype=float)

while True:
    data = conn.recv(8000)
    if not data or data.decode() == '-1 -1 -1':
        break
    # Получаем от клиента коордиаты пикселя
    coordinates = data.decode().split(' ')
    x = int(coordinates[0])
    y = int(coordinates[1])
    z = int(coordinates[2])
    print([x ,y, z])
    #Красим пиксель в черный цвет
    for i in range(img.shape[2]):
        img[y][x][i] = 1.

#Сораняем картинку


imsave('test',img)
# Закрываем соединение
conn.close()

