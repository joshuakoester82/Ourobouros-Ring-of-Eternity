# Ouroboros - Ring of Eternity

A retro top-down action-adventure game inspired by the Atari 2600 era. Explore a mysterious tower and four elemental biomes, solve puzzles with a one-slot inventory system, battle enemies, and claim the legendary Ring of Eternity.

## 🎮 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Requirements
- Python 3.8+
- pygame-ce >= 2.4.0
- numpy >= 1.24.0

## 🕹️ Controls

| Key | Action |
|-----|--------|
| **WASD** or **Arrow Keys** | Move player |
| **SPACE** | Interact (pickup/drop items, use on objects) |
| **ESC** | Quit game |

## 📖 How to Play

### The One-Slot Inventory

You can only hold **ONE item at a time** - just like in classic Atari Adventure!

- **Empty handed + near item** → Press SPACE to pick up
- **Holding item** → Press SPACE to drop at your feet
- **Holding item + near interactable** → Press SPACE to use item

### Your Quest

1. **Explore** the Ouroboros Tower and four elemental biomes
2. **Collect** the four Elemental Crystals (Green, Red, Blue, Yellow)
3. **Place** all crystals on their pedestals in the Tower Hub
4. **Enter** the Final Chamber when the Silver Gate opens
5. **Defeat** The Void boss
6. **Claim** the Ring of Eternity to complete the cycle

## 🗺️ The World

The game consists of **18 interconnected screens**:

### The Ouroboros Tower (Hub)
- **Central nexus** connecting all four biomes
- Contains four corner **pedestals** for the Elemental Crystals
- Has a **fountain** to refill your Watering Can
- The **Silver Gate** opens when all crystals are placed

### North - The Withered Gardens 🌱 (Earth Biome)
- 4 screens of withered plant life
- Find the **Green Crystal** in the Hollow Tree
- Solve the **Tree Bridge** puzzle to cross the chasm
- Enemies: Crawlers (green blobs)

### East - The Catacombs 🔥 (Fire/Dark Biome)
- 4 screens of dark corridors
- Find the **Red Crystal** behind a Cracked Wall
- The **Gold Gate** blocks entry (need Gold Key)
- Defeat the Ogre to get the **Silver Key**
- Enemies: Chasers (red triangles)

### South - The Sunken Ruins 💧 (Water Biome)
- 4 screens of flooded ruins
- Find the **Blue Crystal** in the Toxic Basin
- Navigate the maze to find the Chalice
- Use the **Blessed Spring** to fill the Chalice
- Enemies: Mix of Crawlers and Chasers

### West - The High Cliffs 💨 (Air Biome)
- 4 screens of windswept heights
- Find the **Yellow Crystal** held by the Sleepless Statue
- Play the melody to put the Statue to sleep
- Enemies: Sentinels (yellow serpents on patrol routes)

### The Final Chamber ⚡
- Behind the Silver Gate in the Tower
- Face **The Void** boss (3 hits to defeat)
- Claim the **Ring of Eternity**

## 🧩 Puzzles & Solutions

### Puzzle A: The Tree Bridge 🌳
**Problem:** A chasm blocks the path to the Green Crystal
**Solution:**
1. Find **Acorn** (Gardens - Screen 2)
2. Drop Acorn on **Soft Dirt** patch (Gardens - Screen 3)
3. Find **Watering Can** (Gardens - Screen 1)
4. Fill it at any **Fountain** (Tower Hub or Ruins)
5. Use filled can on planted Acorn → Tree grows across chasm!

### Puzzle B: The Cracked Wall 💣
**Problem:** Red Crystal is trapped behind a destructible wall
**Solution:**
1. Find **Bomb** (Catacombs - Screen 2)
2. Carry it to the **Cracked Wall** (Catacombs - Screen 4)
3. Use Bomb on wall → Wall crumbles, crystal accessible
4. Note: Bomb respawns at original location

### Puzzle C: The Cleansing 🧪
**Problem:** Blue Crystal is submerged in toxic purple slime
**Solution:**
1. Find **Chalice** (Ruins - Screen 2, in the maze)
2. Fill it at the **Blessed Spring** (Ruins - Screen 4)
3. Use filled Chalice on **Toxic Basin** (Ruins - Screen 3)
4. Slime recedes, revealing the Blue Crystal

### Puzzle D: The Sleepless Guardian 🎵
**Problem:** Statue attacks anyone who gets too close
**Solution:**
1. Find **Flute** (Cliffs - Screen 2)
2. Optional: Find Sheet Music hint (Cliffs - Screen 1)
3. Approach the **Sleepless Statue** (Cliffs - Screen 4)
4. Use Flute near the Statue → Plays "Song of Sleep"
5. Statue's eyes close, safe to take Yellow Crystal

## ⚔️ Combat & Enemies

### Enemy Types

**Tier 1: The Crawler** (Green Blob)
- Random wandering movement
- Slow and predictable
- Vulnerable to Sword

**Tier 2: The Chaser** (Red Triangle)
- Detects you within 150 pixels
- Chases at 75% of your speed
- Returns to spawn when you escape
- Vulnerable to Sword

**Tier 3: The Sentinel** (Yellow Serpent)
- Patrols fixed routes rapidly
- Does NOT chase you
- **IMMUNE to Sword** - must be avoided!
- Timing-based bypass challenge

**Boss: The Void** (Flickering Polygon)
- Appears in the Final Chamber
- Bounces around at high speed
- Shoots projectiles when hit
- Teleports to random corner when damaged
- Requires **3 sword hits** to defeat
- Drops the **Ring of Eternity** on defeat

### Combat Rules
- **Without Sword:** Touching ANY enemy = instant death
- **With Sword:** Touch Tier 1/2 enemies to kill them
- **Death:** Respawn at Tower Hub, but items stay where you died
- Sentinels and The Void require strategy, not just sword

## 🎒 Items & Keys

### Progression Keys
- **Gold Key** - Opens Gold Gate to Catacombs (found in Gardens)
- **Silver Key** - Opens Silver Gate to Final Chamber (guarded by Ogre)

### Elemental Crystals (The 4 Main Objectives)
- **Green Crystal** (Earth) - In Hollow Tree
- **Red Crystal** (Fire) - Behind Cracked Wall
- **Blue Crystal** (Water) - In Toxic Basin
- **Yellow Crystal** (Air) - Held by Sleepless Statue

### Puzzle Items
- **Acorn** - Plant in soft dirt
- **Watering Can** - Fill at fountain, water planted acorn
- **Bomb** - Destroys cracked walls
- **Chalice** - Fill at Blessed Spring, cleanses toxic slime
- **Flute** - Plays melody to put Statue to sleep

### Combat & Utility
- **Sword** - Kill Tier 1 & 2 enemies (found in Tower Hub)

### Easter Egg
- **Fish** - Drop near the Cat in Tower Hub to gain a companion!

## 🐱 NPCs

### The Owl 🦉
- Found in the Withered Gardens
- Approach with the **Flute** to get a hint about the "Song of Sleep"

### The Cat 🐈
- Sits in the Tower Hub
- Drop the **Fish** near it to make it follow you
- Cat companion persists across screens!

## 🎵 Audio

All sounds are **procedurally generated** using NumPy arrays:
- Walk sounds (white noise bursts)
- Pickup/drop sounds (arpeggios and slides)
- Combat sounds (sword hits, explosions)
- Puzzle sounds (gate opening, crystal placement)
- Musical sounds (flute melody, victory chord)

**Ambient Audio:**
- Tower Hub: Low mysterious hum
- Outdoor biomes: Wind noise

## 🎨 Visual Style

**Atari 2600 Aesthetic:**
- Native resolution: 160×192 pixels
- Scaled 4× for modern displays (640×768)
- Chunky 16×16 pixel sprites
- Limited color palette per screen
- Biome-specific background colors

**Visual Feedback:**
- White outlines appear on nearby interactable objects
- Colored outlines on crystal pedestals (match crystal color)
- Keyholes on locked gates

## 🏆 Victory Condition

1. Place all 4 Elemental Crystals on pedestals
2. Silver Gate opens automatically
3. Enter Final Chamber (top of Tower Hub)
4. Defeat The Void with 3 sword hits
5. Pick up the Ring of Eternity
6. **"A NEW CYCLE BEGINS"**
7. Press SPACE to restart and play again!

## 💀 Death & Respawn

When you die:
- Respawn at Tower Hub (center screen)
- Held item **drops at death location** (persists in world)
- All puzzles stay solved
- All gates stay open
- Can return to retrieve dropped items

## 🎯 Tips & Strategy

1. **Explore thoroughly** - Items are scattered across biomes
2. **Plan your route** - One-slot inventory means lots of backtracking
3. **Drop items strategically** - Create item caches in key locations
4. **Get the Sword early** - Makes exploration much safer
5. **Sentinels can't be killed** - Watch patrol patterns, time your moves
6. **Toxic slime is deadly** - Don't touch until cleansed
7. **Boss strategy** - Hit and run, dodge projectiles, use corners
8. **The Cat is optional** - But it's a fun companion!

## 📁 Project Structure

```
Ourobouros-Ring-of-Eternity/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── tasks.md               # Development tracking
└── src/
    ├── core/              # Game engine
    │   ├── game.py        # Main game loop
    │   ├── constants.py   # Game constants
    │   └── state_machine.py
    ├── entities/          # Game objects
    │   ├── player.py
    │   ├── enemy.py
    │   ├── item.py
    │   ├── interactable.py
    │   └── npc.py
    ├── world/             # Map system
    │   ├── world.py       # World manager
    │   ├── screen.py      # Room system
    │   └── camera.py      # Screen transitions
    ├── ui/                # User interface
    │   └── hud.py
    └── audio/             # Sound system
        ├── sound_manager.py
        └── ambient.py
```

## 🛠️ Development

Built with:
- **Python 3.8+**
- **Pygame Community Edition** - 2D game framework
- **NumPy** - Procedural audio generation

Inspired by:
- Atari 2600 "Adventure" (1980) - One-slot inventory mechanic
- The Legend of Zelda (1986) - Top-down exploration
- Metroidvania design - Interconnected world, item-gated progression

## 📝 License

This is a personal project created for educational and entertainment purposes.

## 🎮 Have Fun!

Enjoy your journey through the Ouroboros Tower! Can you claim the Ring of Eternity and begin a new cycle?

---

**Created with ❤️ using Python and Pygame**
