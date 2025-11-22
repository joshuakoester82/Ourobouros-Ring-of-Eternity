"""
CRT scanline effect for retro Atari 2600 aesthetic
"""

import pygame


class CRTEffect:
    """
    Applies a CRT scanline effect to give the game a retro feel
    """

    def __init__(self, width: int, height: int, intensity: float = 0.3):
        """
        Initialize CRT effect

        Args:
            width: Screen width
            height: Screen height
            intensity: Scanline darkness (0.0-1.0, higher = darker lines)
        """
        self.width = width
        self.height = height
        self.intensity = max(0.0, min(1.0, intensity))

        # Create scanline overlay surface
        self.scanline_surface = self._create_scanlines()

    def _create_scanlines(self) -> pygame.Surface:
        """
        Create the scanline overlay surface

        Returns:
            Surface with scanline pattern
        """
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw horizontal scanlines (every other line)
        scanline_color = (0, 0, 0, int(255 * self.intensity))

        for y in range(0, self.height, 2):
            pygame.draw.line(surface, scanline_color, (0, y), (self.width, y), 1)

        return surface

    def apply(self, surface: pygame.Surface) -> pygame.Surface:
        """
        Apply CRT effect to a surface

        Args:
            surface: Surface to apply effect to

        Returns:
            Surface with CRT effect applied
        """
        # Create copy to avoid modifying original
        result = surface.copy()

        # Apply scanlines
        result.blit(self.scanline_surface, (0, 0))

        return result


class CRTEffectScaled:
    """
    CRT effect optimized for scaled displays (applies after scaling)
    """

    def __init__(self, width: int, height: int, intensity: float = 0.2):
        """
        Initialize scaled CRT effect

        Args:
            width: Scaled screen width
            height: Scaled screen height
            intensity: Scanline darkness (0.0-1.0)
        """
        self.width = width
        self.height = height
        self.intensity = max(0.0, min(1.0, intensity))

        # Create scanline pattern (every 2-4 pixels depending on scale)
        self.scanline_surface = self._create_scanlines()

    def _create_scanlines(self) -> pygame.Surface:
        """Create scanline overlay for scaled display"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Scanlines every 3 pixels for that authentic CRT look when scaled
        scanline_color = (0, 0, 0, int(255 * self.intensity))

        for y in range(0, self.height, 3):
            pygame.draw.line(surface, scanline_color, (0, y), (self.width, y), 1)

        return surface

    def apply(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply CRT effect to scaled surface"""
        result = surface.copy()
        result.blit(self.scanline_surface, (0, 0))
        return result
