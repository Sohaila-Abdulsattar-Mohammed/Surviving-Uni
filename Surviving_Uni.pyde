#importing necessary modules/libraries
add_library('minim')
import os
import time 

#declaring important global variables
PATH = os.getcwd()
minim = Minim(this)
bgm_status = True
soha_images = {"regular": loadImage(PATH + "\\images\\soha_walk.png"), \\
               "hurt":loadImage(PATH + "\\images\\hurt_soha.png"), \\
               "immune": loadImage(PATH + "\\images\\immune_soha.png")}


#opening the csv files with the locations of
#the platforms, collectibles, and enemies
locs1 = open(PATH+"\\locations\\locationsP.csv","r")
locs2 = open(PATH+"\\locations\\locationsC.csv","r")
enemy1 = open(PATH+"\\locations\\redlocs.csv", "r")
enemy2 = open(PATH+"\\locations\\bluelocs.csv", "r")
enemy3 = open(PATH+"\\locations\\greenlocs.csv", "r")


#Defining the general creature class
class Creature:
    #initializing important attributes
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x = x 
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.w=w
        self.h=h
        self.F=F
        self.f=0
        self.dir = 1
        self.g=g 
        self.img = loadImage(PATH + "\\images\\{0}".format(img))
    
    #defining the gravity function that causes the creatures to "fall down"    
    def gravity(self):
        if self.y + self.r < self.g:
            self.vy += 0.4
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g-self.y-self.r
        else:
            self.vy = 0
        
        #looping through the platforms to change the gravity accordingly        
        for p in game.platforms:
            
            #checking if the platform should be skipped if a yellow crystal
            #has been taken
            if isinstance(self, Soha):
                if p.y == self.skipP:
                    continue

            if self.y+self.r <= p.y and self.x + self.r > p.x and self.x-self.r < p.x + p.w:
                self.g = p.y
                game.levels = p.v
                return        
            
    #defining the function that calls gravity and updates the velocities accordingly    
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
    
    #defining the function that displays the creature
    def display(self):
        self.update()
        
        #creating the animation effect
        if self.vx != 0 and self.vy == 0:
            self.f = (self.f+0.1)%self.F
        elif self.vy != 0:
            self.f = self.F-1
        else:
            self.f = 0
            
        #fixing the orientation of the creature
        if self.dir > 0:
            image (self.img, self.x-self.r, self.y-self.r-game.y, self.w, self.h, int(self.f)*self.w, 0, (int(self.f)+1)*self.w, self.h)
        elif self.dir < 0:
            image (self.img, self.x-self.r, self.y-self.r-game.y, self.w, self.h, (int(self.f)+1)*self.w, 0, int(self.f)*self.w, self.h)
        

#defining a class for the red beam
class Beam:
    
    #initializing important attributes
    def __init__ (self,x,y,img):
        self.x = x
        self.y = y
        self.img = loadImage(PATH + "\\images\\{0}".format(img))
        self.vy = 1.65
        
    #the update function that keeps the beam moving downwards
    def update(self):
        if game.mode == "ON":
            self.y += self.vy

    #display function to show the beam    
    def display(self):
        self.update()
        image (self.img, self.x, self.y)
    
    #the function that detects when the beam "touches" Soha    
    def contact(self):
        if self.y >= game.h//2 - 50:
            return True



#defining a class for the collectibles to essentially just display them
class Crystal(Creature):
    def __init__ (self,x,y,r,img,w,h,F):
        Creature.__init__(self,x,y,r,0,img,w,h,F)
        self.vx = 1
    
    def update(self):
        pass 


#defining a class for the enemies to have them move between two boundaries 
class Enemy(Creature):
    def __init__ (self,x,y,r,g,img,w,h,F,x1,x2):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.x1 = x1
        self.x2 = x2
        self.vx = 2
        
    def update(self):
        self.gravity()
                
        if self.x >= self.x2:
            self.vx = -2
            self.dir = -1
        elif self.x <= self.x1:
            self.vx = 2
            self.dir = 1
            
        self.x += self.vx
        self.y += self.vy
                                      
                                                                                
#defining the class for the main sprite, Soha, inheriting from Creature                                                                                                                                                               
class Soha(Creature):
    
    #initializing important attributes
    def __init__ (self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.keyHandler = {LEFT:False, RIGHT:False}
        self.body_fuel = 100
        self.caffeine = 0
        self.academic = 0
        self.status = "danger"
        self.hurt_time = 0
        self.immuneY_time = 0
        self.immuneA_time = 0
        self.speed = "regular"
        self.slow_time = 0
        self.damage = minim.loadFile(PATH + '\\audio\\hurt.mp3')
        self.collect = minim.loadFile(PATH + '\\audio\\coin.mp3')
        self.skipP = 0


    def display(self):
        #changing self.img based on Soha's status
        if self.status == "danger":
            self.img = soha_images["regular"]  
        elif self.status == "immuneY" or self.status == "immuneA":
            self.img = soha_images["immune"] 
        elif self.status == "hurt":       
            self.img = soha_images["hurt"] 
        
        self.update()        
        
        #displaying the hurt animation regardless of velocity
        if self.status == "hurt":
            self.f = (self.f+0.2)%self.F
        
        #else display depends on if there's vx    
        else:
            if self.vx != 0 and self.vy == 0:
                self.f = (self.f+0.2)%self.F
            elif self.vy != 0:
                self.f = self.F-1
            else:
                self.f = 0
                
        #displaying Soha according to her orientation
        if self.dir > 0:
            image (self.img, self.x-self.r, self.y-self.r-game.y, self.w, self.h, int(self.f)*self.w, 0, (int(self.f)+1)*self.w, self.h)
        elif self.dir < 0:
            image (self.img, self.x-self.r, self.y-self.r-game.y, self.w, self.h, (int(self.f)+1)*self.w, 0, int(self.f)*self.w, self.h)
            
                    
    def update(self):
        self.gravity()
        
        #manipualting Soha's speed according to her status and key pressed
        if self.keyHandler[LEFT] and (self.speed == "regular" or self.status == "immuneY" or self.status == "immuneA"):
            self.vx = -9
            self.dir = -1
        elif self.keyHandler[RIGHT] and (self.speed == "regular" or self.status == "immuneY" or self.status == "immuneA"):
            self.vx = 9
            self.dir = 1
        elif self.keyHandler[LEFT] and self.speed == "slow":
            self.vx = -4
            self.dir = -1
        elif self.keyHandler[RIGHT] and self.speed == "slow":
            self.vx = 4
            self.dir = 1
        else:
            self.vx = 0
        
        #prohibiting the player from taking Soha off the borders of the display
        if self.x < 0:
            self.vx = 1
        elif self.x > 880:
            self.vx = -1
            
       #detecting Soha's collisions with enemies and making subsequent changes
       #every collision changes her status to "hurt", where we stop registering other
       #collision for two seconds
       
        for e in game.enemies1:
            
            #if Soha collides with procrastination, her body fuel decreases by 10%,
            #and she slows down (her speed becomes "slow") for 2 seconds (we track that time in Game class)
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r and self.status == "danger":
                self.damage.play()
                self.damage.rewind()
                if self.body_fuel >= 10:
                    self.body_fuel -= 10
                else:
                    self.body_fuel = 0
                self.hurt_time = game.time
                self.status = "hurt"
                self.speed = "slow"
                self.slow_time = game.time
                self.vy =-5
        
        #if Soha collides with tests and midterms, her body fuel decreases by 25%
        for e in game.enemies2:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r and self.status == "danger":
                self.damage.play()
                self.damage.rewind()
                if self.body_fuel >= 25:
                    self.body_fuel -= 25
                else:
                    self.body_fuel = 0
                self.hurt_time = game.time
                self.status = "hurt"
                self.vy =-5
        
        #if Soha collides with finals and final projects, her body fuel decreases by 35%, and her
        #academic prowess diminishes by 20 points
        for e in game.enemies3:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r and self.status == "danger":
                self.damage.play()
                self.damage.rewind()
                if self.body_fuel >= 35:
                    self.body_fuel -= 35
                else:
                    self.body_fuel = 0
                if self.academic >= 20:
                    self.academic -= 20
                else:
                    self.academic = 0
                self.hurt_time = game.time
                self.status = "hurt"
                self.vy =-5
                
        #Detecting Soha's collisions with the collectibles and making subsequent changes, including
        #removing the collectible from the list of collectibles so it's not displayed
        
        #blue crystals increase Soha's body fuel by 10%
        for e in game.blue_crys:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r:
                tmp = game.blue_crys.remove(e)
                self.collect.play()
                self.collect.rewind()
                if self.body_fuel <= 90:
                    self.body_fuel += 10
                elif self.body_fuel > 90:
                    self.body_fuel = 100
                del tmp
        
        #purple crystals increase Soha's body fuel by 15%
        for e in game.purple_crys:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r:
                tmp = game.purple_crys.remove(e)
                self.collect.play()
                self.collect.rewind()
                if self.body_fuel <= 85:
                    self.body_fuel += 15
                elif self.body_fuel > 85:
                    self.body_fuel = 100
                del tmp

        #yellow crystals make Soha immune for 1 second and make her directly skip the platform she's on                
        for e in game.yellow_crys:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r:
                tmp = game.yellow_crys.remove(e)
                self.collect.play()
                self.collect.rewind()
                if self.status != "immuneA":
                    self.status = "immuneY"
                    self.immuneY_time = game.time
                del tmp
                self.skipP = self.g
                
        #every 50 collected from the pink crystals make Soha immune for 10 seconds       
        for e in game.pink_crys:
            if ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 <= self.r + e.r:
                tmp = game.pink_crys.remove(e)
                self.collect.play()
                self.collect.rewind()
                if self.academic < 50:
                    self.academic += 1
                if self.academic == 50:
                    self.status = "immuneA"
                    self.immuneA_time = game.time
                    self.academic = 0 
                del tmp

        
        #updating Soha's velocities      
        self.x += self.vx
        self.y += self.vy
        
        #tracking the "movement" of the screen display to correctly display Soha
        #and to keep the beam in its original position if Soha's is "faster" than it
        tmp = game.y
        if self.y >= game.h//2:
            game.y += self.vy
            game.beam.display()
            if tmp!=game.y and self.status != "hurt":
                game.beam.y = 60

#moving Soha based on key pressed, so long as game mode is ON    
def keyPressed():
    if game.mode == "ON":
        if keyCode == LEFT:
            game.soha.keyHandler[LEFT] = True
            
        elif keyCode == RIGHT:
            game.soha.keyHandler[RIGHT] = True        

#stopping Soha when key released, so long as game mode is ON    
def keyReleased():
    if game.mode == "ON":
        if keyCode == LEFT:
            game.soha.keyHandler[LEFT] = False
            
        elif keyCode == RIGHT:
            game.soha.keyHandler[RIGHT] = False
 
                       
def mouseClicked():

    #turning background audio on and off based on button clicked
    global bgm_status
    if 20<=mouseX<=63 and 724<=mouseY<=767:
        game.bgm.loop() 
        bgm_status = True   
    if 80<=mouseX<=123 and 724<=mouseY<=767:
        game.bgm.pause()
        bgm_status = False
        
    #changing game mode based on key pressed in the menu    
    if game.mode == "MENU":
        if 325<=mouseX<=571 and 392<=mouseY<=517:
            game.mode = "ON"
        elif 325<=mouseX<=571 and 542<=mouseY<=667:
            game.mode = "INFO"
    
    #when the game reaches an end, win or loss, the game mode changes based on
    #choice picked, restart or menu        
    elif game.mode == "LOST" or game.mode == "WON":
        if 325<=mouseX<=571 and 392<=mouseY<=517:
            game.__init__(game.w,game.h,game.g, "ON")
        elif 325<=mouseX<=571 and 542<=mouseY<=667:
            game.mode = "MENU"
            game.__init__(game.w,game.h,game.g)
            
    #changing game mode when player exits the info section
    elif game.mode == "INFO":
        if 750<=mouseX<=873 and 15<=mouseY<=77.5:
            game.mode = "MENU"
        

#defining a class for the platforms that simply displays the platforms
class Platform:
    def __init__(self,x,y,w,h,img,v):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.v=v
        self.img = loadImage(PATH + "\\images\\{0}".format(img))
        
    def display(self):
        image(self.img, self.x,self.y-game.y)
        

#the main Game class    
class Game:
    
    #initializing important attributes
    def __init__ (self,w,h,g, mode="MENU"):
        self.w=w
        self.h=h
        self.g=g
        self.soha = Soha(200,0,34,g,"soha_walk.png",96,67,6)
        self.time = 0
        self.blue_crys = []
        self.purple_crys = []
        self.pink_crys = []
        self.yellow_crys = []
        self.enemies1 = []
        self.enemies2 = []
        self.enemies3 = []
        self.platforms = []
        self.bg = []
        self.levels = 100
        self.beam = Beam(0,50,"red_beam.png")
        self.title = loadImage(PATH + "\\images\\title.png")
        self.start = loadImage(PATH + "\\images\\start_button.png")
        self.info = loadImage(PATH + "\\images\\info_button.png")
        self.restart = loadImage(PATH + "\\images\\restart.png")
        self.menu = loadImage(PATH + "\\images\\menu.png")
        self.lost1 = loadImage(PATH + "\\images\\lost1.png")
        self.lost2 = loadImage(PATH + "\\images\\lost2.png")
        self.shade = loadImage(PATH + "\\images\\shade.png")
        self.instructions = loadImage(PATH + "\\images\\instructions.png")
        self.won = loadImage(PATH + "\\images\\won.png")
        self.on = loadImage(PATH + "\\images\\on.png")
        self.off = loadImage(PATH + "\\images\\off.png")
        self.success = minim.loadFile(PATH + '\\audio\\success.mp3')
        self.fail = minim.loadFile(PATH + '\\audio\\lost.mp3')
        self.bgm = minim.loadFile(PATH + '\\audio\\bgm.mp3')
        if bgm_status == True:
            self.bgm.loop()
        self.y = 0
        self.mode = mode
        self.scroll = 0
        
        #layering background images
        for i in range (1,3):
            self.bg.append(loadImage(PATH + "\\images\\bg{0}.png".format(i)))
            
        #reading enemy1 locations
        for l in enemy1:
            enemy1.readline()
            l=l.strip().split(",")
            self.enemies1.append(Enemy(int(l[1]),int(l[2]),24,g,"red.png",42,48,3,int(l[3]),int(l[4])))
        
        #reading enemy2 locations
        for l in enemy2:
            l=l.strip().split(",")
            self.enemies2.append(Enemy(int(l[1]),int(l[2]),24,g,"blue.png",42,48,3,int(l[3]),int(l[4])))
        
        #reading enemy3 locations
        for l in enemy3:
            l=l.strip().split(",")
            self.enemies3.append(Enemy(int(l[1]),int(l[2]),24,g,"green.png",42,48,3,int(l[3]),int(l[4])))
               
        #reading platform locations
        for l in locs1:
            l=l.strip().split(",")
            if l[0]=="U":
                self.platforms.append(Platform(int(l[1]), int(l[2]), 1000, 64, "last_platform.png", l[5]))
                break
            self.platforms.append(Platform(int(l[1]), int(l[2]), 768, 64, "long_platform.png", l[5]))
            if int(l[3])!=0:
                self.platforms.append(Platform(int(l[3]), int(l[4]), 192, 64, "platform.png", l[5]))
        
        #reading collectibles' locations
        for l in locs2:
            l=l.strip().split(",")
            #"LL","RL","SR", etc. are just arbitrary notations given to the locations, you can note 
            #what they roughly refer to in the "collectibles_locs.py" file, if that matters
            if l[0] == "LL" or l[0] == "RL" or l[0] == "RH":
                self.pink_crys.append(Crystal(int(l[1]), int(l[2]), 18, "pink_crys_moving.png", 32, 32, 6))
            if l[0] == "LQ" or l[0] == "SM" or l[0] == "SL":
                self.purple_crys.append(Crystal(int(l[1]), int(l[2]), 18, "purple_crys_moving.png", 32, 32, 6))
            if l[0] == "LH" or l[0] == "RM" or l[0] =="SR" or l[0] =="SLM":
                self.blue_crys.append(Crystal(int(l[1]), int(l[2]), 18, "blue_crys_moving.png", 32, 32, 6))
            if l[0] == "M":
                self.yellow_crys.append(Crystal(int(l[1]), int(l[2]), 18, "yellow_crys_moving.png", 32, 32, 6))

    #displaying the game based on its status     
    def display(self):
        
        #in menu mode, we'll have the background scroll, and we'll show all button options
        if self.mode == "MENU":
            self.scroll+=2
            for i, p in enumerate(self.bg):
                x = 2*self.scroll // (6-i)
                image(p, 0, 0-x%self.h)
                image(p, 0, self.h-x%self.h - 3, self.w, x%self.h,0, 0, self.w, int(x%self.h))
                
            image(self.title, 121.5,100)
            image(self.start, 325, 392)
            image(self.info, 325, 542)
 
            #showing when a mouse is over a button
            if 325<=mouseX<=571 and 392<=mouseY<=517:
                tint(216, 156, 190)
                image(self.start, 325, 392)
                noTint()
            elif 325<=mouseX<=571 and 542<=mouseY<=667:
                tint(216, 156, 190)
                image(self.info, 325, 542)
                noTint()
        
        #in lost mode, we'll display the corresponding message and give the option to restart or go to menu
        elif self.mode == "LOST":
            self.bgm.pause()
            self.fail.play()
            if self.soha.body_fuel == 0:
                image(self.lost2, 85, 40)
            else:
                image(self.lost1, 85, 40)
            image(self.restart, 325, 392)
            image(self.menu, 325, 542)
            
            if 325<=mouseX<=571 and 392<=mouseY<=517:
                tint(216, 156, 190)
                image(self.restart, 325, 392)
                noTint()
            elif 325<=mouseX<=571 and 542<=mouseY<=667:
                tint(216, 156, 190)
                image(self.menu, 325, 542)
                noTint()

        #in info mode, the player will see all the needed info to explain how to play            
        elif self.mode == "INFO":
            image(self.instructions,0,0)
            image(self.menu, 750, 15, 123, 62.5)
            if 750<=mouseX<=873 and 15<=mouseY<=77.5:
                tint(216, 156, 190)
                image(self.menu, 750, 15, 123, 62.5)
                noTint()
        
        #in won mode, we'll display the corresponding message and give the option to restart or go to menu
        elif self.mode == "WON":
            self.bgm.pause()
            self.success.play()
            image(self.won, 101,100)
            image(self.restart, 325, 392)
            image(self.menu, 325, 542)
            
            if 325<=mouseX<=571 and 392<=mouseY<=517:
                tint(216, 156, 190)
                image(self.restart, 325, 392)
                noTint()
            elif 325<=mouseX<=571 and 542<=mouseY<=667:
                tint(216, 156, 190)
                image(self.menu, 325, 542)
                noTint()
        
        #ON mode is where the actual game takes place    
        elif self.mode == "ON":
            
            # we'll move the background based on Soha's "falling"
            for i, p in enumerate(self.bg):
                x = 2*self.y // (6-i)
                image(p, 0, 0-x%self.h)
                image(p, 0, self.h-x%self.h - 3, self.w, x%self.h,0, 0, self.w, int(x%self.h))
                
                
            #going through all the previously read platforms, 
            #collectibles, and enemies and displaying them
            for p in self.platforms:
                p.display()
            for l in self.blue_crys:
                l.display()
            for l in self.purple_crys:
                l.display()
            for l in self.pink_crys:
                l.display()
            for l in self.yellow_crys:
                l.display()
            for e in self.enemies1:
                e.display()    
            for e in self.enemies2:
                e.display()
            for e in self.enemies3:
                e.display()
            
            #displaying Soha                
            self.soha.display()
            
            #displaying the game status properties
            fill("#153D72")
            noStroke()
            rect(470, 7, 415, 30, 28)
            rect(560, 13, 270, 52, 28)
            rect(15,7,99+5*len(str(self.time)),30,28)
            fill(255,255,255)
            f = createFont("Stacked_pixel.ttf",10)
            textFont(f)
            textAlign(RIGHT)
            textSize(25)
            text("Body Fuel: " + str(self.soha.body_fuel)+"%", 650,30)
            text("Current Level: " + str(self.levels), 875,30)
            text("Academic Prowess: " + str(self.soha.academic), 820-(5*len(str(self.soha.academic))),55)
            textAlign(LEFT)
            text("Time: " + str(self.time), 25,30)
            
            #tracking the times of hurt, immunity, and slowness
            if self.time-self.soha.hurt_time == 2 and self.soha.hurt_time!= 0 and self.soha.status!= "immuneY" and self.soha.status!= "immuneA":
                self.soha.status = "danger"
            if self.time-self.soha.immuneA_time == 10 and self.soha.immuneA_time!= 0 and self.soha.status != "hurt" and self.soha.status!= "immuneY":
                self.soha.status = "danger"
            if self.time-self.soha.immuneY_time == 1 and self.soha.immuneY_time!= 0 and self.soha.status != "hurt" and self.soha.status!= "immuneA":
                self.soha.status = "danger"            
            if self.time-self.soha.slow_time == 2 and self.soha.speed == "slow":
                self.soha.speed = "regular"

            #checking if player loses via "touching" the beam, or losing all Soha's body fuel
            #to change the status and reset initial properties
            if self.beam.contact() or self.soha.body_fuel == 0:
                locs1.seek(0)
                locs2.seek(0)
                enemy1.seek(0)
                enemy2.seek(0)
                enemy3.seek(0)
                image(self.shade,0,0)
                game.mode = "LOST"
                
            #if the player reaches level 0, then they won, so we change the status and reset initial properties
            if int(self.levels) == 0 and self.soha.y == game.g-self.soha.r:
                locs1.seek(0)
                locs2.seek(0)
                enemy1.seek(0)
                enemy2.seek(0)
                enemy3.seek(0)
                image(self.shade,0,0)
                game.mode = "WON"
         
        #display sound on and off buttons    
        image(self.on, 20, 724)
        image(self.off, 80, 724)
        if 20<=mouseX<=63 and 724<=mouseY<=767:
            tint(216, 156, 190)
            image(self.on, 20, 724)
            noTint()
        if 80<=mouseX<=123 and 724<=mouseY<=767:
            tint(216, 156, 190)
            image(self.off, 80, 724)
            noTint()
            

#instantiating a Game object
game = Game(896,784,20120)

#setting up the game with its corresponding dimensions
def setup():
    size(game.w, game.h)
 
#displaying the game and tracking time
def draw():
    if frameCount % 60 == 0 and game.mode == "ON":
        game.time += 1
    game.display()
