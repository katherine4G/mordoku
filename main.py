from __future__ import annotations

import sys

import pygame

from data.puzzles import PUZZLES
from ui.game import GameScreen
from ui.menu import MenuScreen
from ui.rules import RulesScreen


WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
FPS = 60


def main() -> int:
    pygame.init()
    pygame.display.set_caption("Murdoku")
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    frame_clock = pygame.time.Clock()

    menu_screen = MenuScreen()
    rules_screen = RulesScreen()
    level_index = 0
    game_screen = GameScreen(PUZZLES[level_index], level_index + 1, len(PUZZLES))
    current_screen = "menu"

    running = True
    while running:
        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                running = False
                continue

            if current_screen == "menu":
                screen_action = menu_screen.handle_event(pygame_event)
                if screen_action == "play":
                    level_index = 0
                    game_screen = GameScreen(
                        PUZZLES[level_index],
                        level_index + 1,
                        len(PUZZLES),
                    )
                    game_screen.reset()
                    current_screen = "game"
                elif screen_action == "rules":
                    current_screen = "rules"
                elif screen_action == "quit":
                    running = False
            elif current_screen == "rules":
                screen_action = rules_screen.handle_event(pygame_event)
                if screen_action == "back":
                    current_screen = "menu"
            elif current_screen == "game":
                screen_action = game_screen.handle_event(pygame_event)
                if screen_action == "menu":
                    current_screen = "menu"
                elif screen_action == "next_level" and level_index + 1 < len(PUZZLES):
                    level_index += 1
                    game_screen = GameScreen(
                        PUZZLES[level_index],
                        level_index + 1,
                        len(PUZZLES),
                    )

        if current_screen == "menu":
            menu_screen.draw(display_surface)
        elif current_screen == "rules":
            rules_screen.draw(display_surface)
        elif current_screen == "game":
            game_screen.draw(display_surface)

        pygame.display.flip()
        frame_clock.tick(FPS)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
