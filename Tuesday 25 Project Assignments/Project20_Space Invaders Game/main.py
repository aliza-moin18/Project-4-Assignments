import pygame
import random
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

player_width, player_height, player_speed = 64, 64, 5
player_x, player_y = SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - player_height - 10

base_path = os.path.dirname(__file__)
player_img = pygame.image.load(os.path.join(base_path, "player.png"))

bullet_width, bullet_height, bullet_speed = 5, 10, 7
bullets = []

alien_width, alien_height, alien_speed = 64, 64, 3
aliens = []

font = pygame.font.SysFont("Arial", 30)
score, lives, game_over = 0, 3, False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player_x, player_y

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - player_width:
            self.rect.x += player_speed

    def shoot(self):
        bullets.append(Bullet(self.rect.centerx, self.rect.top))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = x, y

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            bullets.remove(self)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((alien_width, alien_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.y += alien_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - alien_width)
            self.rect.y = random.randint(-100, -40)

player_group = pygame.sprite.Group()
bullet_group, alien_group = pygame.sprite.Group(), pygame.sprite.Group()
player = Player()
player_group.add(player)

for i in range(6):
    for j in range(5):
        alien_group.add(Alien(i * (alien_width + 10) + 50, j * (alien_height + 10) + 50))

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            player.shoot()

    keys = pygame.key.get_pressed()
    player_group.update(keys)
    for bullet in bullets:
        bullet.update()
    for alien in alien_group:
        alien.update()

    for bullet in bullets[:]:
        for alien in alien_group:
            if bullet.rect.colliderect(alien.rect):
                alien_group.remove(alien)
                bullets.remove(bullet)
                score += 10
                break

    for alien in alien_group:
        if alien.rect.colliderect(player.rect):
            lives -= 1
            alien.rect.x = random.randint(0, SCREEN_WIDTH - alien_width)
            alien.rect.y = random.randint(-100, -40)
            if lives == 0:
                game_over = True

    player_group.draw(screen)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    alien_group.draw(screen)

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, WHITE), (SCREEN_WIDTH - 100, 10))

    if game_over:
        game_over_text = font.render("GAME OVER!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
