#create a Maze game!

from pygame import *

#parent class for sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        #every image must store the image property
        self.image = transform.scale(image.load(player_image), (width, height))
        self.player_speed = player_speed
        #every sprite must have the rect property
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        self.dirX = 0
        self.dirY = 0
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.player_speed
            self.dirX = -1
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.player_speed
            self.dirX = 1
        if keys[K_UP] and self.rect.y > 0 :
            self.rect.y -= self.player_speed
            self.dirY = -1
        if keys[K_DOWN] and self.rect.y < win_height - 60:
            self.rect.y += self.player_speed
            self.dirY = 1

class Enemy(GameSprite):
    direction = "left"
    def update(self, minBound, maxBound):
        if self.rect.x <= minBound:
            self.direction = "right"
        if self.rect.x >= maxBound:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.player_speed
        else:
            self.rect.x += self.player_speed

    def updateVertical(self, minBound, maxBound):
        direction = "down"
        if self.rect.y <= minBound:
            self.direction = "up"
        if self.rect.y >= maxBound:
            self.direction = "down"

        if self.direction == "down":
            self.rect.y -= self.player_speed
        else:
            self.rect.y += self.player_speed

#Game display
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = GameSprite('Carpet_Texture.png',0,0, win_width, win_height, 0)

#Game characters:
character1 = Player("Player_Sprite.png",5, win_height - 75,60,60,3)
monster1 = Enemy('Smiler.png', win_width - 300, win_height - 75,75,75,5)
monster2 = Enemy('Smiler.png', win_width - 475, 20 ,75,75,4)
monster3 = Enemy('Smiler.png', win_width - 200, win_height - 75,75,75,4.5)
treasure1 = GameSprite('treasure.png', win_width - 115, win_height - 75,70,70,4)
wall = GameSprite('Backrooms_Wallpaper.png', 360, 120, 15, 400, 4)
wall2 = GameSprite('Backrooms_Wallpaper.png', 0, 120, 290, 15, 4)

game = True
clock = time.Clock()
FPS = 60

font.init()
font = font.SysFont("Times New Roman", 70)
win = font.render(':)', True, (0, 255, 0))
lose = font.render(':(', True, (255, 0, 0))

#Music
mixer.init()
mixer.music.load('Level0.mp3')
mixer.music.play(-1)

finish = False

money = mixer.Sound('money.ogg')
kick = mixer.Sound('Lost.wav')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        character1.update()
        monster1.updateVertical(50,win_height - 60)
        monster2.update(135,win_height - 60)
        monster3.updateVertical(45,win_height - 60)
        background.reset()
        wall.reset()
        wall2.reset()
        character1.reset()
        treasure1.reset()
        monster1.reset()
        monster2.reset()
        monster3.reset()

    #Game Over
    if sprite.collide_rect(character1, monster1) or sprite.collide_rect(character1, monster2) or sprite.collide_rect(character1, monster3):
        window.blit(lose, (200, 200))
        kick.play()
        mixer.music.stop()
        character1.image = transform.scale(image.load("Player_Sprite_Dead.png"), (60, 60))
        character1.reset()
        finish = True

    if sprite.collide_rect(character1, treasure1):
        window.blit(win, (200, 200))
        money.play()
        mixer.music.stop()
        finish = True

    if sprite.collide_rect(character1, wall) or sprite.collide_rect(character1, wall2):
        if character1.dirX > 0:
            character1.rect.x -= character1.player_speed
        if character1.dirX < 0:
            character1.rect.x += character1.player_speed
        if character1.dirY > 0:
            character1.rect.y -= character1.player_speed
        if character1.dirY < 0:
            character1.rect.y += character1.player_speed

#----------------------------------------------------

    display.update()
    clock.tick(FPS)

