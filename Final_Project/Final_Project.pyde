add_library('minim')
import os, random
path = os.getcwd()
player = Minim(this)


class Platform:
    def __init__(self, x, y, w, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = 50
        self.vy = 0
        self.img = loadImage(path + "/assets/images/" + img)
        self.status = 1
        self.fallcounter = 0
        self.shaker = [-10, 0, 0, 10, 10, 0, 0, -10]*8
        
    def show_platform(self):
        fill(0)
        if self.status == 1:
            image(self.img, self.x, self.y + game.y_shift, self.w, self.h)
        elif self.status == 2:
            if len(self.shaker) == 0:
                self.status = 3
            else:
                y = self.shaker.pop()
                x = self.shaker.pop()
                image(self.img, self.x + x, self.y + y + game.y_shift, self.w, self.h)


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
    def __init__(self, x, y, r, g):
        self.status = ""
        self.w_slices = 4
        self.i_slices = 3
        self.s_slices = 4
        self.idle = loadImage(path + "/assets/sprites/harold/idle-harold.png")
        self.walking = loadImage(path + "/assets/sprites/harold/walking-harold.png")
        self.jumping = loadImage(path + "/assets/sprites/harold/jumping-harold.png")
        self.jumping2 = loadImage(path + "/assets/sprites/harold/jumping2-harold.png")
        self.falling = loadImage(path + "/assets/sprites/harold/falling-harold.png")
        self.spinning = loadImage(path + "/assets/sprites/harold/spinning-harold.png")
        self.frame_i = 0
        self.frame_w = 0
        self.frame_s = 0
        self.img_w = {}
        self.img_h = {}
        self.img_w["idle"] = 114/3
        self.img_h["idle"] = 73
        self.img_w["walking"] = 37
        self.img_h["walking"] = 73
        self.img_w["spin"] = 60
        self.img_h["spin"] = 60
        self.img_w["jump"] = 38
        self.img_h["jump"] = 71
        self.img_w["jump2"] = 38
        self.img_h["jump2"] = 71
        self.img_w["fall"] = 38
        self.img_h["fall"] = 71
        
        self.x = x
        self.y = y
        self.r = r
        self.vy = 0
        self.vx = 0
        self.g = g
        self.key_handler = {LEFT: False, RIGHT:False, UP:False}
        self.jump_boost = 1
    
    def gravity(self):
        if self.y + self.r == self.g:
            self.vy = 0
        else:
            self.vy += 4
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
        if self.hitPlatform() == game.platforms[0]:
            self.g = game.g
        else:
            self.g = self.hitPlatform().y

            
    def hitPlatform(self):
        for i in range(1, len(game.platforms)):
            if self.y + self.r <= game.platforms[-i].y and self.x >= game.platforms[-i].x and self.x - self.r/2 <= game.platforms[-i].x + game.platforms[-i].w:
                return game.platforms[-i]
        return game.platforms[0]
        
        
    def friction(self):
        if self.vx < 0:
            self.vx += 1
        if self.vx > 0:
            self.vx -= 1
        if self.vx*10 in range(-4, 5):
            self.vx = 0
    

    def update(self):
        self.gravity()
        if self.key_handler[LEFT]:
            if self.vx > -25:
                self.vx -= 1
            self.direction = LEFT
        elif self.key_handler[RIGHT]:
            if self.vx < 25:
                self.vx += 1
            self.direction = RIGHT
        else:
            self.friction()
            
        self.jump_boost = abs(self.vx)//10
        if self.jump_boost == 0:
            self.jump_boost = 1
        if self.key_handler[UP] and self.distance() == 0 and self.vy >=0:
            self.vy = -35 * self.jump_boost
            
        if self.x - self.r < 75:
            self.x = self.r + 75
            self.vx = - self.vx//2
        elif self.x >= game.w - self.r:
            self.x = game.w - self.r
            self.vx = - self.vx//2
        self.y += self.vy
        self.x += self.vx
        if self.y <= game.h//2:
            game.y_shift -= self.vy
        if frameCount % 5 == 0:
            if -0.5 < self.vx < 0.5:
                self.frame_i = (self.frame_i + 1) % self.i_slices
            elif -0.5 > self.vx or self.vx > 0.5:
                self.frame_w = (self.frame_w + 1) % self.w_slices
        if frameCount% 2 == 0:
            if self.vy < - 65:
                self.status = "boost"
            elif self.vy > 5:
                self.status = ""
            self.frame_s = (self.frame_s + 1) % self.s_slices
        
    def distance(self):
         return (self.y + self.r - self.g)   
        
    def show(self):
        self.update()
        # fill(255, 255, 255)
        # stroke(0, 0, 0)
        # circle(self.x, self.y + game.y_shift, self.r * 2)
        if self.status == "boost":
            image(self.spinning, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["spin"] * 2, self.img_h["spin"] * 2, self.frame_s * self.img_w["spin"], 0, (self.frame_s +1) * self.img_w["spin"], self.img_h["spin"])
        else:
            if -0.5 < self.vx < 0.5 and self.vy < 0:
                image(self.jumping, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["jump"] * 2, self.img_h["jump"] * 2)
            elif self.vx > 0.5 and self.vy < 0:
                image(self.jumping2, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["jump2"] * 2, self.img_h["jump2"] * 2)
            elif self.vx < -0.5 and self.vy < 0:
                image(self.jumping2, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["jump2"] * 2, self.img_h["jump2"] * 2, self.img_w["jump2"], 0, 0, self.img_h["jump2"])
            elif self.vx > 0.5 and self.vy > 0:
                image(self.falling, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["fall"] * 2, self.img_h["fall"] * 2)
            elif self.vy > 0:
                image(self.falling, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["fall"] * 2, self.img_h["fall"] * 2, self.img_w["fall"], 0, 0, self.img_h["fall"])
            elif -0.5 < self.vx < 0.5 and self.vy == 0:
                image(self.idle, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["idle"] * 2, self.img_h["idle"] * 2, self.frame_i * self.img_w["idle"], 0, (self.frame_i +1) * self.img_w["idle"], self.img_h["idle"])
            elif self.vx >= 0.5:
                image(self.walking, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["walking"] * 2, self.img_h["walking"] * 2, self.frame_w * self.img_w["walking"], 0, (self.frame_w +1) * self.img_w["walking"], self.img_h["walking"])
            elif self.vx <= -0.5:
                image(self.walking, self.x - self.r, self.y - 1.5*self.r +  game.y_shift, self.img_w["walking"] * 2, self.img_h["walking"] * 2, (self.frame_w +1) * self.img_w["walking"], 0, self.frame_w * self.img_w["walking"], self.img_h["walking"])
        
        
                      
class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.g = self.h - 120
        self.y_shift = 0
        self.score = 0
        self.wall = loadImage(path + "/assets/images/wall.png")
        self.floor = 0
        self.bg1 = loadImage(path + "/assets/images/bg1.jpg")
        self.platforms = []
        self.platforms.append(Platform(0, self.g, self.w, "platform1.png"))
        for i in range(2, 100):
            w = random.randint(300, 400)
            x = random.randint(75, self.w - w)
            self.platforms.append(Platform(x, self.h - 120*i, w, "platform1.png"))
        for i in range(100, 200):
            w = random.randint(200, 300)
            x = random.randint(75, self.w - w)
            self.platforms.append(Platform(x, self.h - 120*i, w, "platform2.png"))
        for i in range(200, 300):
            w = random.randint(100, 200)
            x = random.randint(75, self.w - w)
            self.platforms.append(Platform(x, self.h - 120*i, w, "platform3.png"))
        self.harold = Hero(self.w/2, self.h - 100, 50, self.g)
                                  
        # self.screen = home_screen
        
    
    def display(self):
        for i in range(50):
            image(self.bg1, 75, 0 - i*self.h + self.y_shift, self.w, self.h)
        for platform in self.platforms:
            platform.show_platform()
        self.harold.show()
        platform = self.harold.hitPlatform()
        if self.platforms.index(platform) > 5:
            for i in range(self.platforms.index(platform) - 4):
                self.platforms.remove(self.platforms[i])
        for i in range(1, 100):
            image(self.wall, self.w, self.h - 480 * i + self.y_shift, 75, 480)
            image(self.wall, 0, self.h - 480 * i + self.y_shift, 75, 480, 75, 0, 0, 480)
        # textSize(50)
        # text("Score: " + str(self.score*10), 50, self.h - 100)
        # if self.harold.y <= self.h//2:
        #     # self.y_shift += 1
        #     if frameCount % 40 == 0:
        #         self.platforms[self.floor].status = 2
        #         self.floor += 1
        # for platform in self.platforms:
        #     if platform.status == 3:
        #         self.platforms.remove(platform)
        #         break
        
        
        
                
        
        
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
        game.harold.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.harold.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.harold.key_handler[UP] = True   
        
def keyReleased():
    if keyCode == LEFT:
        game.harold.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.harold.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.harold.key_handler[UP] = False       
    
# def mouseClicked():
#     for button in game.screen.buttons:
#         if mouseX in range(button.x, button.w) and mouseY in range(button.y, button.h):
#             game.screen.clickButton(button)
#             break
        
def setup():
    size(950, 800)
    background(0)
def draw():
    background(0)
    game.display()
