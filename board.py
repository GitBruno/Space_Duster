import sys, pygame
from pygame import Vector2
from pygame.locals import *
from defines import *
from utilis import load_sprite, infinityBlit
from models import c_Spaceship, c_Bullet

class Board:
    def __init__(self, send, screen):
        self.send = send
        self.screen = screen
        self.playground = pygame.Surface((GROUND_SIZE, GROUND_SIZE)) 
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.id = 0
        self.myShip = c_Spaceship(0, Vector2(MID_GROUND,MID_GROUND), Vector2(0,-1), 100)
        self.foreignShips = []
        self.bullets = []
        self.idFrame  = 0
        self.idFrames = 120

    def requestId(self):
        if self.idFrame < self.idFrames:
            self.idFrame = self.idFrame+1
        else:
            self.idFrame = 0
            self.send(['id_request'])

    def sendUserAction(self):
        if self.id == 0:
            self.requestId()
            return

        key_bulletshield = ''
        key_updown = ''
        key_leftright = ''

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                key_bulletshield = 'B'

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_UP]:
            key_updown = 'U'
            #self.push_Cam()
        elif is_key_pressed[pygame.K_DOWN]:
            key_updown = 'D'
        if is_key_pressed[pygame.K_RIGHT]    :
            key_leftright = 'R'
        elif is_key_pressed[pygame.K_LEFT]:
            key_leftright = 'L'
        if is_key_pressed[pygame.K_LSHIFT] or is_key_pressed[pygame.K_RSHIFT]:
            key_bulletshield = 'S'

        msg = ['key', self.id, key_updown, key_leftright, key_bulletshield]
        self.send(msg)

    def update(self, gameEvent):
        if gameEvent[0] == 'id':
            print(gameEvent)
        if gameEvent[0] == 'id' and self.id == 0:
            self.id = gameEvent[1]
            self.myShip.id = self.id
            self.myShip.alpha = 255
        elif gameEvent[0] == 's':
            gameEvent.pop(0)
            self.foreignShips = []
            for ship in gameEvent:
                if ship[0] == self.id:
                    self.myShip.update(Vector2(ship[1], ship[2]), Vector2(ship[5], ship[6]), ship[4])
                else:
                    self.foreignShips.append(c_Spaceship(ship[0],Vector2(ship[1], ship[2]), Vector2(ship[5], ship[6]), ship[4], ship[3]))
        elif gameEvent[0] == 'b':
            gameEvent.pop(0)
            self.bullets = []
            for b in gameEvent:
                self.bullets.append(c_Bullet(b[0],Vector2(b[1], b[2])))

    def draw(self):
        self.playground.blit(self.background, (0,0))
        myShipPosition = self.myShip.position

        self.myShip.draw(self.playground)

        for ship in self.foreignShips:
            ship.draw(self.playground)
        
        for bullet in self.bullets:
            bullet.draw(self.playground)

        centre_position = (-myShipPosition[0]+MID_SCREEN,-myShipPosition[1]+MID_SCREEN)

        infinityBlit(self.playground, centre_position, self.screen)

    def loop(self):
        while True:
            self.sendUserAction()
            self.draw()
            pygame.display.flip()
