#  LIST OF SPRITES THAT NEED TO BE MADE
# [ ] Player
# [ ] Base (Space Station)
# [X] Asteroids
# [ ] Laser

import arcade
import random
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Superman Survival"
PLAYER_SCALING = 1
ASTEROID_SCALING = 0.8
PLAYER_SPEED = 5
KRYPTO_SCALING = 0.8
SPAWN_SPEED = 1.0

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Music
        self.background_music = arcade.load_sound("space_theme.mp3")
        self.music_player = None

        # Game States
        self.show_instructions = True
        self.game_over = False
        
        # Scoring
        self.score = 0
        self.high_score = self.load_high_score()
        
        # Sprite lists
        self.player_list = None
        self.asteroid_list = None
        self.krypto_list = None
        self.station_list = None 
        
        # Individual Sprites
        self.player_sprite = None
        self.sun_sprite = None
        self.lois_preview = None
        
        self.spawn_timer = 0
        self.collision_sound = arcade.load_sound(":resources:sounds/hit2.wav")
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def load_high_score(self):
        """Loads high score from a file. Returns 0 if file doesn't exist."""
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                try:
                    return int(f.read())
                except:
                    return 0
        return 0

    def save_high_score(self):
        """Saves current high score to a file."""
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def setup(self):
        """Set up the game variables and reset the game state."""
        self.player_list = arcade.SpriteList()
        self.station_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.krypto_list = arcade.SpriteList()
        
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0

        # Player
        self.player_sprite = arcade.Sprite("images/sups.png", PLAYER_SCALING)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        # Lois Preview Sprite (Only used on start screen)
        self.lois_preview = arcade.Sprite("images/louis.png", PLAYER_SCALING)

        # The Sun (Safe Zone Center)
        self.sun_sprite = arcade.Sprite("images/sun.png", 3.5)
        self.sun_sprite.center_x = 100
        self.sun_sprite.center_y = 500
        self.station_list.append(self.sun_sprite)

        for i in range(5):
            self.spawn_asteroid()
        
        if not self.music_player:
            self.music_player = arcade.play_sound(self.background_music, volume=0.5)

    def spawn_asteroid(self):
        asteroid = arcade.Sprite("images/stroid_sprite.png", ASTEROID_SCALING)
        asteroid.center_x = random.randrange(SCREEN_WIDTH)
        asteroid.center_y = SCREEN_HEIGHT + 20
        asteroid.change_y = -random.uniform(1, 3) 
        self.asteroid_list.append(asteroid)

    def spawn_kryptonite(self):
        krap = arcade.Sprite("images/krypto.png", KRYPTO_SCALING)
        krap.center_x = random.randrange(SCREEN_WIDTH)
        krap.center_y = SCREEN_HEIGHT + 20
        krap.change_y = -4 
        self.krypto_list.append(krap)

    def on_draw(self):
        self.clear()
        
        # 1. Draw all game objects
        self.station_list.draw()
        self.asteroid_list.draw()
        self.krypto_list.draw()
        self.player_list.draw()

        # 2. Draw HUD
        arcade.draw_text(f"Score: {self.score}", 10, 40, arcade.color.WHITE, 14)
        arcade.draw_text(f"High Score: {self.high_score}", 10, 20, arcade.color.GOLD, 14)

        # 3. Start Instructions Pop-up
        if self.show_instructions:
            # White Background Box
            arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH/2 - 300, SCREEN_WIDTH/2 + 300, 
                                              SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200, 
                                              arcade.color.WHITE)
            arcade.draw_lrbt_rectangle_outline(SCREEN_WIDTH/2 - 300, SCREEN_WIDTH/2 + 300, 
                                               SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200, 
                                               arcade.color.BLACK, 3)

            arcade.draw_text("SUPERMAN SURVIVAL", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, 
                             arcade.color.BLACK, 35, anchor_x="center", bold=True)
            
            # Lois Sprite on the Left
            if self.lois_preview:
                self.lois_preview.center_x = SCREEN_WIDTH/2 - 180
                self.lois_preview.center_y = SCREEN_HEIGHT/2 + 20
                arcade.draw_sprite(self.lois_preview)
            
            # Instructions on the Right
            rules = ("INSTRUCTIONS:\n"
                     "- Use ARROWS to move Superman.\n"
                     "- Collect Asteroids for +1 point.\n"
                     "- Green Kryptonite = GAME OVER.\n"
                     "- Hide behind the SUN to stay safe!")
            
            arcade.draw_text(rules, SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 30, 
                             arcade.color.BLACK, 14, anchor_x="left", multiline=True, width=300)

            # Centered Start Text at the Bottom
            arcade.draw_text("Press SPACE to Start", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 160, 
                             arcade.color.DARK_BLUE, 24, anchor_x="center", bold=True)

        # 4. Game Over Pop-up
        elif self.game_over:
            arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH/2 - 250, SCREEN_WIDTH/2 + 250, 
                                              SCREEN_HEIGHT/2 - 120, SCREEN_HEIGHT/2 + 80, 
                                              arcade.color.WHITE)
            arcade.draw_lrbt_rectangle_outline(SCREEN_WIDTH/2 - 250, SCREEN_WIDTH/2 + 250, 
                                               SCREEN_HEIGHT/2 - 120, SCREEN_HEIGHT/2 + 80, 
                                               arcade.color.BLACK, 3)

            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10, 
                             arcade.color.RED, 50, anchor_x="center", bold=True)
            
            arcade.draw_text("Press SPACE to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, 
                             arcade.color.BLACK, 20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if (self.show_instructions or self.game_over) and key == arcade.key.SPACE:
            self.show_instructions = False
            self.setup()
            return

        if not self.show_instructions and not self.game_over:
            if key == arcade.key.UP:
                self.player_sprite.change_y = PLAYER_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -PLAYER_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -PLAYER_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        if self.show_instructions or self.game_over:
            return 

        self.spawn_timer += delta_time
        if self.spawn_timer > SPAWN_SPEED:
            self.spawn_asteroid()
            if random.random() < 0.5:
                self.spawn_kryptonite()
            self.spawn_timer = 0

        self.player_list.update()
        
        # --- SCREEN BOUNDARIES ---
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

        self.asteroid_list.update()
        self.krypto_list.update()

        dist = arcade.get_distance_between_sprites(self.player_sprite, self.sun_sprite)
        in_safe_zone = dist < 80 

        asteroids_hit = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
        for a in asteroids_hit:
            a.remove_from_sprite_lists()
            if not in_safe_zone:
                self.score += 1
                arcade.play_sound(self.collision_sound)
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

        kryptonite_hit = arcade.check_for_collision_with_list(self.player_sprite, self.krypto_list)
        if len(kryptonite_hit) > 0:
            if not in_safe_zone:
                self.game_over = True
            else:
                for k in kryptonite_hit:
                    k.remove_from_sprite_lists() 

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()