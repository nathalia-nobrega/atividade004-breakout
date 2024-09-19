import pygame as pg
import sys
import random

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Configurações de Cor
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

#BRICKS
BRICK_RED = (255, 0, 0)
BRICK_GREEN = (0, 255, 0)
BRICK_ORANGE = (255, 165, 0)
BRICK_YELLOW = (255, 255, 0)
brick_col = None

#Configurações de texto
# font = pg.font.Font('assets/PressStart2P.ttf', 20)

#Configuração de variaveis
columms = 12
rows = 8

# Configurações da raquete
PADDLE_WIDTH = 50
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7
PADDLE_COLOR = (70, 130, 180)

# Configurações da bola=
BALL_WIDTH = 15
BALL_HEIGHT = 10
BALL_SPEED = 3
BALL_COLOR = (255, 255, 255)

BACKGROUND_COLOR = (0, 0, 0)
MAX_BALL_SPEED_X = 7  # Velocidade máxima horizontal da bola (pode alterar se necesśario)

# Controla a raquete do jogador. Ela se move horizontalmente com as teclas ← e →
# e tem uma função para desenhá-la na tela
class Paddle:
    def __init__(self, screen):
        self.screen = screen
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.rect = pg.Rect(
            (SCREEN_WIDTH // 2) - (self.width // 2),
            SCREEN_HEIGHT - 30,
            self.width,
            self.height
        )
        self.speed = PADDLE_SPEED

    def move(self, keys):
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shrink(self):
        # Reduz a largura da raquete pela metade
        self.width = self.width // 2
        self.rect.width = self.width
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))  # Ajusta para manter a raquete na tela

    def reset(self):
        """ Restaura a largura da raquete para o valor original. """
        self.width = PADDLE_WIDTH
        self.rect.width = self.width
        self.rect.x = (SCREEN_WIDTH // 2) - (self.width // 2)  # Centraliza a raquete na tela

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

# Representa a bola (quadrado). Ela se move pela tela, verifica colisões com
# as bordas e a raquete, e reseta se cair na parte inferior da tela.
class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.color = BALL_COLOR
        self.rect = pg.Rect(
            (SCREEN_WIDTH // 2) - (self.width // 2),
            SCREEN_HEIGHT // 2,
            self.width,
            self.height
        )
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Verifica colisões com as bordas da tela
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def check_collision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            # Calcular a posição relativa de colisão
            relative_collision_x = (self.rect.centerx - paddle.rect.left) / paddle.width
            # O valor varia entre -1.0 (esquerda) e 1.0 (direita)
            offset = (relative_collision_x - 0.5) * 2

            # Ajustar a velocidade horizontal de acordo com o local de colisão
            self.speed_x += offset * MAX_BALL_SPEED_X
            self.speed_x = max(min(self.speed_x, MAX_BALL_SPEED_X), -MAX_BALL_SPEED_X)

            # Inverter a direção vertical (a bola sempre quica para cima)
            self.speed_y = -abs(self.speed_y)

    def reset(self, paddle):
        # Define uma posição inicial aleatória próxima ao centro da tela
        random_offset_x = random.randint(-100, 100)
        random_offset_y = random.randint(-50, 50)
        self.rect.x = (SCREEN_WIDTH // 2) - (self.width // 2) + random_offset_x
        self.rect.y = (SCREEN_HEIGHT // 2) - (self.height // 2) + random_offset_y

        # Define uma direção aleatória para a bola
        self.speed_x = random.uniform(-BALL_SPEED, BALL_SPEED)
        self.speed_y = BALL_SPEED  # A bola sempre começa indo para baixo

        # Reseta a raquete
        paddle.reset()

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

#classe para configurar os tijolos
class Brick:
    #função principal
    def __init__(self):
        self.game_over = 0
        self.live_ball = False
        self.bricks = None
        self.width = SCREEN_WIDTH // columms
        self.height = 20

    #função pra criar os tijolos
    def wall_create(self):
        strength = 0
        self.bricks = []
        individual_bricks = []
        for row in range(rows):
            brick_row = []
            for col in range(columms):
                brick_x = col * self.width
                brick_y = row * self.height + 70
                rect = pg.Rect(brick_x, brick_y, self.width, self.height)
                if row < 2:
                    strength = 4
                elif row < 4:
                    strength = 3
                elif row < 6:
                    strength = 2
                elif row < 8:
                    strength = 1
                individual_bricks = [rect, strength]
                brick_row.append(individual_bricks)
            self.bricks.append(brick_row)

    def wall_draw(self):
        for row in self.bricks:
            for brick in row:
                if brick[1] == 4:
                    brick_col = BRICK_RED
                elif brick[1] == 3:
                    brick_col = BRICK_ORANGE
                elif brick[1] == 2:
                    brick_col = BRICK_GREEN
                elif brick[1] == 1:
                    brick_col = BRICK_YELLOW
                pg.draw.rect(screen, brick_col, brick[0]) ##
                pg.draw.rect(screen, BACKGROUND_COLOR, (brick[0]), 2)

# Contém o loop principal do jogo, que lida com eventos,
# atualiza o estado do jogo e desenha os objetos na tela.
class Game:
    game_started = False
    def __init__(self):
        pg.init()
        pg.display.set_caption('Breakout')
        self.clock = pg.time.Clock()
        self.paddle = Paddle(screen)
        self.ball = Ball(screen)
        self.paddle_shrinked = False  # Controle se a raquete já foi reduzida
        self.brick = Brick()
        self.brick.wall_create()

    def run(self):
        while True:
            self.handle_events(screen)
            self.update_game_state()
            self.draw()
            self.clock.tick(60)

    # Desenhando texto na tela
    # def draw_text(self, text, font1, color, x, y, surface):
    #     textobj = font.render(text, True, color)
    #     text_rect = textobj.get_rect()
    #     text_rect.x = x
    #     text_rect.y = y
    #     surface2.blit(textobj, text_rect)
    #     game_started = True
    #
    #     screen.fill(BACKGROUND_COLOR)
    #
    #     if not game_started:
    #         draw_text("Pressione qualquer tecla para iniciar", font, COLOR_WHITE, screen, 150, 250)
    #     else:
    #         draw_text("Jogo Iniciado", font, COLOR_WHITE, screen, 300, 250)

    def handle_events(self, screen):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def update_game_state(self):
        keys = pg.key.get_pressed()
        self.paddle.move(keys)
        self.ball.move()
        self.ball.check_collision_with_paddle(self.paddle)

        # Verifica se a bola atingiu o topo da tela e ainda não reduziu a raquete
        if self.ball.rect.top <= 0 and not self.paddle_shrinked:
            self.paddle.shrink()  # Reduz a raquete
            self.paddle_shrinked = True  # Marca que a raquete já foi reduzida

        # Verifica se a bola caiu fora da tela
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.reset(self.paddle)

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        self.paddle.draw()
        self.ball.draw()
        self.brick.wall_draw()
        pg.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
