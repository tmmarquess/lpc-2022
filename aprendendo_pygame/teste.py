from pickletools import pyfloat
from random import randint, choice
import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame1 = pygame.image.load("graphics\Player\player_walk_1.png").convert_alpha()
        self.frame2 = pygame.image.load("graphics\Player\player_walk_2.png").convert_alpha()
        self.jump = pygame.image.load("graphics\Player\jump.png").convert_alpha()
        self.stand = pygame.image.load("graphics\Player\player_stand.png").convert_alpha()
        self.frames = [self.frame1,self.frame2]
        self.image = self.frame1
        self.rect = self.frame1.get_rect(midbottom = (80,300))
        self.index = 0
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio\jump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300 and game_active is True:
            self.gravity = -20 
            self.jump_sound.play()
        if keys[pygame.K_d]:
            self.rect.x += 3
        if keys[pygame.K_a]:
            self.rect.x -= 3
        
    
    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if(self.rect.midbottom[1] > 300):
            self.rect.midbottom = (self.rect.midbottom[0],300)

    def update_animation(self):
        keys = pygame.key.get_pressed()

        if self.rect.bottom < 300:
            self.image = self.jump
        elif keys[pygame.K_a] or keys[pygame.K_d]:
            self.index += 0.1
            if self.index >= len(self.frames):
                self.index = 0
            self.image = self.frames[int(self.index)]
        else:
            self.image = self.stand

    def update(self) :
        self.player_gravity()
        self.player_input()
        self.update_animation()

class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "fly":
            fly_walk1 = pygame.image.load("graphics\Fly\Fly1.png").convert_alpha()
            fly_walk2 = pygame.image.load("graphics\Fly\Fly2.png").convert_alpha()
            self.frames = [fly_walk1,fly_walk2]
            y_pos = 200
        else:
            snail_walk1 = pygame.image.load("graphics\snail\snail1.png").convert_alpha()
            snail_walk2 = pygame.image.load("graphics\snail\snail2.png").convert_alpha()
            self.frames = [snail_walk1,snail_walk2]
            y_pos = 300

        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def update_animation(self):
        self.rect.x -= 5
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.update_animation()
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()        


def sprite_collision():
    global obstacles
    if pygame.sprite.spritecollide(player.sprite,obstacles,False):
        obstacles.empty()
        return False
    else:
        return True
        

# Comando para inicializar o Pygame
pygame.init()

# comando para definir o tamanho da tela
screen = pygame.display.set_mode((800,400))

# comando para definir o nome da janela
pygame.display.set_caption("My game")

# Definindo clock para limitar atualizações da tela por segundo
clock = pygame.time.Clock()
start_time = 0

game_active = False

# Criando uma surface de teste
# test_surface = pygame.Surface((200,100))
# test_surface.fill("blue")

# Adicionando surfaces a partir de imagens
sky_surface = pygame.image.load("graphics\sky.png").convert()
ground_surface = pygame.image.load("graphics\ground.png").convert()

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = font.render(f"Time: {current_time // 1000}s",False,(64,64,64))
    score_rect = score.get_rect(center = (400,40))
    screen.blit(score,score_rect)

#Adicionando Surface de texto
#importando fonte 
font = pygame.font.Font("font\Pixeltype.ttf",50)
# Escrevendo texto na Surface

game_name = font.render("Pixel Runner",False,"#7CC6BA")
game_name_rect = game_name.get_rect(center = (400,80))

game_hint = font.render("Press Space to Start the game",False,"#7CC6BA")
game_hint_rect = game_hint.get_rect(center = (400,320))

atempt = 0
last_score = 0

bg_music = pygame.mixer.Sound("audio\music.wav")
bg_music.play(1).set_volume(0.2)

# HUD_surface  = font.render(texto,False,"black")
# HUD_rect = HUD_surface.get_rect(center = (400,10))

#Objeto animado
snail_walk1 = pygame.image.load("graphics\snail\snail1.png").convert_alpha()
snail_walk2 = pygame.image.load("graphics\snail\snail2.png").convert_alpha()
snail_rectangle = snail_walk1.get_rect(midbottom = (800,300))
snail_walk = [snail_walk1,snail_walk2]
snail_index = 0
snail_surface = snail_walk1

fly_walk1 = pygame.image.load("graphics\Fly\Fly1.png").convert_alpha()
fly_walk2 = pygame.image.load("graphics\Fly\Fly2.png").convert_alpha()
fly_walk = [fly_walk1,fly_walk2]
fly_index = 0
fly_surface = fly_walk1

alternate = randint(0,1)

obstacles = pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1  
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,100)

def obstacle_movement():
    global obstacle_rect_list, game_active, last_score, atempt,alternate
    if len(obstacle_rect_list) != 0:
        for obstacle in obstacle_rect_list:
            obstacle.x -= 5
            if obstacle.y == 160:
                screen.blit(fly_surface,obstacle)
            else:
                screen.blit(snail_surface,obstacle)
            
        
            if obstacle.x < -50:
                obstacle_rect_list.remove(obstacle)
            else:
                '''if player_rectangle.colliderect(obstacle):
                    game_active = False
                    print("vish kk")
                    last_score = pygame.time.get_ticks() - start_time
                    atempt += 1
                    alternate = randint(0,1)
                    obstacle_rect_list.clear()'''



#Surface do player
'''player_walk1 = pygame.image.load("graphics\Player\player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics\Player\player_walk_2.png").convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load("graphics\Player\jump.png").convert_alpha()
player_surface = player_walk[player_index]'''

player = pygame.sprite.GroupSingle()
player.add(Player())



'''def player_animation():
    global player_surface,player_index
    keys = pygame.key.get_pressed()

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    elif keys[pygame.K_a] or keys[pygame.K_d]:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    else:
        player_surface = player_stand'''
        

# player_rectangle = player_walk1.get_rect(midbottom = (100,300))
player_gravity = 0
player_stand = pygame.image.load("graphics\Player\player_stand.png").convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand_scaled.get_rect(center = (400,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
           # if player_rectangle.collidepoint(event.pos):
                # print("caos")
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_active is not True:
                '''player_rectangle.midbottom = (100,300)
                snail_rectangle.midbottom = (800,300)'''
                game_active = True
                start_time = pygame.time.get_ticks()
            else:
                '''if(player_rectangle.bottom == 300):
                    player_gravity = -20'''
        if game_active is True:
            if event.type == obstacle_timer:
                obstacles.add(obstacle(choice(["fly","snail","snail"])))

            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_walk[snail_index]
                    
            if event.type == snail_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_walk[fly_index]

            
    if game_active is True:
        # Adicionando as surfaces na tela
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        display_score()

       # pygame.draw.line(screen,"pink",HUD_rect.topleft,HUD_rect.bottomright,5)

       # screen.blit(HUD_surface,HUD_rect)   
        # screen.blit(snail_surface,snail_rectangle)
        '''player_animation()
        screen.blit(player_surface,player_rectangle)'''
        pygame.draw.circle(screen,"red",pygame.mouse.get_pos(),5)

        player.draw(screen)
        player.update()

        obstacles.draw(screen) 
        obstacles.update()

        game_active = sprite_collision()

        # obstacle_movement()

        '''if snail_rectangle.right < 0:
            snail_rectangle.left = 800
        else:
            snail_rectangle.x -= 5 '''

        '''if player_rectangle.colliderect(snail_rectangle):
            game_active = False
            print("vish kk")
            last_score = pygame.time.get_ticks() - start_time
            atempt += 1
            # HUD_surface  = font.render(f"Colisoes: {colisoes}",False,"black")'''

        '''if player_rectangle.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] is True:
                player_rectangle = player_walk1.get_rect(center = pygame.mouse.get_pos())'''

        keys = pygame.key.get_pressed()

        '''if(player_rectangle.right < 0):
            player_rectangle.left = 800
        if player_rectangle.left > 800:
            player_rectangle.right = 0'''

    else:
        screen.fill("#5D81A1")
        screen.blit(player_stand_scaled,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        screen.blit(game_hint,game_hint_rect)
        if atempt != 0:
            text_score = font.render(f"Last Score: {last_score // 1000}",False,"#7CC6BA")
            score_rect = text_score.get_rect(center = (400, 370))
            screen.blit(text_score,score_rect)


    # Comando para aplicar atualizações na tela
    pygame.display.update()
    #Comando para limitar um máximo de 60 atualizações por segundo
    clock.tick(60)
