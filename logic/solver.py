# logic/solver.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment, ConstraintEngine
from logic.propagation import Domains, build_initial_domains, propagate_constraints


class CSPSolver:
    """Backtracking CSP solver with forward checking, propagation, and MRV."""

    def __init__(self, puzzle: Puzzle) -> None:
        self.puzzle = puzzle
        self.engine = ConstraintEngine(puzzle)
        self.initial_domains = build_initial_domains(puzzle, self.engine)

    def domains_for(self, current_assignment: Assignment) -> Domains | None:
        return propagate_constraints(
            self.puzzle,
            self.engine,
            dict(current_assignment),
            self.initial_domains,
        )

    def is_consistent(self, current_assignment: Assignment) -> bool:
        return self.engine.assignment_consistent(current_assignment)

    def has_solution(self, current_assignment: Assignment) -> bool:
        propagated_domains = self.domains_for(current_assignment)
        if propagated_domains is None:
            return False
        return self._backtrack(dict(current_assignment), propagated_domains) is not None

    def solve(self) -> Assignment | None:
        propagated_domains = self.domains_for({})
        if propagated_domains is None:
            return None
        return self._backtrack({}, propagated_domains)

    def _backtrack(
        self,
        current_assignment: Assignment,
        current_domains: Domains,
    ) -> Assignment | None:
        if len(current_assignment) == len(self.puzzle.characters):
            return (
                dict(current_assignment)
                if self.engine.assignment_consistent(current_assignment)
                else None
            )

        next_character_initial = self._select_unassigned_variable(
            current_assignment,
            current_domains,
        )
        if next_character_initial is None:
            return None

        for candidate_coordinate in sorted(current_domains[next_character_initial]):
            tentative_assignment = dict(current_assignment)
            tentative_assignment[next_character_initial] = candidate_coordinate
            if not self.engine.assignment_consistent(tentative_assignment):
                continue

            propagated_domains = propagate_constraints(
                self.puzzle,
                self.engine,
                tentative_assignment,
                current_domains,
            )
            if propagated_domains is None:
                continue

            solved_assignment = self._backtrack(tentative_assignment, propagated_domains)
            if solved_assignment is not None:
                return solved_assignment

        return None

    def _select_unassigned_variable(
        self,
        current_assignment: Assignment,
        current_domains: Domains,
    ) -> str | None:
        unassigned_initials = [
            character_initial
            for character_initial in self.puzzle.characters
            if character_initial not in current_assignment
        ]
        if not unassigned_initials:
            return None
        return min(
            unassigned_initials,
            key=lambda character_initial: len(current_domains[character_initial]),
        )
