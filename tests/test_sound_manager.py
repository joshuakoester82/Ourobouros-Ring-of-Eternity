"""
Unit tests for SoundManager

Tests the procedural sound generation without requiring audio hardware.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSoundGeneration(unittest.TestCase):
    """Test sound generation methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_rate = 22050

    @patch('pygame.mixer.init')
    @patch('pygame.sndarray.make_sound')
    def test_walk_sound_generation_no_broadcast_error(self, mock_make_sound, mock_mixer_init):
        """Test that walk sound generation doesn't cause broadcasting errors"""
        from src.audio.sound_manager import SoundManager

        # Mock the mixer to avoid audio hardware requirement
        mock_make_sound.return_value = Mock()

        # Create sound manager - should not raise ValueError
        try:
            sound_manager = SoundManager(sample_rate=self.sample_rate)
            self.assertTrue(True, "SoundManager initialized without errors")
        except ValueError as e:
            self.fail(f"SoundManager raised ValueError: {e}")

    def test_walk_sound_array_shapes(self):
        """Test that walk sound arrays have correct shapes"""
        sample_rate = 22050
        duration = 0.05
        samples = int(sample_rate * duration)

        # Generate noise array
        noise = np.random.uniform(-0.3, 0.3, samples)

        # Test the fade envelope logic
        fade_length = samples // 4
        envelope_start = np.linspace(0, 1, fade_length)

        # Test start fade
        start_slice = noise[:fade_length]
        self.assertEqual(len(start_slice), len(envelope_start),
                        "Start fade slice and envelope must have same length")

        # Test end fade
        end_slice = noise[-fade_length:]
        envelope_end = np.linspace(1, 0, len(end_slice))
        self.assertEqual(len(end_slice), len(envelope_end),
                        "End fade slice and envelope must have same length")

        # Apply envelopes (should not raise ValueError)
        noise[:fade_length] *= envelope_start
        noise[-fade_length:] *= envelope_end

    def test_various_sample_rates(self):
        """Test sound generation with various sample rates"""
        sample_rates = [11025, 22050, 44100, 48000]

        for rate in sample_rates:
            with self.subTest(sample_rate=rate):
                duration = 0.05
                samples = int(rate * duration)
                noise = np.random.uniform(-0.3, 0.3, samples)

                fade_length = samples // 4
                envelope_start = np.linspace(0, 1, fade_length)
                end_slice_length = len(noise[-fade_length:])
                envelope_end = np.linspace(1, 0, end_slice_length)

                # Should not raise errors
                noise[:fade_length] *= envelope_start
                noise[-fade_length:] *= envelope_end

    @patch('pygame.mixer.init')
    @patch('pygame.sndarray.make_sound')
    def test_all_sounds_generated(self, mock_make_sound, mock_mixer_init):
        """Test that all sound types are generated"""
        from src.audio.sound_manager import SoundManager, SoundType

        mock_make_sound.return_value = Mock()

        sound_manager = SoundManager(sample_rate=self.sample_rate)

        # Check all sound types are in sounds dictionary
        expected_sounds = [
            SoundType.WALK,
            SoundType.PICKUP,
            SoundType.DROP,
            SoundType.SWORD_HIT,
            SoundType.ENEMY_DEATH,
            SoundType.VICTORY,
            SoundType.BOMB_TIMER,
            SoundType.FLUTE_MELODY,
            SoundType.GATE_OPEN,
            SoundType.CRYSTAL_PLACE
        ]

        for sound_type in expected_sounds:
            with self.subTest(sound_type=sound_type):
                self.assertIn(sound_type, sound_manager.sounds,
                            f"{sound_type} should be in sounds dictionary")

    def test_audio_conversion_to_pcm(self):
        """Test conversion of audio arrays to 16-bit PCM"""
        # Create a simple sine wave
        samples = 1000
        t = np.linspace(0, 1, samples)
        audio = np.sin(2 * np.pi * 440 * t) * 0.5

        # Convert to 16-bit PCM
        pcm_audio = (audio * 32767).astype(np.int16)

        # Check data type
        self.assertEqual(pcm_audio.dtype, np.int16)

        # Check range
        self.assertTrue(np.all(pcm_audio >= -32768))
        self.assertTrue(np.all(pcm_audio <= 32767))

    def test_stereo_array_creation(self):
        """Test stereo array creation from mono"""
        samples = 1000
        mono = np.random.randint(-32768, 32767, samples, dtype=np.int16)

        # Create stereo
        stereo = np.zeros((len(mono), 2), dtype=np.int16)
        stereo[:, 0] = mono
        stereo[:, 1] = mono

        # Check shape
        self.assertEqual(stereo.shape, (samples, 2))

        # Check both channels are identical
        np.testing.assert_array_equal(stereo[:, 0], stereo[:, 1])

    @patch('pygame.mixer.init')
    @patch('pygame.sndarray.make_sound')
    def test_sound_playback(self, mock_make_sound, mock_mixer_init):
        """Test sound playback functionality"""
        from src.audio.sound_manager import SoundManager, SoundType

        mock_sound = Mock()
        mock_make_sound.return_value = mock_sound

        sound_manager = SoundManager(sample_rate=self.sample_rate)

        # Play a sound
        sound_manager.play_sound(SoundType.WALK)

        # Verify play was called
        mock_sound.play.assert_called()

    @patch('pygame.mixer.init')
    @patch('pygame.sndarray.make_sound')
    @patch('pygame.time.get_ticks')
    def test_walk_sound_timing(self, mock_get_ticks, mock_make_sound, mock_mixer_init):
        """Test walk sound timing control"""
        from src.audio.sound_manager import SoundManager

        mock_sound = Mock()
        mock_make_sound.return_value = mock_sound

        sound_manager = SoundManager(sample_rate=self.sample_rate)

        # First walk sound should play (timer starts at 0, so 300ms later will play)
        mock_get_ticks.return_value = 300
        sound_manager.play_walk_sound()
        self.assertEqual(mock_sound.play.call_count, 1)

        # Second call too soon should not play
        mock_get_ticks.return_value = 400  # Only 100ms after first play
        sound_manager.play_walk_sound()
        self.assertEqual(mock_sound.play.call_count, 1)  # Still 1

        # Third call after full interval should play
        mock_get_ticks.return_value = 700  # 300ms after first play (300 + 400 = 700 >= 300 interval)
        sound_manager.play_walk_sound()
        self.assertEqual(mock_sound.play.call_count, 2)  # Now 2

    @patch('pygame.mixer.init')
    @patch('pygame.sndarray.make_sound')
    def test_volume_control(self, mock_make_sound, mock_mixer_init):
        """Test volume control functionality"""
        from src.audio.sound_manager import SoundManager

        mock_sound = Mock()
        mock_make_sound.return_value = mock_sound

        sound_manager = SoundManager(sample_rate=self.sample_rate)

        # Set volume
        sound_manager.set_volume(0.5)

        # Verify set_volume was called on all sounds
        # Should be called once per sound type (10 sound types)
        self.assertEqual(mock_sound.set_volume.call_count, 10)
        mock_sound.set_volume.assert_called_with(0.5)


class TestSoundEnvelopeEdgeCases(unittest.TestCase):
    """Test edge cases in sound envelope generation"""

    def test_very_short_duration(self):
        """Test sound generation with very short duration"""
        sample_rate = 22050
        duration = 0.01  # 10ms
        samples = int(sample_rate * duration)

        noise = np.random.uniform(-0.3, 0.3, samples)
        fade_length = samples // 4

        if fade_length > 0:
            envelope_start = np.linspace(0, 1, fade_length)
            end_slice_length = len(noise[-fade_length:])
            envelope_end = np.linspace(1, 0, end_slice_length)

            noise[:fade_length] *= envelope_start
            noise[-fade_length:] *= envelope_end

    def test_odd_sample_counts(self):
        """Test with odd sample counts that might cause rounding issues"""
        odd_sample_counts = [1101, 1103, 1105, 2207, 2211]

        for samples in odd_sample_counts:
            with self.subTest(samples=samples):
                noise = np.random.uniform(-0.3, 0.3, samples)
                fade_length = samples // 4

                envelope_start = np.linspace(0, 1, fade_length)
                end_slice_length = len(noise[-fade_length:])
                envelope_end = np.linspace(1, 0, end_slice_length)

                # Should not raise ValueError
                noise[:fade_length] *= envelope_start
                noise[-fade_length:] *= envelope_end

    def test_envelope_overlap(self):
        """Test that fade envelopes don't overlap incorrectly"""
        samples = 1000
        fade_length = samples // 4

        # Check that fade regions don't overlap
        start_region = slice(0, fade_length)
        end_region = slice(-fade_length, None)

        # Convert to actual indices
        start_indices = range(*start_region.indices(samples))
        end_indices = range(*end_region.indices(samples))

        # For non-overlapping: max(start) < min(end)
        if len(list(start_indices)) > 0 and len(list(end_indices)) > 0:
            self.assertLess(max(start_indices), min(end_indices),
                          "Fade regions should not overlap")


class TestSoundManagerCleanup(unittest.TestCase):
    """Test cleanup functionality"""

    @patch('pygame.mixer.init')
    @patch('pygame.mixer.quit')
    @patch('pygame.sndarray.make_sound')
    def test_cleanup(self, mock_make_sound, mock_mixer_quit, mock_mixer_init):
        """Test that cleanup properly shuts down the mixer"""
        from src.audio.sound_manager import SoundManager

        mock_make_sound.return_value = Mock()

        sound_manager = SoundManager(sample_rate=22050)
        sound_manager.cleanup()

        mock_mixer_quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
