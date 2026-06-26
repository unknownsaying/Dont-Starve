import pygame
import random
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)

class TimeOfDay(Enum):
    DAY = 1
    DUSK = 2
    NIGHT = 3

class Resource:
    def __init__(self, x, y, resource_type):
        self.x = x
        self.y = y
        self.type = resource_type
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.amount = random.randint(3, 8)
        
        # Set color based on resource type
        if resource_type == "wood":
            self.color = BROWN
        elif resource_type == "stone":
            self.color = GRAY
        elif resource_type == "berries":
            self.color = RED
        elif resource_type == "carrots":
            self.color = ORANGE
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw resource icon
        font = pygame.font.Font(None, 20)
        text = font.render(self.type[0].upper(), True, WHITE)
        screen.blit(text, (self.x + 12, self.y + 8))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 4
        
        # Survival stats
        self.health = 100
        self.max_health = 100
        self.hunger = 100
        self.max_hunger = 100
        self.sanity = 100
        self.max_sanity = 100
        
        # Inventory
        self.inventory = {
            "wood": 0,
            "stone": 0,
            "berries": 0,
            "carrots": 0,
            "axe": 0,
            "pickaxe": 0,
            "campfire": 0
        }
        
        self.selected_item = "wood"
        self.crafting_menu_open = False
    
    def move(self, dx, dy, obstacles):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Keep player in screen bounds
        if 0 <= new_x <= SCREEN_WIDTH - self.width:
            # Simple collision check with obstacles
            temp_rect = pygame.Rect(new_x, self.y, self.width, self.height)
            collision = False
            for obstacle in obstacles:
                if temp_rect.colliderect(obstacle.rect):
                    collision = True
                    break
            if not collision:
                self.x = new_x
        
        if 0 <= new_y <= SCREEN_HEIGHT - self.height:
            temp_rect = pygame.Rect(self.x, new_y, self.width, self.height)
            collision = False
            for obstacle in obstacles:
                if temp_rect.colliderect(obstacle.rect):
                    collision = True
                    break
            if not collision:
                self.y = new_y
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    def gather_resource(self, resource):
        if resource.type in self.inventory:
            self.inventory[resource.type] += 1
            resource.amount -= 1
            return resource.amount <= 0
        return False
    
    def craft(self, item):
        recipes = {
            "axe": {"wood": 2, "stone": 1},
            "pickaxe": {"wood": 2, "stone": 2},
            "campfire": {"wood": 3, "stone": 1}
        }
        
        if item in recipes:
            recipe = recipes[item]
            can_craft = True
            for material, amount in recipe.items():
                if self.inventory[material] < amount:
                    can_craft = False
                    break
            
            if can_craft:
                for material, amount in recipe.items():
                    self.inventory[material] -= amount
                self.inventory[item] += 1
                return True
        return False
    
    def eat(self, food_type):
        food_values = {
            "berries": 10,
            "carrots": 15
        }
        
        if food_type in food_values and self.inventory[food_type] > 0:
            self.inventory[food_type] -= 1
            self.hunger = min(self.max_hunger, self.hunger + food_values[food_type])
            self.health = min(self.max_health, self.health + 5)
            return True
        return False
    
    def update(self, time_of_day):
        # Decrease hunger over time
        self.hunger = max(0, self.hunger - 0.05)
        
        # Decrease sanity at night
        if time_of_day == TimeOfDay.NIGHT:
            self.sanity = max(0, self.sanity - 0.1)
        else:
            self.sanity = min(self.max_sanity, self.sanity + 0.05)
        
        # Health decreases if hunger is 0
        if self.hunger <= 0:
            self.health = max(0, self.health - 0.2)
        
        # Health decreases if sanity is very low
        if self.sanity < 20:
            self.health = max(0, self.health - 0.1)
        
        # Health regenerates slowly if well fed and sane
        if self.hunger > 80 and self.sanity > 50:
            self.health = min(self.max_health, self.health + 0.02)
    
    def draw(self, screen):
        # Draw player character
        pygame.draw.rect(screen, LIGHT_BLUE, self.rect)
        pygame.draw.circle(screen, YELLOW, (self.x + 15, self.y + 10), 8)  # Head
        
        # Draw health bar
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - 5, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.y - 10, bar_width * health_ratio, bar_height))
        
        # Draw hunger bar
        hunger_ratio = self.hunger / self.max_hunger
        pygame.draw.rect(screen, GRAY, (self.x - 5, self.y - 5, bar_width, bar_height))
        pygame.draw.rect(screen, ORANGE, (self.x - 5, self.y - 5, bar_width * hunger_ratio, bar_height))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 1.5
        self.health = 30
        self.max_health = 30
        self.attack_cooldown = 0
        self.attack_damage = 10
    
    def move_toward_player(self, player, obstacles):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
            # Check collisions
            new_x = self.x + dx
            new_y = self.y + dy
            
            temp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            temp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            
            collision_x = False
            collision_y = False
            
            for obstacle in obstacles:
                if temp_rect_x.colliderect(obstacle.rect):
                    collision_x = True
                if temp_rect_y.colliderect(obstacle.rect):
                    collision_y = True
            
            if not collision_x:
                self.x = new_x
            if not collision_y:
                self.y = new_y
            
            self.rect.x = self.x
            self.rect.y = self.y
    
    def attack_player(self, player):
        if self.attack_cooldown <= 0:
            player.health -= self.attack_damage
            self.attack_cooldown = 60  # Attack once per second (at 60 FPS)
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def draw(self, screen):
        pygame.draw.rect(screen, PURPLE, self.rect)
        pygame.draw.circle(screen, RED, (self.x + 15, self.y + 15), 10)
        
        # Draw health bar
        bar_width = 30
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, bar_width * health_ratio, bar_height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Don't Starve Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.resources = []
        self.enemies = []
        self.obstacles = []
        
        # Time system
        self.time_of_day = TimeOfDay.DAY
        self.day_timer = 0
        self.day_duration = 600  # 10 seconds for each phase
        
        # Game state
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
        # Generate world
        self.generate_world()
    
    def generate_world(self):
        # Generate trees (wood)
        for _ in range(10):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.resources.append(Resource(x, y, "wood"))
        
        # Generate rocks (stone)
        for _ in range(8):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.resources.append(Resource(x, y, "stone"))
        
        # Generate berry bushes
        for _ in range(6):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.resources.append(Resource(x, y, "berries"))
        
        # Generate carrots
        for _ in range(5):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.resources.append(Resource(x, y, "carrots"))
        
        # Generate enemies
        for _ in range(2):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            self.enemies.append(Enemy(x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Crafting menu
                if event.key == pygame.K_c:
                    self.player.crafting_menu_open = not self.player.crafting_menu_open
                
                # Craft items
                if self.player.crafting_menu_open:
                    if event.key == pygame.K_1:
                        self.player.craft("axe")
                    elif event.key == pygame.K_2:
                        self.player.craft("pickaxe")
                    elif event.key == pygame.K_3:
                        self.player.craft("campfire")
                
                # Eating
                if event.key == pygame.K_e:
                    self.player.eat("berries")
                elif event.key == pygame.K_f:
                    self.player.eat("carrots")
                
                # Gathering resources
                if event.key == pygame.K_SPACE:
                    player_center = pygame.Rect(
                        self.player.x + self.player.width//2 - 20,
                        self.player.y + self.player.height//2 - 20,
                        40, 40
                    )
                    
                    for resource in self.resources[:]:
                        if player_center.colliderect(resource.rect):
                            if self.player.gather_resource(resource):
                                self.resources.remove(resource)
                            break
                
                # Attack enemies
                if event.key == pygame.K_a:
                    player_center = pygame.Rect(
                        self.player.x + self.player.width//2 - 25,
                        self.player.y + self.player.height//2 - 25,
                        50, 50
                    )
                    
                    for enemy in self.enemies[:]:
                        if player_center.colliderect(enemy.rect):
                            enemy.health -= 25
                            if enemy.health <= 0:
                                self.enemies.remove(enemy)
                            break
                
                # Restart game
                if self.game_over and event.key == pygame.K_r:
                    self.__init__()
    
    def update(self):
        if self.game_over:
            return
        
        # Player movement
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] + keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] + keys[pygame.K_s] - keys[pygame.K_w]
        
        self.player.move(dx, dy, self.obstacles)
        
        # Update time of day
        self.day_timer += 1
        if self.day_timer < self.day_duration:
            self.time_of_day = TimeOfDay.DAY
        elif self.day_timer < self.day_duration * 2:
            self.time_of_day = TimeOfDay.DUSK
        elif self.day_timer < self.day_duration * 3:
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.day_timer = 0
        
        # Update player
        self.player.update(self.time_of_day)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update()
            enemy.move_toward_player(self.player, self.obstacles)
            
            # Check if enemy is touching player
            if enemy.rect.colliderect(self.player.rect):
                enemy.attack_player(self.player)
        
        # Check game over
        if self.player.health <= 0:
            self.game_over = True
    
    def draw_background(self):
        # Draw ground
        self.screen.fill(GREEN)
        
        # Draw some grass details
        for i in range(0, SCREEN_WIDTH, 50):
            for j in range(0, SCREEN_HEIGHT, 50):
                if random.random() < 0.1:
                    pygame.draw.line(self.screen, (0, 100, 0), 
                                   (i, j), (i + 10, j - 10), 2)
    
    def draw_ui(self):
        # Draw inventory
        y_offset = 10
        x_offset = 10
        for item, amount in self.player.inventory.items():
            text = self.font.render(f"{item}: {amount}", True, WHITE)
            self.screen.blit(text, (x_offset, y_offset))
            y_offset += 25
        
        # Draw stats
        stats_x = SCREEN_WIDTH - 200
        health_text = self.font.render(f"Health: {int(self.player.health)}", True, RED)
        hunger_text = self.font.render(f"Hunger: {int(self.player.hunger)}", True, ORANGE)
        sanity_text = self.font.render(f"Sanity: {int(self.player.sanity)}", True, BLUE)
        
        self.screen.blit(health_text, (stats_x, 10))
        self.screen.blit(hunger_text, (stats_x, 35))
        self.screen.blit(sanity_text, (stats_x, 60))
        
        # Draw time of day
        time_colors = {
            TimeOfDay.DAY: YELLOW,
            TimeOfDay.DUSK: ORANGE,
            TimeOfDay.NIGHT: BLUE
        }
        time_text = self.font.render(f"Time: {self.time_of_day.name}", True, time_colors[self.time_of_day])
        self.screen.blit(time_text, (SCREEN_WIDTH//2 - 50, 10))
        
        # Draw crafting menu if open
        if self.player.crafting_menu_open:
            menu_x = SCREEN_WIDTH//2 - 100
            menu_y = SCREEN_HEIGHT//2 - 50
            pygame.draw.rect(self.screen, GRAY, (menu_x, menu_y, 200, 100))
            pygame.draw.rect(self.screen, BLACK, (menu_x, menu_y, 200, 100), 2)
            
            recipes = [
                "1: Axe (2 wood, 1 stone)",
                "2: Pickaxe (2 wood, 2 stone)",
                "3: Campfire (3 wood, 1 stone)"
            ]
            
            y = menu_y + 10
            for recipe in recipes:
                text = self.font.render(recipe, True, BLACK)
                self.screen.blit(text, (menu_x + 10, y))
                y += 25
        
        # Draw controls help
        help_text = [
            "WASD/Arrows: Move",
            "Space: Gather",
            "A: Attack",
            "E: Eat berries",
            "F: Eat carrots",
            "C: Crafting menu"
        ]
        
        help_x = 10
        help_y = SCREEN_HEIGHT - 150
        for text in help_text:
            help_render = pygame.font.Font(None, 20).render(text, True, WHITE)
            self.screen.blit(help_render, (help_x, help_y))
            help_y += 20
    
    def draw(self):
        self.draw_background()
        
        # Draw resources
        for resource in self.resources:
            resource.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 10))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()