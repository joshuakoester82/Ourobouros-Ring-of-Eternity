"""
Unit tests to verify imports are correct

Tests that all required constants and colors can be imported.
"""

import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock pygame before importing anything that uses it
pygame_mock = MagicMock()
sys.modules['pygame'] = pygame_mock
sys.modules['pygame.display'] = MagicMock()
sys.modules['pygame.font'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()
sys.modules['pygame.sndarray'] = MagicMock()
sys.modules['pygame.time'] = MagicMock()


class TestGameImports(unittest.TestCase):
    """Test that game module imports are correct"""

    def test_color_imports_exist(self):
        """Test that all color constants can be imported from game module"""
        # This will fail if any color is not imported
        try:
            from src.core.game import COLOR_WHITE, COLOR_RED, COLOR_YELLOW, COLOR_BLACK, COLOR_GRAY
            self.assertTrue(True, "All colors imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import colors: {e}")

    def test_color_white_imported(self):
        """Test COLOR_WHITE is specifically imported"""
        try:
            from src.core.game import COLOR_WHITE
            self.assertIsNotNone(COLOR_WHITE)
        except ImportError:
            self.fail("COLOR_WHITE not imported in game.py")

    def test_color_red_imported(self):
        """Test COLOR_RED is specifically imported"""
        try:
            from src.core.game import COLOR_RED
            self.assertIsNotNone(COLOR_RED)
        except ImportError:
            self.fail("COLOR_RED not imported in game.py")

    def test_color_yellow_imported(self):
        """Test COLOR_YELLOW is specifically imported"""
        try:
            from src.core.game import COLOR_YELLOW
            self.assertIsNotNone(COLOR_YELLOW)
        except ImportError:
            self.fail("COLOR_YELLOW not imported in game.py")

    def test_color_black_imported(self):
        """Test COLOR_BLACK is specifically imported"""
        try:
            from src.core.game import COLOR_BLACK
            self.assertIsNotNone(COLOR_BLACK)
        except ImportError:
            self.fail("COLOR_BLACK not imported in game.py")

    def test_color_gray_imported(self):
        """Test COLOR_GRAY is specifically imported"""
        try:
            from src.core.game import COLOR_GRAY
            self.assertIsNotNone(COLOR_GRAY)
        except ImportError:
            self.fail("COLOR_GRAY not imported in game.py")

    def test_colors_are_tuples(self):
        """Test that colors are proper RGB tuples"""
        from src.core.game import COLOR_WHITE, COLOR_RED, COLOR_YELLOW, COLOR_BLACK, COLOR_GRAY

        colors = {
            'COLOR_WHITE': COLOR_WHITE,
            'COLOR_RED': COLOR_RED,
            'COLOR_YELLOW': COLOR_YELLOW,
            'COLOR_BLACK': COLOR_BLACK,
            'COLOR_GRAY': COLOR_GRAY
        }

        for name, color in colors.items():
            with self.subTest(color=name):
                self.assertIsInstance(color, tuple, f"{name} should be a tuple")
                self.assertEqual(len(color), 3, f"{name} should have 3 components")
                for component in color:
                    self.assertIsInstance(component, int, f"{name} components should be integers")
                    self.assertGreaterEqual(component, 0, f"{name} components should be >= 0")
                    self.assertLessEqual(component, 255, f"{name} components should be <= 255")

    def test_constants_imported(self):
        """Test that game constants are imported"""
        try:
            from src.core.game import (
                NATIVE_WIDTH, NATIVE_HEIGHT,
                WINDOW_WIDTH, WINDOW_HEIGHT,
                SCALE_FACTOR, FPS, GAME_TITLE
            )
            self.assertTrue(True, "All constants imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import constants: {e}")


class TestColorValues(unittest.TestCase):
    """Test color values are correct"""

    def test_color_white_is_white(self):
        """Test COLOR_WHITE is actually white"""
        from src.core.game import COLOR_WHITE
        self.assertEqual(COLOR_WHITE, (255, 255, 255))

    def test_color_black_is_black(self):
        """Test COLOR_BLACK is actually black"""
        from src.core.game import COLOR_BLACK
        self.assertEqual(COLOR_BLACK, (0, 0, 0))

    def test_color_red_has_red_component(self):
        """Test COLOR_RED has a significant red component"""
        from src.core.game import COLOR_RED
        # Red should be the dominant component
        self.assertGreater(COLOR_RED[0], 100, "Red component should be significant")

    def test_color_yellow_has_red_and_green(self):
        """Test COLOR_YELLOW has both red and green components"""
        from src.core.game import COLOR_YELLOW
        # Yellow should have both red and green
        self.assertGreater(COLOR_YELLOW[0], 100, "Red component should be significant")
        self.assertGreater(COLOR_YELLOW[1], 100, "Green component should be significant")


if __name__ == '__main__':
    unittest.main()
