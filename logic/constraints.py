# logic/constraints.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle

Assignment = dict[str, Coord]


class ConstraintEngine:
    """Rule engine for Murdoku's orthogonal Sudoku-like logic."""

    def __init__(self, puzzle: Puzzle) -> None:
        self.puzzle = puzzle

    def person_constraint_ok(
        self,
        initial: str,
        coord: Coord,
        assignment: Assignment,
    ) -> bool:
        character = self.puzzle.characters[initial]
        rule = character.rule

        if rule == "inside_car":
            return self.puzzle.feature_at(coord, "car")
        if rule == "on_oil":
            return self.puzzle.feature_at(coord, "oil")
        if rule == "inside_chair":
            return self.puzzle.feature_at(coord, "chair")
        if rule == "only_chair":
            return self.puzzle.feature_at(coord, "chair")
        if rule == "on_bed":
            return self.puzzle.feature_at(coord, "bed")
        if rule == "in_kitchen":
            return self.puzzle.room_at(coord) == "kitchen"
        if rule == "alone_waiting_room":
            return self._diane_is_alone(coord, assignment)
        if rule == "beside_shelf":
            return self._beside_feature_in_same_room(coord, "shelf")
        if rule == "beside_tv":
            return self._beside_feature_in_same_room(coord, "tv")
        if rule == "victim":
            return True
        return True

    def assignment_consistent(self, assignment: Assignment) -> bool:
        if not self._rows_and_columns_are_unique(assignment):
            return False
        if not self._exclusive_feature_rules_ok(assignment):
            return False

        for initial, coord in assignment.items():
            if not self.person_constraint_ok(initial, coord, assignment):
                return False

        return self._victim_murderer_rule_ok(assignment)

    def _rows_and_columns_are_unique(self, assignment: Assignment) -> bool:
        rows: set[int] = set()
        cols: set[int] = set()
        cells: set[Coord] = set()

        for coord in assignment.values():
            row, col = coord
            if row in rows or col in cols or coord in cells:
                return False
            rows.add(row)
            cols.add(col)
            cells.add(coord)
        return True

    def _diane_is_alone(self, coord: Coord, assignment: Assignment) -> bool:
        if self.puzzle.room_at(coord) != "waiting_room":
            return False
        for other_initial, other_coord in assignment.items():
            if other_initial != "D" and self.puzzle.room_at(other_coord) == "waiting_room":
                return False
        return True

    def _beside_feature_in_same_room(self, coord: Coord, feature: str) -> bool:
        room = self.puzzle.room_at(coord)
        if room is None:
            return False

        row, col = coord
        orthogonal_neighbors = {
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        }
        for neighbor in orthogonal_neighbors:
            if self.puzzle.room_at(neighbor) == room and self.puzzle.feature_at(neighbor, feature):
                return True
        return False

    def _exclusive_feature_rules_ok(self, assignment: Assignment) -> bool:
        only_chair_initials = {
            initial
            for initial, character in self.puzzle.characters.items()
            if character.rule == "only_chair"
        }
        if not only_chair_initials:
            return True

        for initial, coord in assignment.items():
            if self.puzzle.feature_at(coord, "chair") and initial not in only_chair_initials:
                return False
        return True

    def _victim_murderer_rule_ok(self, assignment: Assignment) -> bool:
        victim = self.puzzle.victim
        murderer = self.puzzle.murderer

        if victim not in assignment:
            return True

        victim_room = self.puzzle.room_at(assignment[victim])
        if victim_room is None:
            return False

        for initial, coord in assignment.items():
            if initial in {victim, murderer}:
                continue
            if self.puzzle.room_at(coord) == victim_room:
                return False

        if murderer in assignment:
            return self.puzzle.room_at(assignment[murderer]) == victim_room
        return True
