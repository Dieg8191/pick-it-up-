import pygame
from pygame.sprite import Group
from ..util.support import load_image
from .action import Action

class Player(pygame.sprite.Sprite):
	def __init__(self, position: pygame.Vector2, groups: list, obstacle_sprites: Group, trash_srpites: Group, grass_srpites: Group, create_player_action: callable, destroy_player_action:callable) -> None:
		super().__init__(groups)
		self.animations = {
			"down": {
				"idle": [load_image("graphics/player/down_idle/idle_down.png")],
				"action": [load_image("graphics/player/down_attack/attack_down.png")],
				"walk": [
					load_image("graphics/player/down/down_0.png"),
					load_image("graphics/player/down/down_1.png"),
					load_image("graphics/player/down/down_2.png"),
					load_image("graphics/player/down/down_3.png"),
				]
			},
			"up": {
				"idle": [load_image("graphics/player/up_idle/idle_up.png")],
				"action": [load_image("graphics/player/up_attack/attack_up.png")],
				"walk": [
					load_image("graphics/player/up/up_0.png"),
					load_image("graphics/player/up/up_1.png"),
					load_image("graphics/player/up/up_2.png"),
					load_image("graphics/player/up/up_3.png"),
				]
			},
			"left": {
				"idle": [load_image("graphics/player/left_idle/idle_left.png")],
				"action": [load_image("graphics/player/left_attack/attack_left.png")],
				"walk": [
					load_image("graphics/player/left/left_0.png"),
					load_image("graphics/player/left/left_1.png"),
					load_image("graphics/player/left/left_2.png"),
					load_image("graphics/player/left/left_3.png"),
				]
			},
			"right": {
				"idle": [load_image("graphics/player/right_idle/idle_right.png")],
				"action": [load_image("graphics/player/right_attack/attack_right.png")],
				"walk": [
					load_image("graphics/player/right/right_0.png"),
					load_image("graphics/player/right/right_1.png"),
					load_image("graphics/player/right/right_2.png"),
					load_image("graphics/player/right/right_3.png"),
				]
			},
			"action": {
				"sword": {
					"down": load_image("graphics/sword/down.png"),
					"up": load_image("graphics/sword/up.png"),
					"left": load_image("graphics/sword/left.png"),
					"right": load_image("graphics/sword/right.png"),
				},
				"collector": {
					"up": load_image("graphics/collector/up.png"),
					"down": load_image("graphics/collector/down.png"),
					"left": load_image("graphics/collector/left.png"),
					"right": load_image("graphics/collector/right.png"),
				}
			}
		}

		self.obstacle_sprites = obstacle_sprites
		self.grass_sprites = grass_srpites

		self.image = self.animations["down"]["idle"][0]
		self.rect = self.image.get_rect(center=position)
		
		self.hitbox = self.rect.inflate(-self.rect.width * 0.3, -self.rect.height * 0.2)
		self.hitbox.center = self.rect.center

		self.create_player_action = create_player_action
		self.destroy_player_action = destroy_player_action

		self.speed = 300 # pixels per second
		self.move_vector = pygame.math.Vector2()
		self.real_pos = pygame.math.Vector2(self.rect.topleft)
  
		# animations
		self.state = 'idle'
		self.direction = 'down'
		self.animation_time_target = 0.15 # seconds
		self.current_animation_time = 0.0
		self.animation_index = 0

		self.action = None
		self.action_time = 0.25 # seconds
		self.current_action_time = 0.0

		# Action cooldown

		self.action_cooldown =self.action_time + 0.15 # seconds
		self.current_action_cooldown = 0.0
		self.on_action_cooldown = False

		# Action
		self.selected_action = "sword"

	def cooldowns(self, dt: float) -> None:
		if self.on_action_cooldown:
			self.current_action_cooldown += dt
			if self.current_action_cooldown >= self.action_cooldown:
				self.on_action_cooldown = False
				self.current_action_cooldown = 0.0

		if self.state == "action":
			self.current_action_time += dt
			if self.current_action_time >= self.action_time:
				self.state = "idle"
				self.destroy_player_action()

	def pick_up(self) -> None:
		pass

	def destroy_grass(self, dt: float) -> None:
		self.state = "action"
		self.current_action_time = 0

		action = Action(self.animations["action"][self.selected_action][self.direction], self.selected_action, self.direction, self)

		self.create_player_action(action_type=self.selected_action, sprite=action)

	def update(self, dt: float) -> None:
		self.handle_input(dt)
		self.animate(dt)
		self.cooldowns(dt)

	def animate(self, dt: float) -> None:
		self.current_animation_time += dt

		if (self.current_animation_time >= self.animation_time_target):
			if self.state == 'walk':
				self.current_animation_time = 0.0
				self.animation_index += 1
				if self.animation_index >= len(self.animations[self.direction][self.state]):
					self.animation_index = 0

		if self.state == 'walk':
			self.image = self.animations[self.direction][self.state][self.animation_index]
		elif self.state == 'idle':
			self.image = self.animations[self.direction][self.state][0]
		elif self.state == 'action':
			self.image = self.animations[self.direction]["action"][0]

	def check_collisions(self, axis: str) -> None:
		if axis == 'x':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.move_vector.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.move_vector.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right
				
		elif axis == 'y':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.move_vector.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.move_vector.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

		else:
			raise ValueError("Axis must be 'x' or 'y'")
		
	def move(self, dt: float):
		if self.move_vector.magnitude() != 0:
			self.move_vector = self.move_vector.normalize()

		self.hitbox.x += self.move_vector.x * self.speed * dt
		self.check_collisions('x')
		self.hitbox.y += self.move_vector.y * self.speed * dt
		self.check_collisions('y')
		self.rect.center = self.hitbox.center

	def handle_input(self, dt: float) -> None:
		keys = pygame.key.get_pressed()
  
		if self.state != "action":
			self.state = 'idle'

			if keys[pygame.K_w]:
				self.move_vector.y = - 1
				self.state = 'walk'
				self.direction = 'up'
			elif keys[pygame.K_s]:
				self.move_vector.y = 1
				self.state = 'walk'
				self.direction = 'down'
			else:
				self.move_vector.y = 0

			if keys[pygame.K_a]:
				self.move_vector.x = - 1
				self.state = 'walk'
				self.direction = 'left'
			elif keys[pygame.K_d]:
				self.move_vector.x = 1
				self.state = 'walk'
				self.direction = 'right'
			else:
				self.move_vector.x = 0

			self.move(dt)

			if keys[pygame.K_SPACE] and not self.on_action_cooldown:
				self.state = "action"
				self.on_action_cooldown = True
				self.destroy_grass(dt)
				
 

