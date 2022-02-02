import turtle

def desenhar_triangulo(x,y):
    #posicionando o pincel nas coordenadas do mouse
    desenho.penup()
    desenho.setposition(x,y)
    desenho.pendown()

    #desenhando a partir das coordenadas do mouse
    desenho.forward(100)
    desenho.left(120)
    for i in range(2):
        desenho.forward(200)
        desenho.left(120)
    desenho.forward(100)


desenho = turtle.Turtle()

#definindo o que fazer quando se clica na tela
turtle.onscreenclick(desenhar_triangulo)
turtle.listen()

turtle.done()