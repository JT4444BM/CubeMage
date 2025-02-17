import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elemental 2D Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Fire
BLUE = (0, 0, 255)  # Water
GREEN = (0, 255, 0)  # Earth
GRAY = (200, 200, 200)  # Wind
BLACK = (0, 0, 0)  # Enemy
DARK_RED = (139, 0, 0)  # Health bars
PINK = (255, 105, 180)  # Medkit
ORANGE = (255, 165, 0)  # Player
PURPLE = (75, 0, 130)  # Dark Magic Projectiles

# Player settings
player_size = 30  # Smaller player size
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5
player_health = 100
max_health = 100
player_element = None  # The single collected ability
player_ammo = 0  # Ammo for the current ability

# Element settings
elements = ["Fire", "Water", "Earth", "Wind"]
element_colors = {"Fire": RED, "Water": BLUE, "Earth": GREEN, "Wind": GRAY}
element_items = []  # List of elements on the map
element_ammo = {"Fire": 10, "Water": 10, "Earth": 10, "Wind": 10}  # Ammo limits for each ability

# Enemy settings
enemy_size = 30  # Smaller enemy size
enemies = [{"x": random.randint(0, WIDTH - enemy_size), "y": random.randint(50, 300), "health": 100, "speed": 2} for _ in range(3)]
enemy_projectiles = []
enemy_projectile_speed = 5

# Medkits settings
medkit_size = 25
medkits = [{"x": random.randint(0, WIDTH - medkit_size), "y": random.randint(50, HEIGHT - medkit_size)} for _ in range(2)]

# Wave counter
wave_count = 1

# Player projectiles
player_projectiles = []

# Functions

def draw_health_bar(x, y, health, max_health):
    pygame.draw.rect(screen, DARK_RED, (x, y, 200, 20))  # Background bar
    pygame.draw.rect(screen, RED, (x, y, 200 * (health / max_health), 20))  # Health amount

def create_element():
    return {
        "x": random.randint(0, WIDTH - player_size),
        "y": random.randint(0, HEIGHT - player_size),
        "size": 30,  # Smaller element size
        "type": random.choice(elements)
    }

# Create initial element items
for _ in range(3):
    element_items.append(create_element())

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement with WASD and arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # Get mouse position for aiming
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate direction from player to mouse
    dx = mouse_x - player_x - player_size // 2  # offset by player center
    dy = mouse_y - player_y - player_size // 2  # offset by player center
    angle = math.atan2(dy, dx)  # angle between player and mouse

    # Shooting action
    if keys[pygame.K_f] and player_ammo > 0:  # Check if the F key is pressed and there is ammo
        if player_element:  # Only shoot if the player has an ability
            speed = 10  # You can adjust the speed of the projectile
            player_projectiles.append({
                "x": player_x + player_size // 2,  # Shoot from the center of the player
                "y": player_y + player_size // 2,
                "angle": angle,
                "element": player_element
            })
            player_ammo -= 1  # Decrease ammo after shooting
        if player_ammo == 0:  # If ammo runs out, get a new ability
            player_element = None  # Reset current ability
            player_ammo = 0  # Reset ammo count
    
    # Move and Draw Player Projectiles
    for projectile in player_projectiles[:]:
        projectile["x"] += math.cos(projectile["angle"]) * speed
        projectile["y"] += math.sin(projectile["angle"]) * speed
        
        # Remove projectiles if they go off-screen
        if not (0 <= projectile["x"] <= WIDTH and 0 <= projectile["y"] <= HEIGHT):
            player_projectiles.remove(projectile)
        
        # Draw the projectile based on its element
        if projectile["element"] == "Fire":
            pygame.draw.circle(screen, RED, (int(projectile["x"]), int(projectile["y"])), 5)
        elif projectile["element"] == "Water":
            pygame.draw.circle(screen, BLUE, (int(projectile["x"]), int(projectile["y"])), 5)
        elif projectile["element"] == "Earth":
            pygame.draw.circle(screen, GREEN, (int(projectile["x"]), int(projectile["y"])), 7)
        elif projectile["element"] == "Wind":
            pygame.draw.circle(screen, GRAY, (int(projectile["x"]), int(projectile["y"])), 5)
    
    # Move enemies and make them shoot
    for enemy in enemies:
        if enemy["x"] < player_x:
            enemy["x"] += enemy["speed"]
        elif enemy["x"] > player_x:
            enemy["x"] -= enemy["speed"]
        if enemy["y"] < player_y:
            enemy["y"] += enemy["speed"]
        elif enemy["y"] > player_y:
            enemy["y"] -= enemy["speed"]
        
        if random.randint(0, 100) < 2:  # Enemy shoots occasionally
            enemy_projectiles.append({"x": enemy["x"] + enemy_size // 2, "y": enemy["y"], "type": "Dark Magic"})
    
    # Move enemy projectiles
    for e_projectile in enemy_projectiles[:]:
        e_projectile["y"] += enemy_projectile_speed
        if e_projectile["y"] > HEIGHT:
            enemy_projectiles.remove(e_projectile)
        elif (player_x < e_projectile["x"] < player_x + player_size and
              player_y < e_projectile["y"] < player_y + player_size):
            player_health -= 10
            enemy_projectiles.remove(e_projectile)
            if player_health <= 0:
                running = False
    
    # Check for player collecting elements
    for element in element_items[:]:
        if (player_x < element["x"] + element["size"] and
            player_x + player_size > element["x"] and
            player_y < element["y"] + element["size"] and
            player_y + player_size > element["y"]):
            player_element = element["type"]  # Replace existing ability
            player_ammo = element_ammo[player_element]  # Set new ammo based on the element
            element_items.remove(element)
    
    # Check for player collecting medkits
    for medkit in medkits[:]:
        if (player_x < medkit["x"] + medkit_size and
            player_x + player_size > medkit["x"] and
            player_y < medkit["y"] + medkit_size and
            player_y + player_size > medkit["y"]):
            player_health = min(max_health, player_health + 20)  # Heal player
            medkits.remove(medkit)
    
    # **Fix here**: Check if player's projectiles hit enemies
    for projectile in player_projectiles[:]:
        for enemy in enemies[:]:
            if (enemy["x"] < projectile["x"] < enemy["x"] + enemy_size and
                enemy["y"] < projectile["y"] < enemy["y"] + enemy_size):
                enemy["health"] -= 25  # Deal damage to enemy
                player_projectiles.remove(projectile)  # Remove projectile after hit
                if enemy["health"] <= 0:
                    enemies.remove(enemy)  # Remove dead enemy
    
    # Draw player
    pygame.draw.rect(screen, ORANGE, (player_x, player_y, player_size, player_size))
    
    # Draw health bar
    draw_health_bar(20, 20, player_health, max_health)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, (enemy["x"], enemy["y"], enemy_size, enemy_size))
    
    # Draw enemy projectiles
    for e_projectile in enemy_projectiles:
        pygame.draw.circle(screen, PURPLE, (e_projectile["x"], e_projectile["y"]), 10)
    
    # Draw elements (abilities)
    for element in element_items:
        pygame.draw.rect(screen, element_colors[element["type"]], (element["x"], element["y"], element["size"], element["size"]))
    
    # Draw medkits
    for medkit in medkits:
        pygame.draw.rect(screen, PINK, (medkit["x"], medkit["y"], medkit_size, medkit_size))

    # Draw wave counter
    font = pygame.font.Font(None, 36)
    wave_text = font.render(f"Wave: {wave_count}", True, BLACK)
    screen.blit(wave_text, (WIDTH - 150, 20))

    # Check if all enemies are dead to trigger the next wave
    if len(enemies) == 0:  # Check if no enemies remain
        wave_count += 1
        # Add new enemies for the next wave
        enemies = [{"x": random.randint(0, WIDTH - enemy_size), "y": random.randint(50, 300), "health": 100, "speed": 2} for _ in range(wave_count * 3)]
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
