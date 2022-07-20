import pygame
from pygame.math import Vector2

from defines import *
from models import s_Spaceship, s_Bullet, s_Asteroid
from utilis import get_random_position

class s_Game:
    clientCounter = 0
    def __init__(self, send):
        self.send = send
        self.clock = pygame.time.Clock()
        self.shipmap = {}
        self.bullets = []
        self.asteroids = []

        for _ in range (16):
            #while True:
            #    position = get_random_position(self.playground)
            #    if (
            #        position.distance_to(self.spaceship.position)
            #        > self.MIN_ASTEROID_DISTANCE
            #    ):
            #        break
            self.asteroids.append(s_Asteroid(get_random_position(), self.asteroids.append))

    def loop(self):
        while True:
            self._update()
            self.clock.tick(60)
 
    def handle_input(self, message, source):

        type, playerId, data = message

        if type == 'id_r':
            self.clientCounter += 1
            self.send(["id", self.clientCounter],source[0])
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
                self.bullets.append(s_Bullet(ship.ownerid, ship.position, ship.direction * BULLET_SPEED + ship.velocity))

    def addPlayer(self, playerId):
        self.shipmap[playerId] = s_Spaceship(playerId)

    def _sendUpdateMsg(self,key,objArr):
        delKeys = []
        updateMsg = [key,[]]
        sendMsg = False

        for item in objArr:
            item.move()
            if hasattr(item,'moves'):
                if(item.moves <= 0):
                    delKeys.append(item)
            updateMsg[1].append(item.getData())
            sendMsg = True

        for key in delKeys:
            objArr.remove(key)

        if(sendMsg) : self.send(updateMsg)

    def _update(self):
        self._sendUpdateMsg('a',self.asteroids)
        self._sendUpdateMsg('b',self.bullets)

        update_ships_msg  = ['s',[]]
        delKeys = []
        sendMsg = False
        for key, ship in self.shipmap.items():
            ship.move()
            ship.alpha = ship.alpha - 0.5
            if(ship.alpha > 0):
                update_ships_msg[1].append(ship.getData())
                ship.thruster = False
                sendMsg = True
            else:
                ship.alpha = 0
                delKeys.append(key)

        for key in delKeys:
            del self.shipmap[key]
            #self.send(['d', key])

        if (sendMsg) : self.send(update_ships_msg)
