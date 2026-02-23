import arcade
import random

# Import constants from main or define them here
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASTEROID_SCALING = 0.8
KRYPTO_SCALING = 0.7

class Spawn:
    @staticmethod
    def asteroid():
        asteroid = arcade.Sprite("images/stroid_sprite.png", ASTEROID_SCALING)
        asteroid.center_x = random.randrange(SCREEN_WIDTH)
        asteroid.center_y = SCREEN_HEIGHT + 20
        asteroid.change_y = -random.uniform(1, 3) 
        return asteroid

    @staticmethod
    def kryptonite():
        krap = arcade.Sprite("images/krypto.png", KRYPTO_SCALING)
        krap.center_x = random.randrange(SCREEN_WIDTH)
        krap.center_y = SCREEN_HEIGHT + 20
        krap.change_y = -4 
        return krap

    @staticmethod
    def earth():
        earth = arcade.Sprite("images/earth.png", 1.5)
        earth.center_x = SCREEN_WIDTH / 2
        earth.bottom = 0
        return earth