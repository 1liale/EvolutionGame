import pygame
import random
from pygame.locals import *
import GeneticAlgo
import NeuralNetwork

WIDTH = 500
HEIGHT = 500
isHuman = False
start_pos = (50, HEIGHT/2)
POPULATION = 100
INTERVAL = 5000


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, id, coefs=0, intercepts=0):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.isJump = False
        self.jumpCount = 8
        self.rect = self.surf.get_rect(
            center=(
                x,
                y,
            )
        )

        self.command = 5
        self.speed = 3
        self.x = x
        self.y = y
        self.score = 0
        if coefs == 0 and intercepts == 0:
            self.coefs, self.intercepts = NeuralNetwork.generate_weights_intercepts()
        else:
            self.coefs = coefs
            self.intercepts = intercepts
        self.intercept = 0
        self.alive = True
        self.winner = False
        self.id = id

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.alive = True

    # action
    # 0: jump
    # 1: jump left
    # 2: jump right
    # 3: move left
    # 4: move right
    # 5: stop
    def computer_update(self, action,):
        x = 0
        y = 0
        if not self.isJump and (action == 0 or action == 1 or action == 2):
            self.isJump = True
        else:
            if self.jumpCount >= -8:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                y -= int((self.jumpCount ** 2) * 0.5 * neg)
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 8
        if action == 1 or action == 3:
            x = -self.speed
        if action == 2 or action == 4:
            x = self.speed
        if action == 5:
            x = 0

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # self.x += x
        # self.y += y
        self.rect.move_ip(x, y)

    def human_update(self, pressed_key):
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
                y -= int((self.jumpCount ** 2) * 0.5 * neg)
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
        x = random.randint(WIDTH + 100, WIDTH + 200)
        self.rect = self.surf.get_rect(
            center=(
                x,
                HEIGHT / 2,
            )
        )
        self.x = x
        self.speed = random.randint(3, 5)
        self.initialized = False
        self.visited = []
        for i in range(POPULATION):
            self.visited.append(False)

    def start(self):
        self.initialized = True
        self.update()

    def update(self):
        if self.initialized:
            x_delta = -self.speed
            self.x += x_delta
            self.rect.move_ip(x_delta, 0)

    def moved_outside(self, players):
        if self.rect.right < 0:
            for player in players:
                player.passed = False
            self.kill()

    def pass_player(self, player, ):
        if player.alive and self.rect.right < player.x and not self.visited[player.id]:
            self.visited[player.id] = True
            player.score += 1
            # print(player.score)
            return True
        return False


class DisplayInfo:
    def __init__(self):
        super(DisplayInfo, self).__init__()
        self.font = pygame.font.SysFont('Arial', 20, False, False)
        self.white = (255, 255, 255)
        x = WIDTH - 110
        y = 50
        self.pos = ((x, y), (x, y + 30), (x, y + 60))

    def update(self, screen, score, alive, gen):
        # print(self.score)
        text0 = self.font.render("Score: " + str(score), True, self.white)
        screen.blit(text0, self.pos[0])
        text1 = self.font.render("Alive: " + str(alive), True, self.white)
        screen.blit(text1, self.pos[1])
        text2 = self.font.render("Generation: " + str(gen), True, self.white)
        screen.blit(text2, self.pos[2])


def run_game():
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jumpy Block")
    display = DisplayInfo()

    ADDOBSTACLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDOBSTACLE, INTERVAL)
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    players = []
    obstacles_array = []
    for i in range(POPULATION):
        player = Player(start_pos[0], start_pos[1], i)
        players.append(player)
        all_sprites.add(player)
        if isHuman:
            break

    # can be an arbitrary number I just set it as the same as the population for simplicity's sake
    for i in range(POPULATION):
        new_obstacle = Obstacle()
        obstacles_array.append(new_obstacle)
        obstacles.add(new_obstacle)
        all_sprites.add(new_obstacle)

    game_over = False
    generation = 1
    obstacle_init = 0
    players[-1].winner = True
    high_score_index = -1
    high_score = -100

    # main loop
    while not game_over:
        screen.fill((0, 0, 0))
        alive = 0

        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                game_over = True
            elif event.type == pygame.QUIT:
                game_over = True
            elif event.type == ADDOBSTACLE:
                obstacles_array[obstacle_init].start()
                obstacle_init += 1
                obstacle_init %= POPULATION

        for i, player in enumerate(players):
            obstacles_array[obstacle_init-1].pass_player(player)

            if isHuman:
                pressed_keys = pygame.key.get_pressed()
                player.human_update(pressed_keys)
                high_score = player.score
            else:
                input = NeuralNetwork.generate_input(player, obstacles_array, i)
                player.command = NeuralNetwork.produce_output(input, player.coefs, player.intercepts)
                # print(player.command)
                if player.score > high_score:
                    high_score = player.score
                    high_score_index = i
                    winner = players[i]
                    winner.winner = True

                player.computer_update(player.command)

            if pygame.sprite.spritecollideany(player, obstacles):
                if isHuman:
                    player.kill()
                    game_over = True
                else:
                    player.alive = False
                    player.kill()

        for player in players:
            if player.alive:
                alive += 1
        display.update(screen, high_score, alive, generation)
        obstacles.update()
        for cur_object in all_sprites:
            screen.blit(cur_object.surf, cur_object.rect)
        pygame.display.flip()

        # reset game when all players are dead
        if alive == 0:
            for cur_object in all_sprites:
                cur_object.kill()
            for obstacle in obstacles:
                obstacle.kill()
            screen.fill((0, 0, 0))
            print("starting next generation")
            pygame.time.delay(2000)
            winner = players[high_score_index]
            print(high_score_index)
            generation += 1
            winner.reset(start_pos[0], start_pos[1])
            players = []
            obstacles_array = []

            high_score_index = -1
            high_score = -100
            obstacle_init = 0

            for i in range(POPULATION - 1):
                new_player = Player(start_pos[0], start_pos[1], i, GeneticAlgo.mutateCoefs(winner.coefs),
                                      GeneticAlgo.mutateIntercepts(winner.intercepts))
                players.append(new_player)
                all_sprites.add(new_player)

            for i in range(POPULATION):
                new_obstacle = Obstacle()
                obstacles_array.append(new_obstacle)
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle)

            players.append(winner)
            all_sprites.add(winner)
        fps_clock.tick(60)

run_game()