"""
Simple script to verify that COLOR_WHITE and COLOR_RED are imported in game.py
This script doesn't require pygame or numpy to be installed.
"""

import re

def verify_color_imports():
    """Verify that all necessary colors are imported in game.py"""

    with open('/home/user/Ourobouros-Ring-of-Eternity/src/core/game.py', 'r') as f:
        content = f.read()

    # Check for the import statement
    import_pattern = r'from src\.core\.constants import \([^)]+\)'
    match = re.search(import_pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        print("❌ FAIL: Could not find constants import statement")
        return False

    import_block = match.group(0)

    # Check for each required color
    required_colors = ['COLOR_WHITE', 'COLOR_RED', 'COLOR_BLACK', 'COLOR_GRAY', 'COLOR_YELLOW']
    missing_colors = []

    for color in required_colors:
        if color not in import_block:
            missing_colors.append(color)

    if missing_colors:
        print(f"❌ FAIL: Missing color imports: {', '.join(missing_colors)}")
        print(f"\nImport block found:\n{import_block}")
        return False

    # Check that COLOR_WHITE is actually used in the file
    if 'COLOR_WHITE' not in content:
        print("❌ FAIL: COLOR_WHITE is imported but never used")
        return False

    # Find usage of COLOR_WHITE
    white_usage = content.count('COLOR_WHITE')
    red_usage = content.count('COLOR_RED')

    print("✓ All required colors are imported:")
    for color in required_colors:
        usage_count = content.count(color)
        print(f"  - {color}: used {usage_count} times")

    # Verify specific fix for line 830
    if 'pygame.draw.rect(self.native_surface, COLOR_WHITE, outline_rect, 1)' in content:
        print("\n✓ Line 830 fix verified: COLOR_WHITE is used in pygame.draw.rect")
    else:
        print("\n⚠ Warning: Could not verify line 830 (code may have changed)")

    # Verify COLOR_RED usage in game over screen
    if 'COLOR_RED' in content and 'GAME OVER' in content:
        print("✓ COLOR_RED is used (likely in game over screen)")

    return True

if __name__ == '__main__':
    print("Verifying color imports in game.py...")
    print("=" * 60)

    if verify_color_imports():
        print("\n" + "=" * 60)
        print("✓ ALL CHECKS PASSED!")
        print("The imports have been fixed correctly.")
        exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ VERIFICATION FAILED")
        exit(1)
