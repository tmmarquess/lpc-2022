import turtle

def desenhar_y(tamanho,nivel):
    """Desenha a arvore a partir do tamanho de linha
     e quantidade de níveis definidas
    """
    if nivel > 0:
        #Definindo a cor da caneta
        turtle.colormode(255)
        caneta.pencolor(0, 255 // nivel, 0)

        #Desenhando a linha
        caneta.forward(tamanho)
        caneta.right(angulo)

        desenhar_y(tamanho * 0.8, nivel-1)

        caneta.left(2 * angulo)
        caneta.pencolor(0, 255 // nivel, 0)

        desenhar_y(tamanho * 0.8, nivel-1)

        caneta.pencolor(0, 255 // nivel, 0)

        caneta.right(angulo)
        caneta.forward(-1 * tamanho)

#Configurando a caneta do turtle
caneta = turtle.Turtle()
caneta.speed('fastest')
caneta.left(90)

#Comprimento da linha inicial
tamanho = 80

#Quantas curvas a linha irá fazer
niveis = 7

#Angulo entre essas linhas
angulo = 30

desenhar_y(tamanho,niveis)

turtle.done()