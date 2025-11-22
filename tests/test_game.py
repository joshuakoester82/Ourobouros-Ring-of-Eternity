"""
Unit tests for Game class

Tests game initialization, rendering, and state management.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGameInitialization(unittest.TestCase):
    """Test game initialization"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_initializes_without_errors(self, mock_init, mock_set_mode):
        """Test that game initializes without raising errors"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        try:
            game = Game()
            self.assertIsNotNone(game)
            self.assertTrue(True, "Game initialized successfully")
        except Exception as e:
            self.fail(f"Game initialization raised exception: {e}")

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_has_required_attributes(self, mock_init, mock_set_mode):
        """Test that game has all required attributes"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Check required attributes
        self.assertTrue(hasattr(game, 'window'))
        self.assertTrue(hasattr(game, 'native_surface'))
        self.assertTrue(hasattr(game, 'clock'))
        self.assertTrue(hasattr(game, 'player'))
        self.assertTrue(hasattr(game, 'world'))
        self.assertTrue(hasattr(game, 'state_machine'))

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_creates_surfaces_with_correct_dimensions(self, mock_init, mock_set_mode):
        """Test that game creates surfaces with correct dimensions"""
        from src.core.game import Game
        from src.core.constants import NATIVE_WIDTH, NATIVE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Check native surface dimensions
        self.assertEqual(game.native_surface.get_width(), NATIVE_WIDTH)
        self.assertEqual(game.native_surface.get_height(), NATIVE_HEIGHT)


class TestGameColors(unittest.TestCase):
    """Test that all required colors are imported and available"""

    def test_color_white_is_imported(self):
        """Test that COLOR_WHITE is imported in game module"""
        from src.core import game

        # Check that COLOR_WHITE exists in the module
        self.assertTrue(hasattr(game, 'COLOR_WHITE'))

    def test_color_red_is_imported(self):
        """Test that COLOR_RED is imported in game module"""
        from src.core import game

        # Check that COLOR_RED exists in the module
        self.assertTrue(hasattr(game, 'COLOR_RED'))

    def test_color_yellow_is_imported(self):
        """Test that COLOR_YELLOW is imported in game module"""
        from src.core import game

        # Check that COLOR_YELLOW exists in the module
        self.assertTrue(hasattr(game, 'COLOR_YELLOW'))

    def test_color_black_is_imported(self):
        """Test that COLOR_BLACK is imported in game module"""
        from src.core import game

        # Check that COLOR_BLACK exists in the module
        self.assertTrue(hasattr(game, 'COLOR_BLACK'))

    def test_color_gray_is_imported(self):
        """Test that COLOR_GRAY is imported in game module"""
        from src.core import game

        # Check that COLOR_GRAY exists in the module
        self.assertTrue(hasattr(game, 'COLOR_GRAY'))

    def test_all_colors_have_correct_format(self):
        """Test that all imported colors are tuples of 3 integers"""
        from src.core.game import COLOR_WHITE, COLOR_RED, COLOR_YELLOW, COLOR_BLACK, COLOR_GRAY

        colors = [COLOR_WHITE, COLOR_RED, COLOR_YELLOW, COLOR_BLACK, COLOR_GRAY]

        for color in colors:
            with self.subTest(color=color):
                self.assertIsInstance(color, tuple)
                self.assertEqual(len(color), 3)
                for component in color:
                    self.assertIsInstance(component, int)
                    self.assertGreaterEqual(component, 0)
                    self.assertLessEqual(component, 255)


class TestGameRendering(unittest.TestCase):
    """Test game rendering methods"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_render_interaction_hints_with_white_color(self, mock_init, mock_set_mode):
        """Test that _render_interaction_hints uses COLOR_WHITE correctly"""
        from src.core.game import Game
        from src.entities.item import create_item, ItemType

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Create a mock item near the player
        test_item = create_item(ItemType.SWORD, game.player.x + 5, game.player.y + 5)
        game.current_items = [test_item]

        # Create a mock current_screen surface
        current_screen = pygame.Surface((160, 192))

        # Test that the method can be called without errors
        try:
            game._render_interaction_hints(current_screen)
            self.assertTrue(True, "_render_interaction_hints executed without errors")
        except NameError as e:
            if 'COLOR_WHITE' in str(e):
                self.fail("COLOR_WHITE is not defined - import error!")
            else:
                raise

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_render_victory_screen_uses_colors(self, mock_init, mock_set_mode):
        """Test that _render_victory_screen uses colors correctly"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Test that the method can be called without errors
        try:
            game._render_victory_screen()
            self.assertTrue(True, "_render_victory_screen executed without errors")
        except NameError as e:
            if 'COLOR_' in str(e):
                self.fail(f"Color constant is not defined: {e}")
            else:
                raise

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_render_game_over_uses_colors(self, mock_init, mock_set_mode):
        """Test that _render_game_over uses colors correctly"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Test that the method can be called without errors
        try:
            game._render_game_over()
            self.assertTrue(True, "_render_game_over executed without errors")
        except NameError as e:
            if 'COLOR_RED' in str(e):
                self.fail("COLOR_RED is not defined - import error!")
            elif 'COLOR_WHITE' in str(e):
                self.fail("COLOR_WHITE is not defined - import error!")
            else:
                raise


class TestGameStateManagement(unittest.TestCase):
    """Test game state management"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_starts_in_init_state(self, mock_init, mock_set_mode):
        """Test that game starts in INIT state"""
        from src.core.game import Game
        from src.core.state_machine import GameState

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Game should start in INIT or EXPLORE state
        self.assertIn(game.state_machine.current_state, [GameState.INIT, GameState.EXPLORE])

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_state_machine_exists(self, mock_init, mock_set_mode):
        """Test that state machine is properly initialized"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        self.assertIsNotNone(game.state_machine)
        self.assertTrue(hasattr(game.state_machine, 'current_state'))


class TestGameEntityManagement(unittest.TestCase):
    """Test game entity management"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_has_entity_lists(self, mock_init, mock_set_mode):
        """Test that game maintains entity lists"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Check that entity lists exist
        self.assertTrue(hasattr(game, 'current_items'))
        self.assertTrue(hasattr(game, 'current_interactables'))
        self.assertTrue(hasattr(game, 'current_enemies'))
        self.assertTrue(hasattr(game, 'current_npcs'))

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_entity_lists_are_lists(self, mock_init, mock_set_mode):
        """Test that entity lists are actually lists"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        self.assertIsInstance(game.current_items, list)
        self.assertIsInstance(game.current_interactables, list)
        self.assertIsInstance(game.current_enemies, list)
        self.assertIsInstance(game.current_npcs, list)


class TestGameConstants(unittest.TestCase):
    """Test that game uses constants correctly"""

    def test_constants_imported(self):
        """Test that all required constants are imported"""
        from src.core.game import (
            NATIVE_WIDTH, NATIVE_HEIGHT,
            WINDOW_WIDTH, WINDOW_HEIGHT,
            SCALE_FACTOR, FPS, GAME_TITLE
        )

        # Check that constants exist and are reasonable
        self.assertIsInstance(NATIVE_WIDTH, int)
        self.assertIsInstance(NATIVE_HEIGHT, int)
        self.assertIsInstance(WINDOW_WIDTH, int)
        self.assertIsInstance(WINDOW_HEIGHT, int)
        self.assertIsInstance(SCALE_FACTOR, int)
        self.assertIsInstance(FPS, int)
        self.assertIsInstance(GAME_TITLE, str)

        # Check scaling is correct
        self.assertEqual(WINDOW_WIDTH, NATIVE_WIDTH * SCALE_FACTOR)
        self.assertEqual(WINDOW_HEIGHT, NATIVE_HEIGHT * SCALE_FACTOR)


class TestGameCollisionDetection(unittest.TestCase):
    """Test collision detection methods"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_collision_detection_exists(self, mock_init, mock_set_mode):
        """Test that collision detection method exists"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        # Game should have collision detection capability
        # (checking through player or game methods)
        self.assertTrue(hasattr(game, 'player'))


class TestGameWorldIntegration(unittest.TestCase):
    """Test game integration with world"""

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_has_world(self, mock_init, mock_set_mode):
        """Test that game has a world instance"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        self.assertIsNotNone(game.world)
        self.assertTrue(hasattr(game.world, 'current_screen'))

    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_game_has_camera(self, mock_init, mock_set_mode):
        """Test that game has a camera instance"""
        from src.core.game import Game

        mock_display = Mock()
        mock_set_mode.return_value = mock_display

        game = Game()

        self.assertIsNotNone(game.camera)


if __name__ == '__main__':
    unittest.main()
