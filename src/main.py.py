import pygame
import random
import os

# Inicializa o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Velocidade inicial do jogo
game_speed = 10
background_speed = game_speed / 2

# FPS (frames por segundo)
clock = pygame.time.Clock()

# Caminhos para arquivos de música e sons
background_music = 'MEUS PROJETOS/alex-dog/assets/music/music.mp3'
jump_sound_path = 'MEUS PROJETOS/alex-dog/assets/sounds/jump_sound.mp3'
coin_sound_path = 'MEUS PROJETOS/alex-dog/assets/sounds/coin_sound.mp3'
shoot_sound_path = 'MEUS PROJETOS/alex-dog/assets/sounds/shoot_sound.mp3'
dino_image_path = 'MEUS PROJETOS/alex-dog/assets/images/dog.png'
cactus_image_path = 'MEUS PROJETOS/alex-dog/assets/images/hidrante.png'
big_cactus_image_path = 'MEUS PROJETOS/alex-dog/assets/images/carteiro.png'
coin_image_path = 'MEUS PROJETOS/alex-dog/assets/images/osso.png'
background_image_path = 'MEUS PROJETOS/alex-dog/assets/images/background.png'
ground_image_path = 'MEUS PROJETOS/alex-dog/assets/images/ground.png'

# Função para tocar a música
def play_music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # Reproduz a música em loop

# Carrega a música inicial
play_music()

# Carrega os sons
def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Erro ao carregar som: {e}")
        return None

jump_sound = load_sound(jump_sound_path)
coin_sound = load_sound(coin_sound_path)
shoot_sound = load_sound(shoot_sound_path)

class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = 495
        self.original_y = self.y
        self.jump = False
        self.double_jump = False
        self.jump_velocity = 8
        self.gravity = 0.8
        self.image = pygame.image.load(dino_image_path)
        self.image = pygame.transform.scale(self.image, (51, 63))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)
        self.coins = 0
        self.bullets = 0
        self.shoot_cost = 1

    def update(self):
        if self.jump:
            self.y -= self.jump_velocity * 3
            self.jump_velocity -= self.gravity
            if self.y >= self.original_y:
                self.y = self.original_y
                self.jump = False
                self.jump_velocity = 8
                self.double_jump = False
        self.rect.bottomleft = (self.x, self.y)

    def jump_action(self):
        if not self.jump:
            self.jump = True
            self.jump_velocity = 8
            if jump_sound:
                jump_sound.play()

    def double_jump_action(self):
        if not self.jump and not self.double_jump:
            self.double_jump = True
            self.jump_velocity = 8
            if jump_sound:
                jump_sound.play()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot_action(self):
        if self.coins >= self.shoot_cost:
            self.coins -= self.shoot_cost
            self.bullets += 1
            if shoot_sound:
                shoot_sound.play()

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x += self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Cactus:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = 495
        self.image = pygame.image.load(cactus_image_path)
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        self.x -= game_speed
        if self.x < -self.rect.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.bottomleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BigCactus:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = 495
        self.image = pygame.image.load(big_cactus_image_path)
        self.image = pygame.transform.scale(self.image, (50, 90))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        self.x -= game_speed
        if self.x < -self.rect.width:
            self.x = SCREEN_WIDTH + random.randint(1600, 2000)
        self.rect.bottomleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Coin:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(300, 450)
        self.image = pygame.image.load(coin_image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.x -= game_speed
        if self.x < -self.rect.width:
            self.x = SCREEN_WIDTH + random.randint(1200, 1600)
            self.y = random.randint(300, 450)
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Background:
    def __init__(self):
        self.background_image = pygame.image.load(background_image_path)
        self.ground_image = pygame.image.load(ground_image_path)
        self.background_width = self.background_image.get_width()
        self.ground_width = self.ground_image.get_width()
        self.background_x1 = 0
        self.background_x2 = self.background_width
        self.ground_x1 = 0
        self.ground_x2 = self.ground_width
        self.y = 0
        self.ground_y = 570 - self.ground_image.get_height()

    def update(self):
        self.background_x1 -= background_speed
        self.background_x2 -= background_speed
        self.ground_x1 -= game_speed
        self.ground_x2 -= game_speed

        if self.background_x1 <= -self.background_width:
            self.background_x1 = self.background_width
        if self.background_x2 <= -self.background_width:
            self.background_x2 = self.background_width

        if self.ground_x1 <= -self.ground_width:
            self.ground_x1 = self.ground_width
        if self.ground_x2 <= -self.ground_width:
            self.ground_x2 = self.ground_width

    def draw(self, screen):
        screen.blit(self.background_image, (self.background_x1, self.y))
        screen.blit(self.background_image, (self.background_x2, self.y))
        screen.blit(self.ground_image, (self.ground_x1, self.ground_y))
        screen.blit(self.ground_image, (self.ground_x2, self.ground_y))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu = False
                    main()
                if event.key == pygame.K_2:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        draw_text('AlexDog', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        font = pygame.font.Font(None, 36)
        draw_text('1. Iniciar', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text('2. Sair', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()
        clock.tick(30)

def game_over_menu(score, coins):
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu = False
                    main()
                if event.key == pygame.K_2:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        draw_text('FIM DE JOGO! Você vai pra carrocinha!', font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        font = pygame.font.Font(None, 36)
        draw_text(f'Pontuação: {score}', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(f'Ossos: {coins}', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text('1. Recomeçar', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        draw_text('2. Sair', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
        pygame.display.update()
        clock.tick(30)

def main():
    global game_speed
    run = True
    score = 0
    dinosaur = Dinosaur()
    cactus = Cactus()
    big_cactus = BigCactus()
    coin = Coin()
    background = Background()
    bullets = []

    frame_count = 0
    speed_increase_interval = 100
    speed_increment = 1

    while run:
        frame_count += 1
        if frame_count >= 300 and frame_count % speed_increase_interval == 0:
            game_speed += speed_increment

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not dinosaur.jump:
                        dinosaur.jump_action()
                    elif not dinosaur.double_jump:
                        dinosaur.double_jump_action()
                if event.key == pygame.K_LSHIFT:
                    dinosaur.shoot_action()

        if dinosaur.bullets > 0:
            new_bullet = Bullet(dinosaur.rect.right, dinosaur.rect.centery)
            bullets.append(new_bullet)
            dinosaur.bullets -= 1

        background.update()
        dinosaur.update()
        cactus.update()
        big_cactus.update()
        coin.update()

        for bullet in bullets:
            bullet.update()

        screen.fill(WHITE)
        background.draw(screen)
        dinosaur.draw(screen)
        cactus.draw(screen)
        big_cactus.draw(screen)
        coin.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        if dinosaur.rect.colliderect(cactus.rect) or dinosaur.rect.colliderect(big_cactus.rect):
            game_over_menu(score, dinosaur.coins)
            return

        for bullet in bullets:
            if bullet.rect.colliderect(cactus.rect):
                cactus.x = SCREEN_WIDTH + random.randint(800, 1000)
                bullets.remove(bullet)
            elif bullet.rect.colliderect(big_cactus.rect):
                big_cactus.x = SCREEN_WIDTH + random.randint(1600, 2000)
                bullets.remove(bullet)

        if dinosaur.rect.colliderect(coin.rect):
            dinosaur.coins += 1
            coin.x = SCREEN_WIDTH + random.randint(1200, 1600)
            coin.y = random.randint(300, 450)
            if coin_sound:
                coin_sound.play()

        score += 1
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Pontuação: {score}', True, BLACK)
        coins_text = font.render(f'Ossos: {dinosaur.coins}', True, BLACK)
        screen.blit(score_text, (600, 10))
        screen.blit(coins_text, (600, 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_menu()