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
        character_initial: str,
        target_coordinate: Coord,
        current_assignment: Assignment,
    ) -> bool:
        if target_coordinate in self.puzzle.blocked_cells:
            return False

        character = self.puzzle.characters[character_initial]
        character_rule = character.rule

        if character_rule == "with_elyse_living_room":
            return self.puzzle.room_at(target_coordinate) == "living_room"
        if character_rule == "inside_car":
            return self.puzzle.feature_at(target_coordinate, "car")
        if character_rule == "on_oil":
            return self.puzzle.feature_at(target_coordinate, "oil")
        if character_rule == "inside_chair":
            return self.puzzle.feature_at(target_coordinate, "chair")
        if character_rule == "only_chair":
            return self.puzzle.feature_at(target_coordinate, "chair")
        if character_rule == "on_bed":
            return self.puzzle.feature_at(target_coordinate, "bed")
        if character_rule == "in_kitchen":
            return self.puzzle.room_at(target_coordinate) == "kitchen"
        if character_rule == "in_shed":
            return self.puzzle.room_at(target_coordinate) == "shed"
        if character_rule == "beside_tree":
            return self._beside_feature_in_same_room(target_coordinate, "tree")
        if character_rule == "bedroom_or_sunroom":
            return self.puzzle.room_at(target_coordinate) in {"bedroom", "sunroom"}
        if character_rule == "on_carpet":
            return self.puzzle.feature_at(target_coordinate, "carpet")
        if character_rule == "in_garden":
            return self.puzzle.room_at(target_coordinate) == "garden"
        if character_rule == "alone":
            return self._character_is_alone_in_room(
                character_initial,
                target_coordinate,
                current_assignment,
            )
        if character_rule == "alone_waiting_room":
            return self._diane_is_alone(target_coordinate, current_assignment)
        if character_rule == "beside_shelf":
            return self._beside_feature_in_same_room(target_coordinate, "shelf")
        if character_rule == "beside_tv":
            return self._beside_feature_in_same_room(target_coordinate, "tv")
        if character_rule == "victim":
            return True
        return True

    def assignment_consistent(self, current_assignment: Assignment) -> bool:
        if not self._rows_and_columns_are_unique(current_assignment):
            return False
        if not self._exclusive_feature_rules_ok(current_assignment):
            return False
        if not self._with_elyse_living_room_rule_ok(current_assignment):
            return False

        for character_initial, assigned_coordinate in current_assignment.items():
            if not self.person_constraint_ok(
                character_initial,
                assigned_coordinate,
                current_assignment,
            ):
                return False

        return self._victim_murderer_rule_ok(current_assignment)

    def _with_elyse_living_room_rule_ok(self, current_assignment: Assignment) -> bool:
        linked_initials = {
            character_initial
            for character_initial, character in self.puzzle.characters.items()
            if character.rule == "with_elyse_living_room"
        }
        if not linked_initials:
            return True

        required_living_room_initials = set(linked_initials)
        if "E" in self.puzzle.characters:
            required_living_room_initials.add("E")

        for character_initial in required_living_room_initials:
            if character_initial not in current_assignment:
                continue
            if self.puzzle.room_at(current_assignment[character_initial]) != "living_room":
                return False
        return True

    def _rows_and_columns_are_unique(self, current_assignment: Assignment) -> bool:
        occupied_rows: set[int] = set()
        occupied_columns: set[int] = set()
        occupied_coordinates: set[Coord] = set()

        for assigned_coordinate in current_assignment.values():
            board_row, board_col = assigned_coordinate
            if (
                board_row in occupied_rows
                or board_col in occupied_columns
                or assigned_coordinate in occupied_coordinates
            ):
                return False
            occupied_rows.add(board_row)
            occupied_columns.add(board_col)
            occupied_coordinates.add(assigned_coordinate)
        return True

    def _diane_is_alone(self, target_coordinate: Coord, current_assignment: Assignment) -> bool:
        if self.puzzle.room_at(target_coordinate) != "waiting_room":
            return False
        for other_character_initial, other_coordinate in current_assignment.items():
            if (
                other_character_initial != "D"
                and self.puzzle.room_at(other_coordinate) == "waiting_room"
            ):
                return False
        return True

    def _character_is_alone_in_room(
        self,
        character_initial: str,
        target_coordinate: Coord,
        current_assignment: Assignment,
    ) -> bool:
        target_room = self.puzzle.room_at(target_coordinate)
        if target_room is None:
            return False

        for other_character_initial, other_coordinate in current_assignment.items():
            if other_character_initial == character_initial:
                continue
            if self.puzzle.room_at(other_coordinate) == target_room:
                return False
        return True

    def _beside_feature_in_same_room(self, target_coordinate: Coord, feature_name: str) -> bool:
        current_room = self.puzzle.room_at(target_coordinate)
        if current_room is None:
            return False

        board_row, board_col = target_coordinate
        orthogonal_neighbors = {
            (board_row - 1, board_col),
            (board_row + 1, board_col),
            (board_row, board_col - 1),
            (board_row, board_col + 1),
        }
        for neighbor_coordinate in orthogonal_neighbors:
            if (
                self.puzzle.room_at(neighbor_coordinate) == current_room
                and self.puzzle.feature_at(neighbor_coordinate, feature_name)
            ):
                return True
        return False

    def _exclusive_feature_rules_ok(self, current_assignment: Assignment) -> bool:
        chair_only_initials = {
            character_initial
            for character_initial, character in self.puzzle.characters.items()
            if character.rule == "only_chair"
        }
        if not chair_only_initials:
            return True

        for character_initial, assigned_coordinate in current_assignment.items():
            if (
                self.puzzle.feature_at(assigned_coordinate, "chair")
                and character_initial not in chair_only_initials
            ):
                return False
        return True

    def _victim_murderer_rule_ok(self, current_assignment: Assignment) -> bool:
        victim_initial = self.puzzle.victim
        murderer_initial = self.puzzle.murderer

        if victim_initial not in current_assignment:
            return True

        victim_room = self.puzzle.room_at(current_assignment[victim_initial])
        if victim_room is None:
            return False

        for character_initial, assigned_coordinate in current_assignment.items():
            if character_initial in {victim_initial, murderer_initial}:
                continue
            if self.puzzle.room_at(assigned_coordinate) == victim_room:
                return False

        if murderer_initial in current_assignment:
            return self.puzzle.room_at(current_assignment[murderer_initial]) == victim_room
        return True
