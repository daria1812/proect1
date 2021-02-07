import pygame
import requests
import os
import sys

a = 39.1412006
b = 53.244008
zoom = 0.002
type = 'map'


def load_map():
    global a, b, zoom, type
    map_request = "http://static-maps.yandex.ru/1.x/?ll={}&spn={}&l={}".format(str(a) + ',' + str(b),
                                                                               str(zoom) + ',' + str(zoom), type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def update(event):
    global zoom, a, b
    if event.key == 1073741899 and zoom < 1:
        zoom += 0.001
    elif event.key == 1073741902 and zoom > 0.001:
        zoom -= 0.001
    elif event.key == 1073741904:
        a -= 0.001
    elif event.key == 1073741903:
        a += 0.001
    elif event.key == 1073741906:
        b += 0.001
    elif event.key == 1073741905:
        b -= 0.001


pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = load_map()
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYUP:
        update(event)
        map_file = load_map()
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
