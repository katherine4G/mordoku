from __future__ import annotations
from pathlib import Path

import pygame

from ui.renderer import ACCENT, BG, MUTED, TEXT, draw_button, draw_text, draw_wrapped_text


WINDOW_HEIGHT = 900


class RulesScreen:

    ROOT = Path(__file__).resolve().parents[1]
    BACKGROUND_IMAGE_PATH = ROOT / "assets" / "images" / "fondo.jpg"

    def __init__(self) -> None:
        self.back_button_rect = pygame.Rect(40, WINDOW_HEIGHT - 84, 180, 52)

    def handle_event(self, pygame_event: pygame.event.Event) -> str | None:
        if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
            if self.back_button_rect.collidepoint(pygame_event.pos):
                return "back"
        if pygame_event.type == pygame.KEYDOWN and pygame_event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG)
        draw_text(surface, "Reglas", (52, 54), 44, ACCENT, bold=True)

        current_rule_y = 140
        rule_texts = [
            "Cada personaje ocupa una unica casilla de la matriz .",
            "No puede repetirse fila ni columna. Cuando una letra es correcta, su fila y columna se bloquean visualmente.",
            "Los movimientos son solo arriba, abajo, izquierda o derecha. Nunca diagonales, y debe estar dentro de la misma habitacion.",
            "El asesino es el unico personaje que queda a solas con la victima en la misma habitacion.",
            "El tablero ilustrado es solo referencia visual. ",
        ]
        for rule_text in rule_texts:
            draw_text(surface, ">", (70, current_rule_y), 24, MUTED)
            current_rule_y = (
                draw_wrapped_text(surface, rule_text, (105, current_rule_y), 95, 24, TEXT)
                + 18
            )

        draw_button(surface, self.back_button_rect, "Volver")
