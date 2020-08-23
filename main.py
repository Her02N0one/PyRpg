import pygame
import sys
import os
import json
from math import ceil

# TODO: Add a camera class or something like that to move around the screen with the player. \
#       after that I'll begin working on the tilemap integration.

# Position the window so that it's fully visible and not in a weird spot
position = 150, 100
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])


def end():
	pygame.quit()
	sys.exit(0)


def main(screen_width, screen_height):
	display = pygame.display.set_mode((screen_width * 2, screen_height * 2))
	screen = pygame.Surface((screen_width, screen_height))
	enter_level(screen, display, 2000, 2000)


def enter_level(
		screen:       pygame.Surface,
		display:      pygame.Surface,
		level_width:  int,
		level_height: int,
		tilemap:      str = None
	):
	"""
	This will be where all the game stuff goes
	every time a different map is loaded, this function is called.
	Note: As of right now its not very flexible.

	:param screen: pygame.Surface
	the screen is the surface that will be rendered to.
	:param display: pygame.Surface
	the display is the actual window.
	it should be larger than the screen and the screen surface should be scaled to fit it
	:param level_width: int
	width of the level. this can be larger than the width of the screen
	:param level_height: int
	same as level_width but with height
	:param tilemap: string
	The location of the tilemap to be loaded. The top left corner will always be loaded at (0, 0)
	:return: None
	"""

	clock = pygame.time.Clock()
	level = pygame.Surface((level_width, level_height))

	with open("data/assets/spritesheets/Character_2_anim.json") as json_file:
		animation_data = json.load(json_file)
		player_spritesheet = pygame.image.load("data/assets/spritesheets/"+animation_data["spritesheet"])

	player = { 	# Normally you'd use a class for this. I don't feel like doing that though lol.
		"pos": pygame.Vector2(),
		"vel": pygame.Vector2(),
		"direction": pygame.Vector2(),
		"facing": "down",
		"moving": False,
		"rect": pygame.Rect(0, 0, 16, 32),
		"speed": 50,
	}

	# Animation timer. goes up by 0.1 every frame. (Never resets, maybe it will in the future)
	# I guess this could technically cause a memory leak.
	# Good thing I'm using Python
	animation = 0

	while True:
		dt = clock.tick(60) / 1000

		""" Update Pygame Events """

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				end()

			# TODO: Implement a better player movement system by using a stack of inputs. This will work for now though.
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:  # up
					player["facing"] = "up"
					player["direction"].y = -1
				if event.key == pygame.K_a:  # left
					player["facing"] = "left"
					player["direction"].x = -1
				if event.key == pygame.K_d:  # right
					player["facing"] = "right"
					player["direction"].x = 1
				if event.key == pygame.K_s:  # down
					player["facing"] = "down"
					player["direction"].y = 1

			# If the player releases a directional key, stop moving in that direction
			# TODO: this system doesn't work well with the animation system and needs to be updated
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					player["direction"].y = 0
				if event.key == pygame.K_a:
					player["direction"].x = 0
				if event.key == pygame.K_d:
					player["direction"].x = 0
				if event.key == pygame.K_s:
					player["direction"].y = 0

		""" Update """

		# Player Collision / Interaction with map and objects
		player["moving"] = False if (player["direction"].x == 0 and player["direction"].y == 0) else True

		# I may add acceleration to this. but honestly, I don't think I'd need it for anything
		if player["moving"]:
			player["vel"] = player["direction"].normalize()
			player["pos"].x += (player["vel"].x * dt) * player["speed"]
			player["pos"].y += (player["vel"].y * dt) * player["speed"]
			player["rect"].x, player["rect"].y = int(player["pos"].x), int(player["pos"].y)

		""" Render """

		animation += 0.1
		screen.fill(0)

		if player["moving"]:
			# Draw the walking sprite in the direction the player is walking
			screen.blit(
					player_spritesheet.subsurface(
							animation_data["walk"][player["facing"]][ceil(animation) % animation_data["walk"]["frames"]]
					),
					player["rect"]
			)
		else:
			# Draw the idle sprite in the direction the player is facing
			screen.blit(
					player_spritesheet.subsurface(
							animation_data["idle"][player["facing"]]
					),
					player["rect"]
			)

		display.blit(pygame.transform.scale(screen, (display.get_width(), display.get_height())), (0, 0))
		pygame.display.flip()


if __name__ == '__main__':
	width, height = 500, 300
	main(width, height)
