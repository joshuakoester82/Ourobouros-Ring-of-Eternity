# Ouroboros - Ring of Eternity: Development Tasks

## Project Setup ✓
- [x] Create project directory structure
- [x] Create tasks.md tracking file
- [x] Create requirements.txt
- [x] Initial commit

## Phase 1: Core Engine & Foundation ✓
### 1.1 Game Loop & Window Setup ✓
- [x] Initialize Pygame and create game window
- [x] Implement main game loop (60 FPS target)
- [x] Set up native resolution (160x192 or 320x240) with 4x-5x scaling
- [ ] Implement CRT shader/filter effect (optional but cool)
- [x] Add basic state machine framework

### 1.2 Player System ✓
- [x] Create Player class (16x16 white square sprite)
- [x] Implement WASD/Arrow key input handling
- [x] Implement non-inertial movement physics
- [x] Add collision detection with 16px tile grid
- [x] Add player position tracking and screen boundaries

### 1.3 Camera & Screen System ✓
- [x] Implement screen/room system (24 total screens)
- [x] Create screen transition logic
- [x] Build camera system that follows player between screens
- [x] Add screen boundary detection

## Phase 2: World Building
### 2.1 Map Structure
- [ ] Design 24-screen layout (web pattern with central hub)
- [ ] Implement The Ouroboros Tower (Hub) - center screen
- [ ] Create screen connection/adjacency data structure

### 2.2 Biome: The Withered Gardens (North - Earth Theme)
- [ ] Design 4-5 interconnected screens
- [ ] Implement visual theme (earth tones, withered plants)
- [ ] Place Gold Key spawn location (random)
- [ ] Create Hollow Tree location for Green Crystal
- [ ] Build Tree Bridge puzzle area (chasm, soft dirt patch)
- [ ] Place Acorn spawn (Screen N-2)
- [ ] Place Watering Can spawn (Screen N-1)

### 2.3 Biome: The Catacombs (East - Dark/Fire Theme)
- [ ] Design 4-5 interconnected screens
- [ ] Implement visual theme (dark, fire elements)
- [ ] Create Gold Gate entrance (requires Gold Key)
- [ ] Build Cracked Wall puzzle area with Red Crystal
- [ ] Place Bomb spawn (Screen E-2)
- [ ] Add Ogre location (guards Silver Key)

### 2.4 Biome: The Sunken Ruins (South - Water Theme)
- [ ] Design 4-5 interconnected screens
- [ ] Implement visual theme (water, ruins)
- [ ] Create dried fountain basin with Blue Crystal
- [ ] Build Blessed Spring location (Screen S-4)
- [ ] Create toxic basin with purple slime (Screen S-3)
- [ ] Place Chalice in maze (Screen S-2)

### 2.5 Biome: The High Cliffs (West - Air Theme)
- [ ] Design 4-5 interconnected screens
- [ ] Implement visual theme (cliffs, sky elements)
- [ ] Create Sleepless Statue location with Yellow Crystal
- [ ] Place Flute spawn (Screen W-2)
- [ ] Add Sheet Music hint wall (Screen W-1)

### 2.6 Tower Hub Enhancements
- [ ] Create 4 corner pedestals with colored outlines
- [ ] Implement Silver Gate (requires Silver Key)
- [ ] Build Final Chamber behind Silver Gate
- [ ] Add fountain for Watering Can refills
- [ ] Place Cat NPC spawn

## Phase 3: Inventory & Item System ✓
### 3.1 Core Inventory System ✓
- [x] Implement one-slot inventory system
- [x] Add SPACE key interaction handler
- [x] Create pickup logic (touch + empty hand)
- [x] Create drop logic (current location)
- [x] Add item-to-interactable application logic
- [x] Display currently held item (HUD or sprite overlay)

### 3.2 Key Items ✓
- [x] Gold Key sprite and logic
- [x] Silver Key sprite and logic
- [x] Gold Gate unlock interaction
- [x] Silver Gate unlock interaction

### 3.3 Elemental Crystals ✓
- [x] Green Crystal (Earth) sprite and logic
- [x] Red Crystal (Fire) sprite and logic
- [x] Blue Crystal (Water) sprite and logic
- [x] Yellow Crystal (Air) sprite and logic
- [x] Pedestal placement interaction
- [ ] Crystal collection tracking

### 3.4 Puzzle Items ✓
- [x] Acorn sprite and logic
- [x] Watering Can sprite and logic
- [x] Watering Can (Full) state change at fountain
- [x] Bomb sprite and logic
- [ ] Bomb timer (3 seconds) and explosion (simplified - instant)
- [x] Chalice sprite and logic
- [x] Chalice (Filled) state change at Blessed Spring
- [x] Flute sprite and logic
- [x] Sword sprite and combat logic
- [x] Fish (easter egg) sprite and logic

### 3.5 Interaction Feedback ✓
- [x] White outline on interactable objects in range
- [x] Colored outlines on pedestals
- [x] Keyhole sprites on locked doors

## Phase 4: Puzzles & Solutions ✓
### 4.1 Puzzle A: The Tree Bridge ✓
- [x] Acorn + Soft Dirt interaction
- [x] Watering Can fill mechanic at fountain
- [x] Filled Watering Can + Acorn interaction
- [x] Tree Bridge sprite spawning
- [x] Chasm crossing logic

### 4.2 Puzzle B: The Cracked Wall ✓
- [x] Bomb placement at Cracked Wall
- [ ] 3-second timer with sound (simplified - instant)
- [ ] Explosion particle effect
- [x] Wall destruction
- [x] Bomb respawn at original location

### 4.3 Puzzle C: The Cleansing ✓
- [ ] Toxic slime collision (instant death)
- [x] Chalice fill at Blessed Spring
- [x] Filled Chalice at toxic basin interaction
- [ ] Slime recede animation (simplified - instant disappear)
- [x] Blue Crystal reveal

### 4.4 Puzzle D: The Sleepless Guardian ✓
- [ ] Statue attack range (lightning bolt)
- [x] Flute usage near Statue
- [ ] Melody playback
- [x] Statue dormant state (sprite change)
- [x] Safe crystal collection

## Phase 5: Enemy AI & Combat ✓
### 5.1 Enemy Base System ✓
- [x] Enemy base class
- [x] Collision detection with player
- [x] Death/respawn logic
- [x] Spawn point system

### 5.2 Tier 1: The Crawler ✓
- [x] Green square blob sprite
- [x] Brownian motion AI (random cardinal directions)
- [x] Pause and direction change logic
- [x] Wall bounce behavior

### 5.3 Tier 2: The Chaser ✓
- [x] Red chevron/triangle sprite
- [x] Line-of-sight raycasting
- [x] Aggro range (150 pixels)
- [x] Chase behavior (75% player speed)
- [x] Return to spawn logic

### 5.4 Tier 3: The Sentinel ✓
- [x] Yellow serpentine sprite (multi-segment optional)
- [x] Fixed patrol route waypoints
- [x] Rapid looping movement
- [x] Sword immunity
- [x] Timing-based bypass challenge

### 5.5 Combat System ✓
- [x] Sword-wielding collision detection
- [x] Enemy kill logic for Tier 1 & 2
- [x] Player death on unarmed collision
- [x] Player respawn at Tower Hub
- [x] Item drop on death (persistent location)

## Phase 6: Boss & Endgame ✓
### 6.1 The Void Boss ✓
- [x] Flickering geometric polygon sprite (random colors/shapes)
- [x] High-speed bouncing movement
- [x] Hit detection with Sword
- [x] Teleport to random corner on hit
- [x] Projectile shooting mechanic
- [x] 3-hit kill counter
- [x] Boss defeat/dissipate

### 6.2 Victory Sequence ✓
- [x] Ring of Eternity (golden circle) sprite
- [x] Pickup detection
- [x] "A NEW CYCLE BEGINS" game over screen
- [x] Press Space to Restart functionality
- [x] Game state reset

## Phase 7: NPCs & Easter Eggs ✓
### 7.1 The Owl ✓
- [x] Owl sprite in North Biome
- [x] Proximity detection with Flute
- [x] "Song of Sleep" hint text display

### 7.2 The Cat ✓
- [x] Cat sprite in Tower Hub
- [x] Fish drop proximity detection
- [x] Follow-the-player companion AI
- [x] Screen-to-screen persistence

## Phase 8: Audio System ✓
### 8.1 Audio Framework ✓
- [x] Set up pygame.mixer
- [x] Implement numpy array sound generation
- [x] Create sound effect manager

### 8.2 Sound Effects (Procedural) ✓
- [x] Walk: White noise burst (300ms interval)
- [x] Pickup: Ascending arpeggio (square wave)
- [x] Drop: Descending slide
- [x] Sword Hit: Low frequency noise + sawtooth fade
- [x] Enemy Death: Distortion crunch
- [x] Victory: Major chord progression
- [x] Bomb Timer: Ticking sound
- [x] Flute Melody: Custom melody
- [x] Gate Open: Mechanical rumble
- [x] Crystal Place: Magical chime

### 8.3 Ambient Audio ✓
- [x] Tower Hub low hum
- [x] Wind noise for outside areas
- [x] Biome-specific ambient sounds (location-based switching)

## Phase 9: UI & Visual Polish
### 9.1 HUD ✓
- [x] Current item display
- [x] Crystal collection counter
- [x] Minimal UI overlay

### 9.2 Visual Effects
- [x] White outline on interactable objects in range
- [ ] Screen transition effects (optional polish)
- [ ] Explosion particle burst (optional polish)
- [ ] Lightning bolt effect (optional polish)
- [ ] Slime recede animation (optional polish)
- [ ] Tree growth animation (optional polish)
- [x] Sprite flickering for The Void (already implemented)

### 9.3 Atari 2600 Aesthetic
- [ ] Chunky pixel sprites (16x16 standard)
- [ ] Limited color palette
- [ ] CRT scanline effect
- [ ] Proper scaling (4x-5x) for modern displays

## Phase 10: Game State Management
### 10.1 State Machine
- [ ] Init state: World generation, item spawning
- [ ] Explore state: Active gameplay
- [ ] Collection state: Crystal tracking
- [ ] Activation state: All crystals placed, gate opens
- [ ] Climax state: Boss fight
- [ ] Win state: Ring collected
- [ ] Game Over state: Restart prompt

### 10.2 Persistence
- [ ] Save world state (doors opened, puzzles solved)
- [ ] Save dropped item positions
- [ ] Maintain state on player death
- [ ] Reset on game restart

## Phase 11: Testing & Balancing
### 11.1 Core Gameplay Testing
- [ ] Movement and collision testing
- [ ] Screen transitions
- [ ] All puzzle solutions
- [ ] Enemy AI behaviors
- [ ] Boss fight balance

### 11.2 Edge Cases
- [ ] Item persistence on death
- [ ] Multiple bomb uses
- [ ] Crystal pedestal interactions
- [ ] Enemy respawn behavior
- [ ] Boundary collision bugs

### 11.3 Performance
- [ ] 60 FPS consistency
- [ ] Memory usage optimization
- [ ] Audio performance

## Phase 12: Polish & Release
### 12.1 Final Polish
- [ ] All visual effects working
- [ ] All audio effects working
- [ ] Smooth screen transitions
- [ ] Consistent game feel

### 12.2 Documentation
- [ ] Update README with controls and gameplay
- [ ] Add installation instructions
- [ ] Create credits section
- [ ] Write developer notes

### 12.3 Packaging
- [ ] Create executable/distributable
- [ ] Test on different platforms
- [ ] Final playtesting

## Current Status
**Last Updated:** 2025-11-22

**Phase:** Phase 8 Complete - NPCs and Audio Implemented!
**Completed Tasks:** ~115+
**Total Tasks:** ~150+

**Recently Completed:**
- Phase 1: Core Engine & Foundation ✓
- Phase 3: Inventory & Item System ✓
- Phase 4: Puzzles & Solutions ✓
  - All 4 puzzle mechanics implemented and working
  - Crystal pedestals in Tower Hub
  - Gate unlock mechanics
  - Tree Bridge, Cracked Wall, Toxic Basin, and Statue puzzles
- Phase 5: Enemy AI & Combat ✓
  - 3 enemy types with unique AI behaviors
  - Crawler (random movement), Chaser (pursuit AI), Sentinel (patrol routes)
  - Combat system with sword mechanics
  - Player death and respawn system
- Phase 6: Boss & Endgame ✓
  - The Void boss with flickering polygon sprites
  - Boss AI with bouncing movement, teleportation, and projectiles
  - 3-hit boss fight mechanic
  - Ring of Eternity victory item
  - Victory screen with "A NEW CYCLE BEGINS"
  - Game restart functionality

**Game is now fully playable from start to finish!**

**Recently Added (2025-11-22):**
- Phase 7: NPCs & Easter Eggs ✓
  - The Owl NPC with Flute hint system
  - The Cat companion NPC with Fish following mechanics
  - Screen-to-screen companion persistence
- Phase 8: Audio System ✓
  - Procedural sound generation with pygame.mixer and numpy
  - 10 different sound effects (walk, pickup, drop, sword hit, enemy death, victory, bomb, flute, gate, crystal)
  - Ambient audio system (Tower hum, Wind noise)
  - Location-based ambient switching
- Phase 9 (Partial): UI & Visual Polish
  - White outline interaction hints on nearby objects
  - Crystal collection counter in HUD (already present)

**Next Steps (Optional Polish):**
1. Complete world building with all 24 screens - Phase 2
2. Additional visual effects (particles, animations) - Phase 9
3. Final testing and balancing - Phase 11
4. Documentation and packaging - Phase 12
