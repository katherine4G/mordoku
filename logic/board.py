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
        return {assigned_coordinate[0] for assigned_coordinate in self.assignment.values()}

    @property
    def blocked_cols(self) -> set[int]:
        return {assigned_coordinate[1] for assigned_coordinate in self.assignment.values()}

    def can_place(self, character_initial: str) -> bool:
        return (
            character_initial in self.puzzle.characters
            and character_initial not in self.assignment
        )

    def place(self, character_initial: str, target_coordinate: Coord) -> MoveResult:
        if not self.can_place(character_initial):
            return MoveResult(False, "Ese personaje ya fue colocado.")

        if self.puzzle.solution[character_initial] != target_coordinate:
            rejection_hint = hint_for_move(
                self.puzzle,
                self.solver,
                self.assignment,
                character_initial,
                target_coordinate,
            )
            return MoveResult(False, rejection_hint)

        tentative_assignment = dict(self.assignment)
        tentative_assignment[character_initial] = target_coordinate
        propagated_domains = self.solver.domains_for(tentative_assignment)
        if propagated_domains is None or not self.solver.has_solution(tentative_assignment):
            rejection_hint = hint_for_move(
                self.puzzle,
                self.solver,
                self.assignment,
                character_initial,
                target_coordinate,
            )
            return MoveResult(False, rejection_hint)

        self.assignment = tentative_assignment
        self.domains = propagated_domains
        character_name = self.puzzle.characters[character_initial].name
        return MoveResult(True, f"{character_name} encaja con las pistas.")

    def character_initial_at(self, target_coordinate: Coord) -> str | None:
        for character_initial, assigned_coordinate in self.assignment.items():
            if assigned_coordinate == target_coordinate:
                return character_initial
        return None

    def is_complete(self) -> bool:
        return len(self.assignment) == len(self.puzzle.characters)

    def validate_murderer(self, candidate_answer: str) -> MoveResult:
        murderer_character = self.puzzle.characters[self.puzzle.murderer]
        victim_character = self.puzzle.characters[self.puzzle.victim]
        expected_murderer_name = murderer_character.name.lower()
        cleaned_answer = candidate_answer.strip().lower()
        if cleaned_answer == expected_murderer_name:
            return MoveResult(
                True,
                f"Correcto: {murderer_character.name} quedo a solas con {victim_character.name}.",
            )
        return MoveResult(False, final_answer_hint(victim_character.name, candidate_answer))
