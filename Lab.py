from pygame import *

win_width = 700
win_height = 500

win = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load('Fon.png'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = speed
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
      
class Enemy(GameSprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__(player_image, x, y, speed)
        self.direction = "left"
        
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
            
        if self.rect.x >= win_width - 85:
            self.direction = "left"
            
        if self.direction == "left":
            self.rect.x -=self.speed

        if self.direction == "right":
            self.rect.x += self.speed
 
            
class Wall(sprite.Sprite):
    def __init__(self, color, x, y, w, h):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h
        
        self.image = Surface((self.w, self.h))
        self.image.fill((color))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                   
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
               
            
game = True
finish = False
clock = time.Clock()
FPS = 60

player = Player('Per.png', 5, win_height - 80, 4)
monster = Enemy('Zloy.png', win_width - 80, 280, 2)
scarb = GameSprite('Scarb.png', win_width - 80, win_height - 80, 5)

w1 = Wall((154, 205, 50), 100, 20, 450, 10)
w2 = Wall((154, 205, 50), 100, 480, 350, 10)
w3 = Wall((154, 205, 50), 100, 20, 10, 380)
w4 = Wall((154, 205, 50), 200, 130, 10, 350)
w5 = Wall((154, 205, 50), 450, 130, 10, 360)
w6 = Wall((154, 205, 50), 300, 20, 10, 350)
w7 = Wall((154, 205, 50), 390, 120, 130, 10)

w_list = [w1, w2, w3, w4, w5, w6, w7]

mixer.init()

mixer.music.load('muzyka-super-mario.mp3')
mixer.music.play(100)

lose_sound = mixer.Sound('game-over-mario.mp3')
win_sound = mixer.Sound('fanfary-pobedy-mar.mp3')

font.init()
f = font.Font(None, 70)
win_text = f.render("YOU WIN", True, (255, 215, 0))
lose_text = f.render("YOU LOSE", True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:        
        win.blit(background, (0, 0))
        player.update()
        player.reset()
        monster.update()
        monster.reset()
        scarb.update()    
        scarb.reset()
        
        for w in w_list:
            w.reset()
            if player.rect.colliderect(monster.rect) or player.rect.colliderect(w.rect):
                finish = True
                win.blit(lose_text, (200, 200))
                lose_sound.play()
                mixer.music.stop()
                
        if player.rect.colliderect(scarb.rect):
            finish = True
            win.blit(win_text, (200, 200))
            win_sound.play()
            mixer.music.stop()
            

    display.update()
    clock.tick(FPS)
