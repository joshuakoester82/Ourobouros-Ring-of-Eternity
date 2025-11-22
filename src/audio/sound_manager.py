"""
Sound Manager for Ouroboros - Ring of Eternity

Generates retro-style procedural sound effects using pygame.mixer and numpy
to keep asset sizes low while maintaining an authentic Atari 2600 feel.
"""

import pygame
import numpy as np
from enum import Enum, auto


class SoundType(Enum):
    """Types of sound effects"""
    WALK = auto()
    PICKUP = auto()
    DROP = auto()
    SWORD_HIT = auto()
    ENEMY_DEATH = auto()
    VICTORY = auto()
    BOMB_TIMER = auto()
    FLUTE_MELODY = auto()
    GATE_OPEN = auto()
    CRYSTAL_PLACE = auto()


class SoundManager:
    """
    Manages procedural sound generation and playback

    Uses pygame.mixer and numpy to create retro synthesized sounds
    """

    def __init__(self, sample_rate=22050):
        """
        Initialize the sound manager

        Args:
            sample_rate: Audio sample rate (22050 Hz for retro feel)
        """
        # Initialize pygame mixer
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=1, buffer=512)

        self.sample_rate = sample_rate
        self.sounds = {}

        # Walk sound timer
        self.walk_timer = 0
        self.walk_interval = 300  # milliseconds

        # Generate all sounds
        self._generate_all_sounds()

        print("Sound manager initialized with procedural synthesis")

    def _generate_all_sounds(self):
        """Generate all sound effects"""
        self.sounds[SoundType.WALK] = self._generate_walk_sound()
        self.sounds[SoundType.PICKUP] = self._generate_pickup_sound()
        self.sounds[SoundType.DROP] = self._generate_drop_sound()
        self.sounds[SoundType.SWORD_HIT] = self._generate_sword_hit_sound()
        self.sounds[SoundType.ENEMY_DEATH] = self._generate_enemy_death_sound()
        self.sounds[SoundType.VICTORY] = self._generate_victory_sound()
        self.sounds[SoundType.BOMB_TIMER] = self._generate_bomb_timer_sound()
        self.sounds[SoundType.FLUTE_MELODY] = self._generate_flute_melody_sound()
        self.sounds[SoundType.GATE_OPEN] = self._generate_gate_open_sound()
        self.sounds[SoundType.CRYSTAL_PLACE] = self._generate_crystal_place_sound()

    def _generate_walk_sound(self):
        """
        Generate walk sound - white noise burst (very short)

        Returns:
            pygame.Sound object
        """
        duration = 0.05  # 50ms
        samples = int(self.sample_rate * duration)

        # White noise
        noise = np.random.uniform(-0.3, 0.3, samples)

        # Apply envelope (fade in/out quickly)
        fade_length = samples // 4
        envelope_start = np.linspace(0, 1, fade_length)
        noise[:fade_length] *= envelope_start

        # For the end fade, create an envelope matching the exact slice length
        end_slice_length = len(noise[-fade_length:])
        envelope_end = np.linspace(1, 0, end_slice_length)
        noise[-fade_length:] *= envelope_end

        # Convert to 16-bit PCM
        audio = (noise * 32767).astype(np.int16)

        # Create stereo array
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_pickup_sound(self):
        """
        Generate pickup sound - ascending arpeggio (square wave)

        Returns:
            pygame.Sound object
        """
        duration = 0.15  # 150ms
        samples = int(self.sample_rate * duration)

        # Frequencies for arpeggio (C-E-G major chord)
        frequencies = [523, 659, 784]  # C5, E5, G5
        segment_length = samples // len(frequencies)

        audio = np.zeros(samples)

        for i, freq in enumerate(frequencies):
            start = i * segment_length
            end = start + segment_length

            # Generate square wave
            t = np.linspace(0, segment_length / self.sample_rate, segment_length)
            square = np.sign(np.sin(2 * np.pi * freq * t))

            audio[start:end] = square * 0.3

        # Apply envelope
        envelope = np.linspace(1, 0.3, samples)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_drop_sound(self):
        """
        Generate drop sound - descending slide

        Returns:
            pygame.Sound object
        """
        duration = 0.1  # 100ms
        samples = int(self.sample_rate * duration)

        # Descending frequency sweep
        start_freq = 600
        end_freq = 200
        t = np.linspace(0, duration, samples)
        freq_sweep = np.linspace(start_freq, end_freq, samples)

        # Generate tone with frequency sweep
        phase = np.cumsum(2 * np.pi * freq_sweep / self.sample_rate)
        audio = np.sin(phase) * 0.3

        # Apply envelope
        envelope = np.linspace(1, 0, samples)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_sword_hit_sound(self):
        """
        Generate sword hit sound - low frequency noise + sawtooth fade

        Returns:
            pygame.Sound object
        """
        duration = 0.2  # 200ms
        samples = int(self.sample_rate * duration)

        # Low frequency sawtooth wave
        freq = 120
        t = np.linspace(0, duration, samples)
        sawtooth = 2 * (t * freq - np.floor(t * freq + 0.5))

        # Add some noise for impact
        noise = np.random.uniform(-0.2, 0.2, samples)
        audio = (sawtooth * 0.4 + noise * 0.3)

        # Apply envelope (sharp attack, quick decay)
        envelope = np.exp(-5 * t)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_enemy_death_sound(self):
        """
        Generate enemy death sound - distortion crunch

        Returns:
            pygame.Sound object
        """
        duration = 0.25  # 250ms
        samples = int(self.sample_rate * duration)

        # Descending frequency with distortion
        start_freq = 400
        end_freq = 80
        t = np.linspace(0, duration, samples)
        freq_sweep = np.linspace(start_freq, end_freq, samples)

        # Generate distorted tone
        phase = np.cumsum(2 * np.pi * freq_sweep / self.sample_rate)
        audio = np.sign(np.sin(phase)) * 0.5  # Square wave for distortion

        # Add noise
        noise = np.random.uniform(-0.3, 0.3, samples)
        audio = audio * 0.6 + noise * 0.4

        # Apply envelope
        envelope = np.exp(-4 * t)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_victory_sound(self):
        """
        Generate victory sound - major chord progression

        Returns:
            pygame.Sound object
        """
        duration = 1.0  # 1 second
        samples = int(self.sample_rate * duration)

        # Major chord progression: I - IV - V - I (C - F - G - C)
        chords = [
            [523, 659, 784],   # C major (C, E, G)
            [698, 880, 1047],  # F major (F, A, C)
            [784, 988, 1175],  # G major (G, B, D)
            [523, 659, 784]    # C major (C, E, G)
        ]

        chord_duration = samples // len(chords)
        audio = np.zeros(samples)

        for i, chord in enumerate(chords):
            start = i * chord_duration
            end = start + chord_duration

            t = np.linspace(0, chord_duration / self.sample_rate, chord_duration)

            # Mix all notes in chord
            chord_audio = np.zeros(chord_duration)
            for freq in chord:
                chord_audio += np.sin(2 * np.pi * freq * t) / len(chord)

            audio[start:end] = chord_audio * 0.4

        # Apply overall envelope
        envelope = np.linspace(1, 0.7, samples)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_bomb_timer_sound(self):
        """
        Generate bomb timer sound - ticking

        Returns:
            pygame.Sound object
        """
        duration = 0.1  # 100ms (single tick)
        samples = int(self.sample_rate * duration)

        # Short high-pitched beep
        freq = 1200
        t = np.linspace(0, duration, samples)
        audio = np.sin(2 * np.pi * freq * t) * 0.3

        # Very short envelope (sharp tick)
        envelope = np.exp(-30 * t)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_flute_melody_sound(self):
        """
        Generate flute melody sound - "Song of Sleep"

        Returns:
            pygame.Sound object
        """
        duration = 1.5  # 1.5 seconds
        samples = int(self.sample_rate * duration)

        # Simple melody (descending scale with vibrato)
        notes = [784, 698, 659, 587, 523]  # G5, F5, E5, D5, C5
        note_duration = samples // len(notes)

        audio = np.zeros(samples)

        for i, freq in enumerate(notes):
            start = i * note_duration
            end = start + note_duration

            t = np.linspace(0, note_duration / self.sample_rate, note_duration)

            # Sine wave with slight vibrato
            vibrato_freq = 5  # Hz
            vibrato_depth = 10  # Hz
            frequency_modulation = freq + vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)
            phase = np.cumsum(2 * np.pi * frequency_modulation / self.sample_rate)
            note_audio = np.sin(phase) * 0.3

            # Envelope for each note
            note_envelope = np.exp(-3 * t)
            note_audio *= note_envelope

            audio[start:end] = note_audio

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_gate_open_sound(self):
        """
        Generate gate opening sound - mechanical rumble

        Returns:
            pygame.Sound object
        """
        duration = 0.5  # 500ms
        samples = int(self.sample_rate * duration)

        # Low rumble with some noise
        freq = 80
        t = np.linspace(0, duration, samples)
        rumble = np.sin(2 * np.pi * freq * t) * 0.4

        # Add metallic noise
        noise = np.random.uniform(-0.2, 0.2, samples)
        audio = rumble + noise

        # Apply envelope
        envelope = np.linspace(1, 0, samples)
        audio *= envelope

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def _generate_crystal_place_sound(self):
        """
        Generate crystal placement sound - magical chime

        Returns:
            pygame.Sound object
        """
        duration = 0.5  # 500ms
        samples = int(self.sample_rate * duration)

        # High-pitched harmonic tones
        frequencies = [1047, 1319, 1568]  # C6, E6, G6
        t = np.linspace(0, duration, samples)

        audio = np.zeros(samples)
        for i, freq in enumerate(frequencies):
            delay = int(i * samples // 10)  # Slight delay between harmonics
            if delay < samples:
                delayed_t = np.zeros(samples)
                delayed_t[delay:] = t[:samples - delay]
                audio += np.sin(2 * np.pi * freq * delayed_t) / len(frequencies)

        # Apply envelope
        envelope = np.exp(-3 * t)
        audio *= envelope * 0.4

        # Convert to 16-bit PCM
        audio = (audio * 32767).astype(np.int16)

        # Create stereo
        stereo = np.zeros((len(audio), 2), dtype=np.int16)
        stereo[:, 0] = audio
        stereo[:, 1] = audio

        return pygame.sndarray.make_sound(stereo)

    def play_sound(self, sound_type):
        """
        Play a sound effect

        Args:
            sound_type: SoundType enum value
        """
        if sound_type in self.sounds:
            self.sounds[sound_type].play()

    def play_walk_sound(self):
        """Play walk sound with timing control"""
        current_time = pygame.time.get_ticks()
        if current_time - self.walk_timer >= self.walk_interval:
            self.play_sound(SoundType.WALK)
            self.walk_timer = current_time

    def set_volume(self, volume):
        """
        Set master volume for all sounds

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def cleanup(self):
        """Clean up sound resources"""
        pygame.mixer.quit()
