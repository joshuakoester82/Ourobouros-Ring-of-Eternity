"""
Simple particle system for visual effects
"""

import pygame
import random
from typing import List


class Particle:
    """Single particle in a particle system"""

    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple, lifetime: int):
        """
        Initialize a particle

        Args:
            x, y: Starting position
            vx, vy: Velocity
            color: RGB color tuple
            lifetime: Frames until particle dies
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alive = True

    def update(self):
        """Update particle physics"""
        if not self.alive:
            return

        # Move particle
        self.x += self.vx
        self.y += self.vy

        # Apply gravity (optional)
        self.vy += 0.1

        # Decrease lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def render(self, surface: pygame.Surface):
        """Render particle"""
        if not self.alive:
            return

        # Fade out as lifetime decreases
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)

        # Draw as small square (1-2 pixels)
        size = 2 if self.lifetime > self.max_lifetime / 2 else 1
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), size, size))


class ParticleSystem:
    """Manages multiple particle effects"""

    def __init__(self):
        """Initialize particle system"""
        self.particles: List[Particle] = []

    def add_explosion(self, x: float, y: float, color: tuple = (255, 100, 0), count: int = 12):
        """
        Create an explosion effect

        Args:
            x, y: Center of explosion
            color: Particle color
            count: Number of particles
        """
        for _ in range(count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(0.5, 2.5)
            vx = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            vy = speed * pygame.math.Vector2(0, 1).rotate_rad(angle).y

            # Create particle
            lifetime = random.randint(15, 30)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)

    def add_sparkle(self, x: float, y: float, color: tuple = (255, 255, 100)):
        """
        Create a sparkle effect (small, quick particles)

        Args:
            x, y: Center of sparkle
            color: Particle color
        """
        for _ in range(6):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(0.3, 1.0)
            vx = speed * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            vy = speed * pygame.math.Vector2(0, 1).rotate_rad(angle).y

            lifetime = random.randint(10, 20)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)

    def add_dust(self, x: float, y: float, direction: tuple = (0, -1), color: tuple = (150, 150, 150)):
        """
        Create a dust puff effect

        Args:
            x, y: Origin of dust
            direction: General direction tuple (vx, vy)
            color: Dust color
        """
        for _ in range(8):
            # Add randomness to direction
            vx = direction[0] + random.uniform(-0.5, 0.5)
            vy = direction[1] + random.uniform(-0.5, 0.5)

            lifetime = random.randint(20, 40)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)

    def add_trail(self, x: float, y: float, color: tuple = (200, 200, 255)):
        """
        Create a small trail effect (for projectiles)

        Args:
            x, y: Position
            color: Trail color
        """
        for _ in range(3):
            vx = random.uniform(-0.2, 0.2)
            vy = random.uniform(-0.2, 0.2)
            lifetime = random.randint(5, 15)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)

    def update(self):
        """Update all particles"""
        # Update all particles
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]

    def render(self, surface: pygame.Surface):
        """Render all particles"""
        for particle in self.particles:
            particle.render(surface)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()
