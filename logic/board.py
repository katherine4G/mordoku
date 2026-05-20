# logic/board.py
from __future__ import annotations

from dataclasses import dataclass

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment
from logic.hints import final_answer_hint, hint_for_move
from logic.solver import CSPSolver


@dataclass(frozen=True)
class MoveResult:
    accepted: bool
    message: str


class BoardState:
    def __init__(self, puzzle: Puzzle) -> None:
        self.puzzle = puzzle
        self.assignment: Assignment = {}
        self.solver = CSPSolver(puzzle)
        self.domains = self.solver.domains_for({}) or {}

    @property
    def blocked_rows(self) -> set[int]:
        return {coord[0] for coord in self.assignment.values()}

    @property
    def blocked_cols(self) -> set[int]:
        return {coord[1] for coord in self.assignment.values()}

    def can_place(self, initial: str) -> bool:
        return initial in self.puzzle.characters and initial not in self.assignment

    def place(self, initial: str, coord: Coord) -> MoveResult:
        if not self.can_place(initial):
            return MoveResult(False, "Ese personaje ya fue colocado.")

        if self.puzzle.solution[initial] != coord:
            hint = hint_for_move(self.puzzle, self.solver, self.assignment, initial, coord)
            return MoveResult(False, hint)

        tentative = dict(self.assignment)
        tentative[initial] = coord
        domains = self.solver.domains_for(tentative)
        if domains is None or not self.solver.has_solution(tentative):
            hint = hint_for_move(self.puzzle, self.solver, self.assignment, initial, coord)
            return MoveResult(False, hint)

        self.assignment = tentative
        self.domains = domains
        name = self.puzzle.characters[initial].name
        return MoveResult(True, f"{name} encaja con las pistas.")

    def cell_value(self, coord: Coord) -> str | None:
        for initial, placed in self.assignment.items():
            if placed == coord:
                return initial
        return None

    def is_complete(self) -> bool:
        return len(self.assignment) == len(self.puzzle.characters)

    def validate_murderer(self, answer: str) -> MoveResult:
        murderer = self.puzzle.characters[self.puzzle.murderer]
        victim = self.puzzle.characters[self.puzzle.victim]
        expected = murderer.name.lower()
        cleaned = answer.strip().lower()
        if cleaned == expected:
            return MoveResult(True, f"Correcto: {murderer.name} quedo a solas con {victim.name}.")
        return MoveResult(False, final_answer_hint(victim.name, answer))
