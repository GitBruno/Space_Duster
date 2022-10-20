import sys, pygame
from pygame import Vector2
from pygame.locals import *
from defines import *
from utilis import load_sprite, infinityBlit, get_image_path, load_sound, channel1, channel2

from models import Spaceship, Bullet, Asteroid
from spritesheet import SpriteSheet

class c_Game:
    states = [
        "STATE_SPLASH",
        "STATE_CONNECTING",
        "STATE_PLAYING",
        "STATE_TOAST"
    ]

    toastTime = 300
    toastedAt = None

    def __init__(self, send, screen):
        self.currentState = "STATE_SPLASH";
        self.clock = pygame.time.Clock()
        self.joystick = None
        self.button1_fresh = True
        self.button2_fresh = True
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.id = 0
        self.idFrame  = 0
        self.idFrames = 120
        self.send = send
        self.screen = screen
        self.playground = pygame.Surface((GROUND_SIZE, GROUND_SIZE)) 
        self.background = load_sprite("space", False)
        self.cam_offset = (0,0)

        self.shipSprites = [load_sprite('spaceship'),load_sprite("spaceship_thrust"),load_sprite("spaceship_shield"),SpriteSheet(get_image_path("ship_explosion_7_41x41_287"))]
        self.s_bullet = load_sprite('bullet')
        self.s_debri  = load_sprite("debri")
        self.asteroidSheet = SpriteSheet(get_image_path("asteroid_8x8-sheet"))

        self.s_title = load_sprite('space_duster_256')
        
        self.shipMap = {}
        self.bulletMap = {}
        self.asteroidMap = {}
        self.debri = []

        self.hit_sound = load_sound("bangSmall")
        self.shoot_sound = load_sound("fire")
        self.shoot_sound.set_volume(0.35)
        self.thrust_sound = load_sound("thrust")
        
        self.score_font  = pygame.font.Font("assets/fonts/PublicPixel-0W5Kv.ttf", FONTSIZE_SCORE)
        self.small_font  = pygame.font.Font("assets/fonts/PublicPixel-0W5Kv.ttf", 10)
        self.action_font = pygame.font.Font("assets/fonts/ARCADE_I.TTF", FONTSIZE_ACTION)

    def requestId(self):
        if(self.idFrame == 0):
            self.send(['id_r',0,0])
            self.idFrame = 1
        elif self.idFrame < self.idFrames:
            self.idFrame = self.idFrame+1
        else:
            self.idFrame = 0


    def handleGameEvents(self):
        if(self.currentState == "STATE_CONNECTING"):
            if self.id == 0:
                self.requestId()
            return

        key_bulletshield = ''
        key_updown = ''
        key_leftright = ''
        action = False

        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if(self.currentState == "STATE_SPLASH"):
                    self.id = 0
                    self.currentState = "STATE_CONNECTING"
                    return
                elif(self.currentState == "STATE_TOAST"):
                    if(self.toastedAt is not None):
                        now = pygame.time.get_ticks()
                        if now - self.toastedAt >= self.toastTime:
                            self.toastedAt = None
                    else:
                        self.id = 0
                        self.currentState = "STATE_CONNECTING"
                    return
                elif(self.currentState == "STATE_PLAYING" and self.id in self.shipMap):
                    key_bulletshield = 'B'
                    channel2.play(self.shoot_sound)
                    action = True

        if (self.currentState != "STATE_PLAYING" or self.id not in self.shipMap):
            print("ID:", self.id, "STATE:", self.currentState)
            return

        is_key_pressed = pygame.key.get_pressed()


        if is_key_pressed[pygame.K_UP]:
            key_updown = 'U'
            action = True
            if not channel1.get_busy():
                channel1.play(self.thrust_sound)
            self.push_Cam()
        elif is_key_pressed[pygame.K_DOWN]:
            key_updown = 'D'
            action = True
        if is_key_pressed[pygame.K_RIGHT]:
            key_leftright = 'R'
            action = True
        elif is_key_pressed[pygame.K_LEFT]:
            key_leftright = 'L'
            action = True
        if is_key_pressed[pygame.K_LSHIFT] or is_key_pressed[pygame.K_RSHIFT]:
            key_bulletshield = 'S'
            action = True

        if self.joystick:
            axisX = round(self.joystick.get_axis(0),1)
            axisY = round(self.joystick.get_axis(1),1)
            button1 = self.joystick.get_button(0)
            button2 = self.joystick.get_button(1)

            if (button2):
                if(self.button2_fresh):
                    key_bulletshield = 'S'
                    action = True
                    self.button2_fresh = False
            else:
                self.button2_fresh = True

            if (button1):
                if(self.button1_fresh):
                    key_bulletshield = 'B'
                    channel2.play(self.shoot_sound)
                    action = True
                    self.button1_fresh = False
            else:
                self.button1_fresh = True

            if (axisX < 0):
                key_leftright = 'L'
                action = True
            elif (axisX > 0):
                key_leftright = 'R'
                action = True
            if (axisY > 0):
                key_updown = 'D'
                action = True
            elif (axisY < 0):
                key_updown = 'U'
                if not channel1.get_busy():
                    channel1.play(self.thrust_sound)
                self.push_Cam()
                action = True

        if action == True:
            msg = ['k', self.id, [key_updown, key_leftright, key_bulletshield]]
            self.send(msg)

    def update(self, gameEvent):
        type, data = gameEvent

        if type == 'id':
            if self.id == 0:
                self.id = data
                self.currentState = "STATE_PLAYING"
                msg = ['pr', self.id, 0]
                self.send(msg)
            return

        if type == 's':
            for ship in data:
                playerId = ship[0]
                if playerId in self.shipMap:
                    if(self.shipMap[playerId].dead == 0):
                        self.shipMap[playerId].update(Vector2(ship[2], ship[3]), Vector2(ship[4], ship[5]), ship[6], ship[7], ship[8], ship[9], ship[10])
                    elif(playerId == self.id):
                        #if(self.shipMap[self.id].dead == 2):
                        if(self.currentState is not "STATE_TOAST"):
                            self.currentState = "STATE_TOAST"
                            self.toastedAt = pygame.time.get_ticks()
                elif(ship[8] == 0): # Not dead
                    self.shipMap[playerId] = Spaceship(ship[0], self.shipSprites, Vector2(ship[2], ship[3]), Vector2(0, 0), Vector2(ship[4], ship[5]), ship[6], ship[7], ship[8], ship[9], ship[10])


        if type == 'b':
            for key, item in self.bulletMap.items():
                item.touched = False

            for bullet in data:
                objectId = bullet[1]
                if objectId in self.bulletMap:
                    self.bulletMap[objectId].update(Vector2(bullet[2], bullet[3]))
                else:
                    self.bulletMap[objectId] = Bullet(bullet[0], bullet[1], self.s_bullet, Vector2(bullet[2], bullet[3]), Vector2(bullet[4], bullet[5]) )
                self.bulletMap[objectId].touched = True

            delete = []
            for key, item in self.bulletMap.items():
                if item.touched == False:
                    delete.append(key)
            
            for key in delete:
                del self.bulletMap[key]
 
        if type == 'a':
            for key, item in self.asteroidMap.items():
                item.touched = False

            for asteroid in data:
                objectId = asteroid[1]
                if objectId in self.asteroidMap:
                    self.asteroidMap[objectId].update(Vector2(asteroid[2], asteroid[3]))
                else: # objectid, sprite_sheet, position, direction, size=3
                    self.asteroidMap[objectId] = Asteroid(objectId, self.asteroidSheet, self.s_debri, Vector2(asteroid[2], asteroid[3]), Vector2(asteroid[4], asteroid[5]), self.asteroidMap.update, self.debri.append, size=asteroid[6])
                self.asteroidMap[objectId].touched = True

            delete = []
            for key, item in self.asteroidMap.items():
                if item.touched == False:
                    item.hit()
                    self.hit_sound.play()
                    delete.append(key)

            for key in delete:
                del self.asteroidMap[key]

        self.draw()
        pygame.display.flip()

    def push_Cam(self):
        ## Give the cam a push on keypress
        if self.id in self.shipMap:
            myship = self.shipMap[self.id]
            if(myship.direction[0] > 0): # positive movement
                if(self.cam_offset[0] > -(SCREEN_SIZE*0.35)):
                    self.cam_offset = (self.cam_offset[0]-(myship.direction[0]),self.cam_offset[1])

            if(myship.direction[0] < 0): # negative movement
                if(self.cam_offset[0] < SCREEN_SIZE*0.35):
                    self.cam_offset = (self.cam_offset[0]+(abs(myship.direction[0])),self.cam_offset[1])

            if(myship.direction[1] > 0): # positive movement
                if(self.cam_offset[1] > -SCREEN_SIZE*0.35):
                    self.cam_offset = (self.cam_offset[0],self.cam_offset[1]-(abs(myship.direction[1])))

            if(myship.direction[1] < 0): # negative movement
                if(self.cam_offset[1] < SCREEN_SIZE*0.35):
                    self.cam_offset = (self.cam_offset[0],self.cam_offset[1]+(abs(myship.direction[1])))

    def draw_state_splash(self):
        self.playground.blit(self.background, (0,0))
        self.screen.blit(self.playground,(-MID_GROUND,-MID_GROUND))
        self.screen.blit(self.s_title,(0,50))

        text_surface = self.small_font.render("SHOOT TO START", True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (MID_SCREEN, MID_SCREEN+35)
        self.screen.blit(text_surface, text_rect)

    def draw_state_connecting(self):
        self.draw_state_playing()
        text_surface = self.small_font.render("CONNECTING", True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (MID_SCREEN, MID_SCREEN+35)
        self.screen.blit(text_surface, text_rect)

    def draw_state_toast(self):
        self.draw_state_playing()
        titleText = "TOAST!"

        if self.id in self.shipMap:
            myship = self.shipMap[self.id]
            if(myship.highScore < myship.score):
                titleText = "HIGH SCORE!"
            else:
                text_surface = self.small_font.render("High Score: " + str(myship.highScore), True, (255,255,255))
                self.screen.blit(text_surface, (45, MID_SCREEN+20))

        text_surface = self.action_font.render(titleText, True, (200,200,200))
        text_rect = text_surface.get_rect()
        text_rect.center = (MID_SCREEN,MID_SCREEN-20)
        self.screen.blit(text_surface, text_rect)

        text_surface = self.small_font.render("Your Score: " + str(myship.score), True, (255,255,255))
        self.screen.blit(text_surface, (45, MID_SCREEN+5))


    def draw_state_playing(self):
        self.playground.blit(self.background, (0,0))

        for key, asteroid in self.asteroidMap.items():
            asteroid.draw(self.playground)

        for key, ship in self.shipMap.items():
            ship.draw(self.playground)

        for dust in self.debri[:]:
            dust.draw(self.playground)
            dust.move()
            if dust.moves < 1:
               self.debri.remove(dust) 

        for key, bullet in self.bulletMap.items():
            bullet.draw(self.playground)

        # Keep centering slowly
        if(self.cam_offset[0] > 1):
            self.cam_offset = (self.cam_offset[0]-0.25,self.cam_offset[1])
        elif(self.cam_offset[0] < 1):
            self.cam_offset = (self.cam_offset[0]+0.25,self.cam_offset[1])
        if(self.cam_offset[1] > 1):
            self.cam_offset = (self.cam_offset[0],self.cam_offset[1]-0.25)
        elif(self.cam_offset[1] < 1):
            self.cam_offset = (self.cam_offset[0],self.cam_offset[1]+0.25)

        if self.id in self.shipMap:
            centre_position = (-self.shipMap[self.id].position[0]+MID_SCREEN,-self.shipMap[self.id].position[1]+MID_SCREEN)
        else:
            centre_position = (-MID_SCREEN,-MID_SCREEN)

        # Add the cam offset to actual center for some more fluid ship moevent
        centre_position = tuple(map(sum, zip(centre_position, self.cam_offset)))

        infinityBlit(self.playground, centre_position, self.screen)

        if self.id in self.shipMap:
            text_surface = self.score_font.render(str(self.shipMap[self.id].score), True, (255,255,255))
            rect = text_surface.get_rect()
            self.screen.blit(text_surface, (10,10))

    def draw(self):
        if self.currentState == self.states[0]:
            self.draw_state_splash()
        elif self.currentState == self.states[1]:
            self.draw_state_connecting()
        elif self.currentState == self.states[3]:
            self.draw_state_toast()
        else:
            self.draw_state_playing()

    def loop(self):
        while True:
            self.handleGameEvents()
            self.clock.tick(60)
