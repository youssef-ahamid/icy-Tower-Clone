add_library('minim')
import os, random
path = os.getcwd()
player = Minim(this)

class Platform:
    def __init__(self, x, y, w, h, img, floor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vy = 0
        self.floor = floor
        self.img = loadImage(path + "/assets/images/" + img)
        self.status = 1
        self.shaker = [-10, 0, 0, 10, 10, 0, 0, -10]*4
        self.tile = False
        self.tile_img = loadImage(path + "/assets/images/tile.jpg")
        
    def showPlatform(self):
        if self.status == 1:
            image(self.img, self.x, self.y + game.y_shift, self.w, self.h)
        elif self.status == 2:
            if len(self.shaker) == 0:
                self.status = 3
            else:
                y = self.shaker.pop()
                x = self.shaker.pop()
                image(self.img, self.x + x, self.y + y + game.y_shift, self.w, self.h)
        if self.floor % 10 == 0 and self.floor != 0:
            image(self.tile_img, self.x + self.w/2 - 35, self.y + game.y_shift, 70, 50)
            fill(255)
            textSize(20)
            text(self.floor, self.x + self.w/2 - 15, self.y + 30 + game.y_shift)


class Button:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/assets/images/buttons/" + img + ".png")
        self.select_sound = player.loadFile(path + "/assets/audio/select.wav")
        
    def showButton(self):
        image(self.img, self.x, self.y, self.w, self.h)
        if mouseX in range(self.x, self.x + self.w) and mouseY in range(self.y, self.y + self.h):
            noFill()
            stroke(255)
            strokeWeight(4)
            rect(self.x - 5, self.y - 5, self.w + 10, self.h + 10)

class Screen:
    def __init__(self, bg, buttons):
        self.bg = loadImage(path + "/assets/images/backgrounds/" + bg)
        self.buttons = buttons
        self.press_sound = player.loadFile(path + "/assets/audio/press.wav")
        self.sound_on = True
        
    def runScreen(self):
        image(self.bg, 0, 0, game.w + 150, game.h)
        if game.screen == game_screen and not game.dead:
            for button in self.buttons:
                if button != play_again and button != main:
                    button.showButton()
        else:
            for button in self.buttons:
                button.showButton()
        # something for the sounds
            
    def clickButton(self, button):
        global game
        self.press_sound.rewind()
        self.press_sound.play()
        # if button == home:
        #     game.screen = home_screen
        if button == instructions:
            game.screen = instructions_screen
        elif button == play:
            game.screen = game_screen
        elif button == pause:
            game.screen = pause_screen
        elif button == back:
            game.screen = home_screen
        elif button == main:
            game = Game(1000, 800)
        elif button == play_again:
            restart()
        # elif button == restart:
        #     restart()
        # elif button == ok:
        #     game.screen = game_screen
        elif button == sound:
            if self.sound_on:
                self.sound_on = False
            else:
                self.sound_on = True
        elif button == leader:
            game.screen = leaderboard_screen


class Confetti:
    def __init__(self, x, y, vy, img, vx = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.img = loadImage(path + "/assets/images/confetti/" + img + ".png")
        self.alive = True
    
    def update(self):
        self.vy += 0.4
        if self.y + game.y_shift >= game.h :
            self.alive = False
        self.x += self.vx
        self.y += self.vy
    
    def showConfetti(self):
        image(self.img, self.x, self.y + game.y_shift, 15, 15)
        self.update()


class PowerUp:
    def __init__(self, x, y, img, slices, img_w, img_h):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/assets/sprites/powerups/" + img + ".png")
        self.type = img
        self.slices = slices
        self.frame = 1
        self.img_w = img_w
        self.img_h = img_h
        self.on = True
        
    def showPowerUp(self):
        self.hitHero()
        if self.type == "spring":
            image(self.img, self.x, self.y + game.y_shift - self.img_h, self.img_w*2, self.img_h*2, self.frame * self.img_w, self.img_h, (self.frame +1) * self.img_w, 0)
        else:
            image(self.img, self.x, self.y + game.y_shift - self.img_h, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame +1) * self.img_w,  self.img_h)
        if frameCount%5 == 0:
            self.frame = (self.frame + 1) % self.slices
    
    def hitHero(self):
        global game
        if (game.harold.y + game.harold.r) in range(self.y - self.img_h*2, self.y) and game.harold.x in range(self.x, self.x + self.img_w*2):
            if self.type == "spring":
                game.harold.vy = - 200
            elif self.type == "multiplier":
                game.score_multiplier = 20
            self.on = False


class Hero:
    def __init__(self, x, y, r, g, img_w, img_h, slices, name):
        self.alive = True
        self.status = ""
        self.i_slices = slices[0]
        self.w_slices = slices[1]
        self.s_slices = slices[2]
        self.idle = loadImage(path + "/assets/sprites/harold/idle-" + name + ".png")
        self.walking = loadImage(path + "/assets/sprites/harold/walking-" + name + ".png")
        self.jumping = loadImage(path + "/assets/sprites/harold/jumping-" + name + ".png")
        self.jumping2 = loadImage(path + "/assets/sprites/harold/jumping2-" + name + ".png")
        self.falling = loadImage(path + "/assets/sprites/harold/falling-" + name + ".png")
        self.spinning = loadImage(path + "/assets/sprites/harold/spinning-" + name + ".png")
        self.frame_i = 0
        self.frame_w = 0
        self.frame_s = 0
        self.img_w = img_w
        self.img_h = img_h
        self.direction = DOWN
        self.x = x
        self.y = y
        self.r = r
        self.vy = 0
        self.vx = 0
        self.g = g
        self.key_handler = {LEFT: False, RIGHT:False, UP:False}
        self.jump_boost = 1
        self.jump_sound = player.loadFile(path + "/assets/audio/jump.wav")
        self.jump2_sound = player.loadFile(path + "/assets/audio/jump2.wav")
        self.spin_sound = player.loadFile(path + "/assets/audio/spin.wav")
        self.die_sound = player.loadFile(path + "/assets/audio/die.wav")
        
    def gravity(self):
        if self.y + self.r == self.g:
            self.vy = 0
        else:
            self.vy += 6
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

    def update(self):
        self.gravity()
        if self.key_handler[LEFT]:
            if self.direction == RIGHT:
                self.vx = -self.vx 
            if self.vx > -40:
                self.vx -= 2
            self.direction = LEFT
        elif self.key_handler[RIGHT]:
            if self.direction == LEFT:
                self.vx = - self.vx
            if self.vx < 40:
                self.vx += 2
            self.direction = RIGHT
        else:
            self.vx = 0

            
        self.jump_boost = abs(self.vx)//20
        if self.jump_boost == 0:
            self.jump_boost = 1
        if self.key_handler[UP] and self.distance() == 0 and self.vy >=0:
            if self.status != "boost":
                if -0.5 < self.vx < 0.5:
                    self.jump_sound.rewind()
                    self.jump_sound.play()
                else:
                    self.jump2_sound.rewind()
                    self.jump2_sound.play()
            else:
                self.spin_sound.rewind()
                self.spin_sound.play()
            self.vy = -50 * self.jump_boost
            
        if self.x - self.r < 75:
            if self.direction == LEFT:
                self.vx = - self.vx//2
            else:
                self.x = self.r + 75
        elif self.x >= game.w + self.r:
            if self.direction == RIGHT:
                self.vx = - self.vx//2
            else:
                self.x = game.w + self.r

        self.y += self.vy
        self.x += self.vx
        if self.y <= 0:
            if game.y_shift +self.y <= 100:
                game.y_shift -= self.vy - 2
            else:
                if self.vy > 0:
                    game.y_shift += 2
                else:
                    game.y_shift -= self.vy//3 - 2
            

                
            # game.y_shift += self.speed
        if frameCount % 5 == 0:
            if -0.5 < self.vx < 0.5:
                self.frame_i = (self.frame_i + 1) % self.i_slices
            elif -0.5 > self.vx or self.vx > 0.5:
                self.frame_w = (self.frame_w + 1) % self.w_slices
        if self.vy < - 65 and game.floor[0] > 5:
            if not self.spin_sound.isPlaying():
                self.spin_sound.rewind()
                self.spin_sound.play()
            self.status = "boost"
        elif self.vy > 20 or self.vy == 0:
            self.status = ""
            if self.spin_sound.isPlaying():
                self.spin_sound.pause()
        self.frame_s = (self.frame_s + 1) % self.s_slices
        
        if self.y + game.y_shift >= game.h:
            self.die_sound.rewind()
            self.die_sound.play()
            self.alive = False
        
    def distance(self):
         return (self.y + self.r - self.g)   
        
    def show(self):
        global game
        self.update()
        if self.status == "boost":
            game.floor[1] += 0.4
            # game.confetti.append(Confetti(self.x + random.randint(-5, 5), self.y, 10, random.choice(game.conf), random.randint(-10, 10)))
            # game.confetti.append(Confetti(self.x + random.randint(-5, 5), self.y, 10, random.choice(game.conf), random.randint(-10, 10)))
            # game.confetti.append(Confetti(self.x + random.randint(-5, 5), self.y, 10, random.choice(game.conf), random.randint(-10, 10)))
            # game.confetti.append(Confetti(self.x + random.randint(-5, 5), self.y, 10, random.choice(game.conf), random.randint(-10, 10)))
            image(self.spinning, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["spin"] * 1.5, self.img_h["spin"] * 1.5, self.frame_s * self.img_w["spin"], 0, (self.frame_s +1) * self.img_w["spin"], self.img_h["spin"])
        else:
            if -0.5 < self.vx < 0.5 and self.vy < 0:
                image(self.jumping, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["jump"] * 1.5, self.img_h["jump"] * 1.5)
            elif self.vx > 0.5 and self.vy < 0:
                image(self.jumping2, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["jump2"] * 1.5, self.img_h["jump2"] * 1.5)
            elif self.vx < -0.5 and self.vy < 0:
                image(self.jumping2, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["jump2"] * 1.5, self.img_h["jump2"] * 1.5, self.img_w["jump2"], 0, 0, self.img_h["jump2"])
            elif self.vx > 0.5 and self.vy > 0:
                image(self.falling, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["fall"] * 1.5, self.img_h["fall"] * 1.5)
            elif self.vy > 0:
                image(self.falling, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["fall"] * 1.5, self.img_h["fall"] * 1.5, self.img_w["fall"], 0, 0, self.img_h["fall"])
            elif -0.5 < self.vx < 0.5 and self.vy == 0:
                image(self.idle, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["idle"] * 1.5, self.img_h["idle"] * 1.5, self.frame_i * self.img_w["idle"], 0, (self.frame_i +1) * self.img_w["idle"], self.img_h["idle"])
            elif self.vx >= 0.5:
                image(self.walking, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["walking"] * 1.5, self.img_h["walking"] * 1.5, self.frame_w * self.img_w["walking"], 0, (self.frame_w +1) * self.img_w["walking"], self.img_h["walking"])
            elif self.vx <= -0.5:
                image(self.walking, self.x - self.r, self.y -self.r +  game.y_shift, self.img_w["walking"] * 1.5, self.img_h["walking"] * 1.5, (self.frame_w +1) * self.img_w["walking"], 0, self.frame_w * self.img_w["walking"], self.img_h["walking"])
        
                        
class Game:
    def __init__(self, w, h):
        self.confetti = []
        self.tile = loadImage(path + "/assets/images/tile.jpg")
        self.conf = ["pink", "blue", "yellow", "red"]
        self.w = w
        self.h = h
        self.high_score_img = loadImage(path + "/assets/images/highscore.png")
        self.score = 0
        self.floor = [0, 0]
        self.screen = home_screen
        self.g = self.h - 120
        self.y_shift = 0
        self.score_multiplier = 10
        self.platforms = []
        self.powerups = []
        self.name = ''
        self.red = random.randint(0, 255)
        self.blue = random.randint(0, 255)
        self.green = random.randint(0, 255)
        self.dead = False
        self.go_img = loadImage(path + "/assets/images/backgrounds/game-over.png")
        for i in range(3):
            self.platforms.append(Platform(75 + (self.w * i)/3, self.g, self.w/3, 50, "platform1.png", 0))
        for i in range(2, 100):
            w = random.randint(300, 400)
            x = random.randint(75, self.w - w)
            platform = Platform(x, self.h - 120*i, w, 50, "platform1.png", i)
            self.platforms.append(platform)
            self.temp = 120 * i 
        for i in range(3):
            self.platforms.append(Platform(75 + (self.w * i)/3, self.g - self.temp, self.w/3, 50, "platform2.png", 100))
        for i in range(101, 200):
            w = random.randint(250, 350)
            x = random.randint(75, self.w - w)
            self.platforms.append(Platform(x, self.h - 120*i, w, 50, "platform2.png", i))
            self.temp = 120 * i 
        for i in range(3):
            self.platforms.append(Platform(75 + (self.w * i)/3, self.g - self.temp, self.w/3 - 20, 50, "platform3.png", 200))
        for i in range(201, 300):
            w = random.randint(150, 250)
            x = random.randint(75, self.w - w)
            self.platforms.append(Platform(x, self.h - 120*i, w, 50, "platform3.png", i))
        random_platform1 = random.choice(self.platforms)
        random_platform2 = random.choice(self.platforms)
        self.powerups.append(PowerUp(int(random_platform1.x + random_platform1.w/2 - 108), random_platform1.y, "spring", 4, 108, 32))
        self.powerups.append(PowerUp(int(random_platform2.x + random_platform2.w/2 - 102), random_platform2.y, "multiplier", 4, 102, 115))
        
        self.harold = Hero(self.w/2, self.h - 30, 40, self.g, {"idle":114/3, "walking":37, "spin":60, "jump":38, "jump2": 38, "fall":38}, {"idle":73, "walking":73, "spin":60, "jump":71, "jump2": 71, "fall":71}, [4, 4, 12], "harold")
        self.background_sound = player.loadFile(path + "/assets/audio/theme-song.mp3")
        self.background_sound.rewind()
        self.background_sound.play()
        
    def display(self):
        self.font = createFont("RoteFlora.ttf", 32)
        global leaderboard
        self.screen.runScreen()
        if self.screen == game_screen:
            self.background_sound.pause()
            for i in range(20):
                if self.platforms[i].y + self.y_shift  - 120 > self.h:
                    self.platforms.remove(self.platforms[i])
                else:
                    self.platforms[i].showPlatform()
            for powerup in self.powerups: 
                if powerup.on:
                    powerup.showPowerUp()
                else:
                    self.powerups.remove(powerup)
            
            # for conf in self.confetti:
            #     if not conf.alive:
            #         self.confetti.remove(conf)
            #     else:
            #         conf.showConfetti()
            if self.harold.alive:
                self.harold.show()
                platform = self.harold.hitPlatform()
                if self.floor[0] < platform.floor:
                    self.floor[0] = platform.floor
                    self.red = random.randint(0, 255)
                    self.blue = random.randint(0, 255)
                    self.green = random.randint(0, 255)
                # for platform in self.platforms:
                #     if platform.status == 3:
                #         self.platforms.remove(platform)                    
                # if self.harold.y < 0:
                #     if frameCount % 10 == 0:
                #         self.platforms[0].status = 2
                self.score = int((self.floor[0] + self.floor[1]) * self.score_multiplier)
                fill(self.red, self.green, self.blue)
                textFont(self.font, 60)
                text(str(self.score), 25, self.h - 100)
                self.temp = self.y_shift
            if not self.harold.alive:
                if self.score > leaderboard[-1][1] and not self.dead:
                    image(self.high_score_img, 344, 300, 462, 86)
                    self.y_shift = self.temp
                    fill(255)
                    textFont(self.font, 70)
                    textAlign(CENTER, BOTTOM)
                    text("Name", self.w/2, 500)
                    textAlign(CENTER, CENTER)
                    text(self.name, self.w/2, 600)
                else:
                    image(self.go_img, 375, 300, 400, 340)
                    fill(0)
                    textFont(self.font, 40)
                    text(self.score, 730, 410)
                    text(self.floor[0], 730, 470)
                    for button in self.screen.buttons:
                        button.showButton()
        else:
            if not self.background_sound.isPlaying():
                self.background_sound.rewind()
                self.background_sound.play()           
                    
        if self.screen == leaderboard_screen:
            fill(0)
            textFont(self.font, 80)
            textAlign(CENTER)
            text("NAME    SCORE", self.w/2, 300)
            i = 0
            for row in leaderboard:
                i += 1
                textAlign(CENTER)
                text(row[0] + "    " + str(row[1]), self.w/2, 300 + 100*i)
       
def restart():
    global game
    game = Game(1000, 800)
    game.screen = game_screen

def getLeaderboard():
    leaderboard = []
    leaderboard_file = open("leaderboard.csv", "r")
    for line in leaderboard_file:
        row = line.strip().split(",")
        row[1] = int(row[1])
        leaderboard.append(row)
    leaderboard_file.close()
    leaderboard.sort(key=lambda x: x[1], reverse = True)
    return leaderboard

def updateLeaderboard():
    global leaderboard, game
    if game.score > leaderboard[2][1]:
        leaderboard[2] = [game.name, game.score]
        leaderboard.sort(key=lambda x: x[1], reverse = True)
    leaderboard_file = open("leaderboard.csv", "w")
    for row in leaderboard:
        leaderboard_file.write(row[0] + "," + str(row[1]) + "\n")
    leaderboard_file.close()

pause = Button(50, 50, 50, 50, "pause")
play = Button(700, 400, 271, 76, "play" )
# home = Button(, , , , )
instructions = Button(700, 500, 271, 76, "instructions")
sound = Button(50, 150, 50, 50, "sound")
play_again = Button(400, 550, 134, 34, "play-again")
main = Button(400, 600, 134, 34, "main-menu")
# ok = Button(, , , , )
leader = Button(700, 600, 271, 76, "leader")
back = Button(200, 700, 195, 60, "back")
home_screen = Screen("bg1.jpg", [play, instructions, leader])
instructions_screen = Screen("instructions.jpg", [back])
game_screen = Screen("bg2.jpg", [pause, play_again, main])
# pause_screen = Screen("bg4", [home, instructions, restart, sound, ok, leader], "bgmusic2")
leaderboard_screen = Screen("high-scores.jpg", [back])    
leaderboard = getLeaderboard()
game = Game(1000, 800)

def keyPressed():
    global game
    if keyCode == LEFT:
        game.harold.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.harold.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.harold.key_handler[UP] = True   
    else:
        if not game.harold.alive and game.screen == game_screen:
            if key == DELETE or key == BACKSPACE:
                game.name = game.name[:-1]
            elif key == RETURN or key == ENTER:
                updateLeaderboard()
                game.dead = True
            else:
                game.name += str(key)
        
def keyReleased():
    if keyCode == LEFT:
        game.harold.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.harold.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.harold.key_handler[UP] = False       
        
def setup():
    size(1150, 800)
    background(0)
    
def draw():
    background(0)
    game.display()
    
def mouseClicked():
    for button in game.screen.buttons:
        if mouseX in range(button.x, button.x + button.w) and mouseY in range(button.y, button.y + button.h):
            game.screen.clickButton(button)
            break
