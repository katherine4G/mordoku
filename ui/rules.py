from __future__ import annotations
from pathlib import Path

import pygame

from ui.renderer import ACCENT, BG, MUTED, TEXT, draw_button, draw_text, draw_wrapped_text


class RulesScreen:

    ROOT = Path(__file__).resolve().parents[1]
    
    image_path = ROOT / "assets" / "images" / "fondo.jpg"
    

    def __init__(self) -> None:
        self.back_button = pygame.Rect(40, 660, 180, 52)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "back"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG)
        draw_text(surface, "Reglas", (52, 54), 42, ACCENT, bold=True)

        y = 130
        rules = [
            "Cada personaje ocupa una única casilla de la matriz .",
            "No puede repetirse fila ni columna. Cuando una letra es correcta, su fila y columna se bloquean visualmente.",
            "Los movimientos son solo arriba, abajo, izquierda o derecha. Nunca diagonales, y debe estar dentro de la misma habitacion.",
            "El asesino es el unico personaje que queda a solas con la victima en la misma habitacion.",
            "El tablero ilustrado es solo referencia visual. ",
        ]
        for rule in rules:
            draw_text(surface, ">", (70, y), 24, MUTED)
            y = draw_wrapped_text(surface, rule, (105, y), 82, 24, TEXT) + 18

        draw_button(surface, self.back_button, "Volver")
