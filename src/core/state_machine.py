"""
State machine for managing game states
"""

from enum import Enum, auto


class GameState(Enum):
    """Game state enumeration"""
    INIT = auto()       # World generation, item spawning
    EXPLORE = auto()    # Active gameplay
    COLLECTION = auto() # Crystal tracking
    ACTIVATION = auto() # All crystals placed, gate opens
    CLIMAX = auto()     # Boss fight
    WIN = auto()        # Ring collected
    GAME_OVER = auto()  # Restart prompt


class StateMachine:
    """
    Manages game state transitions
    """
    def __init__(self):
        self.current_state = GameState.INIT
        self.previous_state = None

    def change_state(self, new_state: GameState):
        """Change to a new game state"""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            print(f"State changed: {self.previous_state} -> {self.current_state}")

    def is_state(self, state: GameState) -> bool:
        """Check if currently in a specific state"""
        return self.current_state == state

    def get_state(self) -> GameState:
        """Get current state"""
        return self.current_state
