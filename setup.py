import arcade
from spawn import Spawn

PLAYER_SCALING = 1

class Setup:
    def __init__(self, game):
        game.player_list = arcade.SpriteList()
        game.station_list = arcade.SpriteList()
        game.asteroid_list = arcade.SpriteList()
        game.krypto_list = arcade.SpriteList()
        
        game.player_sprite = arcade.Sprite("images/sups.png", PLAYER_SCALING)
        game.player_sprite.center_x = 400
        game.player_sprite.center_y = 300
        game.player_list.append(game.player_sprite)

        game.lois_preview = arcade.Sprite("images/louis.png", PLAYER_SCALING)

        game.sun_sprite = arcade.Sprite("images/sun.png", 3.5)
        game.sun_sprite.center_x = 100
        game.sun_sprite.center_y = 500
        game.station_list.append(game.sun_sprite)
        game.station_list.append(Spawn.earth())

        for i in range(5):
            game.asteroid_list.append(Spawn.asteroid())