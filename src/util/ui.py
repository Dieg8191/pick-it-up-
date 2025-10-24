import pygame
from ..entity.player import Player
from .support import load_image, TextRenderer
from ..objects.tile import Tile


class UI:
    def __init__(self, player: Player, trash_sprites: pygame.sprite.Group, text_renderer: TextRenderer):
        self.screen = pygame.display.get_surface()
        self.screen_w, self.screen_h = self.screen.get_size()
        self.golden = (166, 124, 0)

        self.player = player
        self.trash_sprites = trash_sprites
        self.text_renderer = text_renderer

        # Selected Action
        rect_size = 80
        self.selected_action_border_rect = pygame.Rect(5, self.screen_h - rect_size - 5, rect_size, rect_size)
        self.selected_action_bg_rect = self.selected_action_border_rect.copy().inflate(-rect_size * 0.1, -rect_size * 0.1)
        self.selected_action_bg_rect.center = self.selected_action_border_rect.center


        sword = Tile((0, 0), [], "tile", load_image("graphics/sword/full.png"))
        sword.rect.center = self.selected_action_border_rect.center

        collector = Tile((0, 0), [], "tile", load_image("graphics/collector/full.png"))
        collector.rect.center = self.selected_action_border_rect.center

        self.action_images = {
            "sword": sword,
            "collector": collector
        }

    def update(self):
        pass

    def draw_current_action(self):
        # Border
        pygame.draw.rect(self.screen, rect=self.selected_action_border_rect, color=self.golden)

        # Black background
        pygame.draw.rect(self.screen, rect=self.selected_action_bg_rect, color="black")

        # Sprite
        sprite = self.action_images[self.player.selected_action]
        self.screen.blit(sprite.image, sprite.rect)

    def draw_trash_count(self):
        trash_coount = len(self.trash_sprites)
        self.text_renderer.render(f"Basura restante: {trash_coount}", (10, 10), "white", "black", self.golden), 
        

    def draw(self):
        self.draw_current_action()
        self.draw_trash_count()