import pygame
import pygame_gui
from .db import DBManager

class ScoreScreen:
    def __init__(self):
        self.manager = None
        self.clock = pygame.time.Clock()
        self.running = False
        self.name = None
        self.result = None

    def guardar_puntuacion(self, nombre, score):
        db = DBManager()
        db.insert_score(nombre, score)
        db.close()
        self.running = False

    def show(self, score: int):
        """Muestra la pantalla de puntuación centrada en la ventana activa."""
        self.running = True
        self.result = None

        # Usa la superficie del juego existente
        screen = pygame.display.get_surface()
        if screen is None:
            screen = pygame.display.set_mode((800, 600))
        width, height = screen.get_size()

        # Inicializa el UIManager con el tamaño actual
        self.manager = pygame_gui.UIManager((width, height))

        # Coordenadas centradas
        center_x = width // 2
        center_y = height // 2

        # Fondo semitransparente (overlay)
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        # Elementos GUI centrados
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((center_x - 70, center_y - 100), (140, 40)),
            text=f"Score: {score}",
            manager=self.manager
        )

        name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((center_x - 100, center_y - 40), (200, 40)),
            manager=self.manager
        )

        save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x - 100, center_y + 20), (90, 40)),
            text="Guardar",
            manager=self.manager
        )

        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x + 10, center_y + 20), (90, 40)),
            text="Salir",
            manager=self.manager
        )

        # Bucle principal de la pantalla
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.result = "exit"

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == save_button:
                            nombre = name_input.get_text().strip()
                            if nombre and "nombre" not in nombre.lower():
                                self.guardar_puntuacion(nombre, score)
                                name_input.set_text("¡Guardado!")
                                self.result = "save"
                            else:
                                name_input.set_text("Ingresa un nombre")
                        elif event.ui_element == exit_button:
                            self.running = False
                            self.result = "menu"

                self.manager.process_events(event)

            self.manager.update(dt)

            # Dibuja fondo semitransparente + UI
            screen.blit(overlay, (0, 0))
            self.manager.draw_ui(screen)
            pygame.display.update()

        return self.result or "menu"
