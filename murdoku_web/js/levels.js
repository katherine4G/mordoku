(function () {
  "use strict";

  window.MURDOKU_LEVELS = [
    {
      id: "case-1",
      title: "Caso 1: Taller Murdoku",
      summary: "Un taller cerrado, manchas de aceite y una victima que quedo con su asesino.",
      size: 6,
      image: "assets/images/mordoku_nivel1.png",
      victim: "V",
      murderer: "C",
      characters: {
        A: { initial: "A", name: "Anthony", clue: "Dentro de un carro.", rule: "inside_car" },
        B: { initial: "B", name: "Brock", clue: "Sobre aceite.", rule: "on_oil" },
        C: { initial: "C", name: "Crystal", clue: "Sentada en una silla.", rule: "inside_chair" },
        D: { initial: "D", name: "Diane", clue: "En la sala de espera.", rule: "alone_waiting_room" },
        E: { initial: "E", name: "Emilio", clue: "Junto a un estante.", rule: "beside_shelf" },
        V: { initial: "V", name: "Vaughn", clue: "Victima del asesino.", rule: "victim" }
      },
      rooms: {
        reception: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [3, 0]],
        storage: [[0, 4], [0, 5], [1, 5]],
        waiting_room: [[0, 3], [1, 4], [1, 3], [2, 3], [2, 4], [2, 5]],
        garage: [[3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5]]
      },
      features: {
        car: [[5, 3], [5, 4], [4, 1], [4, 2]],
        oil: [[5, 1], [4, 3]],
        chair: [[0, 1], [2, 3], [2, 4]],
        shelf: [[0, 5], [2, 2], [3, 3], [3, 4]]
      },
      solution: {
        A: [5, 4],
        B: [4, 3],
        C: [0, 1],
        D: [2, 5],
        E: [3, 2],
        V: [1, 0]
      },
      blockedCells: []
    },
    {
      id: "case-2",
      title: "Caso 2: Muerte en Netflix",
      summary: "La escena se divide entre dormitorio, cocina, bano y sala de estar.",
      size: 6,
      image: "assets/images/mordoku_nivel2.png",
      victim: "V",
      murderer: "B",
      characters: {
        A: { initial: "A", name: "Austin", clue: "Junto a un estante.", rule: "beside_shelf" },
        B: { initial: "B", name: "Barbara", clue: "En la cama.", rule: "on_bed" },
        C: { initial: "C", name: "Charlotte", clue: "En una silla.", rule: "only_chair" },
        D: { initial: "D", name: "Dean", clue: "En la cocina.", rule: "in_kitchen" },
        E: { initial: "E", name: "Enid", clue: "Junto a la TV.", rule: "beside_tv" },
        V: { initial: "V", name: "Vaughn", clue: "Victima del asesino.", rule: "victim" }
      },
      rooms: {
        bedroom: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]],
        bathroom: [[0, 4], [0, 5], [1, 4], [1, 5], [2, 5]],
        kitchen: [[3, 0], [3, 1], [4, 0], [4, 1], [5, 0], [5, 1]],
        living_room: [[0, 3], [1, 3], [2, 3], [2, 4], [3, 2], [3, 3], [3, 4], [3, 5], [4, 2], [4, 3], [4, 4], [4, 5], [5, 2], [5, 3], [5, 4], [5, 5]]
      },
      features: {
        bed: [[0, 0], [0, 1]],
        chair: [[0, 5], [1, 3], [2, 4], [3, 2], [3, 4]],
        shelf: [[2, 0], [4, 0], [5, 2]],
        tv: [[4, 5]]
      },
      solution: {
        A: [5, 3],
        B: [0, 0],
        C: [2, 4],
        D: [4, 1],
        E: [3, 5],
        V: [1, 2]
      },
      blockedCells: []
    },
    {
      id: "case-3",
      title: "Caso 3: The Backyard Garden",
      summary: "Un jardin amplio con estanque, cobertizo, solario y varias habitaciones interiores.",
      size: 9,
      image: "assets/images/mordoku_nivel3.png",
      victim: "V",
      murderer: "C",
      characters: {
        A: { initial: "A", name: "Aaron", clue: "Con Elyse en la sala de estar.", rule: "with_elyse_living_room" },
        B: { initial: "B", name: "Bruce", clue: "En el cobertizo.", rule: "in_shed" },
        C: { initial: "C", name: "Carissa", clue: "Junto a un arbol.", rule: "beside_tree" },
        D: { initial: "D", name: "Denise", clue: "En el dormitorio o en el solario.", rule: "bedroom_or_sunroom" },
        E: { initial: "E", name: "Elyse", clue: "Sentada en una silla.", rule: "inside_chair" },
        F: { initial: "F", name: "Franklin", clue: "Sobre una alfombra.", rule: "on_carpet" },
        G: { initial: "G", name: "Gilbert", clue: "En el jardin.", rule: "in_garden" },
        H: { initial: "H", name: "Holden", clue: "Estaba solo.", rule: "alone" },
        V: { initial: "V", name: "Violet", clue: "Victima del asesino.", rule: "victim" }
      },
      rooms: {
        backyard: [[0, 0], [0, 1], [0, 2], [0, 6], [1, 0], [1, 1], [1, 6], [2, 0], [2, 1], [2, 3], [2, 4], [2, 5], [2, 6], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [4, 3], [5, 1], [5, 2], [5, 3], [6, 0], [6, 1]],
        pond: [[0, 3], [0, 4], [0, 5], [1, 2], [1, 3], [1, 4], [1, 5], [2, 2]],
        garden: [[0, 7], [0, 8], [1, 7], [1, 8], [2, 7], [2, 8], [3, 8]],
        shed: [[4, 0], [4, 1], [4, 2], [5, 0]],
        sunroom: [[4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8]],
        bedroom: [[6, 2], [7, 0], [7, 1], [7, 2], [8, 0], [8, 1], [8, 2]],
        living_room: [[6, 3], [6, 4], [6, 5], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5]],
        kitchen: [[6, 6], [6, 7], [6, 8], [7, 6], [7, 7], [7, 8], [8, 6], [8, 7], [8, 8]]
      },
      features: {
        chair: [[4, 6], [4, 8], [5, 4], [8, 0], [8, 4]],
        carpet: [[5, 5], [5, 6], [7, 2], [8, 2], [7, 6], [7, 7]],
        tree: [[0, 1], [2, 5]],
        lily_pad: [[0, 4], [1, 2]],
        flowers: [[0, 8], [2, 7], [3, 0], [3, 6], [6, 1]],
        shelf: [[4, 0], [6, 3], [6, 5], [8, 7]],
        tv: [[6, 4]],
        table: [[3, 8], [4, 7], [7, 1], [7, 3], [8, 8]]
      },
      solution: {
        A: [7, 5],
        B: [4, 1],
        C: [0, 0],
        D: [6, 2],
        E: [8, 4],
        F: [5, 6],
        G: [2, 8],
        H: [1, 3],
        V: [3, 7]
      },
      blockedCells: [[0, 1], [2, 5], [0, 4], [1, 2], [0, 8], [2, 7], [3, 0], [3, 6], [6, 1], [4, 0], [6, 3], [6, 5], [8, 7], [6, 4], [3, 8], [4, 7], [7, 1], [7, 3], [8, 8]]
    }
  ];
})();
