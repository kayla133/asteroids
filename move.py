import arcade

PLAYER_SPEED = 5

class Move:
    def __init__(self, player_sprite):
        self.player = player_sprite

    def on_key_press(self, key):
        if key == arcade.key.UP: self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN: self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT: self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT: self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key):
        if key in [arcade.key.UP, arcade.key.DOWN]: self.player.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.RIGHT]: self.player.change_x = 0