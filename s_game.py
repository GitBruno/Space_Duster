import pygame
from pygame.math import Vector2

from defines import *
from models import s_Spaceship, s_Bullet

class s_Game:
    clientCounter = 0
    def __init__(self, send):
        self.send = send
        self.clock = pygame.time.Clock()
        self.shipmap = {}
        self.bullets = []
        self.asteroids = []
        self.debri = []
        self.explosions = []

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

    def _update(self):
        update_ships_msg  = ['s',[]]
        update_bullet_msg = ['b',[]]
        sendShips = False
        sendBullets = False

        delKeys = []
        for b in self.bullets:
            b.move()
            if(b.moves <= 0):
                delKeys.append(b)
            else:
                update_bullet_msg[1].append(b.getData())
                sendBullets = True

        for key in delKeys:
            self.bullets.remove(key)

        delKeys = []
        for key, ship in self.shipmap.items():
            ship.move()
            ship.alpha = ship.alpha - 0.5
            if(ship.alpha > 0):
                update_ships_msg[1].append(ship.getData())
                ship.thruster = False
                sendShips = True
            else:
                ship.alpha = 0
                delKeys.append(key)

        for key in delKeys:
            del self.shipmap[key]
            self.send(['d', key])

        if (sendShips)  : self.send(update_ships_msg)
        if (sendBullets): self.send(update_bullet_msg)
