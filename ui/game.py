# ui/game.py
from __future__ import annotations

import pygame

from data.puzzles import LEVEL_1, Puzzle
from logic.board import BoardState
from ui.renderer import (
    ACCENT,
    BAD,
    BG,
    BLOCKED,
    GOOD,
    LINE,
    MUTED,
    PANEL,
    PANEL_LIGHT,
    TEXT,
    draw_button,
    draw_centered_text,
    draw_text,
    draw_wrapped_text,
)


class GameScreen:
    def __init__(
        self,
        puzzle: Puzzle = LEVEL_1,
        level_number: int = 1,
        total_levels: int = 1,
    ) -> None:
        self.puzzle = puzzle
        self.level_number = level_number
        self.total_levels = total_levels
        self.board = BoardState(puzzle)
        self.selected_initial: str | None = None
        self.message = "Selecciona una inicial y colocala en la matriz."
        self.message_ok = True
        self.answer = ""
        self.final_result: str | None = None
        self.final_ok = False

        self.back_button = pygame.Rect(24, 22, 120, 40)
        self.grid_rect = pygame.Rect(820, 100, 360, 360)
        self.cell_size = self.grid_rect.width // self.puzzle.size
        self.initial_buttons: dict[str, pygame.Rect] = {}
        self._build_initial_buttons()
        self.answer_rect = pygame.Rect(805, 652, 270, 42)
        self.submit_rect = pygame.Rect(1090, 652, 120, 42)
        self.next_rect = pygame.Rect(945, 718, 265, 32)

        self.image = self._load_reference_image()

    def reset(self) -> None:
        self.__init__(self.puzzle, self.level_number, self.total_levels)

    def _build_initial_buttons(self) -> None:
        x = 36
        y = 552
        for index, initial in enumerate(self.puzzle.characters):
            self.initial_buttons[initial] = pygame.Rect(x + index * 76, y, 56, 48)

    def _load_reference_image(self) -> pygame.Surface | None:
        if not self.puzzle.image_path.exists():
            return None
        image = pygame.image.load(str(self.puzzle.image_path)).convert_alpha()
        return pygame.transform.smoothscale(image, (720, 384))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if self.board.is_complete():
                self._handle_answer_key(event)
            else:
                char = event.unicode.upper()
                if char in self.puzzle.characters and self.board.can_place(char):
                    self.selected_initial = char

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "menu"
            for initial, rect in self.initial_buttons.items():
                if rect.collidepoint(event.pos) and self.board.can_place(initial):
                    self.selected_initial = initial
                    return None
            if self.grid_rect.collidepoint(event.pos):
                self._handle_grid_click(event.pos)
            if self.board.is_complete() and self.submit_rect.collidepoint(event.pos):
                self._submit_answer()
            if self.final_ok and self.next_rect.collidepoint(event.pos):
                return "next_level"
        return None

    def _handle_answer_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_BACKSPACE:
            self.answer = self.answer[:-1]
        elif event.key == pygame.K_RETURN:
            self._submit_answer()
        elif event.unicode.isalpha() or event.unicode == " ":
            if len(self.answer) < 24:
                self.answer += event.unicode

    def _handle_grid_click(self, pos: tuple[int, int]) -> None:
        if self.selected_initial is None:
            self.message = "Primero selecciona una inicial."
            self.message_ok = False
            return

        col = (pos[0] - self.grid_rect.x) // self.cell_size
        row = (pos[1] - self.grid_rect.y) // self.cell_size
        result = self.board.place(self.selected_initial, (row, col))
        self.message = result.message
        self.message_ok = result.accepted
        if result.accepted:
            self.selected_initial = None
            if self.board.is_complete():
                self.message = "Todos ubicados. Escribe quien es el asesino."

    def _submit_answer(self) -> None:
        result = self.board.validate_murderer(self.answer)
        self.final_result = result.message
        self.final_ok = result.accepted

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG)
        draw_button(surface, self.back_button, "Menu")
        draw_text(surface, self.puzzle.title, (168, 28), 32, ACCENT, bold=True)
        draw_text(surface, f"Nivel {self.level_number}/{self.total_levels}", (1085, 28), 20, MUTED)
        self._draw_reference(surface)
        self._draw_grid(surface)
        self._draw_character_panel(surface)
        self._draw_message(surface)
        if self.board.is_complete():
            self._draw_final_prompt(surface)

    def _draw_reference(self, surface: pygame.Surface) -> None:
        frame = pygame.Rect(32, 88, 744, 420)
        pygame.draw.rect(surface, PANEL, frame, border_radius=8)
        pygame.draw.rect(surface, LINE, frame, width=2, border_radius=8)
        if self.image:
            surface.blit(self.image, (44, 106))
        else:
            draw_centered_text(surface, "Imagen no encontrada", frame, 28, BAD)
        draw_text(surface, "Referencia visual del caso", (46, 516), 18, MUTED)

    def _draw_grid(self, surface: pygame.Surface) -> None:
        draw_text(surface, "Detective, toma nota aqui:", (820, 58), 26, TEXT)
        pygame.draw.rect(surface, PANEL, self.grid_rect, border_radius=6)

        for row in range(self.puzzle.size):
            for col in range(self.puzzle.size):
                cell = pygame.Rect(
                    self.grid_rect.x + col * self.cell_size,
                    self.grid_rect.y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                blocked = row in self.board.blocked_rows or col in self.board.blocked_cols
                if blocked:
                    pygame.draw.rect(surface, BLOCKED, cell)

                value = self.board.cell_value((row, col))
                if value:
                    pygame.draw.rect(surface, PANEL_LIGHT, cell.inflate(-8, -8), border_radius=4)
                    draw_centered_text(surface, value, cell, 32, ACCENT, bold=True)

                pygame.draw.rect(surface, LINE, cell, width=1)

        if self.selected_initial:
            draw_text(surface, f"Seleccionado: {self.selected_initial}", (820, 478), 22, ACCENT)
        else:
            draw_text(surface, "Selecciona una inicial", (820, 478), 22, MUTED)

    def _draw_character_panel(self, surface: pygame.Surface) -> None:
        draw_text(surface, "Personajes", (36, 610), 24, TEXT, bold=True)
        for initial, rect in self.initial_buttons.items():
            placed = not self.board.can_place(initial)
            selected = self.selected_initial == initial
            draw_button(surface, rect, initial, selected=selected, disabled=placed)

        panel = pygame.Rect(36, 642, 740, 90)
        pygame.draw.rect(surface, PANEL, panel, border_radius=8)
        pygame.draw.rect(surface, LINE, panel, width=2, border_radius=8)
        draw_text(surface, "Pistas", (panel.x + 14, panel.y + 10), 18, ACCENT, bold=True)

        for index, initial in enumerate(self.puzzle.characters):
            col = index % 3
            row = index // 3
            x = panel.x + 14 + col * 235
            y = panel.y + 38 + row * 24
            character = self.puzzle.characters[initial]
            clue = f"{initial} {character.name}: {character.clue}"
            draw_text(surface, clue[:31], (x, y), 15, TEXT)

    def _draw_message(self, surface: pygame.Surface) -> None:
        panel = pygame.Rect(804, 520, 410, 96)
        pygame.draw.rect(surface, PANEL, panel, border_radius=8)
        pygame.draw.rect(surface, GOOD if self.message_ok else BAD, panel, width=2, border_radius=8)
        draw_wrapped_text(
            surface,
            self.message,
            (panel.x + 16, panel.y + 18),
            42,
            20,
            TEXT,
        )

    def _draw_final_prompt(self, surface: pygame.Surface) -> None:
        draw_text(surface, "Quien es el asesino?", (805, 620), 24, ACCENT, bold=True)
        pygame.draw.rect(surface, PANEL_LIGHT, self.answer_rect, border_radius=6)
        pygame.draw.rect(surface, ACCENT, self.answer_rect, width=2, border_radius=6)
        draw_text(surface, self.answer or "Nombre...", (self.answer_rect.x + 12, self.answer_rect.y + 10), 20, TEXT if self.answer else MUTED)
        draw_button(surface, self.submit_rect, "Validar")
        if self.final_result:
            draw_text(
                surface,
                self.final_result,
                (805, 696 if self.final_ok else 704),
                18,
                GOOD if self.final_ok else BAD,
                bold=self.final_ok,
            )
        if self.final_ok:
            if self.level_number < self.total_levels:
                draw_button(surface, self.next_rect, "Siguiente caso", selected=True)
            else:
                draw_text(surface, "Casos disponibles completados.", (805, 732), 18, GOOD, bold=True)
