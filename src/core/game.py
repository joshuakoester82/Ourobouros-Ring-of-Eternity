"""
Main game class for Ouroboros - Ring of Eternity
"""

import pygame
from src.core.constants import (
    NATIVE_WIDTH, NATIVE_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SCALE_FACTOR, FPS, GAME_TITLE,
    COLOR_BLACK
)
from src.core.state_machine import StateMachine, GameState
from src.entities.player import Player
from src.entities.item import create_item, ItemType
from src.world.world import World
from src.world.camera import Camera
from src.world.screen import Direction, ScreenID
from src.ui.hud import HUD


class Game:
    """
    Main game class that handles initialization, game loop, and rendering
    """

    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()

        # Create the display window
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # Create native resolution surface for pixel-perfect rendering
        self.native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Game state
        self.running = False
        self.state_machine = StateMachine()

        # Delta time for frame-independent movement
        self.dt = 0

        # World and camera
        self.world = World()
        self.camera = Camera()

        # HUD
        self.hud = HUD()

        # Player (spawn in center of screen)
        self.player = Player(
            x=NATIVE_WIDTH // 2 - 8,
            y=NATIVE_HEIGHT // 2 - 8
        )

        # Spawn test items
        self._spawn_test_items()

        print(f"Game initialized: {WINDOW_WIDTH}x{WINDOW_HEIGHT} " +
              f"(native: {NATIVE_WIDTH}x{NATIVE_HEIGHT}, scale: {SCALE_FACTOR}x)")
        print(f"Starting in: {self.world.get_current_screen().name}")

    def _spawn_test_items(self):
        """Spawn test items in the world for demonstration"""
        # Hub - spawn some keys and crystals
        hub = self.world.get_screen(ScreenID.TOWER_HUB)
        hub.entities.append(create_item(ItemType.GOLD_KEY, 40, 40))
        hub.entities.append(create_item(ItemType.SWORD, 120, 40))

        # Gardens - spawn acorn and green crystal
        gardens_2 = self.world.get_screen(ScreenID.GARDENS_2)
        gardens_2.entities.append(create_item(ItemType.ACORN, 60, 60))

        gardens_4 = self.world.get_screen(ScreenID.GARDENS_4)
        gardens_4.entities.append(create_item(ItemType.GREEN_CRYSTAL, 80, 96))

        # Catacombs - spawn bomb and red crystal
        catacombs_2 = self.world.get_screen(ScreenID.CATACOMBS_2)
        catacombs_2.entities.append(create_item(ItemType.BOMB, 50, 80))

        catacombs_4 = self.world.get_screen(ScreenID.CATACOMBS_4)
        catacombs_4.entities.append(create_item(ItemType.RED_CRYSTAL, 80, 96))

        # Ruins - spawn chalice and blue crystal
        ruins_2 = self.world.get_screen(ScreenID.RUINS_2)
        ruins_2.entities.append(create_item(ItemType.CHALICE, 70, 70))

        ruins_3 = self.world.get_screen(ScreenID.RUINS_3)
        ruins_3.entities.append(create_item(ItemType.BLUE_CRYSTAL, 80, 96))

        # Cliffs - spawn flute and yellow crystal
        cliffs_2 = self.world.get_screen(ScreenID.CLIFFS_2)
        cliffs_2.entities.append(create_item(ItemType.FLUTE, 65, 75))

        cliffs_4 = self.world.get_screen(ScreenID.CLIFFS_4)
        cliffs_4.entities.append(create_item(ItemType.YELLOW_CRYSTAL, 80, 96))

        # Add silver key to catacombs
        catacombs_3 = self.world.get_screen(ScreenID.CATACOMBS_3)
        catacombs_3.entities.append(create_item(ItemType.SILVER_KEY, 80, 60))

        print("Test items spawned in world")

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.handle_space_interaction()

    def handle_space_interaction(self):
        """Handle SPACE key interaction (pickup/drop items)"""
        if not self.state_machine.is_state(GameState.EXPLORE):
            return

        current_screen = self.world.get_current_screen()

        # If player is holding an item, drop it
        if self.player.has_item():
            dropped_item = self.player.drop_item()
            if dropped_item is not None:
                # Place item at player's current position
                dropped_item.x = self.player.x + self.player.width // 2 - dropped_item.size // 2
                dropped_item.y = self.player.y + self.player.height // 2 - dropped_item.size // 2
                dropped_item.active = True
                current_screen.entities.append(dropped_item)
                print(f"Dropped: {dropped_item.get_name()}")
        else:
            # Try to pick up an item
            for entity in current_screen.entities:
                # Check if it's an item (has item_type attribute)
                if hasattr(entity, 'item_type'):
                    if entity.is_near_player(
                        self.player.x, self.player.y,
                        self.player.width, self.player.height
                    ):
                        if self.player.pick_up_item(entity):
                            entity.active = False
                            current_screen.entities.remove(entity)
                            print(f"Picked up: {entity.get_name()}")
                            break

    def update(self):
        """Update game logic"""
        # State-based updates will go here
        if self.state_machine.is_state(GameState.INIT):
            # Initialize game world, then transition to EXPLORE
            self.state_machine.change_state(GameState.EXPLORE)
        elif self.state_machine.is_state(GameState.EXPLORE):
            # Get current screen
            current_screen = self.world.get_current_screen()

            # Update player
            self.player.handle_input()
            self.player.update(current_screen)

            # Check for screen transitions
            transition_dir = self.camera.check_screen_transition(
                self.player.x, self.player.y,
                self.player.width, self.player.height
            )

            if transition_dir is not None:
                # Attempt to change screens
                if self.world.change_screen(transition_dir):
                    # Move player to opposite side of new screen
                    opposite = self.camera.get_opposite_direction(transition_dir)
                    new_x, new_y = self.camera.get_player_spawn_position(
                        opposite,
                        self.player.width,
                        self.player.height
                    )
                    self.player.x = new_x
                    self.player.y = new_y

    def render(self):
        """Render the game"""
        # Clear the native surface
        self.native_surface.fill(COLOR_BLACK)

        # Render game objects to native surface
        if self.state_machine.is_state(GameState.EXPLORE):
            # Render current screen
            current_screen = self.world.get_current_screen()
            current_screen.render(self.native_surface)

            # Render player
            self.player.render(self.native_surface)

            # Render HUD
            self.hud.render(self.native_surface, self.player)

        # Scale up the native surface to the window
        scaled_surface = pygame.transform.scale(
            self.native_surface,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.window.blit(scaled_surface, (0, 0))

        # Update the display
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        self.running = True
        print("Starting game loop...")

        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Render
            self.render()

            # Maintain 60 FPS and calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0

        # Cleanup
        self.quit()

    def quit(self):
        """Clean up and quit the game"""
        print("Shutting down...")
        pygame.quit()
