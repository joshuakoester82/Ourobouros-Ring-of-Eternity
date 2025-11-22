"""
Ambient audio system for Ouroboros - Ring of Eternity

Provides low-level ambient sounds for different areas:
- Tower Hub: Low hum
- Outside areas: Wind noise
"""

import pygame
import numpy as np
from enum import Enum, auto


class AmbienceType(Enum):
    """Types of ambient sounds"""
    NONE = auto()
    TOWER_HUM = auto()
    WIND = auto()


class AmbientManager:
    """
    Manages ambient background audio

    Creates looping ambient sounds for atmosphere
    """

    def __init__(self, sample_rate=22050):
        """
        Initialize the ambient manager

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.ambient_sounds = {}
        self.current_ambience = AmbienceType.NONE

        # Generate ambient sounds
        self._generate_ambient_sounds()

        # Channel for ambient sounds (use channel 1, leaving 0 for SFX)
        self.ambient_channel = pygame.mixer.Channel(1)
        self.ambient_channel.set_volume(0.3)  # Lower volume for ambience

        print("Ambient audio manager initialized")

    def _generate_ambient_sounds(self):
        """Generate all ambient sounds"""
        self.ambient_sounds[AmbienceType.TOWER_HUM] = self._generate_tower_hum()
        self.ambient_sounds[AmbienceType.WIND] = self._generate_wind()

    def _generate_tower_hum(self):
        """
        Generate low hum for Tower Hub

        Returns:
            pygame.Sound object (loopable)
        """
        duration = 3.0  # 3 seconds (will loop seamlessly)
        samples = int(self.sample_rate * duration)

        # Low frequency hum (60 Hz + harmonics)
        t = np.linspace(0, duration, samples)

        # Base frequency and harmonics
        freq1 = 60   # Fundamental
        freq2 = 120  # First harmonic
        freq3 = 180  # Second harmonic

        audio = (
            np.sin(2 * np.pi * freq1 * t) * 0.3 +
            np.sin(2 * np.pi * freq2 * t) * 0.15 +
            np.sin(2 * np.pi * freq3 * t) * 0.08
        )

        # Add very subtle variations for interest
        modulation = 1 + 0.05 * np.sin(2 * np.pi * 0.2 * t)
        audio *= modulation

        # Normalize
        audio = audio * 0.4

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_wind(self):
        """
        Generate wind noise for outside areas

        Returns:
            pygame.Sound object (loopable)
        """
        duration = 4.0  # 4 seconds
        samples = int(self.sample_rate * duration)

        # Filtered noise for wind effect
        noise = np.random.uniform(-1, 1, samples)

        # Apply low-pass filter by averaging with neighbors
        # This creates a "whooshing" effect
        window_size = 100
        wind = np.convolve(noise, np.ones(window_size) / window_size, mode='same')

        # Add slow amplitude modulation for gusts
        t = np.linspace(0, duration, samples)
        gusts = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)
        wind *= gusts

        # Normalize
        wind = wind * 0.3

        # Convert to 16-bit PCM
        audio = (wind * 32767).astype(np.int16)

        # Create stereo with slight difference for spatial effect
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        # Right channel slightly different for stereo effect
        noise_r = np.random.uniform(-1, 1, samples)
        wind_r = np.convolve(noise_r, np.ones(window_size) / window_size, mode='same')
        wind_r *= gusts * 0.3
        stereo[:, 1] = (wind_r * 32767).astype(np.int16)

        return pygame.sndarray.make_sound(stereo)

    def set_ambience(self, ambience_type):
        """
        Set the current ambient sound

        Args:
            ambience_type: AmbienceType enum value
        """
        if ambience_type == self.current_ambience:
            return  # Already playing this ambience

        # Stop current ambience
        self.ambient_channel.stop()

        # Start new ambience
        if ambience_type != AmbienceType.NONE and ambience_type in self.ambient_sounds:
            sound = self.ambient_sounds[ambience_type]
            self.ambient_channel.play(sound, loops=-1)  # Loop indefinitely

        self.current_ambience = ambience_type

    def set_volume(self, volume):
        """
        Set ambient volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.ambient_channel.set_volume(volume)

    def stop(self):
        """Stop all ambient sounds"""
        self.ambient_channel.stop()
        self.current_ambience = AmbienceType.NONE
