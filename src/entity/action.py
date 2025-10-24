import pygame



class Action(pygame.sprite.Sprite):
	def __init__(self, img: pygame.Surface, action_type: str, direction: str, player: pygame.sprite.Sprite) -> None:
		super().__init__()
		self.action_type = action_type
		self.image = img
		
		if direction == 'right':
			self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
			self.hitbox = self.rect.inflate(- self.rect.width * 0.6, - self.rect.height * 0.3)
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
			self.hitbox = self.rect.inflate(- self.rect.width * 0.6, - self.rect.height * 0.3)
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
			self.hitbox = self.rect.inflate(- self.rect.width * 0.3, - self.rect.height * 0.6)
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
			self.hitbox = self.rect.inflate(- self.rect.width * 0.3, - self.rect.height * 0.6)

		self.hitbox.center = self.rect.center
		