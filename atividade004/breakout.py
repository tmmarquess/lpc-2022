from random import randint, choice
import pygame
from sys import exit


# Class of the Obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, coord: tuple):
        super().__init__()
        self.image = pygame.Surface((35, 15))
        self.image.fill(colors[obstacle_type])
        self.rect = self.image.get_rect(topleft=coord)
        if obstacle_type == 0:
            self.score = 7
        elif obstacle_type == 1:
            self.score = 5
        elif obstacle_type == 2:
            self.score = 3
        else:
            self.score = 1


# Class of the ball
class Ball(pygame.sprite.Sprite):
    def __init__(self, coordinates: tuple):
        super().__init__()
        self.image = pygame.surface.Surface((10, 10))
        self.image.fill("#D2D2D2")
        self.rect = self.image.get_rect(center=coordinates)  # (263, 379)
        self.dx = choice([-2, 2])
        self.dy = 2

    def update_ball(self):
        global half_paddle, paddle_sound

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx *= -1
            paddle_sound.play().set_volume(0.1)

        if self.rect.x >= 516:
            self.rect.x = 516
            self.dx *= -1
            paddle_sound.play().set_volume(0.1)

        if self.rect.y <= 0:
            self.rect.y = 0
            self.dy *= -1

            paddle_sound.play().set_volume(0.1)

            if half_paddle is not True:
                paddle.sprite.image = pygame.surface.Surface((35 / 2, 15))
                paddle.sprite.image.fill("#00476D")
                paddle.sprite.rect = paddle.sprite.image.get_rect(center=paddle.sprite.rect.center)
                half_paddle = True

        if self.rect.y >= 758:
            ball_death()
            self.kill()

    def update(self):
        self.update_ball()


# Class of the paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self, first: bool):
        super().__init__()
        if first:
            self.image = pygame.surface.Surface((263 * 2, 15))
        else:
            self.image = pygame.surface.Surface((35, 15))
        self.image.fill("#00476D")
        self.rect = self.image.get_rect(midbottom=(263, 724))
        self.speed = 5

    def player_input(self):
        if game_active is not True:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > 526:
            self.rect.right = 526

    def update(self):
        self.player_input()


# Class for text inputs
class Texto(pygame.sprite.Sprite):
    def __init__(self, texto, coord: tuple):
        super().__init__()
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render(texto, False, "white")
        self.rect = self.image.get_rect(midtop=coord)

    def update_text(self, text):
        self.image = self.font.render(text, False, "white")


# Function to check collision between the ball and the paddle
def ball_paddle_collision():
    collision = pygame.sprite.spritecollide(ball.sprite, paddle, False)
    if collision:
        global paddle_sound
        paddle_sound.play().set_volume(0.1)

        if collision[0].rect.collidepoint(ball.sprite.rect.midbottom):
            ball.sprite.dy *= -1

        elif collision[0].rect.collidepoint(ball.sprite.rect.bottomleft):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.bottomleft = collision[0].rect.topright

        elif collision[0].rect.collidepoint(ball.sprite.rect.bottomright):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.bottomright = collision[0].rect.topleft

        if collision[0].rect.collidepoint(ball.sprite.rect.midleft):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.left = collision[0].rect.right

        elif collision[0].rect.collidepoint(ball.sprite.rect.topleft):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.topleft = collision[0].rect.bottomright

        if collision[0].rect.collidepoint(ball.sprite.rect.midright):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.right = collision[0].rect.left

        elif collision[0].rect.collidepoint(ball.sprite.rect.topright):
            ball.sprite.dx *= -1
            ball.sprite.dy *= -1
            ball.sprite.rect.topright = collision[0].rect.bottomleft


# Function to check collision between the ball and an obstacle
def ball_obstacle_collision():
    if game_active is not True:
        collision = pygame.sprite.spritecollide(ball.sprite, obstacles, False)
    else:
        collision = pygame.sprite.spritecollide(ball.sprite, obstacles, True)

    if collision:
        global break_sound
        break_sound.play().set_volume(0.1)
        for obstacle in collision:

            update_score(obstacle.score)

            if obstacle.rect.collidepoint(ball.sprite.rect.midtop):
                ball.sprite.dy *= -1
                ball.sprite.rect.top = obstacle.rect.bottom

            if obstacle.rect.collidepoint(ball.sprite.rect.midbottom):
                ball.sprite.dy *= -1
                ball.sprite.rect.bottom = obstacle.rect.top

            if obstacle.rect.collidepoint(ball.sprite.rect.midright):
                ball.sprite.dx *= -1
                ball.sprite.rect.right = obstacle.rect.left

            if obstacle.rect.collidepoint(ball.sprite.rect.midleft):
                ball.sprite.dx *= -1
                ball.sprite.rect.left = obstacle.rect.right

            if obstacle.rect.collidepoint(ball.sprite.rect.topleft):
                ball.sprite.dx *= -1
                ball.sprite.dy *= -1
                ball.sprite.rect.topleft = obstacle.rect.bottomright

            if obstacle.rect.collidepoint(ball.sprite.rect.topright):
                ball.sprite.dx *= -1
                ball.sprite.dy *= -1
                ball.sprite.rect.topright = obstacle.rect.bottomleft

            if obstacle.rect.collidepoint(ball.sprite.rect.bottomleft):
                ball.sprite.dx *= -1
                ball.sprite.dy *= -1
                ball.sprite.rect.bottomleft = obstacle.rect.topright

            if obstacle.rect.collidepoint(ball.sprite.rect.bottomright):
                ball.sprite.dx *= -1
                ball.sprite.dy *= -1
                ball.sprite.rect.bottomright = obstacle.rect.topleft

            if game_active is True:
                update_ball_speed(obstacle.score)
                if len(obstacles) == 0:
                    update_round()


def update_round():
    global second_round, ball_on_screen, counter_4, counter_12
    if second_round is not True:
        second_round = True

        draw_obstacles()

        ball.empty()

        ball_on_screen = False
        paddle.sprite.speed = 5
        counter_4 = counter_12 = 0


# Function to update ball speed according to the conditions
def update_ball_speed(obstacle_score):
    global counter_4, counter_12

    counter_4 += 1
    counter_12 += 1

    if counter_4 % 4 == 0 or counter_12 % 12 == 0 or 7 >= obstacle_score >= 5:
        dx = ball.sprite.dx
        dy = ball.sprite.dy
        negative_x = False
        negative_y = False

        if dx < 0:
            negative_x = True
            dx *= -1
        if dy < 0:
            negative_y = True
            dy *= -1

        dx += 0.4
        dy += 0.4

        if negative_x is True:
            dx *= -1
        if negative_y is True:
            dy *= -1

        ball.sprite.dx = dx
        ball.sprite.dy = dy

        update_paddle_speed()


# Function to update the paddle speed
def update_paddle_speed():
    paddle.sprite.speed += 0.2


# Function to update the attempt and check if it's over 3
def update_attempt():
    global attempt
    attempt += 1
    texts.sprites()[2].update_text(f"{attempt}")

    if attempt == 4:
        game_over()


# Function to reset the score
def reset_score():
    global score
    score = 0
    texts.sprites()[1].update_text(f"{score}")


# Function to update the score
def update_score(points):
    if game_active is True:
        global score
        score += points
        texts.sprites()[1].update_text(f"{score}")


# Function to end the game
def game_over():
    global game_active, attempt, ball_on_screen
    attempt = 0
    paddle.empty()
    game_active = False
    ball_on_screen = True
    start_screen()


# Function to create Obstacles on screen
def draw_obstacles():
    # Obstacles coordinates
    x = 0
    y = 80

    # Distance from one obstacle to another
    dist = 0
    # type of the obstacle
    obstacle_type = 0
    for i in range(4):
        for j in range(2):
            for k in range(14):
                obstacles.add(Obstacle(obstacle_type, (x, y + dist)))
                x += 38
            x = 0
            dist += 17
        obstacle_type += 1


# Function for when the ball dies
def ball_death():
    global ball_on_screen, counter_4, counter_12, half_paddle
    ball_on_screen = False

    if half_paddle is True:
        paddle.sprite.image = pygame.surface.Surface((35, 15))
        paddle.sprite.image.fill("#00476D")
        paddle.sprite.rect = paddle.sprite.image.get_rect(midbottom=paddle.sprite.rect.midbottom)
        half_paddle = False

    paddle.sprite.speed = 5
    counter_4 = counter_12 = 0

    update_attempt()


# Function to show an arcade main screen
def start_screen():
    paddle.add(Paddle(True))
    ball.add(Ball((randint(20, 506), randint(250, 379))))


def start_font():
    global game_active
    if game_active:
        return 0
    start_surface = test_font.render('Press space key', False, 'White')
    start_rectangle = start_surface.get_rect(center=(263, 420))
    screen.blit(start_surface, start_rectangle)


# Initializing Pygame Instance
pygame.init()

# Obstacle colors
colors = ("#9F0800", "#BF6B04", "#008022", "#BFB417")

# Defining sounds
break_sound = pygame.mixer.Sound("break.mp3")
paddle_sound = pygame.mixer.Sound("pong_bounce.wav")

# initiating the pygame Screen
screen = pygame.display.set_mode((263 * 2, 379 * 2))
pygame.display.set_caption("Breakout")

# the clock that defines the speed of the loop
clock = pygame.time.Clock()

# the game using a default font
test_font = pygame.font.Font(None, 50)

# Defines if the game is active
game_active = False

# Defines if it is the 2nd round of obstacles
second_round = False

# Defines if the ball exists
ball_on_screen = True

# Defines if the paddle size is half
half_paddle = False

# Defines the player Score
score = 0

# Number of the current attempt
attempt = 0

# Speed Counters
counter_4 = 0
counter_12 = 0

# Creating the Sprite group of obstacles
obstacles = pygame.sprite.Group()

# Paddle Group
paddle = pygame.sprite.GroupSingle()

# Ball Group
ball = pygame.sprite.GroupSingle()

# Text Group
texts = pygame.sprite.Group()

texts.add(Texto("1", (20, 5)))
texts.add(Texto(f"{score}", (40, 40)))
texts.add(Texto(f"{attempt}", (283, 5)))

draw_obstacles()
start_screen()
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_active is not True:
                obstacles.empty()
                draw_obstacles()

                update_attempt()

                reset_score()

                paddle.empty()
                paddle.add(Paddle(False))

                game_active = True

                ball_on_screen = False
                ball.empty()

            else:
                if ball_on_screen is not True:
                    ball.add(Ball((randint(20, 506), randint(250, 379))))
                    ball_on_screen = True

    screen.fill("black")

    obstacles.draw(screen)
    obstacles.update()

    paddle.draw(screen)
    paddle.update()

    ball.draw(screen)
    ball.update()

    texts.draw(screen)
    texts.update()

    start_font()
    
    if ball_on_screen is True:
        ball_paddle_collision()
        ball_obstacle_collision()

    pygame.display.update()
    clock.tick(60)
