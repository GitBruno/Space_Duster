import pygame
from pygame.math import Vector2

from defines import *
from models import s_Spaceship, s_Bullet

class Game:
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
            self._send_update()
            self.clock.tick(60)
 
    def handle_input(self, data, source):
        
        print(data,source)
        
        messageType = data[0]
        playerId    = data[1]

        if(messageType == 'id'):
            self.clientCounter += 1
            self.send(["id",self.clientCounter],source[0])
            return

        if playerId == 0: return

        return

        ship = self.shipmap[playerId]
        if(ship.alpha <= 250):
            ship.alpha = ship.alpha + 5
        else:
            ship.alpha = 255

        if(messageType == 'key'):
            key_updown       = data[2]
            key_leftright    = data[3]
            key_bulletshield = data[4]

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
                self.bullets.append(s_Bullet(ship.position, ship.direction * ship.BULLET_SPEED + ship.velocity))


    def addPlayer(self, playerId):
        self.shipmap[playerId] = s_Spaceship(playerId)

    def _send_update(self):
        update_ships_msg = ['ships']
        update_bullet_msg = ['bullets']

        for b in self.bullets:
            b.move()
            #if(b.moves <= 0):
            #  bullets.remove(b)
            #else:
            update_bullet_msg.append([b.position[0], b.position[1]])

        for key, ship in self.shipmap.items():
            ship.move()
            update_ships_msg.append([ship.ownerid, ship.position[0], ship.position[1], ship.alpha, ship.thruster, ship.direction[0], ship.direction[1]])
            # Consider ships dead when no control has happend?
            ship.alpha = ship.alpha - 0.5
            if(ship.alpha < 0):
                ship.alpha = 0
            ship.thruster = False

        self.send(update_ships_msg)
        self.send(update_bullet_msg)
