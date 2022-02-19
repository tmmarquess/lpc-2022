import pygame
from random import choice, randint


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

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx *= -1

        if self.rect.x >= 516:
            self.rect.x = 516
            self.dx *= -1

        if self.rect.y <= 0:
            self.rect.y = 0
            self.dy *= -1

        if self.rect.y >= 758:
            self.kill()

    def update(self):
        self.update_ball()


# Class of the paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((35, 15))
        self.image.fill("#00476D")
        self.rect = self.image.get_rect(midbottom=(263, 724))
        self.speed = 5

    def player_input(self):

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


# Function to check collision between the ball and the paddle
def ball_paddle_collision():
    collision = pygame.sprite.spritecollide(ball.sprite, paddle, False)
    if collision:

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
    collision = pygame.sprite.spritecollide(ball.sprite, obstacles, True)

    if collision:

        for obstacle in collision:

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


# Initializing Pygame Instance
pygame.init()

# Obstacle colors
colors = ("#9F0800", "#BF6B04", "#008022", "#BFB417")

# initiating the pygame Screen
screen = pygame.display.set_mode((263 * 2, 379 * 2))
pygame.display.set_caption("Breakout")

# the clock that defines the speed of the loop
clock = pygame.time.Clock()

# Creating the Sprite group of obstacles
obstacles = pygame.sprite.Group()

# Paddle Group
paddle = pygame.sprite.GroupSingle()
paddle.add(Paddle())

# Ball Group
ball = pygame.sprite.GroupSingle()
ball.add(Ball((randint(20, 506), randint(250, 379))))

draw_obstacles()
# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")

    obstacles.draw(screen)
    obstacles.update()

    paddle.draw(screen)
    paddle.update()

    ball.draw(screen)
    ball.update()

    ball_paddle_collision()
    ball_obstacle_collision()

    pygame.display.update()
    clock.tick(60)
