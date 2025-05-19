import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1471, 726
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plant vs Zombies")
clock = pygame.time.Clock()

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

GREEN = (0, 200, 100)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

GAME_SPEED = 5 # 1-5

# Position array
zombie_positions_y = [130, 245, 370, 480, 600]
plants_positions_x = [340, 430, 525, 625, 725, 825, 915, 1010, 1110]

# Speed array
game_speed = [0, 1500, 1200, 1000, 700, 500]

####################### CLASS ########################

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cooldown = 200 
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
        self.health = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
    
    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        fill = (self.health / 3) * bar_width  # 3
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

####################### Functions ########################




plants = pygame.sprite.Group()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

spawn_timer = 750
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            nearest_x = min(plants_positions_x, key=lambda px: abs(px - x))
            nearest_y = min(zombie_positions_y, key=lambda py: abs(py - y))
            if abs(nearest_x - x) < 40 and abs(nearest_y - y) < 40:
                plant = Plant(nearest_x, nearest_y)
                plants.add(plant)

    spawn_timer += 1
    if spawn_timer > game_speed[GAME_SPEED]:
        zombie_x = WIDTH+5
        zombie_y = zombie_positions_y[random.randint(0, 4)]
        zombie = Zombie(zombie_x, zombie_y)
        zombies.add(zombie)
        spawn_timer = random.randint(0, game_speed[GAME_SPEED]-100)

    plants.update()
    zombies.update()
    bullets.update()

    # for bullet in bullets:
    #     hit_zombies = pygame.sprite.spritecollide(bullet, zombies, True)
    #     if hit_zombies:
    #         bullet.kill()
    for bullet in bullets:
        hit_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
        if hit_zombies:
            bullet.kill()
            for zombie in hit_zombies:
                zombie.health -= 1
                if zombie.health <= 0:
                    zombie.kill()

    


    # screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    plants.draw(screen)
    zombies.draw(screen)
    for zombie in zombies:
        zombie.draw_health_bar(screen)
    bullets.draw(screen)
    pygame.display.flip()
    clock.tick(60)
