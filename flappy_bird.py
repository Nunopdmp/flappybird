import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Carrega os sons
flap_sound = pygame.mixer.Sound("flap.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

class Bird:
    def __init__(self):
        self.width = 40  # Largura do retângulo do pássaro
        self.height = 40  # Altura do retângulo do pássaro
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, self.width, self.height)
        self.velocity = 0
        self.gravity = 0.5

    def flap(self):
        self.velocity = -8
        
    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)  # Desenha o pássaro como um retângulo amarelo

    def check_collision_with_edges(self):
        # Verifica colisão com a borda superior (y < 0)
        if self.rect.top < 0:
            return True
        # Verifica colisão com a borda inferior (y > SCREEN_HEIGHT)
        if self.rect.bottom > SCREEN_HEIGHT:
            return True
        return False

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60  # Largura do retângulo do cano
        self.gap = 200  # Espaço entre os canos
        self.height = random.randint(150, 400)  # Altura do cano de cima
        self.passed = False

    def update(self):
        self.x -= 3

    def draw(self):
        # Desenha o cano de cima
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        # Desenha o cano de baixo
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, self.width, SCREEN_HEIGHT - (self.height + self.gap)))

    def collide(self, bird):
        # Cria retângulos para os canos
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.height)
        bottom_pipe_rect = pygame.Rect(self.x, self.height + self.gap, self.width, SCREEN_HEIGHT - (self.height + self.gap))

        # Verifica colisão com o pássaro
        if bird.rect.colliderect(top_pipe_rect) or bird.rect.colliderect(bottom_pipe_rect):
            return True
        return False

def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(2)]
    score = 0
    running = True
    game_over = False  # Variável para controlar o estado do jogo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:  # Só permite bater asas se o jogo não tiver terminado
                        bird.flap()
                    else:  # Reinicia o jogo se a tecla espaço for pressionada após o "Game Over"
                        main()  # Reinicia o jogo

        screen.fill(BLACK)  # Preenche a tela com a cor preta

        if not game_over:
            bird.update()
            for pipe in pipes:
                pipe.update()
                pipe.draw()

                if pipe.collide(bird):
                    
                    game_over = True  # Define o jogo como terminado

                if pipe.x + pipe.width < 0:
                    pipes.remove(pipe)
                    pipes.append(Pipe(SCREEN_WIDTH))

                if not pipe.passed and pipe.x < bird.rect.x:
                    pipe.passed = True
                    score += 1

            # Verifica colisão com as bordas da tela
            if bird.check_collision_with_edges():
                
                game_over = True

        # Desenha o pássaro e os canos, mesmo se o jogo tiver terminado
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Mostra o placar
        font = pygame.font.SysFont("Arial", 40)
        score_text = font.render(f"{score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 20, 50))

        # Mostra a mensagem de "Game Over" se o jogo tiver terminado
        if game_over:
            game_over_font = pygame.font.SysFont("Arial", 50)
            game_over_text = game_over_font.render("Game Over", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()