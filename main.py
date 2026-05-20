from __future__ import annotations

import sys

import pygame

from data.puzzles import PUZZLES
from ui.game import GameScreen
from ui.menu import MenuScreen
from ui.rules import RulesScreen


WIDTH = 1280
HEIGHT = 760
FPS = 60


def main() -> int:
    pygame.init()
    pygame.display.set_caption("Murdoku")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    menu = MenuScreen()
    rules = RulesScreen()
    level_index = 0
    game = GameScreen(PUZZLES[level_index], level_index + 1, len(PUZZLES))
    current = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if current == "menu":
                action = menu.handle_event(event)
                if action == "play":
                    level_index = 0
                    game = GameScreen(PUZZLES[level_index], level_index + 1, len(PUZZLES))
                    game.reset()
                    current = "game"
                elif action == "rules":
                    current = "rules"
                elif action == "quit":
                    running = False
            elif current == "rules":
                action = rules.handle_event(event)
                if action == "back":
                    current = "menu"
            elif current == "game":
                action = game.handle_event(event)
                if action == "menu":
                    current = "menu"
                elif action == "next_level" and level_index + 1 < len(PUZZLES):
                    level_index += 1
                    game = GameScreen(PUZZLES[level_index], level_index + 1, len(PUZZLES))

        if current == "menu":
            menu.draw(screen)
        elif current == "rules":
            rules.draw(screen)
        elif current == "game":
            game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
