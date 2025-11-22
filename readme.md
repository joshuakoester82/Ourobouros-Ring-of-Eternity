Technical Design Document: Ouroboros - Ring of Eternity
1. Project Overview

Engine: Python (Pygame Community Edition)
Genre: Top-down Action-Adventure
Aesthetic: Atari 2600 (Chunky pixels, low color depth, CRT feel)
Resolution: Native logic at 160x192 (or 320x240), scaled up 4x-5x for modern displays.
2. Core Mechanics & Controls
Player Movement

    Avatar: A white 16x16 pixel square.

    Control Scheme: Arrow Keys or WASD for movement (Grid-free movement, but aligns to 16px tiles for collision).

    Physics: Standard non-inertial movement (stop instantly when key released).

The "One-Slot" Inventory System

    Concept: Heavily inspired by Atari Adventure.

    Constraint: The player can only hold ONE item at a time.

    Interaction:

        SPACE BAR: Interaction Key.

        Logic:

            If holding nothing and touching an item → Pick up item.

            If holding an item → Drop item at current location (item persists in world).

            If holding an item and touching a specific "Interactable" (e.g., Lock, Pedestal) → Apply item effect.

3. World Map Structure

Topology: 24 Screens (Rooms) arranged in a Web Pattern.

    Center: The Ouroboros Tower (Hub).

    Directions: Four distinct biomes radiate from the hub, each containing 4-5 interconnected screens.

    Biomes:

        North: The Withered Gardens (Earth Theme)

        East: The Catacombs (Dark/Fire Theme)

        South: The Sunken Ruins (Water Theme)

        West: The High Cliffs (Air Theme)

4. Items, Logic, & Solutions

Note: Items appear as distinct colored sprites.
Keys (Progression Gates)

    Gold Key:

        Location: Randomly placed in the Withered Gardens.

        Use: Unlocks the Gold Gate blocking entrance to the Catacombs.

    Silver Key:

        Location: Guarded by the Ogre in the Catacombs.

        Use: Unlocks the Silver Gate inside the Tower leading to the Final Chamber.

The 4 Elemental Crystals (Primary Objective)

The player must bring all 4 to the Tower Hub and place them on their respective corner pedestals.

    Green Crystal (Earth): Hidden inside the Hollow Tree.

    Red Crystal (Fire): Encased in a cracked wall block.

    Blue Crystal (Water): Inside the dried fountain basin.

    Yellow Crystal (Air): Held by the Sleepless Statue.

Puzzle Items & Solutions
Puzzle A: The Tree Bridge (The Gardens)

Problem: A wide chasm blocks the path to the Green Crystal. There is a patch of soft dirt nearby.
Items Required: Acorn, Watering Can.
Solution:

    Find Acorn (Screen N-2). Drop Acorn on Soft Dirt (Screen N-3).

    Find Watering Can (Screen N-1).

    Go to Fountain (Hub or South Biome) to change state of can to Watering Can (Full).

    Bring filled can to Acorn. Press SPACE.

    Effect: Acorn sprite vanishes, replaced by a Tree Bridge sprite. Player can walk over chasm.

Puzzle B: The Cracked Wall (The Catacombs)

Problem: The Red Crystal is visible but surrounded by Destructible Walls.
Item Required: Bomb.
Solution:

    Locate Bomb (Screen E-2, guarded by Bats).

    Carry Bomb to Cracked Wall (Screen E-4).

    Press SPACE. A timer ticking sound plays (3 seconds).

    Effect: Player must run away. Bomb explodes (simple particle burst). Walls disappear. Crystal is accessible.
    Note: Bomb respawns at original spawn point if used incorrectly.

Puzzle C: The Cleansing (The Sunken Ruins)

Problem: The Blue Crystal is in a basin covered in toxic purple slime (kills on contact).
Item Required: Chalice.
Solution:

    Find Chalice inside a maze (Screen S-2).

    Locate the Blessed Spring (Screen S-4) containing blue water.

    Use Chalice on Spring → Item becomes Chalice (Filled).

    Take Filled Chalice to Toxic Basin (Screen S-3).

    Effect: Slime recedes, Blue Crystal is revealed.

Puzzle D: The Sleepless Guardian (The Cliffs)

Problem: The Yellow Crystal is held by a Statue that kills the player if they get too close (Lightning bolt).
Item Required: Flute.
Solution:

    Find Flute (Screen W-2).

    Find the Sheet Music hint (a specific pattern of colors) painted on a wall in Screen W-1.

    Approach the Statue (Screen W-4) just outside of attack range.

    Use Flute.

    Effect: A melody plays. The Statue's eyes close (sprite change). It is now dormant. The Player can safely grab the crystal.

The Sword

    Utility: Can kill Tier 1 and Tier 2 enemies.

    Mechanism: Player touches enemy while holding Sword → Enemy dies/despawns. (If not holding sword, Player dies).

5. Enemies & AI Behaviors

General Rule: One hit kills the Player. Upon death, Player respawns at the Tower Hub. World state (open doors/solved puzzles) is saved; items dropped on death stay where the player died.
Tier 1: The Crawler (Zombie/Slime)

    Appearance: Green Square blob.

    Behavior: Brownian Motion. Moves in random cardinal directions for 1-2 seconds, pauses, chooses new direction. Bounces off walls. Low threat.

Tier 2: The Chaser (Orc)

    Appearance: Red Chevron/Triangle.

    Behavior: Line-of-Sight Aggro. Uses basic Raycasting. If there is a clear line to the player within 150 pixels, it moves directly toward the player at 75% of player speed. Returns to spawn point if player is lost.

Tier 3: The Sentinel (Dragon/Wyvern)

    Appearance: Yellow serpentine shape (multi-segment sprite optionally).

    Behavior: Fixed Patrol Route. Loops rapidly between specific waypoints. Does not chase. Touches result in death. Requires timing to bypass.

    Immune to Sword. (Must be avoided or distracted).

Boss: The Void (The Final Encounter)

    Location: Behind the Silver Gate in the Tower.

    Appearance: A flickering, shifting geometric polygon (changing random colors/shapes).

    Mechanic: The Ring of Eternity is behind The Void.

    Combat:

        The Void bounces around the room at high speed.

        If hit by Sword, The Void teleports to a random corner and shoots a projectile.

        Must be hit 3 times to dissipate.

6. NPCs

Static sprites that provide context but do not move.

    The Owl: Perched in the North Biome. If Player approaches with the Flute, text appears (subtitle style) hinting at the "Song of Sleep."

    The Cat: Spawns in the Tower Hub. If the player drops the Fish (an easter egg item with no other use) near it, the Cat follows the player from screen to screen as a companion.

7. Game Flow State Machine

    Init: Generate world, spawn items.

    Explore: Player gathers 2 Keys and solves 4 Item Puzzles.

    Collection: Player creates a stockpile of Crystals at the Tower.

    Activation: Placing 4 crystals illuminates the room and opens the Silver Gate.

    Climax: Boss Fight with The Void.

    Win: Pick up the Ring of Eternity (Golden Circle).

    Game Over Screen: "A NEW CYCLE BEGINS" (Press Space to Restart).

8. Audio Specification (Procedural/Synthesized)

Use pygame.mixer and numpy arrays to generate retro sounds to keep assets low.

    Walk: White noise burst (very short) every 300ms.

    Pickup: Ascending arpeggio (Square wave).

    Drop: Descending slide.

    Sword Hit: Low frequency noise + Sawtooth fade.

    Enemy Death: Distortion crunch.

    Victory: Major chord progression.

    Ambience: No continuous music. Just a low "hum" for the Tower and distinct wind noise for outside.

9. Visual Hints & Feedback

    Interaction Range: Draw a subtle white outline around objects when the player is close enough to interact.

    Pedestals: Each pedestal in the tower has a colored outline corresponding to the crystal required (Red, Green, Blue, Yellow).

    Locked Doors: Clearly display a keyhole shape in the color of the key required.