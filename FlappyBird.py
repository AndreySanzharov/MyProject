import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_w = 860
screen_h = 760

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('FlappyBird :)')

# стартовые значения

scroll = 4
flying = False
game_over = False
running = True
# подгрузка изображений
bg = pygame.image.load('data/bg.png')


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


bird_group = pygame.sprite.Group()

bird = Bird(100, int(screen_h / 2))

bird_group.add(bird)

# отрисовка заднего фона
screen.blit(bg, (0, 0))

while running:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    # проверка на столкновение

    if bird.rect.bottom >= 760 or bird.rect.bottom == 760:
        game_over = True
        flying = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
