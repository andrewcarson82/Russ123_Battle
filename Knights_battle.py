import pygame
import random
import button
import logging

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
font = pygame.font.SysFont('Times New Roman', 26)
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

#define game variables
current_fighter = 1
total_fighters = 6  # 3 knights + 3 bandits
action_cooldown = 0
action_wait_time = 90
attack = False
#potion = False
#potion_effect = 15
clicked = False
game_over = 0

#load images
#background image
background_img = pygame.image.load('img/Background/bg_swamp800.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel_800_200.png').convert_alpha()
#button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
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
        with open("Knight_Battle_game_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(console_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def draw_console():
    """Draw the game console on the right side"""
    console_x = 800  # Start console after main game area
    console_y = 0
    console_width = console_panel
    console_height = screen_height
    
    # Draw console background
    pygame.draw.rect(screen, GRAY, (console_x, console_y, console_width, console_height))
    
    # Draw console border
    pygame.draw.rect(screen, WHITE, (console_x, console_y, console_width, console_height), 2)
    
    # Draw console title
    draw_text("BATTLE LOG", font, WHITE, console_x + 10, 10)
    
    # Draw console messages
    for i, message in enumerate(game_console):
        if i < max_console_lines:
            y_pos = 50 + (i * 15)
            draw_text(message, console_font, WHITE, console_x + 10, y_pos)

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
	for count, i in enumerate(knight_list):
		#show name and health
		draw_text(f'{i.name} {count+1} HP: {i.hp}', font, RED, 100, (screen_height - bottom_panel + 10) + count * 50)
	for count, i in enumerate(bandit_list):
		#show name and health
		draw_text(f'{i.name} {count+1} HP: {i.hp}', font, RED, 450, (screen_height - bottom_panel + 10) + count * 50)

#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, attackval, defpoint, exp):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.attackval = attackval
		self.defpoint = defpoint
		self.exp = exp
#		self.start_potions = potions
#		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.attackval + rand
		target.hp -= damage
		#log the attack
		log_message(f"{self.name} attacks {target.name} for {damage} damage!")
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
			log_message(f"{target.name} has been defeated!")
		# Set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def reset (self):
		self.alive = True
#		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def draw(self):
		screen.blit(self.image, self.rect)

class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0

	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()

damage_text_group = pygame.sprite.Group()

# Create fighters - 3 knights and 3 bandits
knight1 = Fighter(100, 260, 'Knight1', 100, random.randint(15,25), 20, 20)
knight2 = Fighter(250, 260, 'Knight2', 100, random.randint(15,25), 20, 20)
knight3 = Fighter(400, 260, 'Knight3', 100, random.randint(15,25), 20, 20)
bandit1 = Fighter(550, 270, 'Bandit1', 100, random.randint(8,15), 20, 20)
bandit2 = Fighter(700, 270, 'Bandit2', 100, random.randint(8,15), 20, 20)
bandit3 = Fighter(850, 270, 'Bandit3', 100, random.randint(8,15), 20, 20)

knight_list = []
knight_list.append(knight1)
knight_list.append(knight2)
knight_list.append(knight3)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)
bandit_list.append(bandit3)

# Create health bars for all fighters
knight1_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight1.hp, knight1.max_hp)
knight2_health_bar = HealthBar(100, screen_height - bottom_panel + 90, knight2.hp, knight2.max_hp)
knight3_health_bar = HealthBar(100, screen_height - bottom_panel + 140, knight3.hp, knight3.max_hp)

bandit1_health_bar = HealthBar(450, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(450, screen_height - bottom_panel + 90, bandit2.hp, bandit2.max_hp)
bandit3_health_bar = HealthBar(450, screen_height - bottom_panel + 140, bandit3.hp, bandit3.max_hp)

#create buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

# Initialize game log
log_message("Battle started! Knights vs Bandits")

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()
	
	#draw console
	draw_console()

	#draw panel
	draw_panel()
	knight1_health_bar.draw(knight1.hp)
	knight2_health_bar.draw(knight2.hp)
	knight3_health_bar.draw(knight3.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)
	bandit3_health_bar.draw(bandit3.hp)

	#draw fighters
	for knight in knight_list:
		knight.update()
		knight.draw()
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()

	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)

	#control player actions
	#reset action variables
	attack = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, bandit in enumerate(bandit_list):
		if bandit.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
			if clicked == True and bandit.alive == True:
				attack = True
				target = bandit_list[count]

	if game_over == 0:
		# Debug: show current fighter
		draw_text(f"Current Fighter: {current_fighter}", font, RED, 10, 10)
		
		#player action (Knights turn 1, 2, and 3)
		alive_knights = [knight for knight in knight_list if knight.alive]
		
		if len(alive_knights) > 0:
			# Handle knight turns (fighters 1, 2, and 3)
			if current_fighter >= 1 and current_fighter <= 3:
				current_knight_index = current_fighter - 1
				if current_knight_index < len(knight_list) and knight_list[current_knight_index].alive:
					action_cooldown += 1
					# Show whose turn it is
					draw_text(f"{knight_list[current_knight_index].name} {current_knight_index + 1}'s turn", font, YELLOW, 10, 40)
					if action_cooldown >= action_wait_time:
						#look for player action
						#attack
						if attack == True and target != None:
							knight_list[current_knight_index].attack(target)
							current_fighter += 1
							action_cooldown = 0
				else:
					# If this knight is dead, skip to next fighter
					current_fighter += 1
					action_cooldown = 0
		else:
			game_over = -1

		#enemy action (Bandit turns 4, 5, and 6)
		if current_fighter == 4:  # First bandit
			if bandit_list[0].alive == True:
				action_cooldown += 1
				draw_text(f"{bandit_list[0].name} 1's turn", font, YELLOW, 10, 40)
				if action_cooldown >= action_wait_time:
					#attack a random alive knight
					alive_knights = [knight for knight in knight_list if knight.alive]
					if len(alive_knights) > 0:
						target_knight = random.choice(alive_knights)
						bandit_list[0].attack(target_knight)
					current_fighter += 1
					action_cooldown = 0
			else:
				# If this bandit is dead, skip to next fighter
				current_fighter += 1
				action_cooldown = 0
				
		elif current_fighter == 5:  # Second bandit
			if bandit_list[1].alive == True:
				action_cooldown += 1
				draw_text(f"{bandit_list[1].name} 2's turn", font, YELLOW, 10, 40)
				if action_cooldown >= action_wait_time:
					#attack a random alive knight
					alive_knights = [knight for knight in knight_list if knight.alive]
					if len(alive_knights) > 0:
						target_knight = random.choice(alive_knights)
						bandit_list[1].attack(target_knight)
					current_fighter += 1
					action_cooldown = 0
			else:
				# If this bandit is dead, skip to next fighter
				current_fighter += 1
				action_cooldown = 0
				
		elif current_fighter == 6:  # Third bandit
			if bandit_list[2].alive == True:
				action_cooldown += 1
				draw_text(f"{bandit_list[2].name} 3's turn", font, YELLOW, 10, 40)
				if action_cooldown >= action_wait_time:
					#attack a random alive knight
					alive_knights = [knight for knight in knight_list if knight.alive]
					if len(alive_knights) > 0:
						target_knight = random.choice(alive_knights)
						bandit_list[2].attack(target_knight)
					current_fighter += 1
					action_cooldown = 0
			else:
				# If this bandit is dead, skip to next fighter
				current_fighter += 1
				action_cooldown = 0

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1
			action_cooldown = 0  # Reset cooldown for new round
			log_message("--- New Round ---")

	#check if all bandits are dead
	alive_bandits = 0
	for bandit in bandit_list:
		if bandit.alive == True:
			alive_bandits += 1
	if alive_bandits == 0:
		game_over = 1
		log_message("Victory! All bandits defeated!")

	#check if all knights are dead
	alive_knights = 0
	for knight in knight_list:
		if knight.alive == True:
			alive_knights += 1
	if alive_knights == 0:
		game_over = -1
		log_message("Defeat! All knights have fallen!")

	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			for knight in knight_list:
				knight.reset()
			for bandit in bandit_list:
				bandit.reset()
			current_fighter = 1
			action_cooldown = 0
			game_over = 0
			game_console.clear()  # Clear console on restart
			log_message("Battle restarted!")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()