import sys, pygame
from pygame import Vector2
from pygame.locals import *
from zmq import FAIL_UNROUTABLE
from defines import *
from utilis import load_sprite, infinityBlit
from models import c_Spaceship, c_GameObject

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
        self.s_bullet = load_sprite('bullet')
        self.shipMap = {}
        self.bulletMap = {}

    def requestId(self):
        if self.idFrame < self.idFrames:
            self.idFrame = self.idFrame+1
        else:
            self.idFrame = 0
            self.send(['id_r',0,0])

    def sendUserAction(self):
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
        if is_key_pressed[pygame.K_RIGHT]    :
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
                    self.shipMap[playerId].update(Vector2(ship[2], ship[3]), Vector2(ship[4], ship[5]), ship[6])
                else:
                    self.shipMap[playerId] = c_Spaceship(ship[0],Vector2(ship[2], ship[3]), Vector2(ship[4], ship[5]), ship[6], ship[7])

        if type == 'b':
            for bullet in data:
                objectId = bullet[1]
                moves = bullet[6]
                if objectId in self.bulletMap:
                    if moves > 4: # in case we miss a few frame
                        self.bulletMap[objectId].update(Vector2(bullet[2], bullet[3]))
                    else:
                        self.bulletMap.pop(objectId)
                elif moves > 4:
                    self.bulletMap[objectId] = c_GameObject(bullet[0], bullet[1], self.s_bullet, Vector2(bullet[2], bullet[3]), Vector2(bullet[4], bullet[5]) )
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.playground.blit(self.background, (0,0))

        for key, bullet in self.bulletMap.items():
            bullet.draw(self.playground)

        for key, ship in self.shipMap.items():
            ship.draw(self.playground)

        if self.id in self.shipMap:
            centre_position = (-self.shipMap[self.id].position[0]+MID_SCREEN,-self.shipMap[self.id].position[1]+MID_SCREEN)
        else:
            centre_position = (-MID_SCREEN,-MID_SCREEN)

        infinityBlit(self.playground, centre_position, self.screen)

    def loop(self):
        # INIT SCREEN BEFORE GETTING UPDATES FROM SERVER
        self.draw()
        pygame.display.flip()
        while True:
            self.sendUserAction()
            self.clock.tick(60)
