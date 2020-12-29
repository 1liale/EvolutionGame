import pygame
import random

from pygame.locals import *

WIDTH = 500
HEIGHT = 500


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.speed = 3
        self.isJump = False
        self.jumpCount = 8
        self.rect = self.surf.get_rect(
            center=(
                50,
                HEIGHT / 2,
            )
        )

    def update(self, pressed_key):
        x = 0
        y = 0
        if not self.isJump:
            if pressed_key[K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -8:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 8
        if pressed_key[K_LEFT]:
            x = -self.speed
        if pressed_key[K_RIGHT]:
            x = self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        self.rect.move_ip(x, y)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH + 100, WIDTH + 200),
                HEIGHT / 2,
            )
        )
        self.speed = 3

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ADDOBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDOBSTACLE, 2000)

    player = Player()

    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    game_over = False

    # main loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_over = True

            elif event.type == pygame.QUIT:
                game_over = True

            elif event.type == ADDOBSTACLE:
                new_obstacle = Obstacle()
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        obstacles.update()
        screen.fill((0, 0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, obstacles):
            player.kill()
            game_over = True

        pygame.display.flip()
        fps_clock.tick(60)


main()