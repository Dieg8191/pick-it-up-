import pygame


class Trash(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: tuple[int, int], image: pygame.surface.Surface):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft= pos)
        self.hitbox = self.rect.inflate(-5, -5)
        self.hitbox.center = self.rect.center