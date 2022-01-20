import pygame
import random

pygame.init()

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 100)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = pygame.image.load("data/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.y = 10
        self.rect.x = 100

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            self.rect = self.rect.move(0, -40)
        if args and args[0].type == MYEVENTTYPE:
            self.rect = self.rect.move(0, 5)


def main():
    width = 900
    height = 800
    running = True
    clock = pygame.time.Clock()
    fps = 60
    flying = False

    score = 0
    game_over = False



    size = width, height
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    Bird(100, 400, all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        screen.fill('white')
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main()
