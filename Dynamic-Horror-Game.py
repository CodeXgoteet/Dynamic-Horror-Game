import pygame
import sys
import random
import heapq
import math

# Define states for the enemy
class EnemyState:
    IDLE = "Idle"
    APPROACHING = "Approaching"
    CHASING = "Chasing"

# Initialize Pygame
pygame.init()

# Create game window (800x600)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dynamic Horror Experience")

# Initialize fear level, darkness, and noise
fear_level = 0
darkness = 0
noise = 0

# Create player and enemy rectangles
player = pygame.Rect(50, 50, 50, 50)
enemy = pygame.Rect(400, 300, 50, 50)

# Create empty list for environmental objects
environment = []
environment_changes = []

# Set up game clock
clock = pygame.time.Clock()

# Initialize enemy state
enemy_state = EnemyState.IDLE

# Define the grid
grid = [[0 for _ in range(800)] for _ in range(600)]

# Define the cost function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
# Define the directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Define the A* algorithm
def a_star_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for direction in directions:
            next = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= next[0] < 800 and 0 <= next[1] < 600:
                new_cost = cost_so_far[current] + grid[next[1]][next[0]]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

    return came_from, cost_so_far

# Function to reconstruct the path from the A* search
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()  # Reverse the path to get it from start to goal
    return path

# Function to move the enemy towards the player using A*
def move_enemy_towards_player():
    start = (enemy.x, enemy.y)
    goal = (player.x, player.y)
    came_from, _ = a_star_search(start, goal)

    # Reconstruct the path from the enemy to the player
    path = reconstruct_path(came_from, start, goal)

    # Move the enemy along the path
    if path:
        next_step = path[0]
        dx, dy = next_step[0] - enemy.x, next_step[1] - enemy.y

        # Update the enemy's position
        enemy.x += dx*5
        enemy.y += dy*5
        
# Function to make the enemy chase the player
def chase_player():
    move_enemy_towards_player()

# Function to clear the screen
def clear_screen():
    screen.fill((0, 0, 0))  # Black background

# Function to check if it's night time
def is_night_time():
    return pygame.time.get_ticks() % 24000 < 12000

# Function to draw the background
def draw_background():
    # Placeholder: Draw a moon and stars during night time
    if is_night_time():
        pygame.draw.circle(screen, (255, 255, 255), (750, 50), 30)
        pygame.draw.circle(screen, (255, 255, 255), (700, 100), 20)
        pygame.draw.circle(screen, (255, 255, 255), (600, 80), 25)

# Function to draw the player and enemy
def draw_player_and_enemy():
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 0, 255), enemy)

# Function to draw environmental objects
def draw_environment_objects():
    for obj_type, obj_x, obj_y in environment:
        draw_object(obj_type, obj_x, obj_y)

# Function to draw a specific environmental object
def draw_object(obj_type, obj_x, obj_y):
    if obj_type == "tree":
        pygame.draw.rect(screen, (34, 139, 34), pygame.Rect(obj_x, obj_y, 30, 50))
    elif obj_type == "rock":
        pygame.draw.circle(screen, (128, 128, 128), (obj_x + 15, obj_y + 25), 15)
    elif obj_type == "fence":
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(obj_x, obj_y, 10, 50))

# Initialize fear_level
fear_level = 0

# Function to update fear level based on darkness and noise
def update_fear_level(darkness, noise):
    global fear_level
    fear_level += darkness + noise

def generate_environment_if_needed():
    global fear_level
    if fear_level > 100:
        generate_environment()
        fear_level -= 100

# Function to increase darkness during night time
def increase_darkness():
    global darkness
    darkness += 1

# Function to increase noise when player is near the enemy
def increase_noise():
    global noise
    noise += 10

# Function to generate environmental objects
def generate_environment():
    global environment, environment_changes
    object_type = random.choice(["tree", "rock", "fence"])
    object_x = random.randint(0, 800)
    object_y = random.randint(0, 600)
    environment.append((object_type, object_x, object_y))

    # Store the change to revert later
    environment_changes.append((object_type, object_x, object_y, pygame.time.get_ticks() + 5000))

# Function to revert environmental changes
def revert_environment_change():
    global environment, environment_changes
    if environment_changes:
        object_type, object_x, object_y, change_time = environment_changes[0]
        if pygame.time.get_ticks() > change_time:
            environment_changes.pop(0)
            # Remove the last added object
            environment.pop()

# Function to update the enemy AI
def update_enemy_ai():
    global enemy_state

    if player_is_near_enemy():
        enemy_state = EnemyState.CHASING
    else:
        enemy_state = EnemyState.IDLE

    if enemy_state == EnemyState.CHASING:
        chase_player()

# Function to check if the player is near the enemy
def player_is_near_enemy():
    return abs(player.x - enemy.x) < 1000 and abs(player.y - enemy.y) < 1000

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5

    update_fear_level(darkness, noise)
    generate_environment_if_needed()
    revert_environment_change()

    if is_night_time():
        increase_darkness()

    if player_is_near_enemy():
        increase_noise()

    update_enemy_ai()

    # Check for collision between player and enemy
    if player.colliderect(enemy):
        pygame.quit()
        sys.exit()

    clear_screen()
    draw_background()
    draw_player_and_enemy()
    draw_environment_objects()

    pygame.display.flip()

    clock.tick(30)  # Cap the frame rate to 30 FPS