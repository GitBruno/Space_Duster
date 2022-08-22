import sys, pygame
from pygame import Vector2
from pygame.locals import *
from defines import *
from utilis import load_sprite, infinityBlit, get_image_path
from models import Spaceship, Bullet, Asteroid
from spritesheet import SpriteSheet

class c_Game:
    def __init__(self, send, screen):
        self.clock = pygame.time.Clock()
        self.id = 0
        self.idFrame  = 0
        self.idFrames = 120
        self.send = send
        self.screen = screen
        self.playground = pygame.Surface((GROUND_SIZE, GROUND_SIZE)) 
        self.background = load_sprite("space", False)

        self.shipSprites = [load_sprite('spaceship'),load_sprite("spaceship_thrust")]
        self.s_bullet = load_sprite('bullet')
        self.asteroidSheet = SpriteSheet(get_image_path("asteroid_8x8-sheet"))

        self.s_title = load_sprite('space_duster_256')
        
        self.shipMap = {}
        self.bulletMap = {}
        self.asteroidMap = {}

    def requestId(self):
        if self.idFrame < self.idFrames:
            self.idFrame = self.idFrame+1
        else:
            self.idFrame = 0
            self.send(['id_r',0,0])

    def sendGameEvents(self):
        if self.id == 0:
            self.requestId()
            return

        key_bulletshield = ''
        key_updown = ''
        key_leftright = ''
        action = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                key_bulletshield = 'B'
                action = True

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_UP]:
            key_updown = 'U'
            action = True
            #self.push_Cam()
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

        if action == True:
            msg = ['k', self.id, [key_updown, key_leftright, key_bulletshield]]
            self.send(msg)

    def update(self, gameEvent):
        type, data = gameEvent

        if type == 'id':
            if self.id == 0:
                self.id = data
            return

        if type == 's':
            for ship in data:
                playerId = ship[0]
                if playerId in self.shipMap:
                    self.shipMap[playerId].update(Vector2(ship[2], ship[3]), Vector2(ship[4], ship[5]), ship[6], ship[8], ship[9])
                else:
                    self.shipMap[playerId] = Spaceship(ship[0], self.shipSprites, Vector2(ship[2], ship[3]), Vector2(0, 0), Vector2(ship[4], ship[5]), ship[6], ship[7], ship[8], ship[9])

        if type == 'b':
            for key, item in self.bulletMap.items():
                item.touched = False

            for bullet in data:
                objectId = bullet[1]
                if objectId in self.bulletMap:
                    self.bulletMap[objectId].update(Vector2(bullet[2], bullet[3]))
                else:
                    self.bulletMap[objectId] = Bullet(bullet[0], bullet[1], self.s_bullet, bullet[6], Vector2(bullet[2], bullet[3]), Vector2(bullet[4], bullet[5]) )
                self.bulletMap[objectId].touched = True

            delete = []
            for key, item in self.bulletMap.items():
                if item.touched == False:
                    delete.append(key)
            
            for key in delete:
                del self.bulletMap[key]
 
        if type == 'a':
            for asteroid in data:
                objectId = asteroid[1]
                if objectId in self.asteroidMap:
                    self.asteroidMap[objectId].update(Vector2(asteroid[2], asteroid[3]))

                else: # objectid, sprite_sheet, position, direction, size=3
                    self.asteroidMap[objectId] = Asteroid(objectId, self.asteroidSheet, Vector2(asteroid[2], asteroid[3]), Vector2(asteroid[4], asteroid[5]), None, size=asteroid[6])

        self.draw()
        pygame.display.flip()

    def draw(self):
        self.playground.blit(self.background, (0,0))

        for key, bullet in self.bulletMap.items():
            bullet.draw(self.playground)

        for key, asteroid in self.asteroidMap.items():
            asteroid.draw(self.playground)

        for key, ship in self.shipMap.items():
            ship.draw(self.playground)

        if self.id in self.shipMap:
            centre_position = (-self.shipMap[self.id].position[0]+MID_SCREEN,-self.shipMap[self.id].position[1]+MID_SCREEN)
        else:
            centre_position = (-MID_SCREEN,-MID_SCREEN)

        infinityBlit(self.playground, centre_position, self.screen)

    def loop(self):
        # INIT SCREEN BEFORE GETTING UPDATES FROM SERVER
        self.playground.blit(self.background, (0,0))
        self.screen.blit(self.playground,(-MID_GROUND,-MID_GROUND))
        self.screen.blit(self.s_title,(0,50))
        pygame.display.flip()
        while True:
            self.sendGameEvents()
            self.clock.tick(60)
