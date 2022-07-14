import sys, pygame
from pygame import Vector2
from pygame.locals import *
from defines import *
from utilis import load_sprite

class Board:
    def __init__(self, send):
        self.id = 0
        self.send = send
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption('Space Duster')
        self.playground = pygame.Surface((GROUND_SIZE, GROUND_SIZE)) 
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.ships = []

    def sendUserAction(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        is_key_pressed = pygame.key.get_pressed()
        key_bulletshield = ''
        key_updown = ''
        key_leftright = ''

        if is_key_pressed[pygame.K_UP]:
            key_updown = 'U'
            #self.push_Cam()
        elif is_key_pressed[pygame.K_DOWN]:
            key_updown = 'D'
        if is_key_pressed[pygame.K_RIGHT]    :
            key_leftright = 'R'
        elif is_key_pressed[pygame.K_LEFT]:
            key_leftright = 'L'
        if is_key_pressed[pygame.K_SPACE]:
            key_bulletshield = 'B'

        msg = ['key', self.id, key_updown, key_leftright, key_bulletshield]
        self.send(msg)

    def update(self, gameEvent):
        print(gameEvent)
        """
        if gameEvent[0] == 'id':
            self.id = gameEvent[1]
        elif gameEvent[0] == 'ships':
            otherShips = []
            for ship in gameEvent:
                if ship[0] == self.id:
                    myShip.update(ship[1], ship[2], ship[4], ship[5], ship[6])
                else:
                    otherShips.append(Spaceship(ship[1], ship[2], ship[0], ship[5], ship[6], ship[3]))
        elif gameEvent[0] == 'bullets':
            gameEvent.pop(0)
            bullets = []
            for b in gameEvent:
                bullets.append(Bullet(Vector2(b[0], b[1])))
        """

    def draw(self):
        self.playground.blit(self.background, (0,0))

        myShipPosition = Vector2(0,0)
        for ship in self.ships:
            if(ship.id == self.id):
                myShipPosition = ship.position
            ship.render()

        centre_position = (-myShipPosition[0]+MID_SCREEN,-myShipPosition[1]+MID_SCREEN)

        # Draw tile 8 borders
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (GROUND_SIZE,-GROUND_SIZE)))))
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (GROUND_SIZE,0)))))
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (GROUND_SIZE,GROUND_SIZE)))))
        
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (0,-GROUND_SIZE)))))
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (0,GROUND_SIZE)))))

        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (-GROUND_SIZE,-GROUND_SIZE)))))
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (-GROUND_SIZE,0)))))
        self.screen.blit(self.playground, tuple(map(sum, zip(centre_position, (-GROUND_SIZE,GROUND_SIZE)))))

        self.screen.blit(self.playground, centre_position)

    def loop(self):
        while True:
            self.sendUserAction()
            self.draw()
            pygame.display.flip()

