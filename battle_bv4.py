import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 6  # Changed to 6 for 3v3
action_cooldown = 0
action_wait_time = 90
attack = False
clicked = False
game_over = 0

# Unit selection variables
selected_unit = None  # Currently selected player unit
game_state = "select_attacker"  # "select_attacker" or "select_target"

#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#Player Images
player_warrior_img = pygame.image.load('img/player_warrior.png').convert_alpha()
player_tank_img = pygame.image.load('img/player_tank.png').convert_alpha()
#Scaling
player_warrior_img = pygame.transform.scale(player_warrior_img, (60, 80))
player_tank_img = pygame.transform.scale(player_tank_img, (60, 80))
#AI_img
ai_warrior_img = pygame.image.load('img/ai_warrior.png').convert_alpha()
ai_tank_img = pygame.image.load('img/ai_tank.png').convert_alpha()
#Scaling
ai_warrior_img = pygame.transform.scale(ai_warrior_img, (60, 80))
ai_tank_img = pygame.transform.scale(ai_tank_img, (60, 80))
#background image
background_img = pygame.image.load('img/Background/bg_swamp800.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#button images
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))

#function for drawing panel - UPDATED for teams
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	
	# Draw player team stats
	draw_text("PLAYER TEAM", font, red, 20, screen_height - bottom_panel + 10)
	for i, unit in enumerate(player_team):
		y_pos = screen_height - bottom_panel + 35 + (i * 25)
		status = "ALIVE" if unit.alive else "DEAD"
		draw_text(f'{unit.name}: HP {unit.hp}/{unit.max_hp} ATK {unit.atk} DEF {unit.def_stat} EXP {unit.exp} [{status}]', 
				 pygame.font.SysFont('Arial', 14), red, 20, y_pos)
	
	# Draw AI team stats
	draw_text("AI TEAM", font, red, 450, screen_height - bottom_panel + 10)
	for i, unit in enumerate(ai_team):
		y_pos = screen_height - bottom_panel + 35 + (i * 25)
		status = "ALIVE" if unit.alive else "DEAD"
		draw_text(f'{unit.name}: HP {unit.hp}/{unit.max_hp} [{status}]', 
				 pygame.font.SysFont('Arial', 14), red, 450, y_pos)

def draw_instructions():
    if game_state == "select_attacker":
        instruction = "Click on your unit to select attacker"
    else:
        instruction = f"Selected: {selected_unit.name}. Click enemy to attack."
    
    draw_text(instruction, pygame.font.SysFont('Arial', 18), (255, 255, 255), 10, 10)

#fighter class
class Fighter:
    def __init__(self, x, y, name, team="player"):
        self.name = name
        self.team = team  # "player" or "ai"
        
        # Core attributes (will be set by subclasses)
        self.hp = 100
        self.max_hp = 100
        self.atk = 0
        self.def_stat = 0  # Using def_stat since 'def' is Python keyword
        self.exp = 0
        self.rank = 1
        
        # Game state
        self.alive = True
        self.selected = False  # New: track if unit is selected
        
        # Visual properties
        self.rect = pygame.Rect(x, y, 80, 100)
        self.image = None
        
        # Load appropriate image based on class type
        self.load_image()
    
    def load_image(self):
        # This will be overridden by subclasses
        # Fallback to colored rectangle if no image
        self.image = pygame.Surface((60, 80))
        self.image.fill((128, 128, 128))  # Gray default
    
    def draw(self, screen):
        # Determine background color based on team
        if self.team == "player":
            bg_color = (100, 150, 255)  # Light blue
        else:
            bg_color = (255, 100, 100)  # Light red
        
        # Highlight selected unit
        if self.selected:
            bg_color = (255, 255, 0)  # Yellow highlight
        
        # Draw background rectangle
        pygame.draw.rect(screen, bg_color, self.rect)
        
        # Draw thicker border if selected
        border_width = 4 if self.selected else 2
        pygame.draw.rect(screen, (0, 0, 0), self.rect, border_width)
        
        # Draw unit image if it exists
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect)
        
        # Draw name below unit (only if alive)
        if self.alive:
            unit_font = pygame.font.SysFont('Arial', 14)
            name_text = unit_font.render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.rect.centerx, self.rect.y + self.rect.height + 10))
            screen.blit(name_text, name_rect)
    
    def attack(self, target):
        # Assignment formula: Damage = attacker.ATK – target.DEF + (random between -5 to 10)
        random_factor = random.randint(-5, 10)
        damage = self.atk - target.def_stat + random_factor
        
        # Ensure damage isn't negative (minimum 0)
        damage = max(1, damage)
        
        # Apply damage
        target.hp -= damage
        if target.hp <= 0:
            target.hp = 0
            target.alive = False
        
        # Experience gain (assignment requirements)
        # Attacker gains EXP based on damage dealt
        self.gain_exp(damage)
        
        # Target gains EXP based on their DEF
        target.gain_exp(target.def_stat)
        
        # Bonus EXP for target based on damage received
        if damage > 10:
            # Target gains extra 20% EXP
            bonus_exp = int(target.def_stat * 0.2)
            target.gain_exp(bonus_exp)
        elif damage <= 0:
            # Target gains extra 50% EXP
            bonus_exp = int(target.def_stat * 0.5)
            target.gain_exp(bonus_exp)
        
        return damage
    
    def gain_exp(self, amount):
        self.exp += amount
        
        # Check for level up (assignment: level up at 100 EXP)
        while self.exp >= 100:
            self.rank += 1
            self.exp -= 100
    
    def reset(self):
        # Reset for new game
        self.hp = self.max_hp
        self.exp = 0
        self.rank = 1
        self.alive = True
        self.selected = False

# Warrior subclass
class Warrior(Fighter):
    def __init__(self, x, y, name, team="player"):
        super().__init__(x, y, name, team)
        
        # Assignment specs: ATK 5-20, DEF 1-10
        self.atk = random.randint(5, 20)
        self.def_stat = random.randint(1, 10)
        
        self.load_image()
    
    def load_image(self):
        # Use the globally loaded images
        if self.team == "player":
            self.image = player_warrior_img
        else:  # AI team
            self.image = ai_warrior_img

# Tank subclass  
class Tank(Fighter):
    def __init__(self, x, y, name, team="player"):
        super().__init__(x, y, name, team)
        
        # Assignment specs: ATK 1-10, DEF 5-15
        self.atk = random.randint(1, 10)
        self.def_stat = random.randint(5, 15)
        
        self.load_image()
    
    def load_image(self):
        # Use the globally loaded images
        if self.team == "player":
            self.image = player_tank_img
        else:  # AI team
            self.image = ai_tank_img

def player_team_setup():
    """Setup player team with console input"""
    print("=== TEAM SETUP ===")
    print("You will create a team of 3 units.")
    print("Each unit can be either a Warrior or Tanker.")
    print()
    
    team = []
    positions = [(50, 50), (50, 170), (50, 290)]
    
    for i in range(3):
        print(f"--- Setting up Unit {i+1} ---")
        
        # Get unit name
        while True:
            name = input(f"Enter name for Unit {i+1}: ").strip()
            if name:  # Make sure name isn't empty
                break
            print("Name cannot be empty. Please try again.")
        
        # Get profession choice
        while True:
            print("Choose profession:")
            print("1. Warrior (High Attack: 5-20, Low Defense: 1-10)")
            print("2. Tanker (Low Attack: 1-10, High Defense: 5-15)")
            choice = input("Enter 1 or 2: ").strip()
            
            if choice == "1":
                unit = Warrior(positions[i][0], positions[i][1], name, "player")
                print(f"Created Warrior '{name}' - ATK: {unit.atk}, DEF: {unit.def_stat}")
                break
            elif choice == "2":
                unit = Tank(positions[i][0], positions[i][1], name, "player")
                print(f"Created Tank '{name}' - ATK: {unit.atk}, DEF: {unit.def_stat}")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        
        team.append(unit)
        print()
    
    print("Player team setup complete!")
    print("=" * 40)
    return team

def create_ai_team():
    """Create AI team with random professions and names"""
    print("Setting up AI team...")
    team = []
    positions = [(650, 50), (650, 170), (650, 290)]
    
    for i, (x, y) in enumerate(positions):
        # Random profession for AI
        if random.choice([True, False]):
            unit = Warrior(x, y, f"AI{random.randint(10, 99)}", "ai")
            print(f"AI Unit {i+1}: {unit.name} (Warrior) - ATK: {unit.atk}, DEF: {unit.def_stat}")
        else:
            unit = Tank(x, y, f"AI{random.randint(10, 99)}", "ai")
            print(f"AI Unit {i+1}: {unit.name} (Tank) - ATK: {unit.atk}, DEF: {unit.def_stat}")
        team.append(unit)
    
    print("AI team setup complete!")
    print("=" * 40)
    print("Starting battle...")
    input("Press Enter to continue...")
    return team

def handle_unit_selection(pos, clicked):
    global selected_unit, game_state
    
    if not clicked:
        return
    
    if game_state == "select_attacker":
        # Player is selecting which unit to attack with
        for unit in player_team:
            if unit.rect.collidepoint(pos) and unit.alive:
                # Deselect previous unit
                if selected_unit:
                    selected_unit.selected = False
                
                # Select new unit
                selected_unit = unit
                unit.selected = True
                game_state = "select_target"
                print(f"Selected {unit.name} to attack with. Now click an enemy unit.")
                return
    
    elif game_state == "select_target":
        # Player is selecting target to attack
        for unit in ai_team:
            if unit.rect.collidepoint(pos) and unit.alive:
                if selected_unit and selected_unit.alive:
                    # Execute attack
                    damage = selected_unit.attack(unit)
                    print(f"{selected_unit.name} attacks {unit.name} for {damage} damage!")
                    
                    # Deselect unit and reset state
                    selected_unit.selected = False
                    selected_unit = None
                    game_state = "select_attacker"
                    
                    # Check if AI team is defeated
                    alive_ai = sum(1 for u in ai_team if u.alive)
                    if alive_ai == 0:
                        global game_over
                        game_over = 1
                    
                    return
        
        # If clicked somewhere else, allow reselecting attacker
        if selected_unit:
            selected_unit.selected = False
            selected_unit = None
            game_state = "select_attacker"
            print("Attack cancelled. Select a unit to attack with.")

def draw_instructions():
    if game_state == "select_attacker":
        instruction = "Click on your unit to select attacker"
    else:
        instruction = f"Selected: {selected_unit.name}. Click enemy to attack."
    
    draw_text(instruction, pygame.font.SysFont('Arial', 18), (255, 255, 255), 10, 10)

# Main setup function
def main():
    # Setup teams BEFORE starting pygame window
    print("Welcome to Turn-Based Battle Game!")
    print()
    
    # Player team setup
    player_team = player_team_setup()
    
    # AI team setup  
    ai_team = create_ai_team()
    
    # Now start the pygame battle with created teams
    return player_team, ai_team

# Setup teams
player_team, ai_team = main()

#create buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()

	#draw fighters
	for unit in player_team:
		if unit.alive:  # Only draw alive units
			unit.draw(screen)
	for unit in ai_team:
		if unit.alive:  # Only draw alive units
			unit.draw(screen)

	# Draw game instructions
	draw_instructions()

	#control player actions
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	
	# Handle unit selection and targeting
	handle_unit_selection(pos, clicked)

	# Show sword cursor when hovering over valid targets
	if game_state == "select_target":
		for unit in ai_team:
			if unit.rect.collidepoint(pos) and unit.alive:
				pygame.mouse.set_visible(False)
				screen.blit(sword_img, pos)
				break

	# Check if all AI units are dead
	alive_ai = sum(1 for unit in ai_team if unit.alive)
	if alive_ai == 0:
		game_over = 1

	# Check if all player units are dead
	alive_players = sum(1 for unit in player_team if unit.alive)
	if alive_players == 0:
		game_over = -1

	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			# Reset all units
			for unit in player_team:
				unit.reset()
			for unit in ai_team:
				unit.reset()
			# Reset game state
			selected_unit = None
			game_state = "select_attacker"
			game_over = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()