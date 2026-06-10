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
    draw_text_block,
)


WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
PANEL_MARGIN = 32
PANEL_PADDING = 16
COLUMN_GAP = 32
SECTION_GAP = 24
RIGHT_COLUMN_WIDTH = 520
REFERENCE_PANEL_HEIGHT = 400
MAX_GRID_SIZE = 450
GRID_LABEL_SIZE = 34
GRID_COLUMN_LABEL_HEIGHT = 22
GRID_TITLE_HEIGHT = 30
GRID_TITLE_TO_LABEL_GAP = 20
GRID_LABEL_TO_GRID_GAP = 8
GRID_TO_SELECTED_GAP = 10
SELECTED_TO_MESSAGE_GAP = 30
MESSAGE_PANEL_HEIGHT = 90
FINAL_PROMPT_GAP = 18
FINAL_ANSWER_BOX_GAP = 34
FINAL_FEEDBACK_GAP = 10
NEXT_BUTTON_WIDTH = 265
NEXT_BUTTON_HEIGHT = 34
CHARACTER_BUTTON_WIDTH = 60
CHARACTER_BUTTON_HEIGHT = 48
CHARACTER_BUTTON_GAP = 16
CHARACTER_BUTTON_ROW_GAP = 12
CLUE_COLUMN_GAP = 24
CLUE_HEADER_HEIGHT = 34
CLUE_LINE_GAP = 2


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
        self.selected_character_initial: str | None = None
        self.message = "Selecciona una inicial y colocala en la matriz."
        self.message_is_positive = True
        self.murderer_answer = ""
        self.final_answer_message: str | None = None
        self.final_answer_is_correct = False

        self.initial_button_rects: dict[str, pygame.Rect] = {}
        self._build_layout()
        self.reference_image = self._load_reference_image()

    def reset(self) -> None:
        self.__init__(self.puzzle, self.level_number, self.total_levels)

    def _build_layout(self) -> None:
        content_top = 88
        left_column_width = (
            WINDOW_WIDTH
            - PANEL_MARGIN * 2
            - COLUMN_GAP
            - RIGHT_COLUMN_WIDTH
        )
        right_column_x = PANEL_MARGIN + left_column_width + COLUMN_GAP

        self.back_button_rect = pygame.Rect(PANEL_MARGIN, 22, 130, 42)
        self.title_position = (PANEL_MARGIN + 160, 26)
        self.level_text_position = (WINDOW_WIDTH - PANEL_MARGIN - 170, 28)

        self.left_column_rect = pygame.Rect(
            PANEL_MARGIN,
            content_top,
            left_column_width,
            WINDOW_HEIGHT - content_top - PANEL_MARGIN,
        )
        self.right_column_rect = pygame.Rect(
            right_column_x,
            content_top,
            RIGHT_COLUMN_WIDTH,
            WINDOW_HEIGHT - content_top - PANEL_MARGIN,
        )

        self.reference_panel_rect = pygame.Rect(
            self.left_column_rect.x,
            self.left_column_rect.y,
            self.left_column_rect.width,
            REFERENCE_PANEL_HEIGHT,
        )
        self.reference_image_bounds_rect = pygame.Rect(
            self.reference_panel_rect.x + PANEL_PADDING,
            self.reference_panel_rect.y + 56,
            self.reference_panel_rect.width - PANEL_PADDING * 2,
            self.reference_panel_rect.height - 72,
        )

        self.character_title_position = (
            self.left_column_rect.x,
            self.reference_panel_rect.bottom + SECTION_GAP,
        )
        self.character_buttons_y = self.character_title_position[1] + 36
        self._build_initial_button_rects()

        character_buttons_bottom = max(
            button_rect.bottom for button_rect in self.initial_button_rects.values()
        )
        clue_panel_y = character_buttons_bottom + SECTION_GAP
        self.clue_panel_rect = pygame.Rect(
            self.left_column_rect.x,
            clue_panel_y,
            self.left_column_rect.width,
            WINDOW_HEIGHT - PANEL_MARGIN - clue_panel_y,
        )

        self.cell_size = MAX_GRID_SIZE // self.puzzle.size
        actual_grid_size = self.cell_size * self.puzzle.size
        grid_x = (
            self.right_column_rect.x
            + GRID_LABEL_SIZE
            + (
                self.right_column_rect.width
                - GRID_LABEL_SIZE
                - actual_grid_size
            )
            // 2
        )
        self.grid_title_position = (self.right_column_rect.x, self.right_column_rect.y)
        grid_y = (
            self.grid_title_position[1]
            + GRID_TITLE_HEIGHT
            + GRID_TITLE_TO_LABEL_GAP
            + GRID_COLUMN_LABEL_HEIGHT
            + GRID_LABEL_TO_GRID_GAP
        )
        self.grid_rect = pygame.Rect(grid_x, grid_y, actual_grid_size, actual_grid_size)
        self.selected_text_position = (
            self.right_column_rect.x,
            self.grid_rect.bottom + GRID_TO_SELECTED_GAP,
        )
        self.message_panel_rect = pygame.Rect(
            self.right_column_rect.x,
            self.selected_text_position[1] + SELECTED_TO_MESSAGE_GAP,
            self.right_column_rect.width,
            MESSAGE_PANEL_HEIGHT,
        )

        final_prompt_y = self.message_panel_rect.bottom + FINAL_PROMPT_GAP
        self.final_prompt_title_position = (self.right_column_rect.x, final_prompt_y)
        self.answer_box_rect = pygame.Rect(
            self.right_column_rect.x,
            final_prompt_y + FINAL_ANSWER_BOX_GAP,
            330,
            44,
        )
        self.submit_answer_button_rect = pygame.Rect(
            self.answer_box_rect.right + 16,
            self.answer_box_rect.y,
            self.right_column_rect.right - self.answer_box_rect.right - 16,
            self.answer_box_rect.height,
        )
        self.final_answer_position = (
            self.right_column_rect.x,
            self.answer_box_rect.bottom + FINAL_FEEDBACK_GAP,
        )
        self.next_level_button_rect = pygame.Rect(
            self.right_column_rect.right - NEXT_BUTTON_WIDTH,
            self.answer_box_rect.bottom + FINAL_FEEDBACK_GAP,
            NEXT_BUTTON_WIDTH,
            NEXT_BUTTON_HEIGHT,
        )

    def _build_initial_button_rects(self) -> None:
        self.initial_button_rects.clear()
        buttons_per_row = max(
            1,
            (
                self.left_column_rect.width
                + CHARACTER_BUTTON_GAP
            )
            // (CHARACTER_BUTTON_WIDTH + CHARACTER_BUTTON_GAP),
        )
        for button_index, character_initial in enumerate(self.puzzle.characters):
            button_col = button_index % buttons_per_row
            button_row = button_index // buttons_per_row
            button_x = (
                self.left_column_rect.x
                + button_col * (CHARACTER_BUTTON_WIDTH + CHARACTER_BUTTON_GAP)
            )
            button_y = (
                self.character_buttons_y
                + button_row * (CHARACTER_BUTTON_HEIGHT + CHARACTER_BUTTON_ROW_GAP)
            )
            self.initial_button_rects[character_initial] = pygame.Rect(
                button_x,
                button_y,
                CHARACTER_BUTTON_WIDTH,
                CHARACTER_BUTTON_HEIGHT,
            )

    def _load_reference_image(self) -> pygame.Surface | None:
        if not self.puzzle.image_path.exists():
            return None
        return pygame.image.load(str(self.puzzle.image_path)).convert_alpha()

    def handle_event(self, pygame_event: pygame.event.Event) -> str | None:
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_ESCAPE:
                return "menu"
            if self.board.is_complete():
                self._handle_answer_text_key(pygame_event)
            else:
                typed_character = pygame_event.unicode.upper()
                if (
                    typed_character in self.puzzle.characters
                    and self.board.can_place(typed_character)
                ):
                    self.selected_character_initial = typed_character

        if pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
            mouse_position = pygame_event.pos
            if self.back_button_rect.collidepoint(mouse_position):
                return "menu"
            for character_initial, button_rect in self.initial_button_rects.items():
                if (
                    button_rect.collidepoint(mouse_position)
                    and self.board.can_place(character_initial)
                ):
                    self.selected_character_initial = character_initial
                    return None
            if self.grid_rect.collidepoint(mouse_position):
                self._handle_grid_click(mouse_position)
            if (
                self.board.is_complete()
                and self.submit_answer_button_rect.collidepoint(mouse_position)
            ):
                self._submit_answer()
            if (
                self.final_answer_is_correct
                and self.next_level_button_rect.collidepoint(mouse_position)
            ):
                return "next_level"
        return None

    def _handle_answer_text_key(self, pygame_event: pygame.event.Event) -> None:
        if pygame_event.key == pygame.K_BACKSPACE:
            self.murderer_answer = self.murderer_answer[:-1]
        elif pygame_event.key == pygame.K_RETURN:
            self._submit_answer()
        elif pygame_event.unicode.isalpha() or pygame_event.unicode == " ":
            if len(self.murderer_answer) < 24:
                self.murderer_answer += pygame_event.unicode

    def _handle_grid_click(self, click_position: tuple[int, int]) -> None:
        if self.selected_character_initial is None:
            self.message = "Primero selecciona una inicial."
            self.message_is_positive = False
            return

        clicked_col = (click_position[0] - self.grid_rect.x) // self.cell_size
        clicked_row = (click_position[1] - self.grid_rect.y) // self.cell_size
        move_result = self.board.place(
            self.selected_character_initial,
            (clicked_row, clicked_col),
        )
        self.message = move_result.message
        self.message_is_positive = move_result.accepted
        if move_result.accepted:
            self.selected_character_initial = None
            if self.board.is_complete():
                self.message = "Todos ubicados. Escribe quien es el asesino."

    def _submit_answer(self) -> None:
        validation_result = self.board.validate_murderer(self.murderer_answer)
        self.final_answer_message = validation_result.message
        self.final_answer_is_correct = validation_result.accepted

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG)
        draw_button(surface, self.back_button_rect, "Menu")
        draw_text(surface, self.puzzle.title, self.title_position, 32, ACCENT, bold=True)
        draw_text(
            surface,
            f"Nivel {self.level_number}/{self.total_levels}",
            self.level_text_position,
            20,
            MUTED,
        )
        self._draw_reference(surface)
        self._draw_grid(surface)
        self._draw_character_panel(surface)
        self._draw_message(surface)
        if self.board.is_complete():
            self._draw_final_prompt(surface)

    def _draw_reference(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, PANEL, self.reference_panel_rect, border_radius=8)
        pygame.draw.rect(surface, LINE, self.reference_panel_rect, width=2, border_radius=8)
        draw_text(
            surface,
            "Referencia visual del caso",
            (
                self.reference_panel_rect.x + PANEL_PADDING,
                self.reference_panel_rect.y + PANEL_PADDING,
            ),
            20,
            MUTED,
        )

        if self.reference_image:
            scaled_image, image_rect = self._scaled_reference_image()
            surface.blit(scaled_image, image_rect)
        else:
            draw_centered_text(
                surface,
                "Imagen no encontrada",
                self.reference_image_bounds_rect,
                28,
                BAD,
            )

    def _scaled_reference_image(self) -> tuple[pygame.Surface, pygame.Rect]:
        image_width, image_height = self.reference_image.get_size()
        scale = min(
            self.reference_image_bounds_rect.width / image_width,
            self.reference_image_bounds_rect.height / image_height,
        )
        scaled_size = (
            int(image_width * scale),
            int(image_height * scale),
        )
        scaled_image = pygame.transform.smoothscale(self.reference_image, scaled_size)
        image_rect = scaled_image.get_rect(center=self.reference_image_bounds_rect.center)
        return scaled_image, image_rect

    def _draw_grid(self, surface: pygame.Surface) -> None:
        draw_text(surface, "Detective, toma nota aqui:", self.grid_title_position, 26, TEXT)
        self._draw_grid_labels(surface)
        pygame.draw.rect(surface, PANEL, self.grid_rect, border_radius=6)
        character_font_size = max(18, int(self.cell_size * 0.45))

        for board_row in range(self.puzzle.size):
            for board_col in range(self.puzzle.size):
                grid_cell_rect = pygame.Rect(
                    self.grid_rect.x + board_col * self.cell_size,
                    self.grid_rect.y + board_row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                row_or_column_blocked = (
                    board_row in self.board.blocked_rows
                    or board_col in self.board.blocked_cols
                )
                if row_or_column_blocked:
                    pygame.draw.rect(surface, BLOCKED, grid_cell_rect)

                placed_character_initial = self.board.character_initial_at(
                    (board_row, board_col),
                )
                if placed_character_initial:
                    pygame.draw.rect(
                        surface,
                        PANEL_LIGHT,
                        grid_cell_rect.inflate(-8, -8),
                        border_radius=4,
                    )
                    draw_centered_text(
                        surface,
                        placed_character_initial,
                        grid_cell_rect,
                        character_font_size,
                        ACCENT,
                        bold=True,
                    )

                pygame.draw.rect(surface, LINE, grid_cell_rect, width=1)

        if self.selected_character_initial:
            selected_text = f"Seleccionado: {self.selected_character_initial}"
            draw_text(surface, selected_text, self.selected_text_position, 22, ACCENT)
        else:
            draw_text(surface, "Selecciona una inicial", self.selected_text_position, 22, MUTED)

    def _draw_grid_labels(self, surface: pygame.Surface) -> None:
        label_font_size = 18 if self.puzzle.size <= 6 else 16
        column_label_y = (
            self.grid_rect.y
            - GRID_LABEL_TO_GRID_GAP
            - GRID_COLUMN_LABEL_HEIGHT
        )

        for board_col in range(self.puzzle.size):
            column_label_rect = pygame.Rect(
                self.grid_rect.x + board_col * self.cell_size,
                column_label_y,
                self.cell_size,
                GRID_COLUMN_LABEL_HEIGHT,
            )
            draw_centered_text(
                surface,
                str(board_col + 1),
                column_label_rect,
                label_font_size,
                MUTED,
            )

        for board_row in range(self.puzzle.size):
            row_label_rect = pygame.Rect(
                self.grid_rect.x - GRID_LABEL_SIZE,
                self.grid_rect.y + board_row * self.cell_size,
                GRID_LABEL_SIZE,
                self.cell_size,
            )
            draw_centered_text(
                surface,
                str(board_row + 1),
                row_label_rect,
                label_font_size,
                MUTED,
            )

    def _draw_character_panel(self, surface: pygame.Surface) -> None:
        draw_text(surface, "Personajes", self.character_title_position, 24, TEXT, bold=True)
        for character_initial, button_rect in self.initial_button_rects.items():
            already_placed = not self.board.can_place(character_initial)
            is_selected = self.selected_character_initial == character_initial
            draw_button(
                surface,
                button_rect,
                character_initial,
                selected=is_selected,
                disabled=already_placed,
            )

        pygame.draw.rect(surface, PANEL, self.clue_panel_rect, border_radius=8)
        pygame.draw.rect(surface, LINE, self.clue_panel_rect, width=2, border_radius=8)
        draw_text(
            surface,
            "Pistas del caso",
            (
                self.clue_panel_rect.x + PANEL_PADDING,
                self.clue_panel_rect.y + PANEL_PADDING,
            ),
            18,
            ACCENT,
            bold=True,
        )
        self._draw_clue_list(surface)

    def _draw_clue_list(self, surface: pygame.Surface) -> None:
        clue_count = len(self.puzzle.characters)
        if clue_count == 0:
            return

        column_count = 2 if self.clue_panel_rect.width >= 620 else 1
        rows_per_column = (clue_count + column_count - 1) // column_count
        clue_font_size = 15 if clue_count <= 6 else 14
        clue_area_top = self.clue_panel_rect.y + PANEL_PADDING + CLUE_HEADER_HEIGHT
        clue_area_bottom = self.clue_panel_rect.bottom - PANEL_PADDING
        row_height = max(
            clue_font_size + CLUE_LINE_GAP,
            (clue_area_bottom - clue_area_top) // rows_per_column,
        )
        max_lines_per_clue = max(
            1,
            (row_height - CLUE_LINE_GAP) // (clue_font_size + CLUE_LINE_GAP),
        )
        column_width = (
            self.clue_panel_rect.width
            - PANEL_PADDING * 2
            - CLUE_COLUMN_GAP * (column_count - 1)
        ) // column_count

        for clue_index, character_initial in enumerate(self.puzzle.characters):
            clue_col = clue_index // rows_per_column
            clue_row = clue_index % rows_per_column
            clue_x = (
                self.clue_panel_rect.x
                + PANEL_PADDING
                + clue_col * (column_width + CLUE_COLUMN_GAP)
            )
            clue_y = clue_area_top + clue_row * row_height
            character = self.puzzle.characters[character_initial]
            clue_text = f"{character_initial} {character.name}: {character.clue}"
            draw_text_block(
                surface,
                clue_text,
                (clue_x, clue_y),
                column_width,
                clue_font_size,
                TEXT,
                line_gap=CLUE_LINE_GAP,
                max_lines=max_lines_per_clue,
            )

    def _draw_message(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, PANEL, self.message_panel_rect, border_radius=8)
        pygame.draw.rect(
            surface,
            GOOD if self.message_is_positive else BAD,
            self.message_panel_rect,
            width=2,
            border_radius=8,
        )
        draw_text_block(
            surface,
            self.message,
            (
                self.message_panel_rect.x + PANEL_PADDING,
                self.message_panel_rect.y + PANEL_PADDING,
            ),
            self.message_panel_rect.width - PANEL_PADDING * 2,
            20,
            TEXT,
            line_gap=5,
            max_lines=3,
        )

    def _draw_final_prompt(self, surface: pygame.Surface) -> None:
        draw_text(
            surface,
            "Quien es el asesino?",
            self.final_prompt_title_position,
            24,
            ACCENT,
            bold=True,
        )
        pygame.draw.rect(surface, PANEL_LIGHT, self.answer_box_rect, border_radius=6)
        pygame.draw.rect(surface, ACCENT, self.answer_box_rect, width=2, border_radius=6)
        draw_text(
            surface,
            self.murderer_answer or "Nombre...",
            (self.answer_box_rect.x + 12, self.answer_box_rect.y + 11),
            20,
            TEXT if self.murderer_answer else MUTED,
        )
        draw_button(surface, self.submit_answer_button_rect, "Validar")
        if self.final_answer_message:
            final_answer_width = self.right_column_rect.width
            if self.final_answer_is_correct and self.level_number < self.total_levels:
                final_answer_width = (
                    self.next_level_button_rect.x
                    - self.final_answer_position[0]
                    - PANEL_PADDING
                )
            draw_text_block(
                surface,
                self.final_answer_message,
                self.final_answer_position,
                final_answer_width,
                18,
                GOOD if self.final_answer_is_correct else BAD,
                bold=self.final_answer_is_correct,
                line_gap=4,
                max_lines=2,
            )
        if self.final_answer_is_correct:
            if self.level_number < self.total_levels:
                draw_button(surface, self.next_level_button_rect, "Siguiente caso", selected=True)
            else:
                draw_text(
                    surface,
                    "Casos disponibles completados.",
                    self.next_level_button_rect.topleft,
                    18,
                    GOOD,
                    bold=True,
                )
