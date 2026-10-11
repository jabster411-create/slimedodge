import pygame
import random
import math
import time


pygame.init()
WIDTH, HEIGHT = 2000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime dodge")


BG = pygame.transform.scale(pygame.image.load("backgorund.jpeg"), (WIDTH, HEIGHT))


PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
player = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
player_image = pygame.image.load("player1.png").convert_alpha()
PLAYER_BASE_SPEED = 4

# Enemy setup: size, speed, starting position, and image.
ENEMY_SIZE = 70
ENEMY_SPEED = 4.5
enemy = pygame.Rect(WIDTH - ENEMY_SIZE - 100, 100, ENEMY_SIZE, ENEMY_SIZE)
enemy_image = pygame.transform.scale(pygame.image.load("slime1.png").convert_alpha(), (ENEMY_SIZE, ENEMY_SIZE))

# Game state flags and timer.
game_over = False
start_time = time.time()
FONT = pygame.font.SysFont("timesnewroman", 30)

# Sprint mechanic: when the player can move faster and when the ability is recharged.
# sprint_until = when the current sprint ends
# sprint_cooldown_until = when the player can sprint again
sprint_until = 0
sprint_cooldown_until = 0
shift_was_down = False

# Main game loop.
Running = True
while Running:
    # Handle window events such as closing the game or restarting after losing.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Reset the player, enemy, timer, and sprint state so the game restarts.
            player = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT - 100, PLAYER_WIDTH, PLAYER_HEIGHT)
            enemy = pygame.Rect(WIDTH - ENEMY_SIZE - 100, 100, ENEMY_SIZE, ENEMY_SIZE)
            start_time = time.time()
            sprint_until = sprint_cooldown_until = 0
            shift_was_down = False
            game_over = False

    if not Running:
        break

    # Check keyboard input for movement, quit, and sprint controls.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        Running = False

    if not game_over:
        now = time.time()

        # Detect a shift press and start a sprint only if the cooldown is over.
        shift_down = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if shift_down and not shift_was_down and now >= sprint_cooldown_until:
            sprint_until = now + 5
            sprint_cooldown_until = now + 3
        shift_was_down = shift_down

        # Move faster while sprinting; otherwise use normal walking speed.
        player_speed = PLAYER_BASE_SPEED * (1.5 if now < sprint_until else 1)

        # Move the player with arrow keys while staying inside the window.
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += player_speed

        # End the game after 60 seconds.
        if time.time() - start_time >= 60:
            Running = False

        # Enemy chases the player by moving toward their center.
        direction_x = player.centerx - enemy.centerx
        direction_y = player.centery - enemy.centery
        distance = math.hypot(direction_x, direction_y)
        if distance > 0:
            enemy.x += round(direction_x / distance * ENEMY_SPEED)
            enemy.y += round(direction_y / distance * ENEMY_SPEED)

        # If the slime touches the player, the game is over.
        game_over = enemy.colliderect(player)

    # Draw the background and game objects every frame.
    WIN.blit(BG, (0, 0))
    WIN.blit(enemy_image, enemy)
    WIN.blit(player_image, player)

    # Show the elapsed timer in the corner.
    time_text = FONT.render(f"clock: {int(time.time() - start_time)}s", True, "red")
    WIN.blit(time_text, (10, 10))

    # Show the game-over message and let the player restart with R.
    if game_over:
        message = FONT.render("Haha, you suck! Try again. Press R to restart.", True, "yellow")
        WIN.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.update()

# Cleanly close the game when the loop ends.
pygame.quit()
