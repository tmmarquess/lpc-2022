import math
import random
import turtle


def desenhar_quadrados():
    """Desenha os quadrados com lado de tamanho igual aos
    n primeiros termos da sequencia de fibonacci
    """
    # Variáveis para Fibonacci
    fibonacci = 1
    anterior = 0

    # Definindo a cor da caneta
    desenho.pencolor("blue")

    # Primeiro quadrado
    for i in range(4):
        desenho.forward(fibonacci * escala)
        desenho.left(90)
    desenho.right(90)

    # Seguindo na sequência de fibonacci
    temporario = fibonacci
    fibonacci += anterior
    anterior = temporario

    # Desenhando resto dos quadrados
    for i in range(1, n):
        # Voltando para a ultima linha
        desenho.backward(anterior * escala)
        desenho.right(90)
        # Terminando o próximo quadrado a
        # partir dessa linha ja desenhada
        for j in range(3):
            desenho.forward(fibonacci * escala)
            desenho.left(90)
        desenho.right(90)

        # Seguindo na sequência de fibonacci
        temporario = fibonacci
        fibonacci += anterior
        anterior = temporario

    # Voltando o pincel para a origem
    desenho.penup()
    desenho.setposition(escala, 0)
    desenho.seth(90)
    desenho.pendown()


def desenhar_espiral():
    """Desenha a espiral de acordo com a escala com raio de acordo
    com os n primeiros termos da sequencia de fibonacci
    """
    # Variáveis para Fibonacci
    fibonacci = 1
    anterior = 0

    for i in range(n):
        # Imprimindo o raio do quarto de circunferencia na tela
        print(fibonacci)

        desenho.pencolor(
            aleatorio.randint(0, 255),
            aleatorio.randint(0, 255),
            aleatorio.randint(0, 255),
        )

        # Definindo a distância que o pincel irá andar
        andar = math.pi * fibonacci * escala / 2
        andar /= 90
        for j in range(90):
            desenho.forward(andar)
            desenho.left(1)

        # Seguindo na sequência de fibonacci
        temporario = fibonacci
        fibonacci += anterior
        anterior = temporario


# Configurando a tela do turtle
desenho = turtle.Turtle()
turtle.colormode(255)
turtle.bgcolor("black")
turtle.title("Espiral de Fibonacci")
desenho.speed("fastest")

# Escala do desenho
escala = 12

# Repetição da sequencia
n = 8

# mudando o modo de cor do Turtle e
# iniciando o algoritimo aleatório
turtle.colormode(255)
aleatorio = random.Random()

desenhar_quadrados()
desenhar_espiral()

turtle.done()
