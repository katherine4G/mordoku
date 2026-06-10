# logic/hints.py
from __future__ import annotations

from data.puzzles import Coord, Puzzle
from logic.constraints import Assignment, ConstraintEngine
from logic.solver import CSPSolver


RULE_HINTS_BY_RULE = {
    "inside_car": "{name} necesita una casilla con carro.",
    "on_oil": "{name} debe estar sobre una mancha de aceite.",
    "inside_chair": "{name} necesita una silla.",
    "only_chair": "{name} debe estar en una silla, y nadie mas puede usar silla.",
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
    current_assignment: Assignment,
    character_initial: str,
    target_coordinate: Coord,
) -> str:
    engine = ConstraintEngine(puzzle)

    for other_character_initial, other_coordinate in current_assignment.items():
        if other_coordinate == target_coordinate:
            occupied_character_name = puzzle.characters[other_character_initial].name
            return f"Esa casilla ya esta ocupada por {occupied_character_name}."
        if other_coordinate[0] == target_coordinate[0]:
            return "No puede repetirse fila: esa fila ya esta bloqueada."
        if other_coordinate[1] == target_coordinate[1]:
            return "No puede repetirse columna: esa columna ya esta bloqueada."

    tentative_assignment = dict(current_assignment)
    tentative_assignment[character_initial] = target_coordinate

    if not engine.person_constraint_ok(
        character_initial,
        target_coordinate,
        tentative_assignment,
    ):
        return _rule_hint(puzzle, character_initial)

    propagated_domains = solver.domains_for(tentative_assignment)
    if propagated_domains is None:
        stranded_character_name = _first_stranded_character(puzzle, solver, tentative_assignment)
        if stranded_character_name:
            return f"Ese movimiento deja sin opciones validas a {stranded_character_name}."
        return "Ese movimiento contradice las pistas al hacer forward checking."

    forced_character_name = _forced_character_name(puzzle, current_assignment, solver)
    if forced_character_name:
        return f"Solo queda una casilla valida para {forced_character_name}."

    return "Al cruzar todas las pistas, esa casilla queda descartada."


def final_answer_hint(victim_name: str, received_answer: str) -> str:
    if not received_answer.strip():
        return f"Escribe el nombre del sospechoso que quedo a solas con {victim_name}."
    return f"{received_answer.strip()} no quedo como el unico sospechoso con {victim_name}."


def _rule_hint(puzzle: Puzzle, character_initial: str) -> str:
    character = puzzle.characters[character_initial]
    template = RULE_HINTS_BY_RULE.get(
        character.rule,
        "{name} no cumple su pista en esa casilla.",
    )
    return template.format(name=character.name)


def _first_stranded_character(
    puzzle: Puzzle,
    solver: CSPSolver,
    current_assignment: Assignment,
) -> str | None:
    initial_domains = solver.domains_for({})
    if initial_domains is None:
        return None
    for character_initial in puzzle.characters:
        if character_initial in current_assignment:
            continue
        propagated_domains = solver.domains_for(current_assignment)
        if propagated_domains is None or not propagated_domains.get(character_initial):
            return puzzle.characters[character_initial].name
    return None


def _forced_character_name(
    puzzle: Puzzle,
    current_assignment: Assignment,
    solver: CSPSolver,
) -> str | None:
    propagated_domains = solver.domains_for(current_assignment)
    if propagated_domains is None:
        return None
    for character_initial, possible_coordinates in propagated_domains.items():
        if character_initial not in current_assignment and len(possible_coordinates) == 1:
            return puzzle.characters[character_initial].name
    return None
