import os
import sys
import pygame
import random 
import sqlite3

dbname = 'database.db'
con = sqlite3.connect(dbname)
cur = con.cursor()

all_sprites = pygame.sprite.Group()
border_group = pygame.sprite.Group()
v_border_group = pygame.sprite.Group()
h_border_group = pygame.sprite.Group()
kill_border_group = pygame.sprite.Group()
kill_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
final_star_group = pygame.sprite.Group()
teleport_group = pygame.sprite.Group()

Stars = [0, 0, 0, 0, 0, 0]
level = 1


def load_image(name, colorkey=None):
    fullname = os.path.join("images", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def Start_screen(screen):  # Стартовый экран
    screen.fill("black")
    font = pygame.font.Font("fonts/NTKnorozov.ttf", 240)
    start_caption = font.render("LABRINTICO", True, (120, 90, 255))
    screen.blit(start_caption, (90, 95))
    font = pygame.font.Font("fonts/NTSakharov-Medium.ttf", 64)
    start_caption = font.render("Для старта нажмите ЛКМ", True, (120, 90, 255))
    screen.blit(start_caption, (150, 500))


def Rules(screen):  # Экран с правилами
    screen.fill("black")
    font = pygame.font.Font("fonts/NTSovTram.ttf", 150)
    start_caption = font.render("ПРАВИЛА ИГРЫ", True, (68, 255, 107))
    screen.blit(start_caption, (240, 95))

    intro_text = ["   Проходите лабиринт и собирайте звезды; ",
                  "   Управляйте спрайтом кнопками со стрелками на клавиатуре; ",
                  "  ",
                  "   Каждый раз вам необходимо пройти три рандомных",
                  "   уровня и собрать девять звезд; ",
                  "   Если вы врезаетесь в враждебную структуру, вы умираете;",
                  "   После прохождения собирается статистика;",
                  "   ",
                  "   Чтобы продолжить, нажмите ЛКМ", "", "",]
    font = pygame.font.Font("fonts/NTSakharov-Medium.ttf", 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 60
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def Final_screen(screen):  # Финальный экран
    global Stars
    global level
    global current_time


    stars = cur.execute(f"""SELECT Stars FROM General WHERE id = 1""").fetchall()[0][0]
    time = cur.execute(f"""SELECT Time FROM General WHERE id = 1""").fetchall()[0][0]

    if sum(Stars) >= stars and level == 4:
        stars = sum(Stars)
        cur.execute(f"""UPDATE General SET Stars = {stars} WHERE id = 1""")
        con.commit()
        if time > current_time:
            cur.execute(f"""UPDATE General SET Time = {current_time} WHERE id = 1""")
            con.commit() 
            time = current_time 

    if level != 4:
        Stars = [0, 0, 0, 0, 0, 0]

    screen.fill("black")

    font = pygame.font.Font("fonts/NTKnorozov.ttf", 180)
    caption = font.render("LABRINTICO", True, (120, 90, 255))
    screen.blit(caption, (230, 85))
    font = pygame.font.Font("fonts/NTSovTram.ttf", 108)
    caption1 = font.render("ИГРА ОКОНЧЕНА", True, (68, 255, 107))
    screen.blit(caption1, (335, 275))
    font = pygame.font.Font("fonts/NTSakharov-Medium.ttf", 36)
    caption2 = font.render("1 Уровень", True, (120, 90, 255))
    screen.blit(caption2, (100, 450))
    caption3 = font.render("2 Уровень", True, (120, 90, 255))
    screen.blit(caption3, (100, 530))
    caption4 = font.render("Рекорд", True, (120, 90, 255))
    screen.blit(caption4, (100, 650))
    caption5 = font.render(f"Кол-во звезд: {stars},       Время {time} сек.", True, (255, 255, 255))
    screen.blit(caption5, (350, 650))
    
    spf1 = Inform_star(550, 430, 0, final_star_group)
    spf2 = Inform_star(630, 430, 1, final_star_group)
    spf3 = Inform_star(710, 430, 2, final_star_group)
    spf4 = Inform_star(550, 510, 3, final_star_group)
    spf5 = Inform_star(630, 510, 4, final_star_group)
    spf6 = Inform_star(710, 510, 5, final_star_group)


def Information_Bar(screen, level_number):  # Полоска со стастистикой во время игры
    font = pygame.font.Font("fonts/NTKnorozov.ttf", 64)
    start_caption = font.render("LABRINTICO", True, (120, 90, 255))
    screen.blit(start_caption, (20, 20))
    font = pygame.font.Font("fonts/NTSakharov-Medium.ttf", 36)
    start_caption = font.render(f"{level_number} Уровень", True, (120, 90, 255))
    screen.blit(start_caption, (320, 27))
    pygame.draw.rect(screen, (120, 90, 255), (0, 85, 1200, 3), 0)


def First_Level(screen):
    screen.fill("black")
    Information_Bar(screen, 1)
    all_sprites.draw(screen)
    all_sprites.update()

    for i in range(18):
        if i != 6 and i != 5:
            if i != 7:
                Off_Border(50, 130 + i * 30, v_border_group)
            Border(50, 130 + i * 30, kill_border_group)
        Off_Border(1100, 130 + i * 30, v_border_group)
        Border(1100, 130 + i * 30, kill_border_group)
        
    for i in range(36):
        if  i != 15 and i != 16 and i != 17 and i != 18 and i != 19 and i != 20 and i != 21:
            Off_Border(50 + i * 30, 640, h_border_group)
        Off_Border(50 + i * 30, 130, h_border_group)
        Border(50 + i * 30, 130, kill_border_group)
        Border(50 + i * 30, 640, kill_border_group)


    for k in range(5):
        Off_Border(110, 130 + k * 30, v_border_group)
        Border(110, 130 + k * 30, kill_border_group)

    for k in range(18):
        if k != 17:
            Off_Border(50 + k * 30, 340, h_border_group)
        Border(50 + k * 30, 340 , kill_border_group)

    for k in range(14):
        Off_Border(740, 220 + k * 30, v_border_group)
        Border(740, 220 + k * 30, kill_border_group)

        Off_Border(800, 160 + k * 30, v_border_group)
        Border(800, 160 + k * 30, kill_border_group)

        Off_Border(860, 220 + k * 30, v_border_group)
        Border(860, 220 + k * 30, kill_border_group)

        Off_Border(920, 160 + k * 30, v_border_group)
        Border(920, 160 + k * 30, kill_border_group)

        Off_Border(980, 220 + k * 30, v_border_group)
        Border(980, 220 + k * 30, kill_border_group)

        Off_Border(1040, 220 + k * 30, v_border_group)
        Border(1040, 220 + k * 30, kill_border_group)

    Off_Border(140, 250, h_border_group)
    Border(140, 250, kill_border_group)

    Off_Border(530, 160, v_border_group)
    Border(530, 160, kill_border_group)

    Off_Border(530, 280, v_border_group)
    Border(530, 280, kill_border_group)
    Off_Border(530, 310, v_border_group)
    Border(530, 310, kill_border_group)

    Off_Border(560, 160, v_border_group)
    Border(560, 160, kill_border_group)

    Border(560, 280, kill_border_group)
    Border(560, 310, kill_border_group)


    Kill_Border(50, 220, kill_border_group)
    Kill_Border(50, 250, kill_border_group)
    Kill_Border(50, 280, kill_border_group)
    Kill_Border(50, 310, kill_border_group)

    Kill_Border(530, 640, kill_border_group)
    Kill_Border(560, 640, kill_border_group)
    Kill_Border(590, 640, kill_border_group)
    Kill_Border(620, 640, kill_border_group)
    Kill_Border(650, 640, kill_border_group)
    Kill_Border(680, 640, kill_border_group)

    st1 = Star(140, 220, 0)
    st2 = Star(560, 370, 1)
    st3 = Star(590, 160, 2)

    Kill(360, 190, "v", kill_group)
    
    Kill(170, 450, "v", kill_group)
    Kill(260, 550, "v", kill_group)
    Kill(350, 450, "v", kill_group)
    Kill(470, 550, "v", kill_group)

    Teleport(1070, 610, teleport_group)

    sp1 = Inform_star(550, 20, 0, star_group)
    sp2 = Inform_star(630, 20, 1, star_group)
    sp3 = Inform_star(710, 20, 2, star_group)


def Second_Level(screen):
    screen.fill("black")
    Information_Bar(screen, 2)
    all_sprites.draw(screen)
    all_sprites.update()

    for i in range(18):
        if i != 13 and i != 14 and i != 15 and i != 16 and i != 17:
            Off_Border(50, 130 + i * 30, v_border_group)
            Border(50, 130 + i * 30, kill_border_group)
        Off_Border(1100, 130 + i * 30, v_border_group)
        Border(1100, 130 + i * 30, kill_border_group)
        
    for i in range(36):
        Off_Border(50 + i * 30, 640, h_border_group)
        Off_Border(50 + i * 30, 130, h_border_group)
        Border(50 + i * 30, 130, kill_border_group)
        Border(50 + i * 30, 640, kill_border_group)

    for k in range(15):
        Off_Border(110, 130 + k * 30, v_border_group)
        Border(110, 130 + k * 30, kill_border_group)

    for k in range(12):
        Off_Border(710, 220 + k * 30, v_border_group)
        Border(710, 220 + k * 30, kill_border_group)
        Off_Border(740, 220 + k * 30, v_border_group)
        Border(740, 220 + k * 30, kill_border_group)
        Off_Border(980, 220 + k * 30, v_border_group)
        Border(980, 220 + k * 30, kill_border_group)
        Off_Border(1040, 220 + k * 30, v_border_group)
        Border(1040, 220 + k * 30, kill_border_group)

    for i in range(7):
        Off_Border(140 + i * 30, 370, h_border_group)
        Border(140 + i * 30, 370, kill_border_group)

    for i in range(3):
        Off_Border(290, 400 + i * 30, v_border_group)
        Border(290, 400 + i * 30, kill_border_group)
        
        Off_Border(350, 490 + i * 30, border_group)
        Border(350, 490 + i * 30, kill_border_group)
        Off_Border(380, 490 + i * 30, border_group)
        Border(380, 490 + i * 30, kill_border_group)
        Off_Border(440, 490 + i * 30, border_group)
        Border(440, 490 + i * 30, kill_border_group)
        Off_Border(470, 490 + i * 30, border_group)
        Border(470, 490 + i * 30, kill_border_group)

        Off_Border(590, 430 + i * 30, border_group)
        Border(590, 430 + i * 30, kill_border_group)
        Off_Border(620, 430 + i * 30, border_group)
        Border(620, 430 + i * 30, kill_border_group)

        Off_Border(830, 160 + i * 30, border_group)
        Border(830, 160 + i * 30, kill_border_group)
        Off_Border(860, 160 + i * 30, border_group)
        Border(860, 160 + i * 30, kill_border_group)

        for j in range(8):
            Kill_Border(290 + j * 30, 220 + i * 30, kill_border_group)

    Off_Border(1070, 310, h_border_group)
    Border(1070, 310, kill_border_group)
    
    Off_Border(440, 490, h_border_group)
    Border(440, 490, kill_border_group)
    
    Off_Border(140, 550, h_border_group)
    Border(140, 550, kill_border_group)
    Off_Border(170, 550, h_border_group)
    Border(170, 550, kill_border_group)
    Off_Border(200, 550, h_border_group)
    Border(200, 550, kill_border_group)

    Off_Border(290, 580, v_border_group)
    Border(290, 580, kill_border_group)
    Off_Border(290, 610, v_border_group)
    Border(290, 610, kill_border_group)

    Off_Border(350, 520, v_border_group)
    Border(350, 520, kill_border_group)
    
    Off_Border(470, 400, v_border_group)
    Border(470, 400, kill_border_group)

    Off_Border(590, 460, v_border_group)
    Border(590, 460, kill_border_group)
    Off_Border(500, 580, v_border_group)
    Border(500, 580, kill_border_group)
    Off_Border(500, 610, v_border_group)
    Border(500, 610, kill_border_group)
    Off_Border(470, 550, h_border_group)
    Border(470, 550, kill_border_group)
    
    Off_Border(830, 160, v_border_group)
    Border(830, 160, kill_border_group)
    Off_Border(860, 160, v_border_group)
    Border(860, 160, kill_border_group)

    Off_Border(470, 370, border_group)
    Border(470, 370, kill_border_group)
    Off_Border(500, 370, border_group)
    Border(500, 370, kill_border_group)
    Off_Border(500, 400, border_group)
    Border(500, 400, kill_border_group)
    Off_Border(500, 490, border_group)
    Border(500, 490, kill_border_group)
    Off_Border(500, 520, border_group)
    Border(500, 520, kill_border_group)
    Off_Border(500, 550, border_group)
    Border(500, 550, kill_border_group)
    
    Off_Border(590, 280, border_group)
    Border(590, 280, kill_border_group)
    Off_Border(620, 280, border_group)
    Border(620, 280, kill_border_group)

    for i in range(4):
        if i != 3:
            Off_Border(770 + i * 30, 370, h_border_group)
        Border(770 + i * 30, 370, kill_border_group)

        Off_Border(860 + i * 30, 520, h_border_group)
        Border(860 + i * 30, 520, kill_border_group)

    Kill_Border(50, 520, kill_border_group)
    Kill_Border(50, 550, kill_border_group)
    Kill_Border(50, 580, kill_border_group)
    Kill_Border(50, 610, kill_border_group)
    
    Kill_Border(200, 460, kill_border_group)
    Kill_Border(410, 280, kill_border_group)
    Kill_Border(440, 280, kill_border_group)
    Kill_Border(400, 770, kill_border_group)
    Kill_Border(400, 800, kill_border_group)
    Kill_Border(400, 830, kill_border_group)
    Kill_Border(400, 860, kill_border_group)

    for i in range(4):
        Kill_Border(590, 160 + i * 30, kill_border_group)
        Kill_Border(620, 160 + i * 30, kill_border_group)
        Kill_Border(590, 520 + i * 30, kill_border_group)
        Kill_Border(620, 520 + i * 30, kill_border_group)

        Kill_Border(770 + i * 30, 400, kill_border_group)
    
    st4 = Star(470, 580, 3)
    st5 = Star(830, 490, 4)
    st6 = Star(1070, 280, 5)

    Kill(200, 250, "v", kill_group)
    Kill(1010, 370, "v", kill_group)

    Teleport(1070, 340, teleport_group)
    
    sp4 = Inform_star(550, 20, 3, star_group)
    sp5 = Inform_star(710, 20, 4, star_group)
    sp6 = Inform_star(630, 20, 5, star_group)


class Inform_star(pygame.sprite.Sprite):
    image = load_image("dark_star.png")

    def __init__(self, x0, y0, num, group):
        super().__init__(all_sprites, group)
        self.image = Inform_star.image
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        self.x = x0
        self.y = y0
        self.num = num

    def update(self):
        global Stars
        if Stars[self.num] == 1:
            image = load_image("light_star.png")
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        
class Border(pygame.sprite.Sprite):
    def __init__(self, x0, y0, group):
        super().__init__(all_sprites, group)
        self.image = pygame.Surface((30, 30))
        self.color = pygame.Color("black")
        self.image.fill(self.color)
        self.rect = pygame.Rect(x0, y0, 30, 30)
        Block_drawer(x0, y0, "white")
        self.x = x0
        self.y = y0

    def update(self):
        Block_drawer(self.x, self.y, (1, 59, 66))


class Off_Border(pygame.sprite.Sprite):
    def __init__(self, x0, y0, group):
        super().__init__(all_sprites, group)
        self.image = pygame.Surface((33, 33))
        self.color = pygame.Color("black")
        self.image.fill(self.color)
        self.rect = pygame.Rect(x0 - 3, y0 - 3, 36, 36)


class Kill_Border(pygame.sprite.Sprite):
    def __init__(self, x0, y0, group):
        super().__init__(all_sprites, group)
        self.image = pygame.Surface((30, 30))
        self.color = pygame.Color("black")
        self.image.fill(self.color)
        self.rect = pygame.Rect(x0, y0, 30, 30)
        Kill_Block_drawer(x0, y0, "white")
        self.x = x0
        self.y = y0 
        self.tick = 0
        self.block_color = (153, 217, 234)

    def update(self):
        pygame.draw.rect(screen, "black", (self.x, self.y, 30, 30), 0)

        self.tick = self.tick + 1
        if self.tick % 40 == 0:
            self.block_color = (153, 217, 234)
        elif  self.tick % 20 == 0:
            self.block_color = (100, 150, 250)
        Kill_Block_drawer(self.x, self.y, self.block_color)


class Teleport(pygame.sprite.Sprite):
    image = load_image("exit.png")

    def __init__(self, x0, y0, group):
        super().__init__(all_sprites, group)
        self.image = Teleport.image
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect().move(x0, y0)

    def update(self):
        global level
        if pygame.sprite.spritecollideany(self, player_group):
            level = level + 1
            self.rect = self.image.get_rect().move(2000, 2000)


def Block_drawer(position_x, position_y, color):
    for a in range(10):
        pygame.draw.rect(screen, color, (position_x + a * 3, position_y, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x, position_y + a * 3, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x + a * 3, position_y + 27, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x + 27, position_y + a * 3, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x + a * 3, position_y + a * 3, 3, 3), 0)
    for a in range(8):
        pygame.draw.rect(screen, color, (position_x  + 6 + a * 3, position_y + a * 3, 3, 3), 0)
    for a in range(6):
        pygame.draw.rect(screen, color, (position_x  + 12 + a * 3, position_y + a * 3, 3, 3), 0)
    for a in range(4):
        pygame.draw.rect(screen, color, (position_x  + 18 + a * 3, position_y + a * 3, 3, 3), 0)


def Kill_Block_drawer(position_x, position_y, color):
    for a in range(8):
        pygame.draw.rect(screen, color, (position_x  + 6 + a * 3, position_y + a * 3, 3, 3), 0)
    for a in range(6):
        pygame.draw.rect(screen, color, (position_x  + 12 + a * 3, position_y + a * 3, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x  + 6 + a * 3, position_y + 6 + a * 3, 3, 3), 0)
    for a in range(4):
        pygame.draw.rect(screen, color, (position_x  + 18 + a * 3, position_y + a * 3, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x  + 6 + a * 3, position_y + 12 + a * 3, 3, 3), 0)
    for a in range(2):
        pygame.draw.rect(screen, color, (position_x  + 24 + a * 3, position_y + a * 3, 3, 3), 0)
        pygame.draw.rect(screen, color, (position_x  + 6 + a * 3, position_y + 18 + a * 3, 3, 3), 0)


class Kill(pygame.sprite.Sprite):
    image1 = load_image("kill.png")
    image2 = load_image("kill_2.png")

    def __init__(self, x0, y0, type, kill_group):
        super().__init__(all_sprites, kill_group)
        self.image1 = Kill.image1
        self.image2 = Kill.image2
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30
        self.tick = 0
        self.rect = self.image.get_rect().move(x0, y0)
        if type == "h":
            self.vx = 3
            self.vy = 0
        if type == "v":
            self.vx = 0
            self.vy = 2

    def update(self):
        self.tick = self.tick + 1
        if self.tick % 40 == 0:
            self.image = self.image1
        elif self.tick % 20 == 0:
            self.image = self.image2
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, h_border_group):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, v_border_group):
            self.vx = -self.vx


class Star(pygame.sprite.Sprite):
    image = load_image("star.png")

    def __init__(self, x0, y0, num):
        super().__init__(all_sprites)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30
        self.x = x0
        self.y = y0
        self.num = num
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        global Stars
        if pygame.sprite.spritecollideany(self, player_group):
            image2 = load_image("pass-star.png")
            self.image = image2
            self.rect = self.image.get_rect()
            self.rect = self.image.get_rect().move(self.x, self.y)
            Stars[self.num] = 1
   
        
class Sprite_First(pygame.sprite.Sprite):
    image = load_image("sprite.png")

    def __init__(self, player_group = player_group):
        super().__init__(player_group)
        self.image = Sprite_First.image
        self.rect = self.image.get_rect()
        
        self.rect.x = 30
        self.rect.y = 30
        self.rect = self.image.get_rect().move(80, 160)
        self.position = 1
        self.step = 5
        self.movement = None
        self.iters = 0
        self.speedx = 0
        self.speedy = 0

    def update(self):
        global running
        keystate = pygame.key.get_pressed()
        self.iters =  self.iters + 1

        if keystate[pygame.K_LEFT] and self.speedx == 0 and self.speedy == 0 and self.iters > 20:
            self.speedx = -15
            self.iters = 10000000000
        if keystate[pygame.K_RIGHT] and self.speedx == 0 and self.speedy == 0 and self.iters > 20:
            self.speedx = 15
            self.iters = 10000000000
        if keystate[pygame.K_UP] and self.speedx == 0 and self.speedy == 0 and self.iters > 20:
            self.speedy = -15
            self.iters = 10000000000
        if keystate[pygame.K_DOWN] and self.speedx == 0 and self.speedy == 0 and self.iters > 20:
            self.speedy = 15
            self.iters = 10000000000
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, v_border_group):
            self.speedx = 0
            if self.iters >= 100000000:
                self.iters = 0
        if pygame.sprite.spritecollideany(self, h_border_group):   
            self.speedy = 0
            if self.iters >= 1000000:
                self.iters = 0
        if pygame.sprite.spritecollideany(self, kill_border_group):
            running = False
        if pygame.sprite.spritecollideany(self, kill_group):
            running = False


if __name__ == '__main__':
    pygame.init()
    size = 1200, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Labrintico")
    screen.fill("black")

    fps = 50

    clock = pygame.time.Clock()

    sprite = Sprite_First()

    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()

    start_flag = True  # Необходимость стартового экрана
    rules_flag = None  # Необходимость экрана с правилами
    final_flag = None  # Необходимость финального экрана
    running = True
    
    t = 0
    current_time = 0
    
    while running:
        screen.fill("black")

        while start_flag:  # Стартовый экран
            Start_screen(screen)
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_flag = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        start_flag = False
                        rules_flag = True
            pygame.display.flip()
            
        while rules_flag:  # Экран с правилами
            Rules(screen)
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rules_flag = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.set_visible(False)
                        rules_flag = False

                        First_Level(screen)
                        all_sprites.draw(screen)
                        
            pygame.display.flip()
        
        player_group.draw(screen)
        star_group.draw(screen)
        all_sprites.draw(screen)

        star_group.update()
        sprite.update()
        t = t + 1
        
        if t == 50:
            current_time = current_time + 1
            t = 0
        

        if level == 1:
            Information_Bar(screen, 1)

        elif level == 2:
            level = level + 1

            all_sprites.remove(all_sprites)
            v_border_group.remove(v_border_group)
            h_border_group.remove(h_border_group)
            kill_border_group.remove(kill_border_group)
            kill_group.remove(kill_group)
            player_group.remove(player_group)
            star_group.remove(star_group)
            teleport_group.remove(teleport_group)
            kill_group.remove(kill_group)

            Second_Level(screen)

            sprite = Sprite_First()
            all_sprites.draw(screen)
            
        elif level == 3:
            Information_Bar(screen, 2)

        elif level == 4:
            running = False
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()

    all_sprites.remove(all_sprites)
    v_border_group.remove(v_border_group)
    h_border_group.remove(h_border_group)
    kill_border_group.remove(kill_border_group)
    kill_group.remove(kill_group)
    player_group.remove(player_group)
    star_group.remove(star_group)
    teleport_group.remove(teleport_group)
    kill_group.remove(kill_group)

    final_flag = True
    Final_screen(screen)

    pygame.display.flip()
    print(level)

    while final_flag:  # Финальный экран
            pygame.mouse.set_visible(True)
            final_star_group.update()
            final_star_group.draw(screen)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    final_flag = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pygame.mouse.set_visible(False)
                        final_flag = False
            pygame.display.flip()

    pygame.quit()
    sys.exit()
