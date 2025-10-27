import pygame
import pygame_gui
from .util.db import DBManager


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.manager = pygame_gui.UIManager(screen.get_size())

        width, height = screen.get_size()

        # Botones del menú principal
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width/2 - 100, height/2 - 80), (200, 50)),
            text='Jugar',
            manager=self.manager
        )

        self.stats_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width/2 - 100, height/2 - 10), (200, 50)),
            text='Estadísticas',
            manager=self.manager
        )

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width/2 - 100, height/2 + 60), (200, 50)),
            text='Salir',
            manager=self.manager
        )

        # Ventana de estadísticas (oculta al inicio)
        self.stats_window = None

    def show_stats(self):
        if self.stats_window:
            self.stats_window.kill()

        self.stats_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.screen.get_width()/2 - 150, self.screen.get_height()/2 - 150), (300, 300)),
            manager=self.manager,
            window_display_title="Estadísticas"
        )

        # Cargar puntajes desde la BD
        db = DBManager()
        top_scores = db.get_top_scores(5)
        db.close()

        y = 40
        for i, (name, score, date) in enumerate(top_scores, start=1):
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y), (260, 30)),
                text=f"{i}. {name} - {score} pts",
                manager=self.manager,
                container=self.stats_window
            )
            y += 35


    def run(self):
        """Ciclo principal del menú."""
        clock = pygame.time.Clock()
        running = True
        next_command = "exit"

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_command = "exit"

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            next_command = "run"
                            running = False

                        elif event.ui_element == self.stats_button:
                            self.show_stats()

                        elif event.ui_element == self.exit_button:
                            next_command = "exit"
                            running = False

                        elif (
                            hasattr(self, "close_stats_button")
                            and event.ui_element == self.close_stats_button
                        ):
                            self.stats_window.kill()
                            self.stats_window = None

                self.manager.process_events(event)

            self.manager.update(dt)
            self.screen.fill((30, 30, 30))
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        return next_command
