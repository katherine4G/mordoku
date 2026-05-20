# data/puzzles.py
from __future__ import annotations

from dataclasses import dataclass
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

    def all_cells(self) -> set[Coord]:
        return {(row, col) for row in range(self.size) for col in range(self.size)}

    def room_at(self, coord: Coord) -> str | None:
        for room, cells in self.rooms.items():
            if coord in cells:
                return room
        return None

    def feature_at(self, coord: Coord, feature: str) -> bool:
        return coord in self.features.get(feature, set())


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

PUZZLES = [LEVEL_1, LEVEL_2]
