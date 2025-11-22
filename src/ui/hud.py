"""
HUD (Heads-Up Display) for Ouroboros - Ring of Eternity
"""

import pygame
from src.core.constants import NATIVE_WIDTH, NATIVE_HEIGHT, COLOR_WHITE, COLOR_BLACK


class HUD:
    """
    Display game information to the player
    """

    def __init__(self):
        """Initialize the HUD"""
        # Initialize pygame font (use default system font)
        pygame.font.init()
        self.font = pygame.font.Font(None, 12)  # Small pixel font

    def render(self, surface: pygame.Surface, player, crystals_placed=None):
        """
        Render the HUD

        Args:
            surface: Surface to render to
            player: Player object with inventory
            crystals_placed: Dict tracking which crystals have been placed
        """
        # Display crystal count in top-right corner
        if crystals_placed is not None:
            crystal_count = sum(1 for placed in crystals_placed.values() if placed)
            text = self.font.render(f"Crystals: {crystal_count}/4", True, COLOR_WHITE)

            # Draw in top-right
            padding = 2
            box_width = text.get_width() + padding * 2
            box_height = text.get_height() + padding * 2
            box_x = NATIVE_WIDTH - box_width - 2
            box_rect = pygame.Rect(box_x, 2, box_width, box_height)

            pygame.draw.rect(surface, COLOR_BLACK, box_rect)
            pygame.draw.rect(surface, COLOR_WHITE, box_rect, 1)  # Border
            surface.blit(text, (box_x + padding, 2 + padding))

        # Display held item in bottom-left corner
        if player.has_item():
            item = player.held_item
            item_name = item.get_name()

            # Create text surface
            text = self.font.render(f"Holding: {item_name}", True, COLOR_WHITE)

            # Draw background box
            padding = 2
            box_width = text.get_width() + padding * 2
            box_height = text.get_height() + padding * 2
            box_rect = pygame.Rect(2, NATIVE_HEIGHT - box_height - 2, box_width, box_height)

            pygame.draw.rect(surface, COLOR_BLACK, box_rect)
            pygame.draw.rect(surface, COLOR_WHITE, box_rect, 1)  # Border

            # Draw text
            surface.blit(text, (4, NATIVE_HEIGHT - box_height))

            # Draw item sprite preview next to player if held
            # (Small indicator that shows what's being carried)
