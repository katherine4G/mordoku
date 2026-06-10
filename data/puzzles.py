# data/puzzles.py
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

Coord = tuple[int, int]


@dataclass(frozen=True)
class Character:
    initial: str
    name: str
    clue: str
    rule: str


@dataclass(frozen=True)
class Puzzle:
    title: str
    size: int
    image_path: Path
    characters: dict[str, Character]
    rooms: dict[str, set[Coord]]
    features: dict[str, set[Coord]]
    solution: dict[str, Coord]
    victim: str
    murderer: str
    blocked_cells: set[Coord] = field(default_factory=set)

    def all_cells(self) -> set[Coord]:
        return {
            (board_row, board_col)
            for board_row in range(self.size)
            for board_col in range(self.size)
        }

    def room_at(self, board_coordinate: Coord) -> str | None:
        for room_name, room_cells in self.rooms.items():
            if board_coordinate in room_cells:
                return room_name
        return None

    def feature_at(self, board_coordinate: Coord, feature_name: str) -> bool:
        return board_coordinate in self.features.get(feature_name, set())

    def occupiable_cells(self) -> set[Coord]:
        return self.all_cells() - self.blocked_cells


ROOT = Path(__file__).resolve().parents[1]

LEVEL_1 = Puzzle(
    title="Caso 1: Taller Murdoku",
    size=6,
    image_path=ROOT / "assets" / "images" / "mordoku_nivel1.png",
    victim="V",
    murderer="C",
    characters={
        "A": Character("A", "Anthony", "Dentro de un carro.", "inside_car"),
        "B": Character("B", "Brock", "Sobre aceite.", "on_oil"),
        "C": Character("C", "Crystal", "Sentada en una silla.", "inside_chair"),
        "D": Character("D", "Diane", "En la sala de espera.", "alone_waiting_room"),
        "E": Character("E", "Emilio", "Junto a un estante.", "beside_shelf"),
        "V": Character("V", "Vaughn", "Victima del asesino.", "victim"),
    },
    rooms={
        "reception": {
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2,0),
            (2,1),
            (2,2),
            (3,0),
        },
        "storage": {
            (0, 4),
            (0, 5),
            (1, 5),
        },
        "waiting_room": {
            (0,3),
            (1, 4),
            (1, 3),
            (2, 3),
            (2, 4),
            (2, 5),
        },
        "garage": {
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
        },
    },
    features={
        "car": {(5, 3), (5, 4),(4, 1), (4, 2)},
        "oil": {(5, 1), (4, 3)},
        "chair": {(0, 1), (2,3), (2,4)},
        "shelf": {(0, 5), (2, 2), (3, 3),(3,4)},
    },
    solution={
        "A": (5, 4),
        "B": (4, 3),
        "C": (0, 1),
        "D": (2, 5),
        "E": (3, 2),
        "V": (1, 0),
    },
)

LEVEL_2 = Puzzle(
    title="Caso 2: Muerte en Netflix",
    size=6,
    image_path=ROOT / "assets" / "images" / "mordoku_nivel2.png",
    characters={
        "A": Character("A", "Austin", "Junto a un estante.", "beside_shelf"),
        "B": Character("B", "Barbara", "En la cama.", "on_bed"),
        "C": Character("C", "Charlotte", "En una silla.", "only_chair"),
        "D": Character("D", "Dean", "En la cocina.", "in_kitchen"),
        "E": Character("E", "Enid", "Junto a la TV.", "beside_tv"),
        "V": Character("V", "Vaughn", "Victima del asesino.", "victim"),
    },
    rooms={
        "bedroom": {
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        },
        "bathroom": {
            (0, 4),
            (0, 5),
            (1, 4),
            (1, 5),
            (2, 5),
        },
        "kitchen": {
            (3, 0),
            (3, 1),
            (4, 0),
            (4, 1),
            (5, 0),
            (5, 1),
        },
        "living_room": {
            (0, 3),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 5),
        },
    },
    features={
        "bed": {(0, 0), (0, 1)},
        "chair": {(0, 5), (1, 3), (2, 4), (3, 2), (3, 4)},
        "shelf": {(2, 0), (4, 0), (5, 2)},
        "tv": {(4, 5)},
    },
    solution={
        "A": (5, 3),
        "B": (0, 0),
        "C": (2, 4),
        "D": (4, 1),
        "E": (3, 5),
        "V": (1, 2),
    },
    victim="V",
    murderer="B",
)

LEVEL_3 = Puzzle(
    title="Caso 3: The Backyard Garden",
    size=9,
    image_path=ROOT / "assets" / "images" / "mordoku_nivel3.png",
    characters={
        "A": Character(
            "A",
            "Aaron",
            "Con Elyse en la sala de estar.",
            "with_elyse_living_room",
        ),
        "B": Character("B", "Bruce", "En el cobertizo.", "in_shed"),
        "C": Character("C", "Carissa", "Junto a un arbol.", "beside_tree"),
        "D": Character(
            "D",
            "Denise",
            "En el dormitorio o en el solario.",
            "bedroom_or_sunroom",
        ),
        "E": Character("E", "Elyse", "Sentada en una silla.", "inside_chair"),
        "F": Character("F", "Franklin", "Sobre una alfombra.", "on_carpet"),
        "G": Character("G", "Gilbert", "En el jardin.", "in_garden"),
        "H": Character("H", "Holden", "Estaba solo.", "alone"),
        "V": Character("V", "Violet", "Victima del asesino.", "victim"),
    },
    rooms={
        "backyard": {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 6),
            (1, 0),
            (1, 1),
            (1, 6),
            (2, 0),
            (2, 1),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7),
            (4, 3),
            (5, 1),
            (5, 2),
            (5, 3),
            (6, 0),
            (6, 1),
        },
        "pond": {
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 2),
        },
        "garden": {
            (0, 7),
            (0, 8),
            (1, 7),
            (1, 8),
            (2, 7),
            (2, 8),
            (3, 8),
        },
        "shed": {
            (4, 0),
            (4, 1),
            (4, 2),
            (5, 0),
        },
        "sunroom": {
            (4, 4),
            (4, 5),
            (4, 6),
            (4, 7),
            (4, 8),
            (5, 4),
            (5, 5),
            (5, 6),
            (5, 7),
            (5, 8),
        },
        "bedroom": {
            (6, 2),
            (7, 0),
            (7, 1),
            (7, 2),
            (8, 0),
            (8, 1),
            (8, 2),
        },
        "living_room": {
            (6, 3),
            (6, 4),
            (6, 5),
            (7, 3),
            (7, 4),
            (7, 5),
            (8, 3),
            (8, 4),
            (8, 5),
        },
        "kitchen": {
            (6, 6),
            (6, 7),
            (6, 8),
            (7, 6),
            (7, 7),
            (7, 8),
            (8, 6),
            (8, 7),
            (8, 8),
        },
    },
    features={
        "chair": {
            (4, 6),
            (4, 8),
            (5, 4),
            (8, 0),
            (8, 4),
        },
        "carpet": {
            (5, 5),
            (5, 6),
            (7, 2),
            (8, 2),
            (7, 6),
            (7, 7),
        },
        "tree": {
            (0, 1),
            (2, 5),
        },
        "lily_pad": {
            (0, 4),
            (1, 2),
        },
        "flowers": {
            (0, 8),
            (2, 7),
            (3, 0),
            (3, 6),
            (6, 1),
        },
        "shelf": {
            (4, 0),
            (6, 3),
            (6, 5),
            (8, 7),
        },
        "tv": {
            (6, 4),
        },
        "table": {
            (3, 8),
            (4, 7),
            (7, 1),
            (7, 3),
            (8, 8),
        },
    },
    solution={
        "A": (7, 5),
        "B": (4, 1),
        "C": (0, 0),
        "D": (6, 2),
        "E": (8, 4),
        "F": (5, 6),
        "G": (2, 8),
        "H": (1, 3),
        "V": (3, 7),
    },
    victim="V",
    murderer="C",
    blocked_cells={
        (0, 1),
        (2, 5),
        (0, 4),
        (1, 2),
        (0, 8),
        (2, 7),
        (3, 0),
        (3, 6),
        (6, 1),
        (4, 0),
        (6, 3),
        (6, 5),
        (8, 7),
        (6, 4),
        (3, 8),
        (4, 7),
        (7, 1),
        (7, 3),
        (8, 8),
    },
)

PUZZLES = [LEVEL_1, LEVEL_2, LEVEL_3]
