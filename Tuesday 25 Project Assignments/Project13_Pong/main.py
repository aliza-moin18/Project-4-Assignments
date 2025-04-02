import pygame
import random

# Initialize Pygame
pygame.init()

# Game Window Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle Settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10

# Initial Paddle & Ball Positions
paddle_a = pygame.Rect(20, (HEIGHT // 2) - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 30, (HEIGHT // 2) - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Ball Movement
ball_speed_x, ball_speed_y = 4, 4

# Paddle Movement
paddle_speed = 6
paddle_a_move = 0
paddle_b_move = 0

# Score
score_a, score_b = 0, 0
font = pygame.font.Font(None, 36)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_a_move = -paddle_speed
            elif event.key == pygame.K_s:
                paddle_a_move = paddle_speed
            elif event.key == pygame.K_UP:
                paddle_b_move = -paddle_speed
            elif event.key == pygame.K_DOWN:
                paddle_b_move = paddle_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle_a_move = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle_b_move = 0

    # Move Paddles
    paddle_a.y += paddle_a_move
    paddle_b.y += paddle_b_move

    # Boundaries
    if paddle_a.top < 0:
        paddle_a.top = 0
    if paddle_a.bottom > HEIGHT:
        paddle_a.bottom = HEIGHT
    if paddle_b.top < 0:
        paddle_b.top = 0
    if paddle_b.bottom > HEIGHT:
        paddle_b.bottom = HEIGHT

    # Move Ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball Collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle Collisions
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        score_b += 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
    if ball.right >= WIDTH:
        score_a += 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1

    # Draw Objects
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Display Score
    text = font.render(f"{score_a} - {score_b}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 20, 20))

    # Update Display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
