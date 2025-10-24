import pygame
from .support import load_image

class Camera(pygame.sprite.Group):
	def __init__(self) -> None:
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.ground = load_image("graphics/tilemap/ground.png")
		self.ground_rect = self.ground.get_rect(topleft=(0, 0))

		self.camera_offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

	def draw_rects(self) -> None:
		for sprite in self.sprites():
			if hasattr(sprite, 'hitbox'):
				rect = sprite.hitbox.copy()
				rect.topleft -= self.camera_offset
				pygame.draw.rect(self.display_surface, (255, 0, 0), rect, 1)
		
	def center_target_camera(self, target: pygame.sprite.Sprite) -> None:
		self.camera_offset.x = target.rect.centerx - self.half_w
		self.camera_offset.y = target.rect.centery - self.half_h

	def custom_draw(self) -> None:
		# Draw ground
		ground_offset = self.ground_rect.topleft + self.camera_offset
		self.display_surface.blit(self.ground, self.ground_rect.topleft - ground_offset)
		
		sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
		for sprite in sorted_sprites:
			offset_pos = sprite.rect.topleft - self.camera_offset
			self.display_surface.blit(sprite.image, offset_pos)

		

