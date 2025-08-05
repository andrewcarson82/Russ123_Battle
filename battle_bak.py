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
player_warrior_img = pygame.image.load('img/Player/player_warrior.png').convert_alpha()
player_tank_img = pygame.image.load('img/Player/player_tank.png').convert_alpha()
#Scaling
player_warrior_img = pygame.transform.scale(player_warrior_img, (60, 80))
player_tank_img = pygame.transform.scale(player_tank_img, (60, 80))
#Enemy_img
enemy_warrior_img = pygame.image.load('img/Enemy/enemy_warrior.png').convert_alpha()
enemy_tank_img = pygame.image.load('img/Enemy/enemy_tank.png').convert_alpha()
#Scaling
enemy_warrior_img = pygame.transform.scale(enemy_warrior_img, (60, 80))
enemy_tank_img = pygame.transform.scale(enemy_tank_img, (60, 80))
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
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.alive = True
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, screen, team_color):
		# Draw rectangle background first
		pygame.draw.rect(screen, team_color, self.rect)
		pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Black border

		# Overlay unit image
		image_rect = self.image.get_rect(center=self.rect.center)
		screen.blit(self.image, image_rect)
	
		# Draw name below
		name_text = font.render(self.name, True, (255, 255, 255))
		screen.blit(name_text, (self.rect.x, self.rect.y + self.rect.height + 5))


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
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


knight = Fighter(200, 260, 'Knight', 3, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)

	#draw fighters
	knight.update()
	knight.draw()
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()

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
		#player action
		if knight.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action
					#attack
					if attack == True and target != None:
						knight.attack(target)
						current_fighter += 1
						action_cooldown = 0
		else:
			game_over = -1


		#enemy action
		for count, bandit in enumerate(bandit_list):
			if current_fighter == 2 + count:
				if bandit.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#attack
# 						else:
# 							bandit.attack(knight)
# 							current_fighter += 1
 							#action_cooldown = 0
							current_fighter += 1
							action_cooldown = 0

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1


	#check if all bandits are dead
	alive_bandits = 0
	for bandit in bandit_list:
		if bandit.alive == True:
			alive_bandits += 1
	if alive_bandits == 0:
		game_over = 1


	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			knight.reset()
			for bandit in bandit_list:
				bandit.reset()
			current_fighter = 1
			action_cooldown
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

