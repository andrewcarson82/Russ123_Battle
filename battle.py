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
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
#potion = False
#potion_effect = 15
clicked = False
game_over = 0


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


#function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	for count, i in enumerate(bandit_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)


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
        
        # Draw background rectangle
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border
        
        # Draw unit image if it exists
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect)
        
        # Draw name below unit
        font = pygame.font.SysFont('Arial', 16)
        name_text = font.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.rect.centerx, self.rect.y + self.rect.height + 10))
        screen.blit(name_text, name_rect)
    
    def attack(self, target):
        # Assignment formula: Damage = attacker.ATK – target.DEF + (random between -5 to 10)
        random_factor = random.randint(-5, 10)
        damage = self.atk - target.def_stat + random_factor
        
        # Ensure damage isn't negative (minimum 0)
        damage = max(0, damage)
        
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


# Warrior subclass
class Warrior(Fighter):
    def __init__(self, x, y, name, team="player"):
        super().__init__(x, y, name, team)
        
        # Assignment specs: ATK 5-20, DEF 1-10
        self.atk = random.randint(5, 20)
        self.def_stat = random.randint(1, 10)
        
        self.load_image()
    
    def load_image(self):
        try:
            if self.team == "player":
                self.image = pygame.image.load('img/player_warrior.png').convert_alpha()
            else:  # AI team
                self.image = pygame.image.load('img/ai_warrior.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
        except:
            # Fallback to colored rectangles
            self.image = pygame.Surface((60, 80))
            if self.team == "player":
                self.image.fill((255, 200, 100))  # Orange for player warrior
            else:
                self.image.fill((200, 100, 50))   # Dark orange for AI warrior


# tank subclass  
class Tank(Fighter):
    def __init__(self, x, y, name, team="player"):
        super().__init__(x, y, name, team)
        
        # Assignment specs: ATK 1-10, DEF 5-15
        self.atk = random.randint(1, 10)
        self.def_stat = random.randint(5, 15)
        
        self.load_image()
    
    def load_image(self):
        try:
            if self.team == "player":
                self.image = pygame.image.load('img/player_tank.png').convert_alpha()
            else:  # AI team
                self.image = pygame.image.load('img/ai_tank.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 80))
        except:
            # Fallback to colored rectangles
            self.image = pygame.Surface((60, 80))
            if self.team == "player":
                self.image.fill((100, 200, 255))  # Blue for player Tank
            else:
                self.image.fill((50, 100, 200))   # Dark blue for AI Tank


# Health Bar class (simplified)
class HealthBar:
    def __init__(self, x, y, max_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.width = 100
        self.height = 10
    
    def draw(self, screen, current_hp):
        # Calculate health ratio
        ratio = max(0, current_hp / self.max_hp)
        
        # Draw background (red)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
        # Draw current health (green)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width * ratio, self.height))
        
        # Draw border
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)


# Example usage for creating teams:
def create_player_team():
    # This would be called from your setup screen
    team = []
    # You'll replace this with user input later
    team.append(Warrior(100, 20, "Player1"))
    team.append(Tank(100, 140, "Player2")) 
    team.append(Warrior(100, 260, "Player3"))
    return team

def create_ai_team():
    team = []
    positions = [(600, 20), (600, 140), (600, 260)]
    
    for i, (x, y) in enumerate(positions):
        # Random profession for AI
        if random.choice([True, False]):
            unit = Warrior(x, y, f"AI{random.randint(10, 99)}", "ai")
        else:
            unit = Tank(x, y, f"AI{random.randint(10, 99)}", "ai")
        team.append(unit)
    
    return team


player_team = create_player_team()
ai_team = create_ai_team()

#create buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
#	draw_panel()
#	knight_health_bar.draw(knight.hp)
#	bandit1_health_bar.draw(bandit1.hp)
#	bandit2_health_bar.draw(bandit2.hp)

	#draw fighters
	for unit in player_team:
		unit.draw(screen)
	for unit in ai_team:
		unit.draw(screen)

# 	#draw the damage text
# 	damage_text_group.update()
# 	damage_text_group.draw(screen)

	#control player actions
	#reset action variables
#	attack = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
# 	for count, bandit in enumerate(bandit_list):
# 		if bandit.rect.collidepoint(pos):
# 			#hide mouse
# 			pygame.mouse.set_visible(False)
# 			#show sword in place of mouse cursor
# 			screen.blit(sword_img, pos)
# 			if clicked == True and bandit.alive == True:
# 				attack = True
# 				target = bandit_list[count]



# 	if game_over == 0:
# 		#player action
# 		if knight.alive == True:
# 			if current_fighter == 1:
# 				action_cooldown += 1
# 				if action_cooldown >= action_wait_time:
# 					#look for player action
# 					#attack
# 					if attack == True and target != None:
# 						knight.attack(target)
# 						current_fighter += 1
# 						action_cooldown = 0
# 		else:
# 			game_over = -1


# 		#enemy action
# 		for count, bandit in enumerate(bandit_list):
# 			if current_fighter == 2 + count:
# 				if bandit.alive == True:
# 					action_cooldown += 1
# 					if action_cooldown >= action_wait_time:
# 						#attack
# # 						else:
# # 							bandit.attack(knight)
# # 							current_fighter += 1
#  							#action_cooldown = 0
# 							current_fighter += 1
# 							action_cooldown = 0

# 		#if all fighters have had a turn then reset
# 		if current_fighter > total_fighters:
# 			current_fighter = 1


# 	#check if all bandits are dead
# 	alive_bandits = 0
# 	for bandit in bandit_list:
# 		if bandit.alive == True:
# 			alive_bandits += 1
# 	if alive_bandits == 0:
# 		game_over = 1


# 	#check if game is over
# 	if game_over != 0:
# 		if game_over == 1:
# 			screen.blit(victory_img, (250, 50))
# 		if game_over == -1:
# 			screen.blit(defeat_img, (290, 50))
# 		if restart_button.draw():
# 			knight.reset()
# 			for bandit in bandit_list:
# 				bandit.reset()
# 			current_fighter = 1
# 			action_cooldown
# 			game_over = 0



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()

