import pygame
import random

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont('Arial', 20)
lose_font = pygame.font.SysFont('Arial', 40)

apple = pygame.Rect((300, 250, 20, 20))

player = pygame.Rect((100, 100, 20, 20))

points = 0

snake = [
    player,
    pygame.Rect(80, 100, 20, 20),
    pygame.Rect(60, 100, 20, 20),
    pygame.Rect(40, 100, 20, 20),
    pygame.Rect(20, 100, 20, 20),
]

move = False

clock = pygame.time.Clock()
speed = 30

run = True

lose = lose_font.render('Lose', True, (255, 255, 255))

stop = True

while run:
    clock.tick(speed)

    screen.fill((0, 0, 0))

    points_ui = font.render('Points: ' + str(points), True, (255, 255, 255))
    screen.blit(points_ui, (700, 20))

    pygame.draw.rect(screen, (255, 0, 0), apple)
    for block in snake:
        pygame.draw.rect(screen, (0, 255, 0), block)

    pygame.display.flip()

    old_pos = [block.topleft for block in snake]
    
    key = pygame.key.get_pressed()
    if stop:
        if key[pygame.K_a]:
            player.move_ip(-20, 0)
            move = True
        elif key[pygame.K_d]:
            player.move_ip(20, 0)
            move = True
        elif key[pygame.K_s]:
            player.move_ip(0, 20)
            move = True
        elif key[pygame.K_w]:
            player.move_ip(0, -20)
            move = True
        else:
            move = False

    head = snake[0]
    head.x = max(0, min(head.x, SCREEN_WIDTH - head.width))
    head.y = max(0, min(head.y, SCREEN_HEIGHT - head.height))

    free = True
    if snake[0].topleft != old_pos[0]:
        for i in range(1, len(snake)):
            for val in snake:
                if val.topleft == old_pos[i - 1]:
                    free = False
            if free:
                snake[i].topleft = old_pos[i - 1]
            free = True

    if player.colliderect(apple):
        points += 1
        apple.topleft = (random.randrange(0, 780, 20),
                         random.randrange(0, 580, 20))
        snake.append(pygame.Rect(100, 100, 20, 20))
        snake[-1].topleft = old_pos[-1]
    
    for block in snake[2:]:
        if head.colliderect(block):
            screen.blit(lose, (350, 300)) 
            stop = False
    
    if head.x == 0 or head.x == 780 or head.y == 0 or head.y == 580:
        screen.blit(lose, (350, 300))
        stop = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()