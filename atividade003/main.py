import turtle
import os

# draw screen
screen = turtle.Screen()
screen.title("My Pong")
screen.bgcolor("black")
screen.setup(800, 600)
screen.tracer(0)

# Draw Paddle 1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape("square")
paddle_1.color("white")
paddle_1.shapesize(stretch_wid=5, stretch_len=1)
paddle_1.penup()
paddle_1.goto(-350, 0)

# Draw Paddle 2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("white")
paddle_2.shapesize(stretch_wid=5, stretch_len=1)
paddle_2.penup()
paddle_2.goto(350, 0)

# Draw Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = 1

# draw HUD
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
hud.write("0 : 0", align="center", font=("Small Fonts", 24, "normal"))


def paddle_1_up():
    y = paddle_1.ycor()
    if y < 250:
        if y + 30 >= 250:
            y = 250
        else:
            y += 30
    else:
        y = 250
    paddle_1.sety(y)


def paddle_1_down():
    y = paddle_1.ycor()
    if y > -250:
        if y - 30 <= -250:
            y = -250
        else:
            y += -30
    else:
        y = -250
    paddle_1.sety(y)


def paddle_2_up():
    y = paddle_2.ycor()
    if y < 250:
        if y + 30 >= 250:
            y = 250
        else:
            y += 30
    else:
        y = 250
    paddle_2.sety(y)


def paddle_2_down():
    y = paddle_2.ycor()
    if y > -250:
        if y - 30 <= -250:
            y = -250
        else:
            y += -30
    else:
        y = -250
    paddle_2.sety(y)


# keyboard
screen.listen()
screen.onkeypress(paddle_1_up, "w")
screen.onkeypress(paddle_1_down, "s")

screen.onkeypress(paddle_2_up, "Up")
screen.onkeypress(paddle_2_down, "Down")

# scores
score_1 = 0
score_2 = 0

ball.speed("slowest")

while True:
    screen.update()

    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # collision with the upper wall
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # collision with the upper wall
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Collision with the paddle 1
    if ball.xcor() < -330 and paddle_1.ycor() + 50 > ball.ycor() > paddle_1.ycor() - 50:
        ball.dx *= -1

    # Collision with the paddle 2
    if ball.xcor() > 330 and paddle_2.ycor() + 50 > ball.ycor() > paddle_2.ycor() - 50:
        ball.dx *= -1

    # collision with left wall
    if ball.xcor() < -390:
        score_2 += 1
        hud.clear()
        hud.write(f"{score_1} : {score_2}", align="center", font=("Small Fonts", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with left wall
    if ball.xcor() > 390:
        score_1 += 1
        hud.clear()
        hud.write(f"{score_1} : {score_2}", align="center", font=("Small Fonts", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1
