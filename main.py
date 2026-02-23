import arcade
import random
from score import Score
from spawn import Spawn
from setup import Setup
from move import Move

# ######################################################
# LIST OF SPRITES THAT NEED TO BE MADE
# [X] Superman / [X] Sun / [X] Asteroids / [X] Kryptonite / [X] Louis
# Features To-Do:
# [X] Add Earth / [X] Organize into Classes / [X] Levels / [X] Reset High Score
# ######################################################

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Superman Survival"
SPAWN_SPEED = 1.0

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Music setup
        self.background_music = arcade.load_sound("space_theme.mp3")
        self.music_player = None

        # Game States
        self.show_instructions = True
        self.game_over = False
        self.spawn_timer = 0
        
        # Initialize Score Class
        self.score_manager = Score()
        
        # Movement handler (set during setup)
        self.mover = None
        
        arcade.set_background_color((8, 48, 55))

    def setup(self):
        """Reset the game using the Setup class logic."""
        Setup(self) 
        self.mover = Move(self.player_sprite)
        self.score_manager.current = 0
        self.game_over = False
        self.spawn_timer = 0
        
        if not self.music_player:
            self.music_player = arcade.play_sound(self.background_music, volume=0.5)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Draw game objects
        self.station_list.draw()
        self.asteroid_list.draw()
        self.krypto_list.draw()
        self.player_list.draw()

        # Draw Score UI
        arcade.draw_text(f"Score: {self.score_manager.current}", 10, 40, arcade.color.WHITE, 14)
        arcade.draw_text(f"High Score: {self.score_manager.high_score}", 10, 20, arcade.color.GOLD, 14)

        # Overlay Screens
        if self.show_instructions:
            self.draw_instructions()
        elif self.game_over:
            self.draw_game_over()

    def draw_instructions(self):
        """Full instruction screen logic."""
        # White Box
        arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH/2 - 300, SCREEN_WIDTH/2 + 300, 
                                          SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200, 
                                          arcade.color.WHITE)
        arcade.draw_lrbt_rectangle_outline(SCREEN_WIDTH/2 - 300, SCREEN_WIDTH/2 + 300, 
                                           SCREEN_HEIGHT/2 - 200, SCREEN_HEIGHT/2 + 200, 
                                           arcade.color.BLACK, 3)

        arcade.draw_text("SUPERMAN SURVIVAL", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, 
                         arcade.color.BLACK, 35, anchor_x="center", bold=True)
        
        # FIX: Changed .draw() to arcade.draw_sprite()
        if self.lois_preview:
            self.lois_preview.center_x = SCREEN_WIDTH/2 - 180
            self.lois_preview.center_y = SCREEN_HEIGHT/2 + 20
            arcade.draw_sprite(self.lois_preview)
        
        rules = ("INSTRUCTIONS:\n"
                 "- Use ARROWS to move Superman.\n"
                 "- Collect Asteroids for +1 point.\n"
                 "- Green Kryptonite = GAME OVER.\n"
                 "- Hide behind the SUN to stay safe!")
        
        arcade.draw_text(rules, SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 30, 
                         arcade.color.BLACK, 14, anchor_x="left", multiline=True, width=300)

        arcade.draw_text("Press SPACE to Start", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 160, 
                         arcade.color.DARK_BLUE, 24, anchor_x="center", bold=True)

    def draw_game_over(self):
        """Full game over screen logic."""
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
        arcade.draw_text("Press R to Reset High Score", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, 
                         arcade.color.GRAY, 14, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.R:
            self.score_manager.reset_high_score()
        if (self.show_instructions or self.game_over) and key == arcade.key.SPACE:
            self.show_instructions = False
            self.setup()
        elif self.mover:
            self.mover.on_key_press(key)

    def on_key_release(self, key, modifiers):
        if self.mover:
            self.mover.on_key_release(key)

    def on_update(self, delta_time):
        if self.show_instructions or self.game_over:
            return 

        # Spawning Logic using Spawn Class
        self.spawn_timer += delta_time
        if self.spawn_timer > SPAWN_SPEED:
            self.asteroid_list.append(Spawn.asteroid())
            if random.random() < 0.5:
                self.krypto_list.append(Spawn.kryptonite())
            self.spawn_timer = 0

        # Update positions
        self.player_list.update()
        
        # Screen boundaries
        if self.player_sprite.left < 0: self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH: self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0: self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT: self.player_sprite.top = SCREEN_HEIGHT

        self.asteroid_list.update()
        self.krypto_list.update()

        # Safe Zone (Sun) Logic
        dist = arcade.get_distance_between_sprites(self.player_sprite, self.sun_sprite)
        in_safe_zone = dist < 80 

        # Asteroid Collisions
        asteroids_hit = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
        for a in asteroids_hit:
            a.remove_from_sprite_lists()
            if not in_safe_zone:
                self.score_manager.current += 1
                if self.score_manager.current > self.score_manager.high_score:
                    self.score_manager.high_score = self.score_manager.current
                    self.score_manager.save_high_score()

        # Kryptonite Collisions
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