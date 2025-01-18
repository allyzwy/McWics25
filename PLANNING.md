# Game Planning

## Elements

### Player

Singleton instance of main player. Should be defined separately as a unique class.

### Enemies

Movable objects in a fixed trajectory. On touch with player, Activate on-hit on player

### Coins

Adds 1 to coin pouch. To incentivise player to move in a defined trajectory.

### Lava

Lava is a special platform that will kill the player and activate Death.

## Mechanisms

### Player On Hit

When the player is hit, bounce the player back x, y velocity. This is recursive

### Death

Return to previous checkpoint (if we have time to implement)
