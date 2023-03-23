import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1366, 700

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

main_surface = pygame.display.set_mode(screen)

ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 2

def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height-20), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.Surface((20, 20))
    bonus.fill(GREEN)
    bonus_rect = pygame.Rect(random.randint(0, width-20), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

enemies = []
bonuses = []

is_working = True
game_over = False

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if not game_over:
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            elif event.type == CREATE_BONUS:
                bonuses.append(create_bonus())

    pressed_keys = pygame.key.get_pressed()

    main_surface.fill(BLACK)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].right < 0:
            #enemies.remove(enemy)
            enemies.pop(enemies.index(enemy))

        if not game_over and ball_rect.colliderect(enemy[1]):
            ball.fill(BLACK)
            enemies = []
            bonuses = []
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].top > height:
            #bonuses.remove(bonus)
            bonuses.pop(bonuses.index(bonus))

        if not game_over and ball_rect.colliderect(bonus[1]):
            #bonuses.remove(bonus)
            bonuses.pop(bonuses.index(bonus))

    if not game_over:

        if ball_rect.bottom >= height:
            ball_rect.bottom = height
        elif ball_rect.top <= 0:
            ball_rect.top = 0

        if ball_rect.right >= width:
            ball_rect.right = width
        elif ball_rect.left <= 0:
            ball_rect.left = 0

        if pressed_keys[K_DOWN]:
            ball_rect = ball_rect.move(0, ball_speed)

        if pressed_keys[K_UP]:
            ball_rect = ball_rect.move(0, -ball_speed)

        if pressed_keys[K_RIGHT]:
            ball_rect = ball_rect.move(ball_speed, 0)

        if pressed_keys[K_LEFT]:
            ball_rect = ball_rect.move(-ball_speed, 0)

    main_surface.blit(ball, ball_rect)

    if game_over:
        font = pygame.font.Font(None, 46)
        text = font.render("GAME OVER!", True, RED)
        text_rect = text.get_rect(center=(width/2, height/2))
        main_surface.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
