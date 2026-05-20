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

    def domains_for(self, assignment: Assignment) -> Domains | None:
        return propagate_constraints(
            self.puzzle,
            self.engine,
            dict(assignment),
            self.initial_domains,
        )

    def is_consistent(self, assignment: Assignment) -> bool:
        return self.engine.assignment_consistent(assignment)

    def has_solution(self, assignment: Assignment) -> bool:
        domains = self.domains_for(assignment)
        if domains is None:
            return False
        return self._backtrack(dict(assignment), domains) is not None

    def solve(self) -> Assignment | None:
        domains = self.domains_for({})
        if domains is None:
            return None
        return self._backtrack({}, domains)

    def _backtrack(self, assignment: Assignment, domains: Domains) -> Assignment | None:
        if len(assignment) == len(self.puzzle.characters):
            return dict(assignment) if self.engine.assignment_consistent(assignment) else None

        initial = self._select_unassigned_variable(assignment, domains)
        if initial is None:
            return None

        for coord in sorted(domains[initial]):
            tentative = dict(assignment)
            tentative[initial] = coord
            if not self.engine.assignment_consistent(tentative):
                continue

            next_domains = propagate_constraints(
                self.puzzle,
                self.engine,
                tentative,
                domains,
            )
            if next_domains is None:
                continue

            result = self._backtrack(tentative, next_domains)
            if result is not None:
                return result

        return None

    def _select_unassigned_variable(
        self,
        assignment: Assignment,
        domains: Domains,
    ) -> str | None:
        candidates = [
            initial for initial in self.puzzle.characters if initial not in assignment
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda initial: len(domains[initial]))
