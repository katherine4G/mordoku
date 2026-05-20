from __future__ import annotations

from pathlib import Path 
import pygame
from ui.renderer import ACCENT, BG, MUTED, TEXT, draw_button, draw_text


class MenuScreen:
    
    ROOT = Path(__file__).resolve().parents[1]
    
    image_path = ROOT / "assets" / "images" / "fondo.jpg"
    
    def __init__(self) -> None:
        self.buttons = {
            "play": pygame.Rect(520, 310, 240, 56),
            "rules": pygame.Rect(520, 390, 240, 56),
            "quit": pygame.Rect(520, 470, 240, 56),
        }

        self.bg_image = pygame.image.load(str(self.image_path)).convert()
        
        self.bg_image = pygame.transform.scale(self.bg_image, (1280, 720))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    return action
        return None

    def draw(self, surface: pygame.Surface) -> None:
        ancho, alto = surface.get_size()
        bg_scaled = pygame.transform.scale(self.bg_image, (ancho, alto))
        surface.blit(bg_scaled, (0, 0))
        
        draw_text(surface, "MURDOKU", (492, 150), 54, ACCENT, bold=True)
        draw_text(surface, "Sudoku  + caso detectivesco", (418, 220), 24, MUTED)
        draw_button(surface, self.buttons["play"], "Jugar")
        draw_button(surface, self.buttons["rules"], "Reglas")
        draw_button(surface, self.buttons["quit"], "Salir")