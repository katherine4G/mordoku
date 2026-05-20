from __future__ import annotations

import pygame

Color = tuple[int, int, int]

BG = (17, 19, 25)
PANEL = (30, 34, 45)
PANEL_LIGHT = (42, 48, 62)
LINE = (97, 107, 133)
TEXT = (235, 231, 220)
MUTED = (166, 170, 184)
ACCENT = (207, 174, 95)
GOOD = (104, 178, 132)
BAD = (202, 96, 96)
BLOCKED = (72, 61, 59)


def font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("consolas,arial", size, bold=bold)


def draw_text(
    surface: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    size: int = 24,
    color: Color = TEXT,
    bold: bool = False,
) -> pygame.Rect:
    rendered = font(size, bold).render(text, True, color)
    rect = rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect


def draw_centered_text(
    surface: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    size: int = 24,
    color: Color = TEXT,
    bold: bool = False,
) -> pygame.Rect:
    rendered = font(size, bold).render(text, True, color)
    text_rect = rendered.get_rect(center=rect.center)
    surface.blit(rendered, text_rect)
    return text_rect


def draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    selected: bool = False,
    disabled: bool = False,
) -> None:
    color = PANEL_LIGHT if selected else PANEL
    border = ACCENT if selected else LINE
    if disabled:
        color = (25, 27, 34)
        border = (55, 59, 70)
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, border, rect, width=2, border_radius=6)
    draw_centered_text(surface, label, rect, 22, MUTED if disabled else TEXT, bold=selected)


def wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped_text(
    surface: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    max_chars: int,
    size: int = 20,
    color: Color = TEXT,
) -> int:
    x, y = pos
    for line in wrap_text(text, max_chars):
        draw_text(surface, line, (x, y), size, color)
        y += size + 6
    return y
