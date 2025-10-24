import pygame
from ..util.support import import_folder
from random import choice


class Animation:
	def __init__(self) -> None:
		self.frames = {
			'leaf': (
				import_folder('graphics/particles/leaf1'),
				import_folder('graphics/particles/leaf2'),
				import_folder('graphics/particles/leaf3'),
				import_folder('graphics/particles/leaf4'),
				import_folder('graphics/particles/leaf5'),
				import_folder('graphics/particles/leaf6'),
				self.reflect_images(import_folder('graphics/particles/leaf1')),
				self.reflect_images(import_folder('graphics/particles/leaf2')),
				self.reflect_images(import_folder('graphics/particles/leaf3')),
				self.reflect_images(import_folder('graphics/particles/leaf4')),
				self.reflect_images(import_folder('graphics/particles/leaf5')),
				self.reflect_images(import_folder('graphics/particles/leaf6'))
			)
		}
	
	def reflect_images(self,frames):
		new_frames = []

		for frame in frames:
			flipped_frame = pygame.transform.flip(frame,True,False)
			new_frames.append(flipped_frame)
		return new_frames
	
	def create_grass_particles(self,pos,groups):
		animation_frames = choice(self.frames['leaf'])
		ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups):
		super().__init__(groups)
		self.sprite_type = 'magic'
		self.frame_index = 0
		self.animation_time = 3
		self.charge_time = self.animation_time / len(animation_frames)
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self, dt):
		self.frame_index += dt * 5
		frame = int(self.frame_index  * self.animation_time)
		if frame >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[frame]

	def update(self, dt):
		self.animate(dt)
