from random import choice
from .util.ui import UI
import pygame

from .entity.player import Player
from .util.camera import Camera
from .util.support import import_csv_layout, import_folder, TextRenderer
from .objects.tile import Tile
from .objects.grass import Grass
from .objects.trash import Trash
from .util.animation import Animation
from .util.scoreSystem import ScoreSystem
from random import randint

class Game:
	def __init__(self) -> None:
		self.screen = pygame.display.get_surface()
		self.clock = pygame.time.Clock()
		self.debug = False
		self.running = True
		self.show_rects = False
		self.text_renderer = TextRenderer()

		self.animation = Animation()
		self.paused = False

		# Level
		self.camera = Camera()
		self.update_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()
		self.trash_sprites = pygame.sprite.Group()
		self.grass_sprites = pygame.sprite.Group()
		self.action = None
		self.player = None
		self.create_map()
		
		game_time = 120
		self.score_system = ScoreSystem(len(self.grass_sprites), len(self.grass_sprites), game_time)

		# UI
		self.ui = UI(self.player, self.trash_sprites, self.text_renderer, self.finish_game, game_time)

	def finish_game(self):
		pass

	def handle_events(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
     
				if event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()

				if event.key == pygame.K_p:
					self.paused = not self.paused
				
				if event.key == pygame.K_F3:
					self.debug = not self.debug

				if  event.key == pygame.K_F2:
						self.show_rects = not self.show_rects

				if event.key == pygame.K_q:
					if self.player.selected_action == "sword":
						self.player.selected_action = "collector"
					else: 
						self.player.selected_action = "sword"

	def update(self) -> None:
		if not self.paused:
			self.update_sprites.update(dt=self.get_dt())
			self.ui.update(self.get_dt())

		if len(self.trash_sprites) <= 0:
			self.finish_game()

	def get_dt(self) -> float:
		return self.clock.get_time() / 1000.0

	def draw(self) -> None:
		self.screen.fill("#71ddee")

		# draw game elements
		self.camera.center_target_camera(self.player)
		self.camera.custom_draw()
		self.ui.draw()

		if self.debug:
			self.text_renderer.render(f"FPS: {int(self.clock.get_fps())}", (10, 100), (255, 255, 255), (0, 0, 0))

		if self.show_rects:
			self.camera.draw_rects()

		pygame.display.flip()

	def create_player_action(self, action_type: str, sprite: pygame.sprite.Sprite) -> None:
		self.action = sprite
		self.action.add(self.camera)

		if action_type == "sword":
			hits = pygame.sprite.spritecollide(self.action, self.grass_sprites, False)
			for grass in hits:
				pos = grass.rect.center
				offset = pygame.math.Vector2(0,75)
				for _ in range(randint(3,6)):
					self.animation.create_grass_particles(pos - offset,[self.camera, self.update_sprites])

				grass.kill()
		else:
			hits = pygame.sprite.spritecollide(self.action, self.trash_sprites, False)

			if hits:
				hits[0].kill()

	def destroy_player_action(self) -> None:
		self.action.kill()
		self.action = None

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('map/map_Grass.csv'),
			'object': import_csv_layout('map/map_Objects.csv'),
			'entities': import_csv_layout('map/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('graphics/Grass'),
			'objects': import_folder('graphics/objects'),
			'trash': import_folder('graphics/trash')
		}

		trash_images = import_folder('graphics/trash')

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * 64
						y = row_index * 64
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							if not randint(0, 100) <= 40:
								random_grass_image = choice(graphics['grass'])
								Grass(
									(x,y),
									[self.camera,self.obstacle_sprites,self.grass_sprites],
									random_grass_image)
							else: 
								random_trash_image = choice(trash_images)
								Trash(
									[self.camera, self.obstacle_sprites, self.trash_sprites],
									(x, y),
									random_trash_image
								)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y), [self.camera,self.obstacle_sprites], "object", surf)

						if style == 'entities':
							if col == '394':
								self.player = Player(
									(x,y),
									[self.camera, self.update_sprites],
									self.obstacle_sprites,
									self.trash_sprites,
									self.grass_sprites,
									self.create_player_action,
									self.destroy_player_action)

	def run(self) -> str:
		while self.running:
			self.handle_events()
			self.update()
			self.draw()
			self.clock.tick(60)

		return "exit"
	