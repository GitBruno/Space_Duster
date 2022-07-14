# Space Duster

> A multiplayer python game inspired by Asteroids

## Objective

Create a multiplayer Asteroids game that runs on a Raspberry Pi and can handle 16 players.

The player controls a single spaceship in an asteroid field that is traversed by the other players ships. The objective of the game is to shoot and destroy all other ships, whilst not colliding with astroids, or being hit by counter-fire.

#### History

This game is based on Asteroids which has it's physics model, control scheme, and gameplay elements derived from Spacewar!, Computer Space, and Space Invaders. The Asteroids game is rendered on a vector display in a two-dimensional view that wraps around both screen axes. As we have 16 players and a very small screen the play area has been made larger and we follow the ship with a camera. The field is still titled for infinacy.

### Specification

  - Screen Size: 256 x 256 pixels
  - 16 Players

## Install

    pip install -r requirements.txt

## Play

Start the server by running:

    py server.py

Then in a separate terminal start the client with:

    py client.py

Foreign clients can join by specifying the servers ipaddress eg:

    py client.py 192.168.0.1


### Dependencies

  See `requirements.txt`
