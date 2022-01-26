import random
import pygame
import os
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_w = 860
screen_h = 760

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('FlappyBird')

# стартовые значения
scroll = 6
flying = False
game_over = False
rasst = 200
pipe_chast = 1600
last_pipe = 0
score = 0
running = True


def play_music():
    pygame.mixer.music.load(r'data\sound_0.mp3')
    # for i in range(6, 0, -1):
    # pygame.mixer.music.queue(r'data\sound_{}.mp3'.format(i))
    pygame.mixer.music.play()


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Не найдено")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Особая благодарность Анечке за прекрасные картинки для игры :)
bg = load_image('Anya.png')
rest_img = load_image('AnyaRestart.png')

score_txt = pygame.font.SysFont('Bauhaus 93', 60)


def davay_po_nowoy_misha():
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = 400


def draw_text(text, score_txt, text_col, x, y):
    img = score_txt.render(text, True, text_col)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("AnyaSpaceShip.png")
        self.rect = self.image.get_rect()
        self.rect.y = screen_h / 2
        self.rect.x = screen_w / 6
        self.grav = 0

    def get_right_pos(self):
        return self.rect.right

    def get_left_pos(self):
        return self.rect.left

    # гравитация
    def update(self):
        if flying:
            self.grav += 1
            if self.grav > 8:
                self.grav = 8
            if self.rect.bottom < 760:
                self.rect.y += self.grav

        # подлет
        if game_over is False:
            if pygame.mouse.get_pressed()[0]:
                self.grav = -10


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("AnyaPipe.png")
        self.rect = self.image.get_rect()

        # позиция 1 - находится сверху, -1 - снизу

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (rasst / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + (rasst / 2)]

    def get_right_pos(self):
        return self.rect.right

    def get_left_pos(self):
        return self.rect.left

    def update(self):
        self.rect.x -= scroll


class Restart():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def draw(self):
        off_func = False
        pos = pygame.mouse.get_pos()
        # проверка условия нажатия мышки
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                off_func = True
                davay_po_nowoy_misha()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return off_func


pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

bird = Bird(100, int(screen_h / 2))

bird_group.add(bird)

# отрисовка заднего фона
screen.blit(bg, (0, 0))
button = Restart(screen_w // 2 - 50, screen_h // 2, rest_img)

play_music()
while running:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)
    bird_group.draw(screen)

    # подсчет очков
    propusk = False
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].get_right_pos() > pipe_group.sprites()[0].get_left_pos():
            propusk = True
        if propusk:
            if bird_group.sprites()[0].get_left_pos() > pipe_group.sprites()[0].get_right_pos():
                score += 1
                propusk = False
    draw_text(str(score // 100), score_txt, "green", int(screen_w / 2), 20)

    # проверка на столкновение
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
        score = 0
        flying = False

    if bird.rect.bottom >= 760 or bird.rect.top <= 0:
        game_over = True
        score = 0
        flying = False

    if flying:
        # новые трубы
        time = pygame.time.get_ticks()
        if time - last_pipe > pipe_chast:
            pipe_h = random.randint(-150, 150)
            niz_pipe = Pipe(screen_w, (screen_h / 2) + pipe_h, -1)
            werh_pipe = Pipe(screen_w, (screen_h / 2) + pipe_h, 1)

            last_pipe = time
            pipe_group.add(niz_pipe)
            pipe_group.add(werh_pipe)

        pipe_group.update()

    # Провека на конец игры и рестарт
    if game_over:
        if button.draw():
            game_over = False
            davay_po_nowoy_misha()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying is False and game_over is False:
            flying = True

    pygame.display.update()
    bird_group.update()

pygame.quit()


