import pygame
from csv import reader
from os import walk


def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map
	
def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

class TextRenderer:
	def __init__(self) -> None:
		self.font = pygame.font.Font("graphics/font/joystix.ttf", 25)
		self.display = pygame.display.get_surface()

	def render(self, text: str, position: tuple | pygame.Vector2, color: tuple = (255, 255, 255), bg_color: tuple = None, border_color: tuple = None) -> None:
		text_surf = self.font.render(text, True, color)
		text_rect = text_surf.get_rect(topleft=position)

		if border_color is not None:
			border_rect = text_rect.copy()
			w, h = text_rect.size
			border_rect = border_rect.inflate(w * 0.02, h * 0.2)
			border_rect.center = text_rect.center
			pygame.draw.rect(self.display, border_color, border_rect)


		if bg_color is not None:
			pygame.draw.rect(self.display, bg_color, text_rect)

		self.display.blit(text_surf, text_rect)
