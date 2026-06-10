from __future__ import annotations

from pathlib import Path

import pygame

from ui.renderer import ACCENT, MUTED, draw_button, draw_text


WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
MENU_BUTTON_WIDTH = 260
MENU_BUTTON_HEIGHT = 58
MENU_BUTTON_GAP = 22


class MenuScreen:

    ROOT = Path(__file__).resolve().parents[1]
    BACKGROUND_IMAGE_PATH = ROOT / "assets" / "images" / "fondo.jpg"

    def __init__(self) -> None:
        button_x = (WINDOW_WIDTH - MENU_BUTTON_WIDTH) // 2
        first_button_y = 390
        self.button_rects = {
            "play": pygame.Rect(button_x, first_button_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
            "rules": pygame.Rect(
                button_x,
                first_button_y + MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP,
                MENU_BUTTON_WIDTH,
                MENU_BUTTON_HEIGHT,
            ),
            "quit": pygame.Rect(
                button_x,
                first_button_y + (MENU_BUTTON_HEIGHT + MENU_BUTTON_GAP) * 2,
                MENU_BUTTON_WIDTH,
                MENU_BUTTON_HEIGHT,
            ),
        }

        self.background_image = pygame.image.load(str(self.BACKGROUND_IMAGE_PATH)).convert()
        self.background_image = pygame.transform.scale(
            self.background_image,
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

    def handle_event(self, pygame_event: pygame.event.Event) -> str | None:
        if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
            for menu_action, button_rect in self.button_rects.items():
                if button_rect.collidepoint(pygame_event.pos):
                    return menu_action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface_width, surface_height = surface.get_size()
        scaled_background = pygame.transform.scale(
            self.background_image,
            (surface_width, surface_height),
        )
        surface.blit(scaled_background, (0, 0))

        draw_text(surface, "MURDOKU", (620, 210), 58, ACCENT, bold=True)
        draw_text(surface, "Sudoku  + caso detectivesco", (558, 285), 24, MUTED)
        draw_button(surface, self.button_rects["play"], "Jugar")
        draw_button(surface, self.button_rects["rules"], "Reglas")
        draw_button(surface, self.button_rects["quit"], "Salir")
