# logic/propagation.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment, ConstraintEngine

Domains = dict[str, set[Coord]]


def build_initial_domains(puzzle: Puzzle, engine: ConstraintEngine) -> Domains:
    domains: Domains = {}
    for initial in puzzle.characters:
        domains[initial] = {
            cell
            for cell in puzzle.all_cells()
            if engine.person_constraint_ok(initial, cell, {})
        }
    return domains


def propagate_constraints(
    puzzle: Puzzle,
    engine: ConstraintEngine,
    assignment: Assignment,
    domains: Domains,
) -> Domains | None:
    """Apply row/column pruning, person rules, and singleton propagation."""

    domains = {initial: set(cells) for initial, cells in domains.items()}
    changed = True

    while changed:
        changed = False
        if not engine.assignment_consistent(assignment):
            return None

        used_rows = {coord[0] for coord in assignment.values()}
        used_cols = {coord[1] for coord in assignment.values()}
        used_cells = set(assignment.values())

        for initial in puzzle.characters:
            if initial in assignment:
                domains[initial] = {assignment[initial]}
                continue

            filtered: set[Coord] = set()
            for coord in domains[initial]:
                if coord in used_cells or coord[0] in used_rows or coord[1] in used_cols:
                    continue
                tentative = dict(assignment)
                tentative[initial] = coord
                if engine.assignment_consistent(tentative):
                    filtered.add(coord)

            if filtered != domains[initial]:
                domains[initial] = filtered
                changed = True

            if not filtered:
                return None

        singles = {
            initial: next(iter(cells))
            for initial, cells in domains.items()
            if initial not in assignment and len(cells) == 1
        }
        for initial, coord in singles.items():
            tentative = dict(assignment)
            tentative[initial] = coord
            if not engine.assignment_consistent(tentative):
                return None
            assignment[initial] = coord
            changed = True

    return domains


def forward_check(
    puzzle: Puzzle,
    engine: ConstraintEngine,
    assignment: Assignment,
    domains: Domains,
) -> Domains | None:
    return propagate_constraints(puzzle, engine, dict(assignment), domains)
