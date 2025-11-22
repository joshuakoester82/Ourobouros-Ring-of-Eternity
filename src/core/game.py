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

        # Player (spawn in center of screen)
        self.player = Player(
            x=NATIVE_WIDTH // 2 - 8,
            y=NATIVE_HEIGHT // 2 - 8
        )

        print(f"Game initialized: {WINDOW_WIDTH}x{WINDOW_HEIGHT} " +
              f"(native: {NATIVE_WIDTH}x{NATIVE_HEIGHT}, scale: {SCALE_FACTOR}x)")

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic"""
        # State-based updates will go here
        if self.state_machine.is_state(GameState.INIT):
            # Initialize game world, then transition to EXPLORE
            self.state_machine.change_state(GameState.EXPLORE)
        elif self.state_machine.is_state(GameState.EXPLORE):
            # Update player
            self.player.handle_input()
            self.player.update()

    def render(self):
        """Render the game"""
        # Clear the native surface
        self.native_surface.fill(COLOR_BLACK)

        # Render game objects to native surface
        if self.state_machine.is_state(GameState.EXPLORE):
            # Render player
            self.player.render(self.native_surface)

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
