import pygame, random
from pygame.math import Vector2

from defines import *
from models import Spaceship, Bullet, Asteroid
from spritesheet import SpriteSheet
from utilis import get_random_position, new_object_id, load_sprite, get_image_path, getInfinityDistance

pygame.init()
pygame.display.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

class s_Game:
    clientCounter = 0
    def __init__(self, send):
        self.send = send
        self.clock = pygame.time.Clock()
        self.shipmap = {}
        self.bullets = []
        self.asteroids = {}
        self.debri = []

        self.shipSprites = [load_sprite('spaceship'),load_sprite("spaceship_thrust"),SpriteSheet(get_image_path("ship_explosion_7_41x41_287"))]
        self.s_bullet = load_sprite('bullet')
        self.s_debri  = load_sprite("debri")
        self.asteroidSheet = SpriteSheet(get_image_path("asteroid_8x8-sheet"))

        for _ in range (16):
            _ID=new_object_id()
            self.asteroids.update({_ID : Asteroid(_ID, self.asteroidSheet, self.s_debri, get_random_position(), Vector2(0, -1), self.asteroids.update, self.debri.append)} )

            #while True:
            #    position = get_random_position()
            #    myBreak = False
            #    for ship in self.shipmap:
            #        if ( position.distance_to(ship.position) > MIN_ASTEROID_DISTANCE):
            #            myBreak = True
            #    if(myBreak):
            #        break
            #self.asteroids.append(Asteroid(new_object_id(), self.asteroidSheet, position, Vector2(0, -1), self.asteroids.append))

    def moveItem(self, item):
        item.move()

        if hasattr(item,'alpha'):
            if(item.alpha <= 0):
                return False

        return True

    def moveItems(self, objCont):
        if type(objCont) is dict:
            for key, item in objCont.items():
                if(not self.moveItem(item)):
                    del objCont[item]
        else: #list
            for item in objCont[:]:
                if(not self.moveItem(item)):
                    objCont.remove(item)                

    def process_game_logic(self):
        self.moveItems(self.asteroids)
        self.moveItems(self.bullets)
        self.moveItems(self.shipmap)

        for bullet in self.bullets[:]:
            removeBullet = False
            deleteAstroids = []

            for key, asteroid in self.asteroids.items():
                if asteroid.collides_with(bullet):
                    removeBullet = True
                    self.shipmap[bullet.ownerid].score = self.shipmap[bullet.ownerid].score + (10-asteroid.size)
                    deleteAstroids.append(key)
            
            if (removeBullet == False):
                for key, ship in self.shipmap.items():
                    if ship.collides_with(bullet):
                        self.shipmap[bullet.ownerid].score += 100 
                        ship.dead = True
            
            if(removeBullet or getInfinityDistance(self.shipmap[bullet.ownerid].position, bullet.position) > SHIP_MAX_BULLET_DIST):
                self.bullets.remove(bullet)
            
            for key in deleteAstroids:
                self.asteroids[key].split()
                del self.asteroids[key]

        for key, ship in self.shipmap.items():
            for key, asteroid in self.asteroids.items():
                if asteroid.collides_with(ship):
                    ship.dead = True



    def loop(self):
        while True:
            self.process_game_logic()
            self.update()
            self.clock.tick(20)
 
    def handle_input(self, message, source):

        type, playerId, data = message

        if type == 'id_r':
            self.clientCounter += 1
            #self.send(["id", self.clientCounter],source[0])
            self.send(["id", self.clientCounter])
            return

        if playerId == 0: return

        if playerId not in self.shipmap:
            self.addPlayer(playerId)
 
        ship = self.shipmap[playerId]
        if(ship.alpha <= 250):
            ship.alpha = ship.alpha + 5
        else:
            ship.alpha = 255

        if(type == 'k'):
            key_updown       = data[0]
            key_leftright    = data[1]
            key_bulletshield = data[2]

            if(key_updown == 'U'):
                ship.accelerate()
                ship.thruster = 1
            elif(key_updown == 'D'):
                ship.slow_down()
                ship.thruster = 0

            if(key_leftright == 'L'):
                ship.rotate(clockwise=False)
            elif(key_leftright == 'R'):
                ship.rotate(clockwise=True)

            if(key_bulletshield == 'B'):
                self.bullets.append(Bullet(ship.ownerid, new_object_id(), self.s_bullet,
                  ship.position, ship.direction * BULLET_SPEED + ship.velocity))

    def addPlayer(self, playerId):
        self.shipmap[playerId] = Spaceship(playerId,self.shipSprites)

    def sendUpdateMsg(self, key, objContainer):
        updateMsg = [key,[]]

        if type(objContainer) is dict:
            for key, item in objContainer.items():
                updateMsg[1].append(item.getData())
                if hasattr(item,'thruster'):
                    item.thruster = 0
        else: # array
            for item in objContainer:
                updateMsg[1].append(item.getData())

        self.send(updateMsg)

    def update(self):
        self.sendUpdateMsg('a',self.asteroids)
        self.sendUpdateMsg('s',self.shipmap)
        self.sendUpdateMsg('b',self.bullets)
        print("UPDATE MESG SENT")
