"""
Main game class for Ouroboros - Ring of Eternity
"""

import pygame
from src.core.constants import (
    NATIVE_WIDTH, NATIVE_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SCALE_FACTOR, FPS, GAME_TITLE,
    COLOR_BLACK, COLOR_GRAY, COLOR_YELLOW
)
from src.core.state_machine import StateMachine, GameState
from src.entities.player import Player
from src.entities.item import create_item, ItemType
from src.entities.interactable import (
    Pedestal, Gate, Fountain, SoftDirt, CrackedWall,
    ToxicBasin, BlessedSpring, SleeplessStatue, Chasm,
    InteractableType
)
from src.entities.enemy import create_enemy, EnemyType
from src.entities.npc import create_npc, NPCType, Cat
from src.world.world import World
from src.world.camera import Camera
from src.world.screen import Direction, ScreenID
from src.ui.hud import HUD
from src.ui.crt_effect import CRTEffectScaled
from src.ui.particles import ParticleSystem
from src.audio import SoundManager, SoundType, AmbientManager, AmbienceType


class Game:
    """
    Main game class that handles initialization, game loop, and rendering
    """

    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()

        # Create the display window
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        # Create native resolution surface for pixel-perfect rendering
        self.native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Game state
        self.running = False
        self.state_machine = StateMachine()

        # Delta time for frame-independent movement
        self.dt = 0

        # Crystal collection tracking
        self.crystals_placed = {
            ItemType.GREEN_CRYSTAL: False,
            ItemType.RED_CRYSTAL: False,
            ItemType.BLUE_CRYSTAL: False,
            ItemType.YELLOW_CRYSTAL: False
        }
        self.all_crystals_placed = False

        # Boss fight tracking
        self.boss = None
        self.boss_defeated = False
        self.victory_timer = 0

        # NPC tracking
        self.cat = None  # The cat companion

        # World and camera
        self.world = World()
        self.camera = Camera()

        # HUD
        self.hud = HUD()

        # CRT Effect for retro aesthetic
        self.crt_effect = CRTEffectScaled(WINDOW_WIDTH, WINDOW_HEIGHT, intensity=0.25)
        self.crt_enabled = True  # Can be toggled

        # Particle system for visual effects
        self.particles = ParticleSystem()

        # Audio
        self.sound_manager = SoundManager()
        self.ambient_manager = AmbientManager()
        self.sound_manager.set_volume(0.6)  # Moderate volume

        # Player (spawn in center of screen)
        self.player = Player(
            x=NATIVE_WIDTH // 2 - 8,
            y=NATIVE_HEIGHT // 2 - 8
        )

        # Spawn test items
        self._spawn_test_items()

        # Add interactables to world
        self._setup_interactables()

        # Add enemies to world
        self._spawn_enemies()

        # Add NPCs to world
        self._spawn_npcs()

        # Setup final chamber
        self._setup_final_chamber()

        print(f"Game initialized: {WINDOW_WIDTH}x{WINDOW_HEIGHT} " +
              f"(native: {NATIVE_WIDTH}x{NATIVE_HEIGHT}, scale: {SCALE_FACTOR}x)")
        print(f"Starting in: {self.world.get_current_screen().name}")

    def _spawn_test_items(self):
        """Spawn test items in the world for demonstration"""
        # Hub - spawn some keys and crystals
        hub = self.world.get_screen(ScreenID.TOWER_HUB)
        hub.entities.append(create_item(ItemType.GOLD_KEY, 40, 40))
        hub.entities.append(create_item(ItemType.SWORD, 120, 40))

        # Gardens - spawn acorn and green crystal
        gardens_2 = self.world.get_screen(ScreenID.GARDENS_2)
        gardens_2.entities.append(create_item(ItemType.ACORN, 60, 60))

        gardens_4 = self.world.get_screen(ScreenID.GARDENS_4)
        gardens_4.entities.append(create_item(ItemType.GREEN_CRYSTAL, 80, 96))

        # Catacombs - spawn bomb and red crystal
        catacombs_2 = self.world.get_screen(ScreenID.CATACOMBS_2)
        catacombs_2.entities.append(create_item(ItemType.BOMB, 50, 80))

        catacombs_4 = self.world.get_screen(ScreenID.CATACOMBS_4)
        catacombs_4.entities.append(create_item(ItemType.RED_CRYSTAL, 80, 96))

        # Ruins - spawn chalice and blue crystal
        ruins_2 = self.world.get_screen(ScreenID.RUINS_2)
        ruins_2.entities.append(create_item(ItemType.CHALICE, 70, 70))

        ruins_3 = self.world.get_screen(ScreenID.RUINS_3)
        ruins_3.entities.append(create_item(ItemType.BLUE_CRYSTAL, 80, 96))

        # Cliffs - spawn flute and yellow crystal
        cliffs_2 = self.world.get_screen(ScreenID.CLIFFS_2)
        cliffs_2.entities.append(create_item(ItemType.FLUTE, 65, 75))

        cliffs_4 = self.world.get_screen(ScreenID.CLIFFS_4)
        cliffs_4.entities.append(create_item(ItemType.YELLOW_CRYSTAL, 80, 96))

        # Add silver key to catacombs
        catacombs_3 = self.world.get_screen(ScreenID.CATACOMBS_3)
        catacombs_3.entities.append(create_item(ItemType.SILVER_KEY, 80, 60))

        print("Test items spawned in world")

    def _setup_interactables(self):
        """Add interactable objects to the world"""
        # Tower Hub - Add crystal pedestals
        hub = self.world.get_screen(ScreenID.TOWER_HUB)

        # Four corner pedestals with colored outlines
        from src.core.constants import COLOR_GREEN, COLOR_RED, COLOR_BLUE, COLOR_YELLOW
        pedestal_green = Pedestal(24, 24, ItemType.GREEN_CRYSTAL, COLOR_GREEN)
        pedestal_red = Pedestal(120, 24, ItemType.RED_CRYSTAL, COLOR_RED)
        pedestal_blue = Pedestal(24, 152, ItemType.BLUE_CRYSTAL, COLOR_BLUE)
        pedestal_yellow = Pedestal(120, 152, ItemType.YELLOW_CRYSTAL, COLOR_YELLOW)

        hub.entities.extend([pedestal_green, pedestal_red, pedestal_blue, pedestal_yellow])

        # Add fountain in hub for watering can refills
        fountain = Fountain(80, 96)
        hub.entities.append(fountain)

        # Gardens - Tree Bridge puzzle
        gardens_3 = self.world.get_screen(ScreenID.GARDENS_3)
        soft_dirt = SoftDirt(48, 80)
        gardens_3.entities.append(soft_dirt)

        gardens_4 = self.world.get_screen(ScreenID.GARDENS_4)
        chasm = Chasm(64, 48, 32, 16)  # Horizontal chasm
        gardens_4.entities.append(chasm)
        # Store reference for puzzle
        self.tree_chasm = chasm
        self.tree_dirt = soft_dirt

        # Catacombs - Gold Gate and Cracked Wall
        catacombs_1 = self.world.get_screen(ScreenID.CATACOMBS_1)
        gold_gate = Gate(72, 48, 16, 32, InteractableType.GOLD_GATE, ItemType.GOLD_KEY, COLOR_YELLOW)
        catacombs_1.entities.append(gold_gate)

        catacombs_4 = self.world.get_screen(ScreenID.CATACOMBS_4)
        cracked_wall = CrackedWall(80, 64)
        catacombs_4.entities.append(cracked_wall)

        # Ruins - Toxic Basin and Blessed Spring
        ruins_3 = self.world.get_screen(ScreenID.RUINS_3)
        toxic_basin = ToxicBasin(60, 80, 24, 24)
        ruins_3.entities.append(toxic_basin)

        ruins_4 = self.world.get_screen(ScreenID.RUINS_4)
        blessed_spring = BlessedSpring(80, 80)
        ruins_4.entities.append(blessed_spring)

        # Cliffs - Sleepless Statue
        cliffs_4 = self.world.get_screen(ScreenID.CLIFFS_4)
        statue = SleeplessStatue(80, 80)
        cliffs_4.entities.append(statue)

        # Hub - Silver Gate (blocks path to final chamber)
        silver_gate = Gate(80, 20, 16, 16, InteractableType.SILVER_GATE, ItemType.SILVER_KEY, COLOR_GRAY)
        hub.entities.append(silver_gate)
        # Store reference for crystal activation
        self.silver_gate = silver_gate

        print("Interactables placed in world")

    def _spawn_enemies(self):
        """Spawn enemies in various screens"""
        # Gardens - Crawlers (Tier 1)
        gardens_2 = self.world.get_screen(ScreenID.GARDENS_2)
        gardens_2.entities.append(create_enemy(EnemyType.CRAWLER, 40, 60))
        gardens_2.entities.append(create_enemy(EnemyType.CRAWLER, 100, 80))

        gardens_3 = self.world.get_screen(ScreenID.GARDENS_3)
        gardens_3.entities.append(create_enemy(EnemyType.CRAWLER, 80, 40))

        # Catacombs - Chasers (Tier 2)
        catacombs_2 = self.world.get_screen(ScreenID.CATACOMBS_2)
        catacombs_2.entities.append(create_enemy(EnemyType.CHASER, 100, 100))

        catacombs_3 = self.world.get_screen(ScreenID.CATACOMBS_3)
        catacombs_3.entities.append(create_enemy(EnemyType.CHASER, 60, 80))
        catacombs_3.entities.append(create_enemy(EnemyType.CHASER, 90, 60))

        # Ruins - Mix of Crawlers and Chasers
        ruins_2 = self.world.get_screen(ScreenID.RUINS_2)
        ruins_2.entities.append(create_enemy(EnemyType.CRAWLER, 50, 100))
        ruins_2.entities.append(create_enemy(EnemyType.CHASER, 110, 90))

        # Cliffs - Sentinels (Tier 3) with patrol routes
        cliffs_2 = self.world.get_screen(ScreenID.CLIFFS_2)
        waypoints_1 = [(40, 40), (120, 40), (120, 140), (40, 140)]
        cliffs_2.entities.append(create_enemy(EnemyType.SENTINEL, 40, 40, waypoints_1))

        cliffs_3 = self.world.get_screen(ScreenID.CLIFFS_3)
        waypoints_2 = [(60, 60), (100, 60), (80, 120)]
        cliffs_3.entities.append(create_enemy(EnemyType.SENTINEL, 60, 60, waypoints_2))

        print("Enemies spawned in world")

    def _spawn_npcs(self):
        """Spawn NPCs in the world"""
        # The Owl - in Gardens (North Biome)
        gardens_2 = self.world.get_screen(ScreenID.GARDENS_2)
        owl = create_npc(NPCType.OWL, 100, 40)
        gardens_2.entities.append(owl)

        # The Cat - in Tower Hub
        hub = self.world.get_screen(ScreenID.TOWER_HUB)
        self.cat = create_npc(NPCType.CAT, 120, 120)
        hub.entities.append(self.cat)

        # Add Fish item to a screen for Cat interaction
        gardens_3 = self.world.get_screen(ScreenID.GARDENS_3)
        gardens_3.entities.append(create_item(ItemType.FISH, 30, 40))

        print("NPCs spawned in world")

    def _setup_final_chamber(self):
        """Setup the final chamber with boss and ring"""
        final_chamber = self.world.get_screen(ScreenID.FINAL_CHAMBER)

        # Spawn The Void boss in the center
        self.boss = create_enemy(EnemyType.VOID, 80, 96)
        final_chamber.entities.append(self.boss)

        print("Final chamber prepared with The Void")

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_c:
                    # Toggle CRT effect
                    self.crt_enabled = not self.crt_enabled
                    status = "ON" if self.crt_enabled else "OFF"
                    print(f"CRT Effect: {status}")
                elif event.key == pygame.K_SPACE:
                    # Handle restart in WIN/GAME_OVER states
                    if self.state_machine.is_state(GameState.WIN) or \
                       self.state_machine.is_state(GameState.GAME_OVER):
                        self._restart_game()
                    else:
                        self.handle_space_interaction()

    def _restart_game(self):
        """Restart the game from the beginning"""
        print("\n" + "=" * 50)
        print("RESTARTING GAME...")
        print("=" * 50 + "\n")

        # Reset state machine
        self.state_machine.change_state(GameState.INIT)

        # Reset crystal tracking
        self.crystals_placed = {
            ItemType.GREEN_CRYSTAL: False,
            ItemType.RED_CRYSTAL: False,
            ItemType.BLUE_CRYSTAL: False,
            ItemType.YELLOW_CRYSTAL: False
        }
        self.all_crystals_placed = False

        # Reset boss tracking
        self.boss_defeated = False
        self.victory_timer = 0

        # Recreate world
        self.world = World()

        # Reset player
        self.player = Player(
            x=NATIVE_WIDTH // 2 - 8,
            y=NATIVE_HEIGHT // 2 - 8
        )

        # Respawn items
        self._spawn_test_items()

        # Reset interactables
        self._setup_interactables()

        # Respawn enemies
        self._spawn_enemies()

        # Respawn NPCs
        self._spawn_npcs()

        # Setup final chamber
        self._setup_final_chamber()

    def handle_space_interaction(self):
        """Handle SPACE key interaction (pickup/drop items, use items on interactables)"""
        if not (self.state_machine.is_state(GameState.EXPLORE) or
                self.state_machine.is_state(GameState.ACTIVATION) or
                self.state_machine.is_state(GameState.CLIMAX)):
            return

        current_screen = self.world.get_current_screen()

        # If player is holding an item
        if self.player.has_item():
            held_item = self.player.held_item
            interacted = False

            # First, try to use item on nearby interactables
            for entity in current_screen.entities:
                if hasattr(entity, 'interactable_type'):
                    if entity.is_near_player(
                        self.player.x, self.player.y,
                        self.player.width, self.player.height
                    ):
                        result = entity.interact(held_item)
                        if result:
                            print(f"Used {held_item.get_name()} on {entity.get_name()}")
                            interacted = True

                            # Handle different interaction results
                            if result == "filled":
                                # Item was transformed (watering can/chalice filled)
                                print(f"-> {held_item.get_name()}")
                                break
                            elif result == "planted":
                                # Acorn planted in dirt
                                self.player.drop_item()
                                print("Acorn planted in soft dirt")
                                break
                            elif result == "grow_tree":
                                # Water planted acorn to grow tree bridge
                                if hasattr(self, 'tree_chasm'):
                                    self.tree_chasm.grow_bridge()
                                    print("A tree grows across the chasm!")
                                # Empty the watering can
                                held_item.item_type = ItemType.WATERING_CAN
                                held_item.color = COLOR_GRAY
                                held_item.sprite.fill(COLOR_GRAY)
                                break
                            elif result == "bomb_placed":
                                # Bomb placed at wall - drop it and it will explode
                                dropped = self.player.drop_item()
                                dropped.x = entity.x
                                dropped.y = entity.y
                                dropped.active = True
                                current_screen.entities.append(dropped)
                                # Mark wall for destruction
                                entity.is_activated = True
                                entity.solid = False
                                entity.active = False
                                self.sound_manager.play_sound(SoundType.BOMB_TIMER)
                                # Add explosion particle effect
                                self.particles.add_explosion(entity.x + entity.width // 2,
                                                            entity.y + entity.height // 2,
                                                            color=(255, 150, 0), count=20)
                                print("Bomb placed! The wall crumbles!")
                                # Respawn bomb at original location
                                catacombs_2 = self.world.get_screen(ScreenID.CATACOMBS_2)
                                catacombs_2.entities.append(create_item(ItemType.BOMB, 50, 80))
                                break
                            elif result == "cleansed":
                                # Toxic basin cleansed
                                print("The toxic slime recedes!")
                                # Empty the chalice
                                self.player.drop_item()
                                break
                            elif result == "sleeping":
                                # Statue put to sleep
                                self.sound_manager.play_sound(SoundType.FLUTE_MELODY)
                                print("The statue's eyes close... it sleeps.")
                                break
                            elif result is True:
                                # Generic success (like pedestal)
                                # Check if it's a crystal being placed
                                if hasattr(entity, 'interactable_type') and 'PEDESTAL' in str(entity.interactable_type):
                                    crystal_type = held_item.item_type
                                    if crystal_type in self.crystals_placed:
                                        self.crystals_placed[crystal_type] = True
                                        self.sound_manager.play_sound(SoundType.CRYSTAL_PLACE)
                                        # Add sparkle effect at pedestal
                                        self.particles.add_sparkle(entity.x + entity.width // 2,
                                                                   entity.y + entity.height // 2,
                                                                   held_item.color)
                                        print(f"Crystal placed: {held_item.get_name()}")
                                        # Check if all crystals are now placed
                                        self._check_crystal_activation()
                                # Check for gate opening
                                elif hasattr(entity, 'interactable_type') and 'GATE' in str(entity.interactable_type):
                                    self.sound_manager.play_sound(SoundType.GATE_OPEN)
                                    # Add dust puff when gate opens
                                    self.particles.add_dust(entity.x + entity.width // 2,
                                                           entity.y + entity.height)
                                # Consume the item
                                self.player.drop_item()
                                print(f"{entity.get_name()} activated!")
                                break

            # If didn't interact with anything, drop the item
            if not interacted:
                dropped_item = self.player.drop_item()
                if dropped_item is not None:
                    # Place item at player's current position
                    dropped_item.x = self.player.x + self.player.width // 2 - dropped_item.size // 2
                    dropped_item.y = self.player.y + self.player.height // 2 - dropped_item.size // 2
                    dropped_item.active = True
                    current_screen.entities.append(dropped_item)
                    self.sound_manager.play_sound(SoundType.DROP)
                    print(f"Dropped: {dropped_item.get_name()}")

                    # Check if Fish was dropped near Cat
                    if dropped_item.item_type == ItemType.FISH and self.cat:
                        for entity in current_screen.entities:
                            if hasattr(entity, 'npc_type') and entity.npc_type == NPCType.CAT:
                                # Check if fish is near cat
                                if entity.is_near_player(dropped_item.x, dropped_item.y,
                                                        dropped_item.size, dropped_item.size,
                                                        distance=30):
                                    entity.activate_following()
                                    # Remove the fish
                                    current_screen.entities.remove(dropped_item)
                                    break
        else:
            # Try to pick up an item
            for entity in current_screen.entities:
                # Check if it's an item (has item_type attribute)
                if hasattr(entity, 'item_type'):
                    if entity.is_near_player(
                        self.player.x, self.player.y,
                        self.player.width, self.player.height
                    ):
                        # Check if it's the Ring of Eternity
                        if entity.item_type == ItemType.RING_OF_ETERNITY:
                            print("\n" + "=" * 50)
                            print("YOU HAVE CLAIMED THE RING OF ETERNITY!")
                            print("=" * 50 + "\n")
                            self.sound_manager.play_sound(SoundType.VICTORY)
                            entity.active = False
                            current_screen.entities.remove(entity)
                            self.state_machine.change_state(GameState.WIN)
                            break
                        elif self.player.pick_up_item(entity):
                            entity.active = False
                            current_screen.entities.remove(entity)
                            self.sound_manager.play_sound(SoundType.PICKUP)
                            print(f"Picked up: {entity.get_name()}")
                            break

    def update(self):
        """Update game logic"""
        # State-based updates will go here
        if self.state_machine.is_state(GameState.INIT):
            # Initialize game world, then transition to EXPLORE
            self.state_machine.change_state(GameState.EXPLORE)
        elif self.state_machine.is_state(GameState.EXPLORE) or self.state_machine.is_state(GameState.ACTIVATION):
            # Get current screen
            current_screen = self.world.get_current_screen()

            # Update ambient audio based on location
            self._update_ambient_audio()

            # Check for final chamber entry (special transition)
            if self.world.current_screen_id == ScreenID.TOWER_HUB and self.all_crystals_placed:
                # If player is near the silver gate (top center), enter final chamber
                gate_x, gate_y = 80, 20
                if abs(self.player.x - gate_x) < 20 and abs(self.player.y - gate_y) < 20:
                    if self.player.y < 30:  # Moving upward through gate
                        self.world.current_screen_id = ScreenID.FINAL_CHAMBER
                        self.player.x = NATIVE_WIDTH // 2 - 8
                        self.player.y = NATIVE_HEIGHT - 32
                        self.state_machine.change_state(GameState.CLIMAX)
                        print("\n" + "=" * 50)
                        print("ENTERING THE FINAL CHAMBER...")
                        print("=" * 50 + "\n")
                        return

            # Update player
            old_x, old_y = self.player.x, self.player.y
            self.player.handle_input()
            self.player.update(current_screen)

            # Play walk sound if player moved
            if (old_x != self.player.x or old_y != self.player.y):
                self.sound_manager.play_walk_sound()

            # Update enemies
            for entity in current_screen.entities:
                if hasattr(entity, 'enemy_type'):
                    entity.update(self.player.x, self.player.y, current_screen)

            # Update NPCs
            for entity in current_screen.entities:
                if hasattr(entity, 'npc_type'):
                    entity.update(self.player.x, self.player.y, self.player.held_item)

            # Update particles
            self.particles.update()

            # Check combat and collisions
            self._handle_combat(current_screen)

            # Check for screen transitions
            transition_dir = self.camera.check_screen_transition(
                self.player.x, self.player.y,
                self.player.width, self.player.height
            )

            if transition_dir is not None:
                # Attempt to change screens
                if self.world.change_screen(transition_dir):
                    # Move player to opposite side of new screen
                    opposite = self.camera.get_opposite_direction(transition_dir)
                    new_x, new_y = self.camera.get_player_spawn_position(
                        opposite,
                        self.player.width,
                        self.player.height
                    )
                    self.player.x = new_x
                    self.player.y = new_y

                    # Move cat to new screen if following
                    if self.cat and self.cat.following:
                        # Remove cat from old screen
                        for screen_id in [ScreenID.TOWER_HUB, ScreenID.GARDENS_1, ScreenID.GARDENS_2,
                                        ScreenID.GARDENS_3, ScreenID.GARDENS_4, ScreenID.CATACOMBS_1,
                                        ScreenID.CATACOMBS_2, ScreenID.CATACOMBS_3, ScreenID.CATACOMBS_4,
                                        ScreenID.RUINS_1, ScreenID.RUINS_2, ScreenID.RUINS_3, ScreenID.RUINS_4,
                                        ScreenID.CLIFFS_1, ScreenID.CLIFFS_2, ScreenID.CLIFFS_3, ScreenID.CLIFFS_4]:
                            screen = self.world.get_screen(screen_id)
                            screen.entities = [e for e in screen.entities
                                             if not (hasattr(e, 'npc_type') and e.npc_type == NPCType.CAT)]

                        # Add cat to new screen at player position
                        new_screen = self.world.get_current_screen()
                        self.cat.set_position(new_x, new_y + 20)  # Slightly behind player
                        new_screen.entities.append(self.cat)

        elif self.state_machine.is_state(GameState.CLIMAX):
            # Boss fight state
            current_screen = self.world.get_current_screen()

            # Update player
            self.player.handle_input()
            self.player.update(current_screen)

            # Update particles
            self.particles.update()

            # Update boss
            if self.boss and self.boss.alive:
                self.boss.update(self.player.x, self.player.y, current_screen)

                # Check if player hit boss with sword
                player_has_sword = (self.player.held_item and
                                   hasattr(self.player.held_item, 'item_type') and
                                   self.player.held_item.item_type == ItemType.SWORD)

                if player_has_sword and self.boss.is_colliding_with_player(
                    self.player.x, self.player.y,
                    self.player.width, self.player.height
                ):
                    # Boss takes hit
                    defeated = self.boss.take_hit(self.player.x, self.player.y)
                    if defeated:
                        self.boss.alive = False
                        self.boss_defeated = True
                        # Spawn Ring of Eternity
                        ring = create_item(ItemType.RING_OF_ETERNITY, NATIVE_WIDTH // 2 - 6, NATIVE_HEIGHT // 2 - 6)
                        current_screen.entities.append(ring)
                        print("\n" + "=" * 50)
                        print("THE VOID HAS BEEN DEFEATED!")
                        print("The Ring of Eternity appears...")
                        print("=" * 50 + "\n")

                # Check if player is hit by boss or projectiles
                if self.boss.is_colliding_with_player(
                    self.player.x, self.player.y,
                    self.player.width, self.player.height
                ) and not player_has_sword:
                    self._player_death()
                    return

                # Check projectile collisions
                for projectile in self.boss.projectiles:
                    if projectile.is_colliding_with_player(
                        self.player.x, self.player.y,
                        self.player.width, self.player.height
                    ):
                        self._player_death()
                        return

        elif self.state_machine.is_state(GameState.WIN):
            # Victory state - wait for restart
            self.victory_timer += 1

        elif self.state_machine.is_state(GameState.GAME_OVER):
            # Game over - wait for restart
            pass

    def _handle_combat(self, current_screen):
        """
        Handle combat between player and enemies

        Args:
            current_screen: Current screen
        """
        player_has_sword = (self.player.held_item and
                           hasattr(self.player.held_item, 'item_type') and
                           self.player.held_item.item_type == ItemType.SWORD)

        for entity in current_screen.entities:
            if hasattr(entity, 'enemy_type') and entity.alive:
                # Check collision with player
                if entity.is_colliding_with_player(
                    self.player.x, self.player.y,
                    self.player.width, self.player.height
                ):
                    # Check if enemy is immune to sword (Sentinel)
                    is_immune = hasattr(entity, 'immune_to_sword') and entity.immune_to_sword

                    if player_has_sword and not is_immune:
                        # Player kills enemy
                        entity.alive = False
                        current_screen.entities.remove(entity)
                        self.sound_manager.play_sound(SoundType.SWORD_HIT)
                        self.sound_manager.play_sound(SoundType.ENEMY_DEATH)
                        # Add small explosion effect at enemy position
                        enemy_color = getattr(entity, 'color', (100, 100, 100))
                        self.particles.add_explosion(entity.x + entity.width // 2,
                                                     entity.y + entity.height // 2,
                                                     color=enemy_color, count=10)
                        print(f"Defeated enemy!")
                    else:
                        # Player dies
                        self._player_death()
                        return

        # Check deadly interactables (toxic basin)
        for entity in current_screen.entities:
            if hasattr(entity, 'deadly') and entity.deadly:
                entity_rect = entity.get_rect()
                player_rect = pygame.Rect(
                    self.player.x, self.player.y,
                    self.player.width, self.player.height
                )
                if entity_rect.colliderect(player_rect):
                    self._player_death()
                    return

    def _player_death(self):
        """Handle player death"""
        print("You died! Respawning at Tower Hub...")

        # Drop held item at death location if any
        if self.player.has_item():
            current_screen = self.world.get_current_screen()
            dropped_item = self.player.drop_item()
            if dropped_item:
                dropped_item.x = self.player.x
                dropped_item.y = self.player.y
                dropped_item.active = True
                current_screen.entities.append(dropped_item)
                print(f"Dropped {dropped_item.get_name()} at death location")

        # Respawn player at hub
        self.world.current_screen_id = ScreenID.TOWER_HUB
        self.player.x = NATIVE_WIDTH // 2 - 8
        self.player.y = NATIVE_HEIGHT // 2 - 8

    def _update_ambient_audio(self):
        """Update ambient audio based on current screen"""
        current_screen_id = self.world.current_screen_id

        # Determine ambient type based on screen
        if current_screen_id == ScreenID.TOWER_HUB or current_screen_id == ScreenID.FINAL_CHAMBER:
            ambience = AmbienceType.TOWER_HUM
        else:
            ambience = AmbienceType.WIND

        # Set ambience (will only change if different)
        self.ambient_manager.set_ambience(ambience)

    def _check_crystal_activation(self):
        """Check if all crystals have been placed and activate accordingly"""
        if all(self.crystals_placed.values()) and not self.all_crystals_placed:
            self.all_crystals_placed = True
            print("\n" + "=" * 50)
            print("ALL CRYSTALS PLACED!")
            print("The Tower resonates with elemental power...")
            print("The Silver Gate has opened!")
            print("=" * 50 + "\n")

            # Open the silver gate (if it hasn't been opened with a key already)
            if hasattr(self, 'silver_gate') and not self.silver_gate.is_activated:
                self.silver_gate.is_activated = True
                self.silver_gate.solid = False
                self.silver_gate.active = False

            # Transition to Activation state
            self.state_machine.change_state(GameState.ACTIVATION)

    def render(self):
        """Render the game"""
        # Clear the native surface
        self.native_surface.fill(COLOR_BLACK)

        # Render game objects to native surface
        if self.state_machine.is_state(GameState.EXPLORE) or \
           self.state_machine.is_state(GameState.ACTIVATION) or \
           self.state_machine.is_state(GameState.CLIMAX):
            # Render current screen
            current_screen = self.world.get_current_screen()
            current_screen.render(self.native_surface)

            # Render white outlines on nearby interactable objects
            self._render_interaction_hints(current_screen)

            # Render player
            self.player.render(self.native_surface)

            # Render particles (on top of entities but below HUD)
            self.particles.render(self.native_surface)

            # Render HUD
            self.hud.render(self.native_surface, self.player, self.crystals_placed)

        elif self.state_machine.is_state(GameState.WIN):
            # Victory screen
            self._render_victory_screen()

        elif self.state_machine.is_state(GameState.GAME_OVER):
            # Game over screen (currently unused, but prepared)
            self._render_game_over_screen()

        # Scale up the native surface to the window
        scaled_surface = pygame.transform.scale(
            self.native_surface,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        # Apply CRT effect if enabled
        if self.crt_enabled:
            scaled_surface = self.crt_effect.apply(scaled_surface)

        self.window.blit(scaled_surface, (0, 0))

        # Update the display
        pygame.display.flip()

    def _render_interaction_hints(self, current_screen):
        """
        Render white outlines around interactable objects near the player

        Args:
            current_screen: Current screen
        """
        for entity in current_screen.entities:
            # Check if it's an interactable or item
            is_interactable = hasattr(entity, 'interactable_type')
            is_item = hasattr(entity, 'item_type')

            if (is_interactable or is_item) and entity.active:
                # Check if player is near
                if entity.is_near_player(
                    self.player.x, self.player.y,
                    self.player.width, self.player.height
                ):
                    # Draw white outline
                    outline_rect = pygame.Rect(
                        int(entity.x - 1),
                        int(entity.y - 1),
                        entity.width + 2 if hasattr(entity, 'width') else entity.size + 2,
                        entity.height + 2 if hasattr(entity, 'height') else entity.size + 2
                    )
                    pygame.draw.rect(self.native_surface, COLOR_WHITE, outline_rect, 1)

    def _render_victory_screen(self):
        """Render the victory screen"""
        # Fill with dark background
        self.native_surface.fill((10, 10, 20))

        # Initialize font
        pygame.font.init()
        font_large = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 16)

        # Main victory text
        text1 = font_large.render("A NEW CYCLE", True, COLOR_YELLOW)
        text2 = font_large.render("BEGINS", True, COLOR_YELLOW)

        # Center the text
        x1 = (NATIVE_WIDTH - text1.get_width()) // 2
        y1 = NATIVE_HEIGHT // 2 - 40
        x2 = (NATIVE_WIDTH - text2.get_width()) // 2
        y2 = y1 + 30

        self.native_surface.blit(text1, (x1, y1))
        self.native_surface.blit(text2, (x2, y2))

        # Restart instruction (blinking)
        if (self.victory_timer // 30) % 2 == 0:  # Blink every 0.5 seconds
            restart_text = font_small.render("Press SPACE to Restart", True, COLOR_WHITE)
            rx = (NATIVE_WIDTH - restart_text.get_width()) // 2
            ry = NATIVE_HEIGHT - 40
            self.native_surface.blit(restart_text, (rx, ry))

    def _render_game_over_screen(self):
        """Render the game over screen"""
        # Fill with dark background
        self.native_surface.fill((20, 10, 10))

        # Initialize font
        pygame.font.init()
        font_large = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 16)

        # Game over text
        text = font_large.render("GAME OVER", True, COLOR_RED)
        x = (NATIVE_WIDTH - text.get_width()) // 2
        y = NATIVE_HEIGHT // 2 - 20

        self.native_surface.blit(text, (x, y))

        # Restart instruction
        restart_text = font_small.render("Press SPACE to Restart", True, COLOR_WHITE)
        rx = (NATIVE_WIDTH - restart_text.get_width()) // 2
        ry = NATIVE_HEIGHT - 40
        self.native_surface.blit(restart_text, (rx, ry))

    def run(self):
        """Main game loop"""
        self.running = True
        print("Starting game loop...")

        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Render
            self.render()

            # Maintain 60 FPS and calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0

        # Cleanup
        self.quit()

    def quit(self):
        """Clean up and quit the game"""
        print("Shutting down...")
        self.sound_manager.cleanup()
        self.ambient_manager.stop()
        pygame.quit()
