# logic/hints.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment, ConstraintEngine
from logic.solver import CSPSolver


RULE_HINTS_BY_RULE = {
    "inside_car": "{name} necesita una casilla con carro.",
    "on_oil": "{name} debe estar sobre una mancha de aceite.",
    "inside_chair": "{name} necesita una silla.",
    "only_chair": "{name} debe estar en una silla, y nadie más puede usar silla.",
    "on_bed": "{name} debe estar sobre una cama.",
    "in_kitchen": "{name} debe estar en la cocina.",
    "alone_waiting_room": "{name} debe quedar sola en la sala de espera.",
    "beside_shelf": "{name} debe estar junto a un estante. Recuerda que no incluye diagonales.",
    "beside_tv": "{name} debe estar junto al televisor. Recuerda que no incluye diagonales.",
    "victim": "{name} solo puede quedar con el asesino.",
}


def hint_for_move(
    puzzle: Puzzle,
    solver: CSPSolver,
    assignment: Assignment,
    initial: str,
    coord: Coord,
) -> str:
    engine = ConstraintEngine(puzzle)

    for other_initial, other_coord in assignment.items():
        if other_coord == coord:
            return f"Esa casilla ya esta ocupada por {puzzle.characters[other_initial].name}."
        if other_coord[0] == coord[0]:
            return "No puede repetirse fila: esa fila ya esta bloqueada."
        if other_coord[1] == coord[1]:
            return "No puede repetirse columna: esa columna ya esta bloqueada."

    tentative = dict(assignment)
    tentative[initial] = coord

    if not engine.person_constraint_ok(initial, coord, tentative):
        return _rule_hint(puzzle, initial)

    domains = solver.domains_for(tentative)
    if domains is None:
        stranded = _first_stranded_character(puzzle, solver, tentative)
        if stranded:
            return f"Ese movimiento deja sin opciones validas a {stranded}."
        return "Ese movimiento contradice las pistas al hacer forward checking."

    forced = _forced_character_name(puzzle, assignment, solver)
    if forced:
        return f"Solo queda una casilla valida para {forced}."

    return "Al cruzar todas las pistas, esa casilla queda descartada."


def final_answer_hint(victim_name: str, received: str) -> str:
    if not received.strip():
        return f"Escribe el nombre del sospechoso que quedo a solas con {victim_name}."
    return f"{received.strip()} no quedo como el unico sospechoso con {victim_name}."


def _rule_hint(puzzle: Puzzle, initial: str) -> str:
    character = puzzle.characters[initial]
    template = RULE_HINTS_BY_RULE.get(
        character.rule,
        "{name} no cumple su pista en esa casilla.",
    )
    return template.format(name=character.name)


def _first_stranded_character(
    puzzle: Puzzle,
    solver: CSPSolver,
    assignment: Assignment,
) -> str | None:
    base_domains = solver.domains_for({})
    if base_domains is None:
        return None
    for initial in puzzle.characters:
        if initial in assignment:
            continue
        domains = solver.domains_for(assignment)
        if domains is None or not domains.get(initial):
            return puzzle.characters[initial].name
    return None


def _forced_character_name(
    puzzle: Puzzle,
    assignment: Assignment,
    solver: CSPSolver,
) -> str | None:
    domains = solver.domains_for(assignment)
    if domains is None:
        return None
    for initial, cells in domains.items():
        if initial not in assignment and len(cells) == 1:
            return puzzle.characters[initial].name
    return None
