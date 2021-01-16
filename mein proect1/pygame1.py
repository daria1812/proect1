import pygame
# импорт библиотеки pygame

# импорт модуля random
import random
# инициализация pygame
pygame.init()

# размеры окна
# ширина дисплея
display_width = 900
# высота дисплея
display_height = 800

# параметры дисплея игры
display = pygame.display.set_mode((display_width, display_height))
# надпись на дисплее
pygame.display.set_caption('Новый год')

# загрузка фоновой музыки
pygame.mixer.music.load('snow.mp3')
# громкость фоновой музыки
pygame.mixer.music.set_volume(0.5)


# загрузка звука кнопки
button_sound = pygame.mixer.Sound('button.wav')


# загрузка изображения иконки
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# загрузка изображений препятствий
barrier_img = [pygame.image.load('moros0.png'), pygame.image.load('moros1.png'), pygame.image.load('moros2.png')]
barrier_options = [69, 630, 37, 660, 40, 620]

# загрузка изображений персонажа
alpha_santa_img = [pygame.image.load('ded0.png'), pygame.image.load('ded1.png'), pygame.image.load('ded2.png'),
                   pygame.image.load('ded3.png'), pygame.image.load('ded4.png')]

# счётчик изображений
img_counter = 0


# класс препятствий
class Barrier:
    # инициализация класса
    def __init__(self, x, y, width, image, speed):
        # координата x препятствия
        self.x = x
        # координата y препятствия
        self.y = y
        # ширина препятствия
        self.width = width
        # изображение препятствия
        self.image = image
        # скорость препятствия
        self.speed = speed

    # Функция движения препятствий
    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 100 + random.randrange(-80, 60)
            return False

    # Функция возврата параметров
    def return_self(self, radius, y, width, image):
        # радиус
        self.x = radius
        # координата y
        self.y = y
        # ширина
        self.width = width
        # изображение
        self.image = image
        # прорисовка препятствий
        display.blit(self.image, (self.x, self.y))


# класс кнопки
class Button:
    # инициализация класса
    def __init__(self, width, height):
        # ширина
        self.width = width
        # высота
        self.height = height
        # цвет кнопки, когда курсор не наведён
        self.inactive_color = (13, 162, 58)
        # цвет кнопки, когда курсор наведён
        self.active_color = (23, 204, 58)

    # прорисовка кнопки
    def draw(self, x, y, message, action=None, font_size=30):
        # переменная, которая отражает позицию курсора
        mouse = pygame.mouse.get_pos()
        # получение состояния кнопки на клавиатуре
        click = pygame.mouse.get_pressed()

        # Проверка нахождения курсора по координатам
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            # прорисовываем кнопку
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            # Если пользователь нажал на левую кнопку мыши
            if click[0] == 1:
                # проигрывается звук нажатия кнопки
                pygame.mixer.Sound.play(button_sound)
                # временная задержка
                pygame.time.delay(300)
                # Если левая кнопка мыши не нажата
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        # прорисовка текста на кнопке
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


# ширина персонажа
santa_width = 60
# высота персонажа
santa_height = 100
# координата x персонажа
santa_x = display_width // 3
# координата y персонажа
santa_y = display_height - santa_height - 100

# ширина препятствия
barrier_width = 20
# высота препятствия
barrier_height = 70
# координата x препятствия
barrier_x = display_width - 50
# координата y препятствия
barrier_y = display_height - barrier_height - 100

# обновление кадров игры
clock = pygame.time.Clock()

# переменная, отвечающая за функцию прыжка персонажа
make_jump = False
# счётчик прыжка
jump_counter = 30

# очки
scores = 0
# максимальное количество очков
max_scores = 0
# переменная, которая проверяет находимся ли мы над препятствием
max_above = 0


# Функция меню
def show_menu():
    menu_game = pygame.image.load('mn1.jpg')

    # параметры кнопки начала игры
    start_btn = Button(200, 70)
    # параметры кнопки конца игры
    quit_btn = Button(300, 70)

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # изображения меню игры и кнопок начала и завершения игры
        display.blit(menu_game, (0, 0))
        start_btn.draw(595, 200, 'Начать игру', start_game, 40)
        quit_btn.draw(530, 300, 'Завершить игру', quit_btn, 40)

        # обновление изображения
        pygame.display.update()
        # время на один кадр
        clock.tick(60)


# функция начала игры
def start_game():
    # вводим глобальные переменнные
    global scores, make_jump, jump_counter, santa_y

    # игровой цикл
    while game_cycle():
        # очки
        scores = 0
        # переменная прыжка
        make_jump = False
        # счётчик прыжка
        jump_counter = 30
        # координата y персонажа
        santa_y = display_height - santa_height - 100


# функция игрового цикла
def game_cycle():
    global make_jump

    # музыка играет непрерывно
    pygame.mixer.music.play(-1)

    game = True
    # список массива препятствий
    barrier_arr = []
    create_barrier_arr(barrier_arr)
    # загрузка фона
    land = pygame.image.load('dom1.jpg')

    # параметры кнопки
    button = Button(80, 50)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Если пользователь нажал клавишу пробел
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()
        # Если есть переменная, отвечающая за функцию прыжка, то осуществляется функция прыжка
        if make_jump:
            jump()

        # подсчитывает очки
        count_scores(barrier_arr)

        # прорисовка дисплея фона
        display.blit(land, (0, 0))
        # создание надписи "очки"
        # прорисовка надписи по x и y
        print_text('Очки: ' + str(scores), 800, 100)

        # параметры кнопки "wow"
        button.draw(20, 100, 'wow')

        # прорисовка препятствия
        draw_array(barrier_arr)

        # прорисовка деда Мороза
        draw_santa()

        # Проверяет столкновения
        # Если есть столкновения, то игровой цикл завершается
        if check_collision(barrier_arr):
            pygame.mixer.music.stop()
            game = False

        # обновление дисплея
        pygame.display.update()
        # время на кадр
        clock.tick(80)
    return game_over()


# Функция прыжка
def jump():
    # создаём глобальные переменные
    global santa_y, jump_counter, make_jump
    if jump_counter >= -30:
        santa_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


# массив препятствий
def create_barrier_arr(array):
    # выбираем одно случайное изображение из трёх
    choice = random.randrange(0, 3)
    # загрузка изображения
    img = barrier_img[choice]
    # ширина
    width = barrier_options[choice * 2]
    # высота
    height = barrier_options[choice * 2 + 1]
    array.append(Barrier(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = barrier_options[choice * 2]
    height = barrier_options[choice * 2 + 1]
    array.append(Barrier(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = barrier_options[choice * 2]
    height = barrier_options[choice * 2 + 1]
    array.append(Barrier(display_width + 20, height, width, img, 4))


# прорисовка персонажа
def draw_santa():
    # Создаётся глобальная переменнная
    global img_counter
    if img_counter == 25:
        img_counter = 0

    # прорисовка персонажа на окне
    display.blit(alpha_santa_img[img_counter // 5], (santa_x, santa_y))
    img_counter += 1


# функция поиска радиуса препятствия
def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


# прорисовка массивов
def draw_array(array):
    for barrier in array:
        barrier.move()
        check = barrier.move()
        if not check:
            radius = find_radius(array)

            # выбор случайного изображения
            choice = random.randrange(0, 3)
            # загрузка изображения
            img = barrier_img[choice]
            # ширина
            width = barrier_options[choice * 2]
            # высота
            height = barrier_options[choice * 2 + 1]

            barrier.return_self(radius, height, width, img)


# функция прорисовки текста на экране
def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


#  функция паузы
def pause():
    paused = True

    # музыка на паузе
    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Создание надписи
        print_text('Игра на паузе. Нажмите Enter, чтобы продолжить', 160, 300)

        # Если нажата клавиша Enter
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        # обновление дисплея
        pygame.display.update()
        # время на один кадр
        clock.tick(15)
    # возобновление музыки
    pygame.mixer.music.unpause()


# функция проверки нахождения персонажа в области препятствия
def check_collision(barriers):
    # Если персонаж столкнулся с  первым препятствием
    for barrier in barriers:
        if barrier.y == 630:
            # Если прыжок не сделан
            if not make_jump:
                if barrier.x <= santa_x + santa_width - 50 <= barrier.x + barrier.width:
                    return True
            # Если первая часть прыжка положительна
            elif jump_counter >= 0:
                # Проверяем есть ли столкновения по оси y
                if santa_y + santa_height - 10 >= barrier.y:
                    # Проверяем есть ли столкновения по оси x
                    if barrier.x <= santa_x + santa_width - 50 <= barrier.x + barrier.width:
                        return True
            else:
                if santa_y + santa_height - 5 >= barrier.y:
                    if barrier.x <= santa_x <= barrier.x + barrier.width:
                        return True
        else:
            # Если нет прыжка перед следующими препятствиями
            if not make_jump:
                if barrier.x <= santa_x + santa_width - 5 <= barrier.x + barrier.width:
                    return True
            # Начало прыжка
            elif jump_counter == 10:
                # проверка по координате y персонажа столкновения с препятствием
                if santa_y + santa_height - 5 >= barrier.y:
                    # проверка по координате x персонажа с препятствим
                    if barrier.x <= santa_x + santa_width - 5 <= barrier.x + barrier.width:
                        return True
            # Проверка прыжка до падения вниз
            elif jump_counter >= -1:
                # проверка координаты y персонажа с препятствием
                if santa_y + santa_height - 10 >= barrier.y:
                    # проверка координаты x персонажа с препятствием
                    if barrier.x <= santa_x + santa_width - 35 <= barrier.x + barrier.width:
                        return True
                else:
                    # Сверяем координаты y персонажа и препятствия
                    if santa_y + santa_height - 5 >= barrier.y:
                        # Сверяем координаты x персонажа и препятствия
                        if barrier.x <= santa_x + 5 <= barrier.x + barrier.width:
                            return True
    # Если условия не выполнились
    return False


# Функция посчёта очков
def count_scores(barriers):
    # создаём глобальные переменные
    global scores, max_above
    above_barrier = 0

    # проверка прыжка персонажа
    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if santa_y + santa_height - 5 <= barrier.y:
                if barrier.x <= santa_x <= barrier.x + barrier.width:
                    above_barrier += 1
                elif barrier.x <= santa_x + santa_width <= barrier.x + barrier.width:
                    above_barrier += 1

        max_above = max(max_above, above_barrier)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


# функция завершения игры
def game_over():
    # создаём глобальные переменнные
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Создание надписи
        # Создание параметров надписи
        print_text('Игра завершена. Нажмите клавишу Enter - сыграть, Esc - выход', 80, 300)
        # Создание надписи
        # Создание параметров надписи
        print_text('рекорд: ' + str(max_scores), 300, 350)

        # если нажата клавиша Enter
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        # если нажата клавиша пробел
        if keys[pygame.K_ESCAPE]:
            return False

        # обновление дисплея
        pygame.display.update()
        # показывает время на кадр
        clock.tick(15)


# функция меню
show_menu()
# завершение игры
pygame.quit()
quit()