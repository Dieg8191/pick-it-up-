import pygame
from sys import exit
from os import path
from src.game import Game


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w * 0.8, info.current_h * 0.8))
        
        pygame.display.set_caption("Clean It Up!")

    def run(self) -> None:
        command = "run game"

        while command != "exit":
            match command:
                case "run game":
                    game = Game()
                    command = game.run()
                    continue
                
                case "main menu":
                    # Placeholder for main menu logic
                    raise NotImplementedError("Main menu not implemented yet.")
                    continue
					
                case _:
                    raise ValueError(f"Unknown command: {command}")

        pygame.quit()
        exit(0)


if __name__ == "__main__":
    app = App()
    app.run()