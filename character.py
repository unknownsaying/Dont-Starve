import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
DARK_PURPLE = (75, 0, 130)

# Game Enums
class TimeOfDay(Enum):
    DAY = "Day"
    DUSK = "Dusk"
    NIGHT = "Night"

class Season(Enum):
    AUTUMN = "Autumn"
    WINTER = "Winter"
    SPRING = "Spring"
    SUMMER = "Summer"

class CharacterClass(Enum):
    WILSON = "Wilson"
    WILLOW = "Willow"
    WOLFGANG = "Wolfgang"
    WENDY = "Wendy"
    WX78 = "WX-78"
    WICKERBOTTOM = "Wickerbottom"
    WOODIE = "Woodie"
    WES = "Wes"
    MAXWELL = "Maxwell"
    WIGFRID = "Wigfrid"
    WEBBER = "Webber"
    WINONA = "Winona"
    WARLY = "Warly"
    WORMWOOD = "Wormwood"
    WURT = "Wurt"

class ResourceType(Enum):
    WOOD = "Wood"
    STONE = "Stone"
    FLINT = "Flint"
    GOLD = "Gold"
    BERRIES = "Berries"
    CARROTS = "Carrots"
    GRASS = "Grass"
    TWIGS = "Twigs"
    SILK = "Silk"
    MEAT = "Meat"
    MONSTER_MEAT = "Monster Meat"
    COOKED_MEAT = "Cooked Meat"
    HONEY = "Honey"
    BUTTERFLY_WINGS = "Butterfly Wings"
    PETALS = "Petals"
    LOG = "Log"
    ROCK = "Rock"
    GOLD_NUGGET = "Gold Nugget"
    NIGHTMARE_FUEL = "Nightmare Fuel"
    LIVING_LOG = "Living Log"
    GEARS = "Gears"

class StructureType(Enum):
    CAMPFIRE = "Campfire"
    FIRE_PIT = "Fire Pit"
    SCIENCE_MACHINE = "Science Machine"
    ALCHEMY_ENGINE = "Alchemy Engine"
    CHEST = "Chest"
    CROCK_POT = "Crock Pot"
    ICE_BOX = "Ice Box"
    TENT = "Tent"
    LIGHTNING_ROD = "Lightning Rod"
    BIRD_CAGE = "Bird Cage"

class ToolType(Enum):
    AXE = "Axe"
    PICKAXE = "Pickaxe"
    SHOVEL = "Shovel"
    HAMMER = "Hammer"
    FISHING_ROD = "Fishing Rod"
    BUG_NET = "Bug Net"
    RAZOR = "Razor"

class WeaponType(Enum):
    SPEAR = "Spear"
    TENTACLE_SPIKE = "Tentacle Spike"
    HAMBAT = "Ham Bat"
    DARK_SWORD = "Dark Sword"
    BATTLE_SPEAR = "Battle Spear"

@dataclass
class CharacterStats:
    health: int
    max_health: int
    hunger: int
    max_hunger: int
    sanity: int
    max_sanity: int
    damage_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    hunger_rate: float = 1.0
    sanity_rate: float = 1.0

class Character:
    def __init__(self, name: CharacterClass):
        self.name = name
        self.stats = self.get_base_stats()
        self.perks = []
        self.drawbacks = []
        self.special_items = []
        self.character_quote = ""
        self.setup_character()
    
    def get_base_stats(self) -> CharacterStats:
        base_stats = {
            CharacterClass.WILSON: CharacterStats(150, 150, 150, 150, 200, 200),
            CharacterClass.WILLOW: CharacterStats(150, 150, 150, 150, 120, 120),
            CharacterClass.WOLFGANG: CharacterStats(200, 300, 200, 300, 200, 200),
            CharacterClass.WENDY: CharacterStats(150, 150, 150, 150, 200, 200),
            CharacterClass.WX78: CharacterStats(100, 400, 100, 200, 100, 300),
            CharacterClass.WICKERBOTTOM: CharacterStats(150, 150, 150, 250, 250, 250),
            CharacterClass.WOODIE: CharacterStats(150, 150, 150, 150, 200, 200),
            CharacterClass.WES: CharacterStats(75, 75, 75, 75, 75, 75),
            CharacterClass.MAXWELL: CharacterStats(75, 75, 150, 150, 200, 200),
            CharacterClass.WIGFRID: CharacterStats(200, 200, 120, 120, 120, 120),
            CharacterClass.WEBBER: CharacterStats(175, 175, 175, 175, 100, 100),
            CharacterClass.WINONA: CharacterStats(150, 150, 150, 150, 200, 200),
            CharacterClass.WARLY: CharacterStats(150, 150, 250, 250, 200, 200),
            CharacterClass.WORMWOOD: CharacterStats(150, 150, 150, 150, 200, 200),
            CharacterClass.WURT: CharacterStats(150, 250, 150, 200, 200, 200),
        }
        return base_stats.get(self.name, CharacterStats(150, 150, 150, 150, 200, 200))
    
    def setup_character(self):
        character_configs = {
            CharacterClass.WILSON: {
                "perks": ["Grows a magnificent beard", "Balanced stats"],
                "drawbacks": ["No special abilities"],
                "quote": "I will conquer it all with the power of my MIND!",
                "special_items": []
            },
            CharacterClass.WILLOW: {
                "perks": ["Immune to fire damage", "Gains sanity from fire", "Has a lighter"],
                "drawbacks": ["Loses sanity when cold", "Freezing deals extra damage"],
                "quote": "All will bathe in the prettiest of flames.",
                "special_items": ["Lighter"]
            },
            CharacterClass.WOLFGANG: {
                "perks": ["Damage multiplies with fullness", "Speed increases with fullness"],
                "drawbacks": ["Loses sanity faster when hungry", "Hunger drains faster"],
                "quote": "I am mighty! Nobody will fight me!",
                "special_items": []
            },
            CharacterClass.WENDY: {
                "perks": ["Summons ghost sister Abigail", "Less sanity drain from darkness"],
                "drawbacks": ["Deals less damage", "Abigail can be dangerous"],
                "quote": "Abigail? Come back! I'm not done playing with you.",
                "special_items": ["Abigail's Flower"]
            },
            CharacterClass.WX78: {
                "perks": ["Can upgrade with gears", "Gains health from eating gears"],
                "drawbacks": ["Takes damage in rain", "Low starting stats"],
                "quote": "EMPATHY MODULE NOT RESPONDING",
                "special_items": []
            },
            CharacterClass.WICKERBOTTOM: {
                "perks": ["Knows many recipes", "Can craft books", "Has high sanity"],
                "drawbacks": ["Can't sleep", "Spoiled food hurts more"],
                "quote": "Everything can be found in a book.",
                "special_items": ["Books"]
            },
            CharacterClass.WOODIE: {
                "perks": ["Has an axe named Lucy", "Can transform into werebeaver"],
                "drawbacks": ["Random transformations", "Beaver form has drawbacks"],
                "quote": "That's a nice lookin' tree, eh?",
                "special_items": ["Lucy the Axe"]
            },
            CharacterClass.WES: {
                "perks": ["Balloonomancy"],
                "drawbacks": ["Can't talk", "Lowest stats overall", "Hunger drains faster"],
                "quote": "...",
                "special_items": ["Balloons"]
            },
            CharacterClass.MAXWELL: {
                "perks": ["Starts with dark sword and armor", "High sanity regen"],
                "drawbacks": ["Low maximum health", "Summons shadow puppets drain sanity"],
                "quote": "Freedom! At last!",
                "special_items": ["Codex Umbra"]
            },
            CharacterClass.WIGFRID: {
                "perks": ["Absorbs health and sanity from enemies", "High damage"],
                "drawbacks": ["Can only eat meat", "Low starting hunger"],
                "quote": "Valhalla awaits!",
                "special_items": ["Battle Spear", "Battle Helm"]
            },
            CharacterClass.WEBBER: {
                "perks": ["Can befriend spiders", "Can eat monster meat safely"],
                "drawbacks": ["Pigs and bunnymen attack on sight", "Low sanity"],
                "quote": "We can go anywhere we want!",
                "special_items": ["Spider Eggs"]
            },
            CharacterClass.WINONA: {
                "perks": ["Crafts faster", "Can repair structures"],
                "drawbacks": ["Hunger drains faster when crafting", "No special combat abilities"],
                "quote": "A broken clock is right at least twice a day!",
                "special_items": ["Trusty Tape"]
            },
            CharacterClass.WARLY: {
                "perks": ["Has unique recipes", "Portable crock pot"],
                "drawbacks": ["Gets less hunger from raw food", "Hunger drains faster"],
                "quote": "Nothing worthwhile is ever accomplished quickly.",
                "special_items": ["Portable Crock Pot", "Chef Pouch"]
            },
            CharacterClass.WORMWOOD: {
                "perks": ["Can plant seeds without farms", "Heals from planting"],
                "drawbacks": ["Can't heal from food", "Fire damage increased"],
                "quote": "Hello friend!",
                "special_items": []
            },
            CharacterClass.WURT: {
                "perks": ["Can craft merm structures", "Can breathe underwater"],
                "drawbacks": ["Can't trade with pigs", "Vegetarian"],
                "quote": "Glub glub! Mermfolk best folk!",
                "special_items": ["Merm Structures"]
            }
        }
        
        config = character_configs[self.name]
        self.perks = config["perks"]
        self.drawbacks = config["drawbacks"]
        self.character_quote = config["quote"]
        self.special_items = config["special_items"]

class Item:
    def __init__(self, name: str, item_type: str, durability: int = -1):
        self.name = name
        self.type = item_type
        self.durability = durability
        self.max_durability = durability
        self.stack_size = 1
    
    def use(self) -> bool:
        if self.durability > 0:
            self.durability -= 1
            return True
        return False
    
    def is_broken(self) -> bool:
        return self.durability == 0

class Inventory:
    def __init__(self, max_slots: int = 15):
        self.max_slots = max_slots
        self.items: Dict[str, int] = {}
        self.equipment: Dict[str, Optional[Item]] = {
            "weapon": None,
            "tool": None,
            "head": None,
            "body": None,
        }
    
    def add_item(self, item_name: str, amount: int = 1) -> bool:
        if len(self.items) >= self.max_slots and item_name not in self.items:
            return False
        
        if item_name in self.items:
            self.items[item_name] += amount
        else:
            self.items[item_name] = amount
        return True
    
    def remove_item(self, item_name: str, amount: int = 1) -> bool:
        if item_name in self.items and self.items[item_name] >= amount:
            self.items[item_name] -= amount
            if self.items[item_name] <= 0:
                del self.items[item_name]
            return True
        return False
    
    def has_item(self, item_name: str, amount: int = 1) -> bool:
        return item_name in self.items and self.items[item_name] >= amount
    
    def get_item_count(self, item_name: str) -> int:
        return self.items.get(item_name, 0)

class CraftingRecipe:
    def __init__(self, name: str, ingredients: Dict[str, int], category: str, station_required: str = "None"):
        self.name = name
        self.ingredients = ingredients
        self.category = category
        self.station_required = station_required

class CraftingSystem:
    def __init__(self):
        self.recipes: Dict[str, CraftingRecipe] = {}
        self.setup_recipes()
    
    def setup_recipes(self):
        # Basic tools
        self.add_recipe("Axe", {"Twigs": 1, "Flint": 1}, "Tools")
        self.add_recipe("Pickaxe", {"Twigs": 2, "Flint": 2}, "Tools")
        self.add_recipe("Shovel", {"Twigs": 2, "Flint": 2}, "Tools")
        
        # Weapons
        self.add_recipe("Spear", {"Twigs": 2, "Flint": 2}, "Weapons")
        self.add_recipe("Ham Bat", {"Meat": 2, "Twigs": 2}, "Weapons")
        
        # Light
        self.add_recipe("Torch", {"Twigs": 2, "Grass": 2}, "Light")
        self.add_recipe("Campfire", {"Log": 2, "Grass": 3}, "Light")
        self.add_recipe("Fire Pit", {"Log": 4, "Rock": 8}, "Structures")
        
        # Structures
        self.add_recipe("Science Machine", {"Gold": 1, "Log": 4, "Rock": 4}, "Structures")
        self.add_recipe("Chest", {"Log": 3}, "Structures")
        self.add_recipe("Crock Pot", {"Rock": 3, "Twigs": 3}, "Structures")
        
        # Survival
        self.add_recipe("Trap", {"Twigs": 2, "Grass": 6}, "Survival")
        self.add_recipe("Bird Cage", {"Rock": 4, "Gold": 2}, "Structures", "Science Machine")
        
        # Character specific
        self.add_recipe("Battle Spear", {"Twigs": 2, "Flint": 2, "Gold": 2}, "Weapons")
        self.add_recipe("Battle Helm", {"Rock": 2, "Gold": 2}, "Armor")
        self.add_recipe("Lucy the Axe", {"Log": 3, "Flint": 1}, "Tools")
        self.add_recipe("Codex Umbra", {"Nightmare Fuel": 5}, "Magic", "Science Machine")
        self.add_recipe("Portable Crock Pot", {"Rock": 3, "Twigs": 6}, "Structures")
        
        # Food
        self.add_recipe("Meatballs", {"Meat": 1, "Berries": 3}, "Food", "Crock Pot")
        self.add_recipe("Meaty Stew", {"Meat": 3, "Monster Meat": 1}, "Food", "Crock Pot")
        self.add_recipe("Honey Ham", {"Meat": 2, "Honey": 2}, "Food", "Crock Pot")
    
    def add_recipe(self, name: str, ingredients: Dict[str, int], category: str, station: str = "None"):
        self.recipes[name] = CraftingRecipe(name, ingredients, category, station)
    
    def can_craft(self, recipe_name: str, inventory: Inventory, station: str = "None") -> bool:
        if recipe_name not in self.recipes:
            return False
        
        recipe = self.recipes[recipe_name]
        if station != "All" and recipe.station_required != station and recipe.station_required != "None":
            return False
        
        for item, amount in recipe.ingredients.items():
            if not inventory.has_item(item, amount):
                return False
        
        return True
    
    def craft(self, recipe_name: str, inventory: Inventory) -> bool:
        if not self.can_craft(recipe_name, inventory):
            return False
        
        recipe = self.recipes[recipe_name]
        for item, amount in recipe.ingredients.items():
            inventory.remove_item(item, amount)
        
        inventory.add_item(recipe_name)
        return True

class Resource:
    def __init__(self, x: float, y: float, resource_type: str, amount: int = 5):
        self.x = x
        self.y = y
        self.type = resource_type
        self.amount = amount
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.color = self.get_resource_color()
        self.regrow_timer = 0
        self.can_regrow = resource_type in ["Berries", "Grass", "Twigs", "Carrots"]
    
    def get_resource_color(self) -> Tuple[int, int, int]:
        color_map = {
            "Tree": BROWN,
            "Boulder": GRAY,
            "Flint": DARK_GRAY,
            "Gold Nugget": GOLD,
            "Berries": RED,
            "Carrots": ORANGE,
            "Grass": GREEN,
            "Twigs": BROWN,
            "Flower": PINK,
            "Butterfly": YELLOW,
            "Beehive": GOLD,
            "Spider Den": BLACK,
        }
        return color_map.get(self.type, WHITE)
    
    def gather(self, tool_multiplier: float = 1.0) -> List[Tuple[str, int]]:
        loot = []
        gather_amount = int(self.amount * tool_multiplier)
        
        loot_map = {
            "Tree": [("Log", gather_amount), ("Twigs", gather_amount // 2)],
            "Boulder": [("Rock", gather_amount), ("Flint", gather_amount // 2)],
            "Flint": [("Flint", gather_amount)],
            "Gold Nugget": [("Gold", gather_amount)],
            "Berries": [("Berries", gather_amount)],
            "Carrots": [("Carrots", gather_amount)],
            "Grass": [("Grass", gather_amount)],
            "Twigs": [("Twigs", gather_amount)],
            "Flower": [("Petals", 1)],
            "Butterfly": [("Butterfly Wings", 1)],
            "Beehive": [("Honey", 3)],
            "Spider Den": [("Silk", 3), ("Monster Meat", 2)],
        }
        
        loot = loot_map.get(self.type, [])
        self.amount = max(0, self.amount - 1)
        
        if self.amount <= 0 and self.can_regrow:
            self.regrow_timer = random.randint(300, 600)  # 5-10 seconds
        
        return loot
    
    def update(self):
        if self.regrow_timer > 0:
            self.regrow_timer -= 1
            if self.regrow_timer <= 0:
                self.amount = random.randint(3, 8)
    
    def draw(self, screen: pygame.Surface):
        if self.amount > 0:
            pygame.draw.rect(screen, self.color, self.rect)
            font = pygame.font.Font(None, 16)
            text = font.render(self.type[0], True, WHITE)
            screen.blit(text, (self.x + 12, self.y + 8))

class Player:
    def __init__(self, x: float, y: float, character_class: CharacterClass):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        self.character = Character(character_class)
        self.stats = self.character.stats
        self.inventory = Inventory()
        self.crafting = CraftingSystem()
        
        self.speed = 4 * self.stats.speed_multiplier
        self.attack_damage = 25 * self.stats.damage_multiplier
        self.attack_range = 50
        self.attack_cooldown = 0
        
        self.selected_item = 0
        self.crafting_menu_open = False
        self.inventory_menu_open = False
        self.character_select_open = True
        self.map_open = False
        
        self.temperature = 20  # Celsius
        self.wetness = 0
        self.beard_growth = 0
        self.woodie_transformation = False
        self.abigail_active = False
        
        # Give starting items based on character
        self.give_starting_items()
    
    def give_starting_items(self):
        starting_items = {
            CharacterClass.WILLOW: ["Lighter", "Torch"],
            CharacterClass.WENDY: ["Abigail's Flower"],
            CharacterClass.WOODIE: ["Lucy the Axe"],
            CharacterClass.MAXWELL: ["Codex Umbra", "Dark Sword", "Night Armor"],
            CharacterClass.WIGFRID: ["Battle Spear", "Battle Helm", "Meat", "Meat"],
            CharacterClass.WX78: ["Gears"],
            CharacterClass.WARLY: ["Portable Crock Pot", "Chef Pouch"],
        }
        
        items = starting_items.get(self.character.name, [])
        for item in items:
            self.inventory.add_item(item)
    
    def move(self, dx: float, dy: float, obstacles: List[pygame.Rect], resources: List[Resource]):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Screen boundaries
        new_x = max(0, min(new_x, SCREEN_WIDTH - self.width))
        new_y = max(0, min(new_y, SCREEN_HEIGHT - self.height))
        
        # Collision with obstacles
        temp_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # Check resource collisions (can walk through resources)
        for resource in resources:
            if temp_rect.colliderect(resource.rect) and resource.amount > 0:
                # Push player back slightly
                dx = self.x - resource.x
                dy = self.y - resource.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    new_x += dx / distance * 2
                    new_y += dy / distance * 2
                    new_x = max(0, min(new_x, SCREEN_WIDTH - self.width))
                    new_y = max(0, min(new_y, SCREEN_HEIGHT - self.height))
        
        self.x = new_x
        self.y = new_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def update(self, time_of_day: TimeOfDay, season: Season):
        # Update stats
        hunger_drain = 0.03 * self.character.stats.hunger_rate
        sanity_drain = 0.02 * self.character.stats.sanity_rate
        
        # Time of day effects
        if time_of_day == TimeOfDay.NIGHT:
            sanity_drain *= 2
        elif time_of_day == TimeOfDay.DAY:
            sanity_drain *= 0.5
        
        # Season effects
        if season == Season.WINTER:
            self.temperature -= 0.05
            hunger_drain *= 1.3
        elif season == Season.SUMMER:
            self.temperature += 0.05
            self.wetness = max(0, self.wetness - 0.1)
        
        # Character specific effects
        if self.character.name == CharacterClass.WILLOW:
            if self.temperature < 10:
                sanity_drain *= 2
        elif self.character.name == CharacterClass.WOLFGANG:
            hunger_ratio = self.stats.hunger / self.stats.max_hunger
            self.attack_damage = 25 * (0.5 + hunger_ratio)
            self.speed = 4 * (0.8 + hunger_ratio * 0.4)
        elif self.character.name == CharacterClass.WX78:
            if self.wetness > 50:
                self.stats.health -= 0.5
        elif self.character.name == CharacterClass.WOODIE:
            if random.random() < 0.001:  # Random werebeaver transformation
                self.woodie_transformation = not self.woodie_transformation
                if self.woodie_transformation:
                    self.attack_damage *= 2
                    self.speed *= 1.5
                else:
                    self.attack_damage /= 2
                    self.speed /= 1.5
        
        # Apply stat changes
        self.stats.hunger = max(0, min(self.stats.max_hunger, self.stats.hunger - hunger_drain))
        self.stats.sanity = max(0, min(self.stats.max_sanity, self.stats.sanity - sanity_drain))
        
        # Temperature effects
        if self.temperature < 0:
            self.stats.health -= 0.5
        elif self.temperature > 40:
            self.stats.health -= 0.3
        
        # Wetness effects
        if self.wetness > 50:
            self.temperature -= 0.1
        
        # Health regeneration
        if self.stats.hunger > 100 and self.stats.sanity > 150:
            self.stats.health = min(self.stats.max_health, self.stats.health + 0.1)
        
        # Starvation damage
        if self.stats.hunger <= 0:
            self.stats.health -= 0.5
        
        # Insanity damage
        if self.stats.sanity < 30:
            self.stats.health -= 0.2
        
        # Beard growth for Wilson
        if self.character.name == CharacterClass.WILSON and self.beard_growth < 100:
            self.beard_growth += 0.01
        
        # Attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Wickerbottom's sanity bonus
        if self.character.name == CharacterClass.WICKERBOTTOM:
            self.stats.sanity = min(self.stats.max_sanity, self.stats.sanity + 0.05)
    
    def gather(self, resource: Resource) -> List[Tuple[str, int]]:
        tool_multiplier = 1.0
        
        # Check if player has appropriate tool equipped
        if resource.type == "Tree" and self.inventory.equipment["tool"] and self.inventory.equipment["tool"].name == "Axe":
            tool_multiplier = 2.0
        elif resource.type == "Boulder" and self.inventory.equipment["tool"] and self.inventory.equipment["tool"].name == "Pickaxe":
            tool_multiplier = 2.0
        
        # Wigfrid's combat bonus
        if self.character.name == CharacterClass.WIGFRID:
            tool_multiplier *= 1.25
        
        loot = resource.gather(tool_multiplier)
        
        for item_name, amount in loot:
            self.inventory.add_item(item_name, amount)
        
        return loot
    
    def eat(self, food_name: str) -> bool:
        if not self.inventory.has_item(food_name):
            return False
        
        # Check dietary restrictions
        if self.character.name == CharacterClass.WIGFRID and "Meat" not in food_name and "Monster" not in food_name:
            return False
        if self.character.name == CharacterClass.WURT and "Meat" in food_name:
            return False
        
        food_stats = {
            "Berries": (10, 0, 5),
            "Carrots": (15, 5, 0),
            "Meat": (20, 5, -5),
            "Cooked Meat": (30, 10, 0),
            "Monster Meat": (15, -10, -15),
            "Butterfly Wings": (8, 10, 0),
            "Honey": (10, 0, 5),
            "Meatballs": (40, 5, 10),
            "Meaty Stew": (60, 10, 0),
            "Honey Ham": (50, 15, 10),
        }
        
        stats = food_stats.get(food_name, (10, 0, 0))
        
        # Webber can eat monster meat safely
        if self.character.name == CharacterClass.WEBBER and food_name == "Monster Meat":
            stats = (15, 5, 0)
        
        # Warly gets less from raw food
        if self.character.name == CharacterClass.WARLY and "Cooked" not in food_name and "Meatballs" not in food_name:
            stats = (stats[0] * 0.7, stats[1] * 0.7, stats[2] * 0.7)
        
        self.stats.hunger = min(self.stats.max_hunger, self.stats.hunger + stats[0])
        self.stats.health = min(self.stats.max_health, self.stats.health + stats[1])
        self.stats.sanity = min(self.stats.max_sanity, self.stats.sanity + stats[2])
        
        self.inventory.remove_item(food_name)
        return True
    
    def draw(self, screen: pygame.Surface):
        # Draw player body
        color_map = {
            CharacterClass.WILSON: (255, 200, 150),
            CharacterClass.WILLOW: (255, 150, 100),
            CharacterClass.WOLFGANG: (255, 100, 50),
            CharacterClass.WENDY: (200, 200, 255),
            CharacterClass.WX78: (150, 150, 150),
            CharacterClass.WICKERBOTTOM: (200, 180, 160),
            CharacterClass.WOODIE: (255, 200, 100),
            CharacterClass.WES: (255, 255, 255),
            CharacterClass.MAXWELL: (100, 100, 100),
            CharacterClass.WIGFRID: (255, 200, 150),
            CharacterClass.WEBBER: (100, 50, 50),
            CharacterClass.WINONA: (255, 200, 150),
            CharacterClass.WARLY: (200, 150, 100),
            CharacterClass.WORMWOOD: (100, 200, 100),
            CharacterClass.WURT: (100, 200, 150),
        }
        
        color = color_map.get(self.character.name, LIGHT_BLUE)
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw character specific features
        if self.character.name == CharacterClass.WILSON and self.beard_growth > 10:
            beard_rect = pygame.Rect(self.x - 5, self.y + 20, self.width + 10, int(self.beard_growth / 10))
            pygame.draw.rect(screen, BLACK, beard_rect)
        
        elif self.character.name == CharacterClass.WOLFGANG and self.stats.hunger > 200:
            # Mighty form indicator
            pygame.draw.circle(screen, RED, (int(self.x + self.width//2), int(self.y - 10)), 5)
        
        elif self.character.name == CharacterClass.WEBBER:
            # Spider features
            for i in range(4):
                leg_x = self.x + random.randint(-5, self.width + 5)
                leg_y = self.y + self.height + random.randint(5, 15)
                pygame.draw.line(screen, BLACK, (leg_x, self.y + self.height), (leg_x + 5, leg_y), 2)
        
        elif self.character.name == CharacterClass.WOODIE and self.woodie_transformation:
            # Werebeaver form
            pygame.draw.circle(screen, BROWN, (int(self.x + self.width//2), int(self.y + self.height//2)), 20)
        
        # Draw equipment
        if self.inventory.equipment["weapon"]:
            weapon_rect = pygame.Rect(self.x + self.width, self.y + 10, 15, 5)
            pygame.draw.rect(screen, GRAY, weapon_rect)
        
        # Draw stat bars
        bar_width = self.width
        bar_height = 4
        bar_y = self.y - 8
        
        # Health bar
        health_ratio = self.stats.health / self.stats.max_health
        pygame.draw.rect(screen, RED, (self.x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, bar_y, bar_width * health_ratio, bar_height))
        
        # Hunger bar
        hunger_ratio = self.stats.hunger / self.stats.max_hunger
        pygame.draw.rect(screen, GRAY, (self.x, bar_y + bar_height, bar_width, bar_height))
        pygame.draw.rect(screen, ORANGE, (self.x, bar_y + bar_height, bar_width * hunger_ratio, bar_height))
        
        # Sanity bar
        sanity_ratio = self.stats.sanity / self.stats.max_sanity
        pygame.draw.rect(screen, GRAY, (self.x, bar_y + bar_height * 2, bar_width, bar_height))
        pygame.draw.rect(screen, PURPLE, (self.x, bar_y + bar_height * 2, bar_width * sanity_ratio, bar_height))

class Enemy:
    def __init__(self, x: float, y: float, enemy_type: str):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.type = enemy_type
        self.speed = 2
        self.health = 50
        self.max_health = 50
        self.attack_damage = 15
        self.attack_cooldown = 0
        self.attack_range = 40
        self.detection_range = 200
        
        self.setup_enemy()
    
    def setup_enemy(self):
        enemy_stats = {
            "Spider": {"speed": 1.5, "health": 30, "damage": 10, "range": 30},
            "Hound": {"speed": 3, "health": 40, "damage": 20, "range": 50},
            "Tentacle": {"speed": 0, "health": 100, "damage": 30, "range": 80},
            "Clockwork Knight": {"speed": 2, "health": 150, "damage": 25, "range": 40},
            "Clockwork Bishop": {"speed": 1, "health": 100, "damage": 30, "range": 200},
            "Treeguard": {"speed": 1.5, "health": 300, "damage": 40, "range": 50},
            "Deerclops": {"speed": 3, "health": 500, "damage": 75, "range": 60},
            "Shadow Creature": {"speed": 2, "health": 50, "damage": 20, "range": 40},
        }
        
        stats = enemy_stats.get(self.type, {"speed": 2, "health": 50, "damage": 15, "range": 40})
        self.speed = stats["speed"]
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.attack_damage = stats["damage"]
        self.attack_range = stats["range"]
    
    def update(self, player: Player, obstacles: List[pygame.Rect]):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Check if player is in detection range
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.detection_range and self.speed > 0:
            # Move toward player
            if distance > 0:
                dx = dx / distance * self.speed
                dy = dy / distance * self.speed
                
                self.x += dx
                self.y += dy
                
                # Keep in bounds
                self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
                self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
                
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
            
            # Attack if close enough
            if distance < self.attack_range and self.attack_cooldown <= 0:
                player.stats.health -= self.attack_damage
                self.attack_cooldown = 60
    
    def take_damage(self, damage: int) -> bool:
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen: pygame.Surface):
        color_map = {
            "Spider": BLACK,
            "Hound": DARK_GRAY,
            "Tentacle": PURPLE,
            "Clockwork Knight": GRAY,
            "Clockwork Bishop": GOLD,
            "Treeguard": BROWN,
            "Deerclops": LIGHT_BLUE,
            "Shadow Creature": (50, 0, 50),
        }
        
        color = color_map.get(self.type, RED)
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw health bar
        bar_width = self.width
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y - 8, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 8, bar_width * health_ratio, bar_height))

class Particle:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], lifetime: int = 30):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
    
    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen: pygame.Surface):
        alpha = self.lifetime / self.max_lifetime
        color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Don't Starve - Complete Character Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player = None
        self.resources = []
        self.enemies = []
        self.structures = []
        self.particles = []
        
        self.time_of_day = TimeOfDay.DAY
        self.season = Season.AUTUMN
        self.day_timer = 0
        self.day_duration = 1800  # 30 seconds per phase at 60 FPS
        
        self.game_over = False
        self.paused = False
        
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 18)
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.character_select_menu()
        self.generate_world()
    
    def character_select_menu(self):
        selecting = True
        selected_char = CharacterClass.WILSON
        char_list = list(CharacterClass)
        chars_per_row = 5
        char_spacing = 160
        row_spacing = 200
        
        while selecting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    selecting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Calculate which character was clicked
                    for i, char in enumerate(char_list):
                        row = i // chars_per_row
                        col = i % chars_per_row
                        char_x = 50 + col * char_spacing
                        char_y = 200 + row * row_spacing
                        
                        if char_x <= mouse_x <= char_x + 140 and char_y <= mouse_y <= char_y + 180:
                            selected_char = char
                            selecting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selecting = False
            
            self.screen.fill((30, 30, 30))
            
            # Title
            title_text = self.large_font.render("Choose Your Character", True, GOLD)
            self.screen.blit(title_text, (SCREEN_WIDTH//2 - 200, 50))
            
            # Draw character options
            for i, char in enumerate(char_list):
                row = i // chars_per_row
                col = i % chars_per_row
                char_x = 50 + col * char_spacing
                char_y = 200 + row * row_spacing
                
                # Character box
                box_rect = pygame.Rect(char_x, char_y, 140, 180)
                pygame.draw.rect(self.screen, DARK_GRAY, box_rect)
                pygame.draw.rect(self.screen, GOLD if char == selected_char else GRAY, box_rect, 2)
                
                # Character name
                name_text = self.font.render(char.value, True, WHITE)
                self.screen.blit(name_text, (char_x + 10, char_y + 10))
                
                # Character portrait (colored square)
                portrait_colors = {
                    CharacterClass.WILSON: (255, 200, 150),
                    CharacterClass.WILLOW: (255, 150, 100),
                    CharacterClass.WOLFGANG: (255, 100, 50),
                    CharacterClass.WENDY: (200, 200, 255),
                    CharacterClass.WX78: (150, 150, 150),
                    CharacterClass.WICKERBOTTOM: (200, 180, 160),
                    CharacterClass.WOODIE: (255, 200, 100),
                    CharacterClass.WES: (255, 255, 255),
                    CharacterClass.MAXWELL: (100, 100, 100),
                    CharacterClass.WIGFRID: (255, 200, 150),
                    CharacterClass.WEBBER: (100, 50, 50),
                    CharacterClass.WINONA: (255, 200, 150),
                    CharacterClass.WARLY: (200, 150, 100),
                    CharacterClass.WORMWOOD: (100, 200, 100),
                    CharacterClass.WURT: (100, 200, 150),
                }
                
                portrait_rect = pygame.Rect(char_x + 40, char_y + 50, 60, 60)
                pygame.draw.rect(self.screen, portrait_colors.get(char, WHITE), portrait_rect)
                
                # Character stats
                char_obj = Character(char)
                stats_text = [
                    f"HP: {char_obj.stats.max_health}",
                    f"Hunger: {char_obj.stats.max_hunger}",
                    f"Sanity: {char_obj.stats.max_sanity}",
                ]
                
                for j, stat in enumerate(stats_text):
                    stat_render = self.small_font.render(stat, True, WHITE)
                    self.screen.blit(stat_render, (char_x + 10, char_y + 120 + j * 15))
            
            # Instructions
            inst_text = self.font.render("Click on a character to select, or press ENTER for default (Wilson)", True, WHITE)
            self.screen.blit(inst_text, (SCREEN_WIDTH//2 - 350, SCREEN_HEIGHT - 50))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Create player with selected character
        if self.running:
            self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, selected_char)
    
    def generate_world(self):
        # Generate various resources
        resource_configs = [
            ("Tree", 15),
            ("Boulder", 10),
            ("Flint", 8),
            ("Gold Nugget", 5),
            ("Berries", 8),
            ("Carrots", 6),
            ("Grass", 12),
            ("Twigs", 10),
            ("Flower", 15),
            ("Butterfly", 8),
            ("Beehive", 3),
            ("Spider Den", 4),
        ]
        
        for resource_type, count in resource_configs:
            for _ in range(count):
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                amount = random.randint(3, 8) if resource_type not in ["Flower", "Butterfly", "Beehive", "Spider Den"] else 1
                self.resources.append(Resource(x, y, resource_type, amount))
        
        # Generate enemies
        enemy_configs = [
            ("Spider", 3),
            ("Hound", 2),
            ("Clockwork Knight", 1),
        ]
        
        for enemy_type, count in enemy_configs:
            for _ in range(count):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                self.enemies.append(Enemy(x, y, enemy_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.player.inventory_menu_open or self.player.crafting_menu_open:
                        self.player.inventory_menu_open = False
                        self.player.crafting_menu_open = False
                    else:
                        self.paused = not self.paused
                
                elif event.key == pygame.K_r and self.game_over:
                    self.__init__()
                
                elif not self.game_over and not self.paused:
                    # Inventory toggle
                    if event.key == pygame.K_TAB:
                        self.player.inventory_menu_open = not self.player.inventory_menu_open
                    
                    # Crafting menu
                    elif event.key == pygame.K_c:
                        self.player.crafting_menu_open = not self.player.crafting_menu_open
                    
                    # Map toggle
                    elif event.key == pygame.K_m:
                        self.player.map_open = not self.player.map_open
                    
                    # Gather resources
                    elif event.key == pygame.K_SPACE:
                        self.gather_nearby_resources()
                    
                    # Eat food
                    elif event.key == pygame.K_f:
                        self.eat_food()
                    
                    # Attack
                    elif event.key == pygame.K_a:
                        self.attack_nearby_enemies()
                    
                    # Craft items
                    elif self.player.crafting_menu_open:
                        self.handle_crafting_keys(event.key)
                    
                    # Equipment management
                    elif self.player.inventory_menu_open:
                        self.handle_inventory_keys(event.key)
    
    def handle_crafting_keys(self, key):
        craft_keys = {
            pygame.K_1: "Axe",
            pygame.K_2: "Pickaxe",
            pygame.K_3: "Shovel",
            pygame.K_4: "Spear",
            pygame.K_5: "Torch",
            pygame.K_6: "Campfire",
            pygame.K_7: "Science Machine",
            pygame.K_8: "Chest",
            pygame.K_9: "Crock Pot",
        }
        
        if key in craft_keys:
            self.player.crafting.craft(craft_keys[key], self.player.inventory)
    
    def handle_inventory_keys(self, key):
        items = list(self.player.inventory.items.keys())
        num_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
        
        for i, num_key in enumerate(num_keys):
            if key == num_key and i < len(items):
                item_name = items[i]
                
                # Try to eat or equip the item
                if item_name in ["Berries", "Carrots", "Meat", "Cooked Meat", "Monster Meat", "Honey"]:
                    self.player.eat(item_name)
                else:
                    self.player.selected_item = i
    
    def gather_nearby_resources(self):
        gather_rect = pygame.Rect(
            self.player.x - 20, self.player.y - 20,
            self.player.width + 40, self.player.height + 40
        )
        
        for resource in self.resources[:]:
            if resource.amount > 0 and gather_rect.colliderect(resource.rect):
                self.player.gather(resource)
                
                # Add gathering particles
                for _ in range(5):
                    self.particles.append(
                        Particle(resource.x + TILE_SIZE//2, resource.y + TILE_SIZE//2, resource.color)
                    )
                
                if resource.amount <= 0 and not resource.can_regrow:
                    self.resources.remove(resource)
                break
    
    def eat_food(self):
        food_items = ["Berries", "Carrots", "Meat", "Cooked Meat", "Monster Meat", "Butterfly Wings", "Honey"]
        for food in food_items:
            if self.player.inventory.has_item(food):
                self.player.eat(food)
                break
    
    def attack_nearby_enemies(self):
        if self.player.attack_cooldown > 0:
            return
        
        attack_rect = pygame.Rect(
            self.player.x - 30, self.player.y - 30,
            self.player.width + 60, self.player.height + 60
        )
        
        for enemy in self.enemies[:]:
            if attack_rect.colliderect(enemy.rect):
                damage = self.player.attack_damage
                
                # Wolfgang's damage bonus
                if self.player.character.name == CharacterClass.WOLFGANG:
                    damage *= (0.5 + self.player.stats.hunger / self.player.stats.max_hunger)
                
                # Wigfrid's health and sanity steal
                if self.player.character.name == CharacterClass.WIGFRID:
                    self.player.stats.health = min(self.player.stats.max_health, self.player.stats.health + damage * 0.25)
                    self.player.stats.sanity = min(self.player.stats.max_sanity, self.player.stats.sanity + damage * 0.25)
                
                if enemy.take_damage(damage):
                    # Enemy defeated
                    for _ in range(10):
                        color = RED if enemy.type == "Spider" else GRAY
                        self.particles.append(
                            Particle(enemy.x + enemy.width//2, enemy.y + enemy.height//2, color)
                        )
                    
                    # Drop loot
                    loot_tables = {
                        "Spider": [("Silk", 2), ("Monster Meat", 1)],
                        "Hound": [("Monster Meat", 1), ("Meat", 1)],
                        "Clockwork Knight": [("Gears", 2)],
                    }
                    
                    for item_name, amount in loot_tables.get(enemy.type, []):
                        self.player.inventory.add_item(item_name, amount)
                    
                    self.enemies.remove(enemy)
                
                self.player.attack_cooldown = 20
                break
    
    def spawn_random_enemies(self):
        # Spawn enemies periodically
        if random.random() < 0.001:  # 0.1% chance per frame
            enemy_types = ["Spider", "Hound"]
            if self.time_of_day == TimeOfDay.NIGHT:
                enemy_types.append("Shadow Creature")
            
            enemy_type = random.choice(enemy_types)
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            
            # Spawn away from player
            while abs(x - self.player.x) < 200 and abs(y - self.player.y) < 200:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
            
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        # Handle input
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        
        self.player.move(dx, dy, [], self.resources)
        
        # Update time system
        self.day_timer += 1
        if self.day_timer < self.day_duration:
            self.time_of_day = TimeOfDay.DAY
        elif self.day_timer < self.day_duration * 2:
            self.time_of_day = TimeOfDay.DUSK
        elif self.day_timer < self.day_duration * 3:
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.day_timer = 0
            # Cycle seasons every 3 days
            season_order = [Season.AUTUMN, Season.WINTER, Season.SPRING, Season.SUMMER]
            current_index = season_order.index(self.season)
            self.season = season_order[(current_index + 1) % 4]
        
        # Update player
        self.player.update(self.time_of_day, self.season)
        
        # Update resources
        for resource in self.resources:
            resource.update()
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, [])
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Spawn new enemies
        self.spawn_random_enemies()
        
        # Check game over
        if self.player.stats.health <= 0:
            self.game_over = True
    
    def draw_background(self):
        # Color based on season and time of day
        season_colors = {
            Season.AUTUMN: (100, 80, 50),
            Season.WINTER: (200, 200, 220),
            Season.SPRING: (50, 150, 50),
            Season.SUMMER: (150, 150, 50),
        }
        
        time_tints = {
            TimeOfDay.DAY: 1.0,
            TimeOfDay.DUSK: 0.6,
            TimeOfDay.NIGHT: 0.3,
        }
        
        base_color = season_colors[self.season]
        tint = time_tints[self.time_of_day]
        
        bg_color = tuple(int(c * tint) for c in base_color)
        self.screen.fill(bg_color)
        
        # Draw ground details
        if self.time_of_day != TimeOfDay.NIGHT:
            for i in range(0, SCREEN_WIDTH, 40):
                for j in range(0, SCREEN_HEIGHT, 40):
                    if random.random() < 0.05:
                        grass_color = tuple(int(c * 0.8 * tint) for c in base_color)
                        pygame.draw.line(self.screen, grass_color, 
                                       (i, j), (i + 10, j - 10), 2)
    
    def draw_ui(self):
        # Draw inventory if open
        if self.player.inventory_menu_open:
            self.draw_inventory_menu()
        
        # Draw crafting menu if open
        if self.player.crafting_menu_open:
            self.draw_crafting_menu()
        
        # Draw map if open
        if self.player.map_open:
            self.draw_map()
        
        # Main UI elements
        self.draw_status_bars()
        self.draw_item_bar()
        self.draw_time_and_season()
        self.draw_character_info()
        self.draw_pause_menu()
        self.draw_game_over()
    
    def draw_inventory_menu(self):
        menu_width = 300
        menu_height = 400
        menu_x = SCREEN_WIDTH//2 - menu_width//2
        menu_y = SCREEN_HEIGHT//2 - menu_height//2
        
        # Semi-transparent background
        bg_surface = pygame.Surface((menu_width, menu_height))
        bg_surface.set_alpha(200)
        bg_surface.fill(DARK_GRAY)
        self.screen.blit(bg_surface, (menu_x, menu_y))
        
        # Title
        title = self.font.render("Inventory", True, GOLD)
        self.screen.blit(title, (menu_x + 100, menu_y + 10))
        
        # Items
        y_offset = menu_y + 50
        for i, (item_name, amount) in enumerate(self.player.inventory.items.items()):
            if y_offset < menu_y + menu_height - 30:
                item_text = f"{i+1}. {item_name}: {amount}"
                color = GOLD if i == self.player.selected_item else WHITE
                text_surface = self.font.render(item_text, True, color)
                self.screen.blit(text_surface, (menu_x + 20, y_offset))
                y_offset += 25
        
        # Equipment
        equip_title = self.font.render("Equipment:", True, GOLD)
        self.screen.blit(equip_title, (menu_x + 20, y_offset + 20))
        
        y_offset += 50
        for slot, item in self.player.inventory.equipment.items():
            item_name = item.name if item else "Empty"
            equip_text = f"{slot}: {item_name}"
            text_surface = self.small_font.render(equip_text, True, WHITE)
            self.screen.blit(text_surface, (menu_x + 40, y_offset))
            y_offset += 20
    
    def draw_crafting_menu(self):
        menu_width = 400
        menu_height = 300
        menu_x = SCREEN_WIDTH - menu_width - 20
        menu_y = 50
        
        # Semi-transparent background
        bg_surface = pygame.Surface((menu_width, menu_height))
        bg_surface.set_alpha(200)
        bg_surface.fill(DARK_GRAY)
        self.screen.blit(bg_surface, (menu_x, menu_y))
        
        # Title
        title = self.font.render("Crafting", True, GOLD)
        self.screen.blit(title, (menu_x + 150, menu_y + 10))
        
        # Craftable items
        craftable_items = [
            "Axe", "Pickaxe", "Shovel", "Spear", "Torch", 
            "Campfire", "Science Machine", "Chest", "Crock Pot"
        ]
        
        y_offset = menu_y + 50
        for i, item_name in enumerate(craftable_items):
            if y_offset < menu_y + menu_height - 30:
                can_craft = self.player.crafting.can_craft(item_name, self.player.inventory)
                color = GREEN if can_craft else GRAY
                
                text = f"{i+1}. {item_name}"
                text_surface = self.font.render(text, True, color)
                self.screen.blit(text_surface, (menu_x + 20, y_offset))
                
                # Show ingredients
                if item_name in self.player.crafting.recipes:
                    recipe = self.player.crafting.recipes[item_name]
                    ingredient_text = ", ".join([f"{mat}({amt})" for mat, amt in recipe.ingredients.items()])
                    ing_surface = self.small_font.render(ingredient_text, True, GRAY)
                    self.screen.blit(ing_surface, (menu_x + 180, y_offset))
                
                y_offset += 25
    
    def draw_status_bars(self):
        # Health bar
        bar_x = 10
        bar_y = SCREEN_HEIGHT - 80
        bar_width = 200
        bar_height = 20
        
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.player.stats.health / self.player.stats.max_health))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, health_width, bar_height))
        
        health_text = self.small_font.render(f"HP: {int(self.player.stats.health)}/{int(self.player.stats.max_health)}", True, WHITE)
        self.screen.blit(health_text, (bar_x + 5, bar_y + 2))
        
        # Hunger bar
        bar_y += 25
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        hunger_width = int(bar_width * (self.player.stats.hunger / self.player.stats.max_hunger))
        pygame.draw.rect(self.screen, ORANGE, (bar_x, bar_y, hunger_width, bar_height))
        
        hunger_text = self.small_font.render(f"Hunger: {int(self.player.stats.hunger)}/{int(self.player.stats.max_hunger)}", True, WHITE)
        self.screen.blit(hunger_text, (bar_x + 5, bar_y + 2))
        
        # Sanity bar
        bar_y += 25
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        sanity_width = int(bar_width * (self.player.stats.sanity / self.player.stats.max_sanity))
        pygame.draw.rect(self.screen, PURPLE, (bar_x, bar_y, sanity_width, bar_height))
        
        sanity_text = self.small_font.render(f"Sanity: {int(self.player.stats.sanity)}/{int(self.player.stats.max_sanity)}", True, WHITE)
        self.screen.blit(sanity_text, (bar_x + 5, bar_y + 2))
    
    def draw_item_bar(self):
        bar_x = SCREEN_WIDTH // 2 - 150
        bar_y = SCREEN_HEIGHT - 50
        bar_width = 300
        bar_height = 40
        
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
        
        items = list(self.player.inventory.items.keys())[:5]
        for i, item_name in enumerate(items):
            item_x = bar_x + 10 + i * 60
            color = GOLD if i == self.player.selected_item else WHITE
            text_surface = self.small_font.render(item_name[:6], True, color)
            self.screen.blit(text_surface, (item_x, bar_y + 12))
    
    def draw_time_and_season(self):
        time_colors = {
            TimeOfDay.DAY: YELLOW,
            TimeOfDay.DUSK: ORANGE,
            TimeOfDay.NIGHT: BLUE,
        }
        
        season_colors = {
            Season.AUTUMN: ORANGE,
            Season.WINTER: LIGHT_BLUE,
            Season.SPRING: GREEN,
            Season.SUMMER: RED,
        }
        
        time_text = self.font.render(f"{self.time_of_day.value}", True, time_colors[self.time_of_day])
        self.screen.blit(time_text, (SCREEN_WIDTH//2 - 30, 10))
        
        season_text = self.font.render(f"{self.season.value}", True, season_colors[self.season])
        self.screen.blit(season_text, (SCREEN_WIDTH//2 - 30, 35))
        
        # Temperature
        temp_text = self.small_font.render(f"Temp: {int(self.player.temperature)}°C", True, WHITE)
        self.screen.blit(temp_text, (SCREEN_WIDTH - 120, 10))
    
    def draw_character_info(self):
        char_text = self.font.render(f"Character: {self.player.character.name.value}", True, GOLD)
        self.screen.blit(char_text, (10, 10))
        
        # Character quote
        quote_text = self.small_font.render(f'"{self.player.character.character_quote}"', True, GRAY)
        self.screen.blit(quote_text, (10, 35))
    
    def draw_map(self):
        map_width = 200
        map_height = 200
        map_x = SCREEN_WIDTH - map_width - 20
        map_y = SCREEN_HEIGHT - map_height - 100
        
        # Background
        pygame.draw.rect(self.screen, BLACK, (map_x, map_y, map_width, map_height))
        pygame.draw.rect(self.screen, GRAY, (map_x, map_y, map_width, map_height), 2)
        
        # Player position on map
        player_map_x = map_x + int(self.player.x / SCREEN_WIDTH * map_width)
        player_map_y = map_y + int(self.player.y / SCREEN_HEIGHT * map_height)
        pygame.draw.circle(self.screen, YELLOW, (player_map_x, player_map_y), 3)
        
        # Enemy positions
        for enemy in self.enemies:
            enemy_map_x = map_x + int(enemy.x / SCREEN_WIDTH * map_width)
            enemy_map_y = map_y + int(enemy.y / SCREEN_HEIGHT * map_height)
            pygame.draw.circle(self.screen, RED, (enemy_map_x, enemy_map_y), 2)
    
    def draw_pause_menu(self):
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.large_font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            
            resume_text = self.font.render("Press ESC to resume", True, WHITE)
            self.screen.blit(resume_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
    
    def draw_game_over(self):
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("YOU HAVE PERISHED", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 50))
            
            restart_text = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
    
    def draw_controls(self):
        controls = [
            "WASD/Arrows: Move",
            "Space: Gather",
            "A: Attack",
            "F: Eat food",
            "C: Crafting menu",
            "Tab: Inventory",
            "M: Map",
            "ESC: Pause"
        ]
        
        y_offset = SCREEN_HEIGHT - 200
        for control in controls:
            text_surface = self.small_font.render(control, True, WHITE)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 18
    
    def draw(self):
        self.draw_background()
        
        # Draw resources
        for resource in self.resources:
            if resource.amount > 0:
                resource.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        self.draw_controls()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()