import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920/2, 1080/2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plant vs Zombies")
clock = pygame.time.Clock()

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cooldown = 60 
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.cooldown:
            bullet = Bullet(self.rect.right, self.rect.centery)
            bullets.add(bullet)
            self.timer = 0

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

plants = pygame.sprite.Group()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

spawn_timer = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            plant = Plant(x - x % 50, y - y % 50)
            plants.add(plant)

    spawn_timer += 1
    if spawn_timer > 120:
        zombie = Zombie(WIDTH, 100)
        zombies.add(zombie)
        spawn_timer = 0

    plants.update()
    zombies.update()
    bullets.update()

    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, True)
        if hit_zombies:
            bullet.kill()

    # screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    plants.draw(screen)
    zombies.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()
    clock.tick(60)
