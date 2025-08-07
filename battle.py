import pygame
import random
import button

# Initialize pygame first
pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 200
console_panel = 600  # New: side console width
screen_width = 800 + console_panel  # Expanded width for console
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define fonts
font = pygame.font.SysFont('Arial', 26)
console_font = pygame.font.SysFont('Courier', 12)  # Monospace font for console

#define colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)  # Dark gray for console background
YELLOW = (255, 255, 0)

# Game console for messages and logging
game_console = []  # List to store console messages
max_console_lines = 35  # Maximum lines to show in console

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

def log_message(message):
    """Add message to game console and log file"""
    import datetime
    
    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    console_message = f"[{timestamp}] {message}"
    
    # Add to console display
    game_console.append(console_message)
    
    # Keep only recent messages for display
    if len(game_console) > max_console_lines:
        game_console.pop(0)
    
    # Write to log file
    try:
        with open("game_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(console_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def draw_console():
    """Draw the game console panel"""
    console_x = 800  # Start after main game area
    console_y = 0
    console_width = console_panel
    console_height = screen_height
    
    # Draw console background
    pygame.draw.rect(screen, GRAY, (console_x, console_y, console_width, console_height))
    pygame.draw.rect(screen, WHITE, (console_x, console_y, console_width, console_height), 2)
    
    # Draw console title
    title_text = pygame.font.SysFont('Arial', 18, bold=True).render("BATTLE GAME LOG", True, YELLOW)
    screen.blit(title_text, (console_x + 10, 10))
    
    # Draw console messages
    y_offset = 40
    line_height = 13
    
    for i, message in enumerate(game_console):
        y_pos = y_offset + (i * line_height)
        if y_pos < console_height - 20:  # Don't overflow
            # Trim message if too long for display
            if len(message) > 42:
                display_message = message[:39] + "..."
            else:
                display_message = message
                
            text_surface = console_font.render(display_message, True, WHITE)
            screen.blit(text_surface, (console_x + 5, y_pos))

def player_team_setup():
    """Setup player team with console input"""
    print("=== TEAM SETUP ===")
    print("You will create a team of 3 units.")
    print("Each unit can be either a Warrior or Tank.")
    print()
    
    # Get player name
    while True:
        global player_name
        player_name = input("Enter your name: ").strip()
        if player_name:
            break
        print("Name cannot be empty. Please try again.")
    
    team = []
    positions = [(50, 50), (50, 170), (50, 290)]
    warrior_count = 0
    tank_count = 0
    
    for i in range(3):
        print(f"--- Setting up Unit {i+1} ---")
        
        # Get profession choice
        while True:
            print("Choose profession:")
            print("1. Warrior (High Attack: 5-20, Low Defense: 1-10)")
            print("2. Tank (Low Attack: 1-10, High Defense: 5-15)")
            choice = input("Enter 1 or 2: ").strip()
            
            if choice == "1":
                warrior_count += 1
                unit_name = f"{player_name}_Warrior{warrior_count}"
                unit = Warrior(positions[i][0], positions[i][1], unit_name, "player")
                print(f"Created Warrior '{unit_name}' - ATK: {unit.atk}, DEF: {unit.def_stat}")
                break
            elif choice == "2":
                tank_count += 1
                unit_name = f"{player_name}_Tank{tank_count}"
                unit = Tank(positions[i][0], positions[i][1], unit_name, "player")
                print(f"Created Tank '{unit_name}' - ATK: {unit.atk}, DEF: {unit.def_stat}")
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

def text1(word,x,y):
    font = pygame.font.SysFont(None, 25)
    text = font.render("{}".format(word), True, RED)
    return screen.blit(text,(x,y))

def inpt():
    word=""
    text1("Please enter your name: ",300,400) #example asking name
    pygame.display.flip()
    done = True
    while done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    word+=str(chr(event.key))
                if event.key == pygame.K_b:
                    word+=chr(event.key)
                if event.key == pygame.K_c:
                    word+=chr(event.key)
                if event.key == pygame.K_d:
                    word+=chr(event.key)
                if event.key == pygame.K_RETURN:
                    done=False
                #events...
    return text1(word,700,30)

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
        self.selected = False  # Track if unit is selected
        
        # Visual properties
        self.rect = pygame.Rect(x, y, 80, 100)
        self.image = None
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
        
        # Draw name below unit
        if self.alive:
            unit_font = pygame.font.SysFont('Arial', 12)
            name_text = unit_font.render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.rect.centerx, self.rect.y + self.rect.height + 10))
            screen.blit(name_text, name_rect)
    
    def attack(self, target):
        # Assignment formula: Damage = attacker.ATK – target.DEF + (random between -5 to 10)
        random_factor = random.randint(-5, 10)
        damage = self.atk - target.def_stat + random_factor
        
        # DEBUG: Print the calculation in the log
        print(f"DEBUG: {self.name} ATK({self.atk}) - {target.name} DEF({target.def_stat}) + random({random_factor}) = {damage}")
        
        # Ensure minimum damage of 1 (changed from 0)
        damage = max(1, damage)
        print(f"Final damage: {damage}")
        
        # Apply damage
        target.hp -= damage
        if target.hp <= 0:
            target.hp = 0
            target.alive = False
            log_message(f"{target.name} has been defeated!")
        
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
            log_message(f"{target.name} gains bonus EXP for taking heavy damage!")
        elif damage <= 0:
            # Target gains extra 50% EXP (shouldn't happen with min damage 1)
            bonus_exp = int(target.def_stat * 0.5)
            target.gain_exp(bonus_exp)
            log_message(f"{target.name} gains bonus EXP for strong defense!")
        
        return damage
    
    def gain_exp(self, amount):
        self.exp += amount
        
        # Check for level up (assignment: level up at 100 EXP)
        while self.exp >= 100:
            self.rank += 1
            self.exp -= 100
            log_message(f"{self.name} leveled up! Now Rank {self.rank}")
    
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
        
        self.atk = random.randint(1, 10)
        self.def_stat = random.randint(5, 15)
        
        self.load_image()
    
    def load_image(self):
        # Use the globally loaded images
        if self.team == "player":
            self.image = player_tank_img
        else:  # AI team
            self.image = ai_tank_img

def handle_unit_selection(pos, clicked):
    global selected_unit, game_state, ai_turn_timer, player_attacks_this_round
    
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
                log_message(f"Selected {unit.name} to attack with.")
                return
    
    elif game_state == "select_target":
        # Player is selecting target to attack
        for unit in ai_team:
            if unit.rect.collidepoint(pos) and unit.alive:
                if selected_unit and selected_unit.alive:
                    # Execute attack
                    damage = selected_unit.attack(unit)
                    player_attacks_this_round += 1
                    
                    # Log the attack
                    log_message(f"{selected_unit.name} attacks {unit.name} for {damage} damage!")
                    log_message(f"Player attacks this round: {player_attacks_this_round}/{max_attacks_per_round}")
                    
                    # Deselect unit
                    selected_unit.selected = False
                    selected_unit = None
                    
                    # Check if AI team is defeated
                    alive_ai = sum(1 for u in ai_team if u.alive)
                    if alive_ai == 0:
                        global game_over
                        game_over = 1
                        return
                    
                    # Check if all player units have attacked this round
                    if player_attacks_this_round >= max_attacks_per_round:
                        game_state = "ai_turn"
                        ai_turn_timer = pygame.time.get_ticks()
                        player_attacks_this_round = 0  # Reset for next round
                        log_message("=== AI TURN BEGINS ===")
                    else:
                        game_state = "select_attacker"
                        alive_players = sum(1 for u in player_team if u.alive)
                        remaining_attacks = min(max_attacks_per_round - player_attacks_this_round, alive_players)
                        log_message(f"Select next unit! ({remaining_attacks} attacks remaining)")
                    
                    return
        
        # If clicked somewhere else, allow reselecting attacker
        if selected_unit:
            selected_unit.selected = False
            selected_unit = None
            game_state = "select_attacker"
            log_message("Attack cancelled. Select a unit to attack with.")

def ai_turn():
    """Handle AI turn - All AI units attack in sequence"""
    global game_state, ai_turn_timer
    
    # Get all alive AI units
    alive_ai_units = [unit for unit in ai_team if unit.alive]
    alive_player_units = [unit for unit in player_team if unit.alive]
    
    if not alive_ai_units or not alive_player_units:
        game_state = "select_attacker"
        return
    
    # Each alive AI unit attacks once
    for ai_unit in alive_ai_units:
        if not alive_player_units:  # Check if any players still alive
            break
            
        # AI Strategy: Target weakest player unit (lowest HP)
        target = min(alive_player_units, key=lambda unit: unit.hp)
        
        # Execute attack
        damage = ai_unit.attack(target)
        log_message(f"AI ATTACK: {ai_unit.name} attacks {target.name} for {damage} damage!")
        
        # Remove from alive list if killed
        if not target.alive:
            alive_player_units.remove(target)
            log_message(f"{target.name} has been defeated!")
    
    # Check if player team is defeated
    alive_players = sum(1 for u in player_team if u.alive)
    if alive_players == 0:
        global game_over
        game_over = -1
        return
    
    # Return to player turn
    game_state = "select_attacker"
    log_message("=== PLAYER ROUND BEGINS ===")
    log_message("Select your first unit to attack with!")

def draw_instructions():
    if game_state == "select_attacker":
        remaining = max_attacks_per_round - player_attacks_this_round
        alive_players = sum(1 for u in player_team if u.alive)
        remaining = min(remaining, alive_players)
        instruction = f"Your Turn: Select unit to attack ({remaining} attacks left this round)"
    elif game_state == "select_target":
        instruction = f"Selected: {selected_unit.name}. Click enemy to attack."
    elif game_state == "ai_turn":
        instruction = "AI Turn: All AI units attacking..."
    
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

# Setup teams AFTER images are loaded
player_team, ai_team = main()

# Initialize game log
log_message("=== GAME STARTED ===")
log_message("Battle begins!")

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
game_state = "select_attacker"  # "select_attacker", "select_target", or "ai_turn"
ai_turn_timer = 0  # Timer for AI turn delay

# Round-based turn management
player_attacks_this_round = 0  # Track how many player units have attacked
max_attacks_per_round = 3  # All 3 units must attack before AI turn

#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))

def log_message(message):
    """Add message to game console and log file"""
    import datetime
    
    # Add timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    console_message = f"[{timestamp}] {message}"
    
    # Add to console display
    game_console.append(console_message)
    
    # Keep only recent messages for display
    if len(game_console) > max_console_lines:
        game_console.pop(0)
    
    # Write to log file
    try:
        with open("game_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(console_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
    
    # Also print to console for debugging
    print(console_message)

def draw_console():
    """Draw the game console panel"""
    console_x = 800  # Start after main game area
    console_y = 0
    console_width = console_panel
    console_height = screen_height
    
    # Draw console background
    pygame.draw.rect(screen, GRAY, (console_x, console_y, console_width, console_height))
    pygame.draw.rect(screen, WHITE, (console_x, console_y, console_width, console_height), 2)
    
    # Draw console title
    title_text = font.render("GAME LOG", True, WHITE)
    screen.blit(title_text, (console_x + 10, 10))
    
    # Draw console messages
    y_offset = 50
    line_height = 15
    
    for i, message in enumerate(game_console):
        if y_offset + (i * line_height) < console_height - 20:  # Don't overflow
            # Split long messages if needed
            if len(message) > 35:
                # Split message into multiple lines
                words = message.split()
                current_line = ""
                lines = []
                
                for word in words:
                    if len(current_line + word) < 70:
                        current_line += word + " "
                    else:
                        if current_line:
                            lines.append(current_line.strip())
                        current_line = word + " "
                
                if current_line:
                    lines.append(current_line.strip())
                
                # Draw each line
                for line_num, line in enumerate(lines):
                    text_surface = console_font.render(line, True, WHITE)
                    screen.blit(text_surface, (console_x + 5, y_offset + (i * line_height) + (line_num * line_height)))
                    if line_num > 0:
                        i += 1  # Adjust spacing for wrapped lines
            else:
                text_surface = console_font.render(message, True, WHITE)
                screen.blit(text_surface, (console_x + 5, y_offset + (i * line_height)))

#function for drawing panel - UPDATED for teams
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	
	# Draw player team stats
	draw_text(player_name + " TEAM", font, RED, 20, screen_height - bottom_panel + 10)
	for i, unit in enumerate(player_team):
		y_pos = screen_height - bottom_panel + 35 + (i * 25)
		status = "ALIVE" if unit.alive else "DEAD"
		draw_text(f'{unit.name}: HP {unit.hp}/{unit.max_hp} ATK {unit.atk} DEF {unit.def_stat} EXP {unit.exp} [{status}]', 
				 pygame.font.SysFont('Arial', 14), RED, 20, y_pos)
	
	# Draw AI team stats
	draw_text("ENEMY TEAM", font, RED, 450, screen_height - bottom_panel + 10)
	for i, unit in enumerate(ai_team):
		y_pos = screen_height - bottom_panel + 35 + (i * 25)
		status = "ALIVE" if unit.alive else "DEAD"
		draw_text(f'{unit.name}: HP {unit.hp}/{unit.max_hp} [{status}]', 
				 pygame.font.SysFont('Arial', 14), RED, 450, y_pos)

#create buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw console
	draw_console()

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

	# Handle AI turn with delay
	if game_state == "ai_turn":
		if pygame.time.get_ticks() - ai_turn_timer > 3000: # Wait 3 seconds before AI acts (so player can see what happened)
			ai_turn()

	#control player actions (only during player turns)
	if game_state in ["select_attacker", "select_target"]:
		target = None
		#make sure mouse is visible
		pygame.mouse.set_visible(True)
		pos = pygame.mouse.get_pos()
		
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
			# Process click immediately in event loop
			if game_state in ["select_attacker", "select_target"]:
				pos = pygame.mouse.get_pos()
				handle_unit_selection(pos, True)

	pygame.display.update()

pygame.quit()