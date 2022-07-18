# Space Duster

> A multiplayer python game inspired by Asteroids

## Objective

Create a multiplayer Asteroids game that runs on a Raspberry Pi and can handle 16 players.

The player controls a single spaceship in an asteroid field that is traversed by the other players ships. The objective of the game is to shoot and destroy all other ships, whilst not colliding with astroids, or being hit by counter-fire.

#### History

This game is based on Asteroids which has it's physics model, control scheme, and gameplay elements derived from Spacewar!, Computer Space, and Space Invaders. The Asteroids game is rendered on a vector display in a two-dimensional view that wraps around both screen axes. As we have 16 players and a very small screen the play area has been made larger and we follow the ship with a camera. The field is still titled for infinacy.

## Install

    pip install -r requirements.txt

## Play

Start the server by running:

    py server.py

Then in a separate terminal start the client with:

    py client.py

Foreign clients can join by specifying the servers ipaddress eg:

    py client.py 192.168.0.1

### Specification

  - Screen Size: 256 x 256 pixels
  - 16 Players

#### Messages

**Client Messages**
| Event            | [0] Message type | [1] Player ID | [2] Data     |
|------------------|------------------|---------------|--------------|
| ID Request       | "id_r"           | `0`           | `0`          |
| Key Event        | "k"              | `int`         | `[Key Data]` |

**Server Messages**

| Event            | [0] Message type | [1] Data Array           |
|------------------|------------------|--------------------------|
| Id Assignment    | "id"             | [`int`]                  |
| Ships Update     | "s"              | [`[Ship Data]`]          |
| Bullets Update   | "b"              | [`[Bullet Data]`]        |

`Key Data`(array):
    0. key_updown
    1. key_leftright
    2. key_bulletshield

`Ship Data`(array):
    0. OwnerId (int)
    1. ObjectId (int)
    2. Position X (float)
    3. Position Y (float)
    4. Direction X (Float)
    5. Direction Y (Float)
    6. Thruster (Bool)
    7. Alpha (0-255)

`Bullet Data`(array):
    0. OwnerId (int)
    1. ObjectId (int)
    2. Position X (float)
    3. Position Y (float)
    4. Direction X (Float)
    5. Direction Y (Float)
    6. Moves (int)

### Dependencies

  See `requirements.txt`
