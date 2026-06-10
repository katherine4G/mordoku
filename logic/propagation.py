# logic/propagation.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment, ConstraintEngine

Domains = dict[str, set[Coord]]


def build_initial_domains(puzzle: Puzzle, engine: ConstraintEngine) -> Domains:
    initial_domains: Domains = {}
    for character_initial in puzzle.characters:
        initial_domains[character_initial] = {
            candidate_coordinate
            for candidate_coordinate in puzzle.all_cells()
            if engine.person_constraint_ok(character_initial, candidate_coordinate, {})
        }
    return initial_domains


def propagate_constraints(
    puzzle: Puzzle,
    engine: ConstraintEngine,
    current_assignment: Assignment,
    current_domains: Domains,
) -> Domains | None:
    """Apply row/column pruning, person rules, and singleton propagation."""

    propagated_domains = {
        character_initial: set(possible_coordinates)
        for character_initial, possible_coordinates in current_domains.items()
    }
    changed = True

    while changed:
        changed = False
        if not engine.assignment_consistent(current_assignment):
            return None

        assigned_rows = {
            assigned_coordinate[0]
            for assigned_coordinate in current_assignment.values()
        }
        assigned_columns = {
            assigned_coordinate[1]
            for assigned_coordinate in current_assignment.values()
        }
        assigned_coordinates = set(current_assignment.values())

        for character_initial in puzzle.characters:
            if character_initial in current_assignment:
                propagated_domains[character_initial] = {current_assignment[character_initial]}
                continue

            valid_coordinates: set[Coord] = set()
            for candidate_coordinate in propagated_domains[character_initial]:
                if (
                    candidate_coordinate in assigned_coordinates
                    or candidate_coordinate[0] in assigned_rows
                    or candidate_coordinate[1] in assigned_columns
                ):
                    continue
                tentative_assignment = dict(current_assignment)
                tentative_assignment[character_initial] = candidate_coordinate
                if engine.assignment_consistent(tentative_assignment):
                    valid_coordinates.add(candidate_coordinate)

            if valid_coordinates != propagated_domains[character_initial]:
                propagated_domains[character_initial] = valid_coordinates
                changed = True

            if not valid_coordinates:
                return None

        forced_assignments = {
            character_initial: next(iter(possible_coordinates))
            for character_initial, possible_coordinates in propagated_domains.items()
            if character_initial not in current_assignment and len(possible_coordinates) == 1
        }
        for character_initial, forced_coordinate in forced_assignments.items():
            tentative_assignment = dict(current_assignment)
            tentative_assignment[character_initial] = forced_coordinate
            if not engine.assignment_consistent(tentative_assignment):
                return None
            current_assignment[character_initial] = forced_coordinate
            changed = True

    return propagated_domains


def forward_check(
    puzzle: Puzzle,
    engine: ConstraintEngine,
    current_assignment: Assignment,
    current_domains: Domains,
) -> Domains | None:
    return propagate_constraints(puzzle, engine, dict(current_assignment), current_domains)
