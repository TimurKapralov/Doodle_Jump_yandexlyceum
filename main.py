import random
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pygame

conn = sqlite3.connect('data/data_us')
cursor = conn.cursor()


class Button:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (125, 62))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def game_over_screen(current_score, max_score):
    lose = pygame.mixer.music.load('data/lose.mp3')

    if max_score > int(cursor.execute("SELECT * FROM scores WHERE username=?",
                                      (username,)).fetchall()[0][1]):
        cursor.execute("UPDATE scores SET max_score=? WHERE username=?", (max_score, username))
        conn.commit()
    pygame.mixer.music.play(1)
    game_over_image = pygame.image.load("data/game over-PhotoRoom.png-PhotoRoom.png")
    screen = pygame.display.set_mode((530, 750))
    background_finish = pygame.image.load("data/fon2.jpg")
    screen.blit(background_finish, (0, 0))
    width = screen.get_width()
    height = screen.get_height()
    screen.blit(game_over_image, (100, 200))  # Display at the bottom

    # Счёт под конец игры и максимальный счёт
    font = pygame.font.Font(None, 46)
    score_text = font.render(f"Score: {current_score}", True, (0, 0, 0))
    max_score_text = font.render(f"Max Score: {max_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, height - game_over_image.get_height() - 40))
    screen.blit(max_score_text, (10, height - game_over_image.get_height() - 70))

    # "Click space to run" сообщение
    restart_text = font.render("Click space to run", True, (0, 0, 0))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2))

    back_to_main_text = font.render("Click esc to menu", True, (0, 0, 0))
    screen.blit(back_to_main_text, ((width // 2 - restart_text.get_width() // 2, height // 2 + 20)))

    pygame.display.flip()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                return False  # конец
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False
                if event.key == pygame.K_ESCAPE:
                    init_main()

    return True  # рестарт


def get_new_name():
    global root, combo_box, username
    new_name = name_entry.get()
    if cursor.execute("SELECT username FROM scores").fetchall():
        cur = combo_box.get()
    if new_name:
        username = new_name
        namers = list(el[0] for el in cursor.execute("SELECT username FROM scores").fetchall())
        print(namers)
        if username in namers:
            tk.messagebox.showinfo("Внимание", f"Данное имя уже зарегистрировано. Введите новое!😀")
            pygame.quit()
            conn.close()
            quit()
        else:
            print(0)
            cursor.execute("INSERT INTO scores VALUES(?, ?)", (username, 0))
            conn.commit()

        combo_box['values'] = cursor.execute("SELECT username FROM scores").fetchall()
        combo_box.current(0)
    else:
        username = cur
    root.destroy()


def clear_text_entry_tk():
    name_entry.delete(0, len(name_entry.get()))


def to_game():
    global name_entry, combo_box, root
    root = tk.Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.title('Выберите пользователя:')

    button = tk.Button(root, text="Подтвердить", command=get_new_name)
    names = cursor.execute("SELECT username FROM scores").fetchall()
    if names:
        combo_box = ttk.Combobox(root, values=names,
                                 state='readonly', postcommand=clear_text_entry_tk)
    try:
        combo_box.current(0)
    except tk.TclError:
        pass

    label1 = tk.Label(root, text="ИЛИ")
    label2 = tk.Label(root, text='Введите новое имя пользователя:')
    combo_label = tk.Label(root, text="Выберите пользователя:")

    name_entry = tk.Entry(root)
    combo_label.pack()
    if names:
        combo_box.pack()
    label1.pack()
    label2.pack()
    name_entry.pack()
    button.pack()
    root.mainloop()


def save_user_data(username, score):
    cursor.execute("UPDATE scores SET max_score = ? WHERE username = ?",
                   (score, username))
    conn.commit()


def load_user_data():
    global username
    outy = cursor.execute("SELECT username, max_score FROM scores WHERE username=?",
                          (username,)).fetchall()
    return outy[0][0], int(outy[0][1])


def loop_game():
    game_over_y = 1000
    score_y = 1000
    max_score_y = 1000

    def create_platform(x, y):
        platform = pygame.sprite.Sprite(platform_sprites)
        platform.image = platform_main
        platform.rect = platform.image.get_rect()

        if x == -1:
            x = random.randint(minX, maxX)
        platform.rect.x = x
        platform.rect.y = y

        return platform

    def gen_direction(level):
        if level == 1:
            return 0
        return random.randint(1, 2)

    def doodler_init():
        doodler = pygame.sprite.Sprite(doodler_sprites)
        rnd = random.randint(0, 1)
        if rnd == 0:
            doodler.image = doodler_right
        else:
            doodler.image = doodler_left
        doodler.rect = doodler.image.get_rect()
        doodler.rect.x = doodlerX
        doodler.rect.y = doodlerY
        return doodler

    def platforms_init():
        platforms = []
        directions = []
        platform = create_platform(doodlerX, minY)
        platforms.append(platform)
        directions.append(0)
        for i in range(1, platform_count):
            platformY = minY - i * deltaY
            platform = create_platform(-1, platformY)
            platforms.append(platform)
            directions.append(gen_direction(1))
        return platforms, directions

    pygame.init()
    mus = random.randint(1, 2)
    if mus == 1:
        music = pygame.mixer.music.load("data/Doodlemusic.mp3")
    else:
        music = pygame.mixer.music.load("data/SUBWAY SURFERS.mp3")

    pygame.mixer.music.play(-1)
    res = (530, 750)
    screen = pygame.display.set_mode(res)

    width = screen.get_width()
    height = screen.get_height()

    doodlerRightImage = "data/doodler.png"
    doodlerLeftImage = "data/doodler1.png"
    springImage = "data/spring.png"
    back = random.randint(1, 3)
    if back == 1:
        backgroundImage = "data/fon2.jpg"
    elif back == 2:
        backgroundImage = "data/Fonfutboll.jpg"
    else:
        backgroundImage = "data/SnowFon.jpg"
    plat = random.randint(1, 2)
    if plat == 1:
        platformImage = "data/Платформа.png"
    else:
        platformImage = "data/Платформа1.png"

    doodler_right = pygame.image.load(doodlerLeftImage)
    doodler_left = pygame.image.load(doodlerRightImage)
    background = pygame.image.load(backgroundImage)
    platform_main = pygame.image.load(platformImage)
    spring_image = pygame.image.load(springImage)

    doodlerX = 300
    doodlerY = 530

    minX = 20
    maxX = width - 100

    platform_count = 4
    stepX = 5
    stepY = 15
    deltaY = 250
    minY = 600
    maxY = minY - (platform_count - 1) * deltaY

    clock = pygame.time.Clock()
    fps = 20
    speed = 20

    maxVelY = 30
    stepVelY = 4

    background = pygame.transform.scale(background, (530, 750))
    doodler_sprites = pygame.sprite.Group()
    platform_sprites = pygame.sprite.Group()

    doodler = doodler_init()
    platforms, directions = platforms_init()

    font = pygame.font.Font(None, 36)

    vel_y = maxVelY
    flag = False
    counter = 0
    maxScore = 0
    level = 1

    level2Limit = 4000

    while True:
        screen.blit(background, (0, 0))
        username, maxScore = load_user_data()

        text1 = font.render(f'score = {counter}', 1, (0, 0, 0))
        text2 = font.render(f'previous_max_score = {maxScore}', 1, (0, 0, 0))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))

        doodler_sprites.draw(screen)
        platform_sprites.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()

        if doodler.rect.y > height:
            # maxScore
            current_score = counter
            maxScore = max(maxScore, current_score)
            save_user_data(username, maxScore)
            screen.blit(background, (0, 0))
            if game_over_screen(current_score, maxScore):
                doodler.rect.y = doodlerY
                counter = 0
                level = 1
                vel_y = maxVelY
                doodler.kill()
                for i in range(platform_count):
                    platforms[i].kill()
                doodler = doodler_init()
                platforms, directions = platforms_init()
                mus = random.randint(1, 2)
                if mus == 1:
                    music = pygame.mixer.music.load("data/Doodlemusic.mp3")
                else:
                    music = pygame.mixer.music.load("data/SUBWAY SURFERS.mp3")
                pygame.mixer.music.play(-1)

        if counter >= level2Limit:
            level = 2
        else:
            level = 1

        doodler.rect.y -= vel_y
        vel_y -= stepVelY

        for i in range(platform_count):
            if directions[i] != 0:
                if platforms[i].rect.x <= minX:
                    directions[i] = 2
                if platforms[i].rect.x >= maxX:
                    directions[i] = 1
                if directions[i] == 2:
                    platforms[i].rect.x += stepX
                else:
                    platforms[i].rect.x -= stepX

        if flag == True:
            for i in range(platform_count):
                platforms[i].rect.y += stepY
            counter += stepY

        if platforms[0].rect.y >= minY + deltaY:
            flag = False
            platforms[0].kill()
            for i in range(1, platform_count):
                platforms[i - 1] = platforms[i]
                directions[i - 1] = directions[i]
            platforms[platform_count - 1] = create_platform(-1, maxY)
            directions[platform_count - 1] = gen_direction(level)

        if vel_y < 0 and pygame.sprite.spritecollideany(doodler, platform_sprites):
            vel_y = maxVelY
            if platforms[0].rect.y + stepY >= minY:
                flag = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            doodler.rect.x -= speed
            doodler.image = doodler_right
        elif keys[pygame.K_RIGHT]:
            doodler.rect.x += speed
            doodler.image = doodler_left

        if doodler.rect.x > width:
            doodler.rect.x = 0
        if doodler.rect.x < 0:
            doodler.rect.x = width

        pygame.display.update()
        clock.tick(fps)


to_game()


def init_main():
    pygame.init()
    res = (530, 750)

    black = (0, 0, 0)

    mus = random.randint(1, 2)
    if mus == 1:
        music = pygame.mixer.music.load("data/Doodlemusic.mp3")
    else:
        music = pygame.mixer.music.load("data/SUBWAY SURFERS.mp3")

    background_start = pygame.image.load("data/fon.jpg")
    background_start = pygame.transform.scale(background_start, res)

    background_finish = pygame.image.load("data/fon2.jpg")
    background_finish = pygame.transform.scale(background_finish, res)

    all_sprites = pygame.sprite.Group()
    spring_sprites = pygame.sprite.Group()
    doodler = pygame.sprite.Sprite(all_sprites)
    doodler.image = pygame.image.load("data/doodler.png")
    doodler.rect = doodler.image.get_rect()

    doodler.rect.x = 90
    doodler.rect.y = 510
    vel_y = 40

    clock = pygame.time.Clock()
    fps = 25

    try:
        pre_text = cursor.execute("SELECT username, max_score FROM scores ORDER BY max_score DESC").fetchall()[0]
    except IndexError:
        tk.messagebox.showinfo("Внимание", f"Вам необходимо ввести имя пользователя!😀")
        pygame.quit()
        conn.close()
        exit()

    screen = pygame.display.set_mode(res)

    text = f"max_score is {pre_text[1]} by {pre_text[0]}"
    fonty = pygame.font.Font(None, 36)

    font = pygame.font.Font(None, 36)

    text_width, text_height = font.size(text)

    x_pos = res[0]
    y_pos = 630

    button_image = "data/button.png"
    button = Button(100, 200, button_image)

    while True:
        screen.blit(background_start, (0, 0))
        all_sprites.draw(screen)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if button.is_clicked(pygame.mouse.get_pos()):
                    loop_game()

        text_surface = font.render(text, True, black)

        screen.blit(text_surface, (x_pos, y_pos))

        x_pos -= 2
        if x_pos < -text_width:
            x_pos = res[0]

        button.draw(screen)
        doodler.rect.y -= vel_y
        vel_y -= 5
        if vel_y < -40:
            vel_y = 40

        pygame.display.update()
        clock.tick(fps)

        # Проверка нажатия на кнопку
        mouse_pos = pygame.mouse.get_pos()


init_main()
