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
    top_left_position: tuple[int, int],
    size: int = 24,
    color: Color = TEXT,
    bold: bool = False,
) -> pygame.Rect:
    rendered_text = font(size, bold).render(text, True, color)
    text_rect = rendered_text.get_rect(topleft=top_left_position)
    surface.blit(rendered_text, text_rect)
    return text_rect


def draw_centered_text(
    surface: pygame.Surface,
    text: str,
    target_rect: pygame.Rect,
    size: int = 24,
    color: Color = TEXT,
    bold: bool = False,
) -> pygame.Rect:
    rendered_text = font(size, bold).render(text, True, color)
    text_rect = rendered_text.get_rect(center=target_rect.center)
    surface.blit(rendered_text, text_rect)
    return text_rect


def draw_button(
    surface: pygame.Surface,
    button_rect: pygame.Rect,
    label: str,
    selected: bool = False,
    disabled: bool = False,
) -> None:
    fill_color = PANEL_LIGHT if selected else PANEL
    border_color = ACCENT if selected else LINE
    if disabled:
        fill_color = (25, 27, 34)
        border_color = (55, 59, 70)
    pygame.draw.rect(surface, fill_color, button_rect, border_radius=6)
    pygame.draw.rect(surface, border_color, button_rect, width=2, border_radius=6)
    draw_centered_text(
        surface,
        label,
        button_rect,
        22,
        MUTED if disabled else TEXT,
        bold=selected,
    )


def wrap_text(text: str, max_chars: int) -> list[str]:
    text_words = text.split()
    wrapped_lines: list[str] = []
    current_line = ""
    for word in text_words:
        candidate_line = word if not current_line else f"{current_line} {word}"
        if len(candidate_line) <= max_chars:
            current_line = candidate_line
        else:
            if current_line:
                wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines


def wrap_text_to_width(
    text: str,
    max_width: int,
    size: int = 20,
    bold: bool = False,
) -> list[str]:
    text_font = font(size, bold)
    wrapped_lines: list[str] = []
    current_line = ""

    for word in text.split():
        candidate_line = word if not current_line else f"{current_line} {word}"
        if text_font.size(candidate_line)[0] <= max_width:
            current_line = candidate_line
            continue

        if current_line:
            wrapped_lines.append(current_line)
        current_line = word

    if current_line:
        wrapped_lines.append(current_line)
    return wrapped_lines


def draw_wrapped_text(
    surface: pygame.Surface,
    text: str,
    top_left_position: tuple[int, int],
    max_chars: int,
    size: int = 20,
    color: Color = TEXT,
) -> int:
    text_x, current_y = top_left_position
    for wrapped_line in wrap_text(text, max_chars):
        draw_text(surface, wrapped_line, (text_x, current_y), size, color)
        current_y += size + 6
    return current_y


def draw_text_block(
    surface: pygame.Surface,
    text: str,
    top_left_position: tuple[int, int],
    max_width: int,
    size: int = 20,
    color: Color = TEXT,
    bold: bool = False,
    line_gap: int = 6,
    max_lines: int | None = None,
) -> int:
    text_x, current_y = top_left_position
    wrapped_lines = wrap_text_to_width(text, max_width, size, bold)
    if max_lines is not None:
        wrapped_lines = wrapped_lines[:max_lines]

    for wrapped_line in wrapped_lines:
        draw_text(surface, wrapped_line, (text_x, current_y), size, color, bold=bold)
        current_y += size + line_gap
    return current_y
