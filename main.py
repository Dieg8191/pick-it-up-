import pygame
from sys import exit, platform
from src.game import Game
from src.menu import MainMenu
import ctypes

class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w * 0.8, info.current_h * 0.8))
        
        pygame.display.set_caption("Clean It Up!")

        self.game = Game()

    def set_dpi_awareness():
        """Configura la aplicación para escalar correctamente en pantallas HiDPI (Windows)."""
        if platform == "win32":
            try:
                # Windows 8.1 o superior
                ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1 = system DPI aware
            except Exception:
                try:
                    # Windows Vista o 7
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

    def run(self) -> None:
        command = "menu"

        while command != "exit":
            match command:
                case "run":
                    command = self.game.run()
                    continue

                case "menu":
                    menu = MainMenu(self.screen)
                    command = menu.run()
                    continue

                case _:
                    raise ValueError(f"Unknown command: {command}")

        pygame.quit()
        exit(0)


if __name__ == "__main__":
    app = App()
    app.run()