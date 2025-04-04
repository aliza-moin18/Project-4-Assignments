import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player setup
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

# Enemy setup
enemy_size = 50
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = 50
enemy_speed = 3  # Speed increases as score increases

# Bullet setup
bullet_width, bullet_height = 5, 15
bullets = []
bullet_speed = 7

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
game_over = False

while running:
    screen.fill(WHITE)

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart game
            score = 0
            enemy_speed = 3
            bullets.clear()
            player_x = WIDTH // 2
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = 50
            game_over = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE]:  # Fire bullet
        bullets.append([player_x + player_size // 2, player_y])

    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Move enemy
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        game_over = True  # Enemy reaches bottom = Game Over

    # Collision detection (Bullet hits enemy)
    for bullet in bullets:
        if enemy_x < bullet[0] < enemy_x + enemy_size and enemy_y < bullet[1] < enemy_y + enemy_size:
            bullets.remove(bullet)
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = 50
            score += 1
            enemy_speed += 0.2  # Increase speed as score increases

    # Draw player, enemy, bullets
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_size, enemy_size))
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Refresh screen
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
