import pygame
from .tile import Tile

class Grass(Tile):
    def __init__(self, position: tuple[int, int], groups: list[pygame.sprite.Group], image: pygame.Surface) -> None:
        super().__init__(position, groups, 'grass', image)

    def destroy(self) -> None:
        print("! Grass destroyed!")

        self.kill()