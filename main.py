import pygame as pg
import sys
import random

# Configurações da tela
pg.init()
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 680
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurações de Cor
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# BRICKS
BRICK_RED = (255, 0, 0)
BRICK_GREEN = (0, 255, 0)
BRICK_ORANGE = (255, 165, 0)
BRICK_YELLOW = (255, 255, 0)

# Configurações de texto
NORMAL_FONT = pg.font.Font("assets/breakout_font.ttf", 60)

# start_text = NORMAL_FONT.render("PRESSIONE QUALQUER TECLA PARA INICIAR", True, COLOR_WHITE)
# start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))

points_string = NORMAL_FONT.render('000', True, COLOR_WHITE)
points_text_rect = points_string.get_rect(center=(110, 100))

attempts_string = NORMAL_FONT.render('1', True, COLOR_WHITE)
attempts_text_rect = attempts_string.get_rect(center=(SCREEN_WIDTH - 200, 50))

points_string_2 = NORMAL_FONT.render('000', True, COLOR_WHITE)
points_text_rect_2 = points_string_2.get_rect(center=(SCREEN_WIDTH - 120, 100))

attempts_string_2 = NORMAL_FONT.render('1', True, COLOR_WHITE)
attempts_text_rect_2 = attempts_string_2.get_rect(center=(30, 50))


# Configuração de som
PADDLE_SFX = pg.mixer.Sound("assets/ball_hit_paddle.wav")
WALL_SFX = pg.mixer.Sound("assets/ball_hit_wall.wav")
BRICK_SFX = pg.mixer.Sound("assets/ball_hit_block.wav")
PADDLE_SFX.set_volume(0.5)
WALL_SFX.set_volume(0.5)
BRICK_SFX.set_volume(0.5)

# Configuração de variaveis
COLUMNS = 14
ROWS = 8
MAX_ATTEMPTS = 3

# Configurações da raquete
PADDLE_WIDTH = 40
PADDLE_HEIGHT = 14
PADDLE_SPEED = 10
PADDLE_COLOR = (70, 130, 180)

# Configurações da bola
BALL_WIDTH = 10
BALL_HEIGHT = 8
BALL_SPEED = 4
BALL_COLOR = (255, 255, 255)
PADDLE_DELAY = 30

BACKGROUND_COLOR = (0, 0, 0)
MAX_BALL_SPEED_X = 7  # Velocidade máxima horizontal da bola (pode alterar se necesśario)
MAX_BALL_SPEED_Y = 10  # Velocidade máxima vertical da bola (pode alterar se necesśario)

# Controla a raquete do jogador. Ela se move horizontalmente com as teclas ← e →
# e tem uma função para desenhá-la na tela
class Paddle:
    def __init__(self, given_screen):
        self.screen = given_screen
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.rect = pg.Rect(
            (SCREEN_WIDTH // 2) - (self.width // 2),
            SCREEN_HEIGHT - 46,
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

    def fill(self):
        # Faz a raquete ocupar a área toda horizontal quando em menu
        self.rect.width = SCREEN_WIDTH
        self.rect.x = max(0, min(0, SCREEN_WIDTH))  # Ajusta para manter a raquete na tela

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
    def __init__(self, given_screen):
        self.screen = given_screen
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
        self.score = 0
        self.ball_hits = 0
        self.ball_tick = 0 # Serve apenas para evitar multiplos hits quando atingir as bordas
        self.can_hit_brick = False # Evitar bola de atingir tijolos incorretamente

    def move(self, on_menu):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Verifica colisões com as bordas da tela
        if self.rect.left <= 10 or self.rect.right >= SCREEN_WIDTH - 10:
            self.speed_x = -self.speed_x
            if not on_menu:
                WALL_SFX.play()
        if self.rect.top <= 25:
            self.speed_y = -self.speed_y
            self.can_hit_brick = True

            if not on_menu:
                WALL_SFX.play()


    def check_collision_with_paddle(self, paddle, on_menu):
        if self.rect.colliderect(paddle.rect):
            # Calcular a posição relativa de colisão
            relative_collision_x = (self.rect.centerx - paddle.rect.left) / paddle.width
            # O valor varia entre -1.0 (esquerda) e 1.0 (direita)
            offset = (relative_collision_x - 0.5) * 2

            # Aumentar velocidade vertical da bola em diferentes intervalos
            if self.ball_tick >= PADDLE_DELAY and not on_menu:
                self.ball_tick = 0
                self.ball_hits += 1
                PADDLE_SFX.play()

            if self.ball_hits == 4:
                self.speed_y = abs(self.speed_y) + 2
            elif self.ball_hits == 12:
                self.speed_y = abs(self.speed_y) + 2

            # Ajustar as velocidades de acordo com o local de colisão e velocidade máxima
            if not on_menu:
                self.speed_x += offset * MAX_BALL_SPEED_X
            self.speed_x = max(min(self.speed_x, MAX_BALL_SPEED_X), -MAX_BALL_SPEED_X)
            self.speed_y = max(min(self.speed_y, MAX_BALL_SPEED_Y), -MAX_BALL_SPEED_Y)

            # Inverter a direção vertical (a bola sempre quica para cima)
            self.speed_y = -abs(self.speed_y)

            # Permitir atingir tijolos novamente
            self.can_hit_brick = True

    def check_collision_with_brick(self, current_wall, on_menu):
        for row in range(ROWS):
            for col in range(COLUMNS):
                brick = current_wall.bricks[row][col]

                # Verificar condições do tijolo
                if brick[1] > 0 and brick[0].colliderect(self.rect) and self.can_hit_brick:
                    # Apenas maximiza velocidade Y se atingir tijolos laranja e vermelho
                    if brick[1] == 3 or brick[1] == 4 and abs(self.speed_y) < MAX_BALL_SPEED_Y:
                        self.speed_y = MAX_BALL_SPEED_Y
                    else:
                        self.speed_y = -self.speed_y

                    if not on_menu:
                        brick[1] = 0  # Quebra o tijolo
                        self.score += brick[2]  # Adicionar pontos
                        BRICK_SFX.play()

                    self.rect.y += self.speed_y  # Move a bola para longe do tijolo
                    self.can_hit_brick = False
                    break


    def reset(self):
        # Define uma posição inicial aleatória próxima ao centro da tela
        random_offset_x = random.randint(-100, 100)
        random_offset_y = random.randint(-50, 50)
        self.rect.x = (SCREEN_WIDTH // 2) - (self.width // 2) + random_offset_x
        self.rect.y = (SCREEN_HEIGHT // 2) - (self.height // 2) + random_offset_y

        # Define uma direção aleatória para a bola
        self.speed_x = random.uniform(-BALL_SPEED, BALL_SPEED)
        self.speed_y = BALL_SPEED  # A bola sempre começa indo para baixo
        self.can_hit_brick = True
        self.ball_hits = 0

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

#classe para configurar os tijolos
class Brick:
    #função principal
    def __init__(self):
        self.live_ball = False
        self.bricks = None
        self.width = (SCREEN_WIDTH - 20) // COLUMNS
        self.height = 14

    #função pra criar os tijolos
    def wall_create(self):
        strength = 0
        worth = 0
        self.bricks = []

        for row in range(ROWS):
            brick_row = []
            for col in range(COLUMNS):
                brick_x = col * self.width + 14
                brick_y = row * self.height + 130
                rect = pg.Rect(brick_x, brick_y, self.width, self.height)
                #strength of bricks
                if row < 2:
                    strength = 4
                    worth = 7
                elif row < 4:
                    strength = 3
                    worth = 5
                elif row < 6:
                    strength = 2
                    worth = 3
                elif row < 8:
                    strength = 1
                    worth = 1
                individual_bricks = [rect, strength, worth]
                brick_row.append(individual_bricks)
            self.bricks.append(brick_row)

    def wall_draw(self):
        for row in self.bricks:
            for brick in row:
                brick_col = None

                if brick[1] > 0:
                    if brick[1] == 4:
                        brick_col = BRICK_RED
                    elif brick[1] == 3:
                        brick_col = BRICK_ORANGE
                    elif brick[1] == 2:
                        brick_col = BRICK_GREEN
                    elif brick[1] == 1:
                        brick_col = BRICK_YELLOW
                    pg.draw.rect(screen, brick_col, brick[0])
                    pg.draw.rect(screen, BACKGROUND_COLOR, (brick[0]), 2)
                else:
                    pg.draw.rect(screen, BACKGROUND_COLOR, (brick[0]), 2)
                    pg.draw.rect(screen, COLOR_BLACK, brick[0])

    #desenha a borda do jogo

    def draw_border(self):
        # Desenhar bordas brancas: topo, esquerda e direita
        pg.draw.rect(screen, COLOR_WHITE, (0, 0, SCREEN_WIDTH, 25))  # Borda superior
        pg.draw.rect(screen, COLOR_WHITE, (0, 0, 10, SCREEN_HEIGHT))  # Borda esquerda
        pg.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))  # Borda direita

        # Desenhar "tijolos" coloridos
        pg.draw.rect(screen, BRICK_RED, (0, 130, SCREEN_WIDTH, 28))  # Borda superior vermelha
        pg.draw.rect(screen, BRICK_ORANGE, (0, 158, SCREEN_WIDTH, 28))  # Borda laranja
        pg.draw.rect(screen, BRICK_GREEN, (0, 186, SCREEN_WIDTH, 28))  # Borda verde
        pg.draw.rect(screen, BRICK_YELLOW, (0, 214, SCREEN_WIDTH, 28))  # Borda amarela

        paddle_width = 10
        paddle_height = 30
        paddle_offset = 25

        # Paddle esquerdo
        pg.draw.rect(screen, PADDLE_COLOR,
                     (0, SCREEN_HEIGHT - paddle_height - paddle_offset, paddle_width, paddle_height))

        # Paddle direito
        pg.draw.rect(screen, PADDLE_COLOR, (
        SCREEN_WIDTH - paddle_width, SCREEN_HEIGHT - paddle_height - paddle_offset, paddle_width, paddle_height))

        # Desenhar a parede de tijolos
        self.wall_draw()


wall = Brick()

# Contém o loop principal do jogo, que lida com eventos,
# atualiza o estado do jogo e desenha os objetos na tela.
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Breakout')
        self.clock = pg.time.Clock()
        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)
        self.brick = Brick()

        self.points_text = points_string
        self.attempts_text = attempts_string

        self.paddle_shrinked = False  # Controle se a raquete já foi reduzida
        self.waiting_start = True  # Verificar se a partida foi inciada
        self.attempts = 1

        self.brick.wall_create()
        self.brick.draw_border()

    def run(self):
        # Loop principal do jogo
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw()
            self.clock.tick(60)

    def reset_values(self):
        # Espera até que uma tecla seja pressionada
        self.paddle.reset()
        self.ball.reset()
        self.attempts = 1
        self.ball.score = 0
        self.paddle_shrinked = False
        self.waiting_start = False
        self.brick.wall_create()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and self.waiting_start:
                self.reset_values()

    def update_game_state(self):
        keys = pg.key.get_pressed()
        self.paddle.move(keys)
        self.ball.draw()
        self.ball.move(self.waiting_start)
        self.ball.check_collision_with_paddle(self.paddle, self.waiting_start)
        self.ball.check_collision_with_brick(self.brick, self.waiting_start)
        self.ball.ball_tick += 1

        self.points_text = NORMAL_FONT.render(str("{:03d}".format(self.ball.score)), True, COLOR_WHITE)
        self.attempts_text = NORMAL_FONT.render(str(self.attempts), True, COLOR_WHITE)

        # Verifica se a bola atingiu o topo da tela
        if self.ball.rect.top <= 0:
            self.ball.can_hit_brick = True

            if not self.paddle_shrinked and not self.waiting_start:
                self.paddle.shrink()  # Reduz a raquete
                self.paddle_shrinked = True  # Marca que a raquete já foi reduzida

        # Verifica se a bola caiu fora da tela e aplicar punição
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.reset()
            self.paddle.reset()
            self.attempts += 1
            self.paddle_shrinked = False
            self.attempts_text = NORMAL_FONT.render(str(self.attempts), True, COLOR_WHITE)

            if self.attempts > MAX_ATTEMPTS:
                # Bloqueia a partida
                self.waiting_start = True


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.brick.draw_border()
        self.brick.wall_draw()
        if self.waiting_start: # Mudar raquete em menu
            self.paddle.fill()
        else:
            self.paddle.rect.width = PADDLE_WIDTH

        self.paddle.draw()
        self.ball.draw()
        self.screen.blit(self.points_text, points_text_rect)
        self.screen.blit(self.attempts_text, attempts_text_rect)
        self.screen.blit(points_string_2, points_text_rect_2)
        self.screen.blit(attempts_string_2, attempts_text_rect_2)

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()