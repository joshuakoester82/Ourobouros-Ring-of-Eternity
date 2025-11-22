"""
Enemy AI system for Ouroboros - Ring of Eternity
"""

import pygame
import random
import math
from enum import Enum, auto
from typing import List, Tuple, Optional
from src.core.constants import (
    COLOR_GREEN, COLOR_RED, COLOR_YELLOW,
    NATIVE_WIDTH, NATIVE_HEIGHT
)


class EnemyType(Enum):
    """Types of enemies"""
    CRAWLER = auto()  # Tier 1: Random movement
    CHASER = auto()   # Tier 2: Chases player
    SENTINEL = auto() # Tier 3: Patrols fixed route
    VOID = auto()     # Boss: Flickering polygon


class Enemy:
    """
    Base class for all enemies
    """

    def __init__(self, enemy_type: EnemyType, x: float, y: float,
                 size: int = 16, color: tuple = COLOR_GREEN, speed: float = 1.0):
        """
        Initialize an enemy

        Args:
            enemy_type: Type of enemy
            x: Starting X position
            y: Starting Y position
            size: Size of the enemy sprite
            color: Color of the enemy
            speed: Movement speed
        """
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.spawn_x = x  # Original spawn point
        self.spawn_y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.active = True
        self.alive = True

        # Create simple sprite
        self.sprite = pygame.Surface((size, size))
        self.sprite.fill(color)

    def get_rect(self) -> pygame.Rect:
        """Get the enemy's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_colliding_with_player(self, player_x: float, player_y: float,
                                  player_width: int, player_height: int) -> bool:
        """
        Check if enemy is colliding with player

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_width: Player width
            player_height: Player height

        Returns:
            True if colliding, False otherwise
        """
        enemy_rect = self.get_rect()
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        return enemy_rect.colliderect(player_rect)

    def respawn(self):
        """Respawn enemy at original spawn point"""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.alive = True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """
        Update enemy logic - override in subclasses

        Args:
            player_x: Player X position
            player_y: Player Y position
            current_screen: Current screen for collision detection
        """
        pass

    def render(self, surface: pygame.Surface):
        """
        Render the enemy

        Args:
            surface: Surface to render to
        """
        if self.active and self.alive:
            surface.blit(self.sprite, (int(self.x), int(self.y)))


class Crawler(Enemy):
    """
    Tier 1 Enemy: Green blob with random Brownian motion
    """

    def __init__(self, x: float, y: float):
        super().__init__(EnemyType.CRAWLER, x, y, 16, COLOR_GREEN, 0.5)

        # Movement state
        self.direction_x = 0
        self.direction_y = 0
        self.move_timer = 0
        self.pause_timer = 0
        self.is_paused = False

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Crawler AI - random movement with pauses"""
        if not self.alive:
            return

        # Handle pause state
        if self.is_paused:
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                self.is_paused = False
                self.move_timer = random.randint(60, 120)  # Move for 1-2 seconds
                # Choose new random direction (cardinal only)
                direction = random.choice(['north', 'south', 'east', 'west'])
                self.direction_x = 0
                self.direction_y = 0
                if direction == 'north':
                    self.direction_y = -1
                elif direction == 'south':
                    self.direction_y = 1
                elif direction == 'east':
                    self.direction_x = 1
                elif direction == 'west':
                    self.direction_x = -1
            return

        # Handle movement state
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.is_paused = True
            self.pause_timer = random.randint(30, 60)  # Pause for 0.5-1 seconds
            return

        # Store old position for collision recovery
        old_x = self.x
        old_y = self.y

        # Move in current direction
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

        # Check wall collisions - bounce off walls
        if current_screen:
            # Check if hit a wall
            corners = [
                (self.x, self.y),
                (self.x + self.size - 1, self.y),
                (self.x, self.y + self.size - 1),
                (self.x + self.size - 1, self.y + self.size - 1)
            ]

            hit_wall = False
            for corner_x, corner_y in corners:
                if current_screen.is_tile_solid(corner_x, corner_y):
                    hit_wall = True
                    break

            if hit_wall:
                # Revert position and reverse direction
                self.x = old_x
                self.y = old_y
                self.direction_x = -self.direction_x
                self.direction_y = -self.direction_y

        # Keep within screen bounds
        if self.x < 16 or self.x > NATIVE_WIDTH - self.size - 16:
            self.x = old_x
            self.direction_x = -self.direction_x
        if self.y < 16 or self.y > NATIVE_HEIGHT - self.size - 16:
            self.y = old_y
            self.direction_y = -self.direction_y


class Chaser(Enemy):
    """
    Tier 2 Enemy: Red chevron/triangle that chases player using line-of-sight
    """

    def __init__(self, x: float, y: float):
        super().__init__(EnemyType.CHASER, x, y, 16, COLOR_RED, 1.5)

        # Create triangle sprite
        self.sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
        points = [(8, 2), (14, 14), (2, 14)]  # Upward pointing triangle
        pygame.draw.polygon(self.sprite, COLOR_RED, points)

        # AI state
        self.aggro_range = 150  # Pixels
        self.is_chasing = False
        self.return_timer = 0

    def has_line_of_sight(self, player_x: float, player_y: float, current_screen) -> bool:
        """
        Check if enemy has clear line of sight to player

        Args:
            player_x: Player X position
            player_y: Player Y position
            current_screen: Current screen for raycasting

        Returns:
            True if line of sight is clear
        """
        # Calculate distance to player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > self.aggro_range:
            return False

        # Simple raycasting - check a few points along the line
        steps = int(distance / 8)  # Check every 8 pixels
        if steps == 0:
            return True

        for i in range(1, steps):
            t = i / steps
            check_x = self.x + dx * t
            check_y = self.y + dy * t
            if current_screen and current_screen.is_tile_solid(check_x, check_y):
                return False

        return True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Chaser AI - chase player if in line of sight"""
        if not self.alive:
            return

        # Check line of sight
        if current_screen and self.has_line_of_sight(player_x, player_y, current_screen):
            self.is_chasing = True
            self.return_timer = 180  # 3 seconds to return if player lost
        else:
            if self.is_chasing:
                self.return_timer -= 1
                if self.return_timer <= 0:
                    self.is_chasing = False

        if self.is_chasing:
            # Chase player at 75% of player speed (roughly)
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 0:
                # Normalize and apply speed
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed

                # Store old position
                old_x = self.x
                old_y = self.y

                # Move
                self.x += move_x
                self.y += move_y

                # Check collisions
                if current_screen:
                    corners = [
                        (self.x, self.y),
                        (self.x + self.size - 1, self.y),
                        (self.x, self.y + self.size - 1),
                        (self.x + self.size - 1, self.y + self.size - 1)
                    ]

                    for corner_x, corner_y in corners:
                        if current_screen.is_tile_solid(corner_x, corner_y):
                            self.x = old_x
                            self.y = old_y
                            break
        else:
            # Return to spawn point
            dx = self.spawn_x - self.x
            dy = self.spawn_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance > 2:  # If not at spawn yet
                move_x = (dx / distance) * self.speed * 0.5
                move_y = (dy / distance) * self.speed * 0.5
                self.x += move_x
                self.y += move_y


class Sentinel(Enemy):
    """
    Tier 3 Enemy: Yellow serpentine shape that patrols a fixed route
    Immune to sword - must be avoided or distracted
    """

    def __init__(self, x: float, y: float, waypoints: List[Tuple[float, float]]):
        super().__init__(EnemyType.SENTINEL, x, y, 16, COLOR_YELLOW, 2.0)

        # Create serpentine sprite
        self.sprite = pygame.Surface((16, 16))
        self.sprite.fill(COLOR_YELLOW)
        pygame.draw.rect(self.sprite, (200, 200, 0), (4, 4, 8, 8))

        # Patrol route
        self.waypoints = waypoints if waypoints else [(x, y)]
        self.current_waypoint = 0
        self.immune_to_sword = True

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update Sentinel AI - patrol fixed route"""
        if not self.alive:
            return

        if not self.waypoints:
            return

        # Get current target waypoint
        target_x, target_y = self.waypoints[self.current_waypoint]

        # Calculate direction to waypoint
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # If reached waypoint, move to next
        if distance < 5:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
            return

        # Move towards waypoint
        if distance > 0:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.x += move_x
            self.y += move_y


class Projectile:
    """
    Projectile fired by The Void boss
    """

    def __init__(self, x: float, y: float, target_x: float, target_y: float, speed: float = 2.0):
        """
        Initialize a projectile

        Args:
            x: Starting X position
            y: Starting Y position
            target_x: Target X position (player)
            target_y: Target Y position (player)
            speed: Movement speed
        """
        self.x = x
        self.y = y
        self.size = 8
        self.speed = speed
        self.active = True
        self.color = (255, 0, 255)  # Magenta

        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0

        # Create sprite
        self.sprite = pygame.Surface((self.size, self.size))
        self.sprite.fill(self.color)

    def update(self):
        """Update projectile position"""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Deactivate if out of bounds
        if self.x < 0 or self.x > NATIVE_WIDTH or self.y < 0 or self.y > NATIVE_HEIGHT:
            self.active = False

    def get_rect(self) -> pygame.Rect:
        """Get the projectile's bounding rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_colliding_with_player(self, player_x: float, player_y: float,
                                  player_width: int, player_height: int) -> bool:
        """Check if projectile hit the player"""
        proj_rect = self.get_rect()
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        return proj_rect.colliderect(player_rect)

    def render(self, surface: pygame.Surface):
        """Render the projectile"""
        if self.active:
            surface.blit(self.sprite, (int(self.x), int(self.y)))


class TheVoid(Enemy):
    """
    Final Boss: The Void - A flickering geometric polygon
    """

    def __init__(self, x: float, y: float):
        super().__init__(EnemyType.VOID, x, y, 24, (255, 255, 255), 3.0)

        # Boss properties
        self.hits_remaining = 3
        self.immune_to_sword = False
        self.invulnerable = False
        self.invulnerable_timer = 0

        # Movement
        self.velocity_x = random.uniform(-1, 1) * self.speed
        self.velocity_y = random.uniform(-1, 1) * self.speed

        # Visual effects
        self.flicker_timer = 0
        self.current_shape = "square"
        self.shapes = ["square", "triangle", "pentagon", "hexagon"]

        # Projectiles
        self.projectiles: List[Projectile] = []
        self.shoot_cooldown = 0

        # Create initial sprite
        self._create_sprite()

    def _create_sprite(self):
        """Create a flickering geometric shape sprite"""
        # Random color
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 255) # White
        ]
        self.color = random.choice(colors)

        # Create surface
        self.sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Draw shape based on current shape
        center = self.size // 2
        if self.current_shape == "square":
            pygame.draw.rect(self.sprite, self.color, (4, 4, 16, 16), 0)
        elif self.current_shape == "triangle":
            points = [(center, 4), (4, 20), (20, 20)]
            pygame.draw.polygon(self.sprite, self.color, points)
        elif self.current_shape == "pentagon":
            # Simple approximation
            points = [(center, 2), (22, 10), (18, 22), (6, 22), (2, 10)]
            pygame.draw.polygon(self.sprite, self.color, points)
        else:  # hexagon
            points = [(center, 2), (20, 8), (20, 16), (center, 22), (4, 16), (4, 8)]
            pygame.draw.polygon(self.sprite, self.color, points)

    def take_hit(self, player_x: float, player_y: float):
        """
        Boss takes a hit from the sword

        Args:
            player_x: Player X position for projectile targeting
            player_y: Player Y position for projectile targeting

        Returns:
            True if boss is defeated, False otherwise
        """
        if self.invulnerable:
            return False

        self.hits_remaining -= 1
        print(f"The Void hit! {self.hits_remaining} hits remaining")

        if self.hits_remaining <= 0:
            print("The Void dissipates!")
            return True

        # Teleport to random corner
        corners = [
            (40, 40),
            (NATIVE_WIDTH - 64, 40),
            (40, NATIVE_HEIGHT - 64),
            (NATIVE_WIDTH - 64, NATIVE_HEIGHT - 64)
        ]
        self.x, self.y = random.choice(corners)

        # Shoot projectile at player
        projectile = Projectile(
            self.x + self.size // 2,
            self.y + self.size // 2,
            player_x, player_y
        )
        self.projectiles.append(projectile)

        # New random velocity
        self.velocity_x = random.uniform(-1, 1) * self.speed
        self.velocity_y = random.uniform(-1, 1) * self.speed

        # Brief invulnerability
        self.invulnerable = True
        self.invulnerable_timer = 30  # 0.5 seconds

        return False

    def update(self, player_x: float, player_y: float, current_screen=None):
        """Update The Void boss AI"""
        if not self.alive:
            return

        # Handle invulnerability
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Flicker effect - change shape every few frames
        self.flicker_timer += 1
        if self.flicker_timer > 10:  # Change every ~0.16 seconds
            self.flicker_timer = 0
            self.current_shape = random.choice(self.shapes)
            self._create_sprite()

        # Bouncing movement
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off walls
        if self.x < 32 or self.x > NATIVE_WIDTH - self.size - 32:
            self.velocity_x = -self.velocity_x
            self.x = max(32, min(self.x, NATIVE_WIDTH - self.size - 32))
        if self.y < 32 or self.y > NATIVE_HEIGHT - self.size - 32:
            self.velocity_y = -self.velocity_y
            self.y = max(32, min(self.y, NATIVE_HEIGHT - self.size - 32))

        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)

        # Shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def render(self, surface: pygame.Surface):
        """Render The Void boss and its projectiles"""
        if self.active and self.alive:
            # Render boss with flicker effect
            if not self.invulnerable or (self.invulnerable_timer % 4 < 2):
                surface.blit(self.sprite, (int(self.x), int(self.y)))

            # Render projectiles
            for projectile in self.projectiles:
                projectile.render(surface)


def create_enemy(enemy_type: EnemyType, x: float, y: float,
                 waypoints: Optional[List[Tuple[float, float]]] = None) -> Enemy:
    """
    Factory function to create enemies

    Args:
        enemy_type: Type of enemy to create
        x: X position
        y: Y position
        waypoints: Optional waypoints for Sentinel

    Returns:
        Enemy instance
    """
    if enemy_type == EnemyType.CRAWLER:
        return Crawler(x, y)
    elif enemy_type == EnemyType.CHASER:
        return Chaser(x, y)
    elif enemy_type == EnemyType.SENTINEL:
        return Sentinel(x, y, waypoints or [])
    elif enemy_type == EnemyType.VOID:
        return TheVoid(x, y)
    else:
        return Enemy(enemy_type, x, y)
