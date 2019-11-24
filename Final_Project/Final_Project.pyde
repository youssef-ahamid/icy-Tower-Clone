add_library('minim')
import os, random
path = os.getcwd()
player = Minim(this)


class Platform:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
        self.h = 50
        self.vy = 0
        # self.img = loadImage(path + "/" + img + ".png")
        self.status = 1
        self.fallcounter = 0
        self.shaker = [-10, 0, 0, 10, 10, 0, 0, -10]*8
        
    def show_platform(self):
        fill(0)
        if self.status == 1:
            # image(self.img, self.x, self.y, self.w, self.h)
            rect(self.x, self.y + game.y_shift, self.w, self.h)
        elif self.status == 2:
            if len(self.shaker) == 0:
                self.status = 3
            else:
                y = self.shaker.pop()
                x = self.shaker.pop()
                rect(self.x + x, self.y + y + game.y_shift, self.w, self.h)
            
        elif self.status == 3:
            rect(self.x, self.y + game.y_shift, self.w, self.h)
            self.fall()
        
        
                
    def fall(self):
        self.vy += 0.1
        self.y += self.vy
        self.fallcounter += 1


class Buttons:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/" + img + ".png")
    
    def showButton(self):
        image(self.img, self.x, self.y, self.w, self.h)
        if mouseX in range(self.x, self.w) and mouseY in range(self.y, self.h):
            noFill()
            stroke(255)
            strokeWeight(10)
            rect(self.x - 10, self.y - 10, self.w + 20, self.h + 20)

class Screen:
    def __init__(self, bg, buttons, sound):
        self.bg = loadImage(path + "/" + bg + ".png")
        self.buttons = buttons
        self.sound = player.loadFile(path + "/sounds/" + sound + ".mp3")
        self.sound_on = True
    
    def runScreen(self):
        image(self.bg, 0, 0, game.w, game.h)
        for button in self.buttons:
            button.showButton()
        # something for the sounds
            
    def clickButton(button):
        global game
        if button == home:
            game.screen = home_screen
        elif button == instructions:
            game.screen = instructions_screen
        elif button == play:
            game.screen = game_screen
        elif button == pause:
            game.screen = pause_screen
        elif button == restart:
            restart()
        elif button == ok:
            game.screen = game_screen
        elif button == sound:
            if self.sound_on:
                self.sound_on = False
            else:
                self.sound_on = True
        elif button == leader:
            game.screen = leaderboard_screen
    
class Hero:
    def __init__(self, x, y, r, platforms):
        self.x = x
        self.y = y
        self.r = r
        self.vy = 0
        self.vx = 0
        self.key_handler = {LEFT: False, RIGHT:False, UP:False}
        self.jump_boost = 1
    
    def gravity(self):
        self.g = self.hitPlatform().y
        if self.y + self.r == self.g:
            self.vy = 0
        else:
            self.vy += 0.6
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        

            
    def hitPlatform(self):
        for i in range(1, len(game.platforms)):
            if self.y + self.r <= game.platforms[-i].y and self.x + self.r >= game.platforms[-i].x and self.x - self.r <= game.platforms[-i].x + game.platforms[-i].w:
                return game.platforms[-i]
        return game.platforms[0]
        
        
    def friction(self):
        if self.vx < 0:
            self.vx += 0.4
        if self.vx > 0:
            self.vx -= 0.4 
        if self.vx*10 in range(-4, 5):
            self.vx = 0
    

    def update(self):
        self.gravity()
        if self.key_handler[LEFT]:
            if self.vx > -12:
                self.vx -= 0.4
            self.direction = LEFT
        elif self.key_handler[RIGHT]:
            if self.vx < 12:
                self.vx += 0.4
            self.direction = RIGHT
        else:
            self.friction()
            
        self.jump_boost = abs(self.vx)

        if self.key_handler[UP] and self.y + self.r == self.g:
            self.vy = -20 - self.jump_boost
            
        if self.x - self.r < 0:
            self.x = self.r
            self.vx = - self.vx
        elif self.x >= game.w - self.r:
            self.x = game.w - self.r
            self.vx = - self.vx
        self.y += self.vy
        self.x += self.vx
        if self.y <= game.h//2:
            game.y_shift -= self.vy
        
    def distance(self):
         return (self.y + self.r - self.g)   
        
    def show(self):
        
        fill(255, 255, 255)
        stroke(0, 0, 0)
        circle(self.x, self.y + game.y_shift, self.r * 2)
        self.update()
                      
class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.g = self.h - 50
        self.y_shift = 0
        self.score = 0
        self.floor = 0
        self.platforms = []
        self.platforms.append(Platform(0, self.h - 50, self.w))
        for i in range(50):
            w = random.randint(200, 400)
            x = random.randint(0, self.w - w)
            self.platforms.append(Platform(x, self.h - 300*i, w))
        self.hero = Hero(self.w/2, self.h - 150, 50, self.platforms)
                                  
        # self.screen = home_screen
        
    
    def display(self):
        # if self.hero.y <= self.h//2:
        #     # self.y_shift += 1
        #     if frameCount % 180 == 0:
        #         self.platforms[self.floor].status = 2
        #         self.floor += 1
        # for platform in self.platforms:
        #     if platform.fallcounter == 300:
        #         self.platforms.remove(platform)
        #         break
        for platform in self.platforms:
            platform.show_platform()
        self.hero.show()
        
                
        
        
def restart():
    global game
    game = Game()
    game.screen = play

def getLeaderboard():
    leaderboard = []
    leaderboard_file = open("leaderboard.csv", "r")
    for line in leaderboard_file:
        row = line.strip().split(",")
        leaderboard.append(row)
    return leaderboard

# pause = Button(, , , , )
# play = Button(, , , , )
# home = Button(, , , , )
# instructions = Button(, , , , )
# sound = Button(, , , , )
# restart = Button(, , , , )
# ok = Button(, , , , )
# leader = Button(, , , , )

# home_screen = Screen("bg1", [play, instructions, sound, leader], "bgmusic1")
# instructions_screen = Screen("bg2", [home], "bgmusic1")
# game_screen = Screen("bg3", [pause], "bgmusic2")
# pause_screen = Screen("bg4", [home, instructions, restart, sound, ok, leader], "bgmusic2")
# leaderboard_screen = Screen("bg5", [home], "bgmusic3")
                
leaderboard = getLeaderboard()

game = Game(800, 800)
def keyPressed():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.hero.key_handler[UP] = True   
        
def keyReleased():
    if keyCode == LEFT:
        game.hero.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.hero.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.hero.key_handler[UP] = False       
    
# def mouseClicked():
#     for button in game.screen.buttons:
#         if mouseX in range(button.x, button.w) and mouseY in range(button.y, button.h):
#             game.screen.clickButton(button)
#             break
        
def setup():
    size(game.w, game.h)
    background(255)
    
def draw():
    background(255)
    game.display()
