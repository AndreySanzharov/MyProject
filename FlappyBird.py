import random
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_w = 860
screen_h = 760

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('FlappyBird')

#font = pygame.font.SysFont('Bauhaus 93', 60)

# стартовые значения
scroll = 6
flying = False
game_over = False
rasst = 160
pipe_chast = 1600
last_pipe = 0
# score = 0
running = True

bg = pygame.image.load('data/bg.png')
rest_img = pygame.image.load('data/restart.png')


def text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def davay_po_nowoy_misha():
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = 400


class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.y = screen_h / 2
        self.rect.x = screen_w / 6
        self.grav = 0

    def update(self):

        if flying == True:
            # гравитация
            self.grav += 1
            if self.grav > 8:
                self.grav = 8
            if self.rect.bottom < 760:
                self.rect.y += self.grav

        if game_over == False:
            # подлет
            if pygame.mouse.get_pressed()[0]:
                self.grav = -10


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/pipe.png")
        self.rect = self.image.get_rect()

        # позиция 1 - находится сверху, -1 - снизу

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (rasst / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + (rasst / 2)]

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

while running:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # проверка на столкновение
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True
        flying = False

    if bird.rect.bottom >= 760 or bird.rect.bottom == 760:
        game_over = True
        flying = False

    if flying == True:
        # новые трубы
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_chast:
            pipe_h = random.randint(-150, 150)
            niz_pipe = Pipe(screen_w, (screen_h / 2) + pipe_h, -1)
            werh_pipe = Pipe(screen_w, (screen_h / 2) + pipe_h, 1)

            pipe_group.add(niz_pipe)
            pipe_group.add(werh_pipe)
            last_pipe = time_now

        pipe_group.update()

    # Провека на конец игры и рестарт
    if game_over:
        if button.draw():
            game_over = False
            davay_po_nowoy_misha()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()

