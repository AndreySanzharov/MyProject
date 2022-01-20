import pygame

pygame.init()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = pygame.image.load("data/bird1.png")
        self.rect = self.image.get_rect()
        self.rect.y = 10
        self.rect.x = 100


def main():
    width = 700
    height = 700
    running = True

    size = width, height
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    Bird(100, 400, all_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('white')
        all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
