import pygame
from pygame.math import Vector2

from defines import *
from models import s_Spaceship, s_Bullet

class Game:
    def __init__(self, broadcast):
        self.broadcast = broadcast
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
 
    def handle_input(self, arr):
 
        print(str(arr))
        
        messageType = arr[0]
        playerid = arr[1]
 
        if playerid == 0: return
        ship = self.shipmap[playerid]
        if(ship.alpha <= 250):
            ship.alpha = ship.alpha + 5
        else:
            ship.alpha = 255

        if(messageType == 'key'):
            key_updown       = arr[2]
            key_leftright    = arr[3]
            key_bulletshield = arr[4]

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

        self._send_update()

    def addPlayer(self, playerID):
        self.shipmap[playerID] = s_Spaceship(playerID)

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

        self.broadcast(update_ships_msg)
        self.broadcast(update_bullet_msg)
