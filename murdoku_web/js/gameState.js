(function () {
  "use strict";

  const RULE_HINTS_BY_RULE = {
    with_elyse_living_room: "{name} debe estar con Elyse en la sala de estar.",
    inside_car: "{name} necesita una casilla con carro.",
    on_oil: "{name} debe estar sobre una mancha de aceite.",
    inside_chair: "{name} necesita una silla.",
    only_chair: "{name} debe estar en una silla, y nadie mas puede usar silla.",
    on_bed: "{name} debe estar sobre una cama.",
    in_kitchen: "{name} debe estar en la cocina.",
    in_shed: "{name} debe estar en el cobertizo.",
    beside_tree: "{name} debe estar junto a un arbol.",
    bedroom_or_sunroom: "{name} debe estar en el dormitorio o en el solario.",
    on_carpet: "{name} debe estar sobre una alfombra.",
    in_garden: "{name} debe estar en el jardin.",
    alone: "{name} debe estar solo en su area.",
    alone_waiting_room: "{name} debe quedar sola en la sala de espera.",
    beside_shelf: "{name} debe estar junto a un estante. Recuerda que no incluye diagonales.",
    beside_tv: "{name} debe estar junto al televisor. Recuerda que no incluye diagonales.",
    victim: "{name} solo puede quedar con el asesino."
  };

  function coordKey(coord) {
    return coord[0] + "," + coord[1];
  }

  function sameCoord(a, b) {
    return Boolean(a && b && a[0] === b[0] && a[1] === b[1]);
  }

  function cloneAssignment(assignment) {
    const cloned = {};
    Object.keys(assignment).forEach((initial) => {
      cloned[initial] = assignment[initial].slice();
    });
    return cloned;
  }

  function cloneDomains(domains) {
    const cloned = {};
    Object.keys(domains).forEach((initial) => {
      cloned[initial] = domains[initial].map((coord) => coord.slice());
    });
    return cloned;
  }

  function sortedCoords(coords) {
    return coords.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  }

  function domainsEqual(a, b) {
    if (a.length !== b.length) {
      return false;
    }
    const aKeys = new Set(a.map(coordKey));
    return b.every((coord) => aKeys.has(coordKey(coord)));
  }

  class PuzzleAdapter {
    constructor(rawPuzzle) {
      this.raw = rawPuzzle;
      this.title = rawPuzzle.title;
      this.summary = rawPuzzle.summary;
      this.size = rawPuzzle.size;
      this.image = rawPuzzle.image;
      this.characters = rawPuzzle.characters;
      this.victim = rawPuzzle.victim;
      this.murderer = rawPuzzle.murderer;
      this.solution = rawPuzzle.solution;
      this.blockedCellKeys = new Set((rawPuzzle.blockedCells || []).map(coordKey));
      this.roomCells = rawPuzzle.rooms;
      this.featureCells = rawPuzzle.features;
    }

    characterInitials() {
      return Object.keys(this.characters);
    }

    allCells() {
      const cells = [];
      for (let row = 0; row < this.size; row += 1) {
        for (let col = 0; col < this.size; col += 1) {
          cells.push([row, col]);
        }
      }
      return cells;
    }

    occupiableCells() {
      return this.allCells().filter((coord) => !this.isBlockedCell(coord));
    }

    isBlockedCell(coord) {
      return this.blockedCellKeys.has(coordKey(coord));
    }

    roomAt(coord) {
      const targetKey = coordKey(coord);
      const roomNames = Object.keys(this.roomCells);
      for (let i = 0; i < roomNames.length; i += 1) {
        const roomName = roomNames[i];
        if (this.roomCells[roomName].some((roomCoord) => coordKey(roomCoord) === targetKey)) {
          return roomName;
        }
      }
      return null;
    }

    featureAt(coord, featureName) {
      const cells = this.featureCells[featureName] || [];
      const targetKey = coordKey(coord);
      return cells.some((featureCoord) => coordKey(featureCoord) === targetKey);
    }
  }

  class ConstraintEngine {
    constructor(puzzle) {
      this.puzzle = puzzle;
    }

    personConstraintOk(initial, targetCoord, assignment) {
      if (this.puzzle.isBlockedCell(targetCoord)) {
        return false;
      }

      const rule = this.puzzle.characters[initial].rule;
      if (rule === "with_elyse_living_room") {
        return this.puzzle.roomAt(targetCoord) === "living_room";
      }
      if (rule === "inside_car") {
        return this.puzzle.featureAt(targetCoord, "car");
      }
      if (rule === "on_oil") {
        return this.puzzle.featureAt(targetCoord, "oil");
      }
      if (rule === "inside_chair" || rule === "only_chair") {
        return this.puzzle.featureAt(targetCoord, "chair");
      }
      if (rule === "on_bed") {
        return this.puzzle.featureAt(targetCoord, "bed");
      }
      if (rule === "in_kitchen") {
        return this.puzzle.roomAt(targetCoord) === "kitchen";
      }
      if (rule === "in_shed") {
        return this.puzzle.roomAt(targetCoord) === "shed";
      }
      if (rule === "beside_tree") {
        return this.besideFeatureInSameRoom(targetCoord, "tree");
      }
      if (rule === "bedroom_or_sunroom") {
        return ["bedroom", "sunroom"].includes(this.puzzle.roomAt(targetCoord));
      }
      if (rule === "on_carpet") {
        return this.puzzle.featureAt(targetCoord, "carpet");
      }
      if (rule === "in_garden") {
        return this.puzzle.roomAt(targetCoord) === "garden";
      }
      if (rule === "alone") {
        return this.characterIsAloneInRoom(initial, targetCoord, assignment);
      }
      if (rule === "alone_waiting_room") {
        return this.dianeIsAlone(targetCoord, assignment);
      }
      if (rule === "beside_shelf") {
        return this.besideFeatureInSameRoom(targetCoord, "shelf");
      }
      if (rule === "beside_tv") {
        return this.besideFeatureInSameRoom(targetCoord, "tv");
      }
      return true;
    }

    assignmentConsistent(assignment) {
      if (!this.rowsAndColumnsAreUnique(assignment)) {
        return false;
      }
      if (!this.exclusiveFeatureRulesOk(assignment)) {
        return false;
      }
      if (!this.withElyseLivingRoomRuleOk(assignment)) {
        return false;
      }

      const initials = Object.keys(assignment);
      for (let i = 0; i < initials.length; i += 1) {
        const initial = initials[i];
        if (!this.personConstraintOk(initial, assignment[initial], assignment)) {
          return false;
        }
      }
      return this.victimMurdererRuleOk(assignment);
    }

    rowsAndColumnsAreUnique(assignment) {
      const rows = new Set();
      const cols = new Set();
      const coords = new Set();
      const values = Object.values(assignment);

      for (let i = 0; i < values.length; i += 1) {
        const coord = values[i];
        const key = coordKey(coord);
        if (rows.has(coord[0]) || cols.has(coord[1]) || coords.has(key)) {
          return false;
        }
        rows.add(coord[0]);
        cols.add(coord[1]);
        coords.add(key);
      }
      return true;
    }

    dianeIsAlone(targetCoord, assignment) {
      if (this.puzzle.roomAt(targetCoord) !== "waiting_room") {
        return false;
      }
      return Object.keys(assignment).every((otherInitial) => {
        return otherInitial === "D" || this.puzzle.roomAt(assignment[otherInitial]) !== "waiting_room";
      });
    }

    characterIsAloneInRoom(initial, targetCoord, assignment) {
      const targetRoom = this.puzzle.roomAt(targetCoord);
      if (!targetRoom) {
        return false;
      }
      return Object.keys(assignment).every((otherInitial) => {
        return otherInitial === initial || this.puzzle.roomAt(assignment[otherInitial]) !== targetRoom;
      });
    }

    besideFeatureInSameRoom(targetCoord, featureName) {
      const currentRoom = this.puzzle.roomAt(targetCoord);
      if (!currentRoom) {
        return false;
      }

      const row = targetCoord[0];
      const col = targetCoord[1];
      const neighbors = [
        [row - 1, col],
        [row + 1, col],
        [row, col - 1],
        [row, col + 1]
      ];
      return neighbors.some((coord) => {
        return this.puzzle.roomAt(coord) === currentRoom && this.puzzle.featureAt(coord, featureName);
      });
    }

    exclusiveFeatureRulesOk(assignment) {
      const chairOnlyInitials = this.puzzle.characterInitials().filter((initial) => {
        return this.puzzle.characters[initial].rule === "only_chair";
      });
      if (chairOnlyInitials.length === 0) {
        return true;
      }
      return Object.keys(assignment).every((initial) => {
        return !this.puzzle.featureAt(assignment[initial], "chair") || chairOnlyInitials.includes(initial);
      });
    }

    withElyseLivingRoomRuleOk(assignment) {
      const linkedInitials = this.puzzle.characterInitials().filter((initial) => {
        return this.puzzle.characters[initial].rule === "with_elyse_living_room";
      });
      if (linkedInitials.length === 0) {
        return true;
      }

      const required = new Set(linkedInitials);
      if (this.puzzle.characters.E) {
        required.add("E");
      }

      return Array.from(required).every((initial) => {
        return !assignment[initial] || this.puzzle.roomAt(assignment[initial]) === "living_room";
      });
    }

    victimMurdererRuleOk(assignment) {
      const victimInitial = this.puzzle.victim;
      const murdererInitial = this.puzzle.murderer;
      if (!assignment[victimInitial]) {
        return true;
      }

      const victimRoom = this.puzzle.roomAt(assignment[victimInitial]);
      if (!victimRoom) {
        return false;
      }

      const initials = Object.keys(assignment);
      for (let i = 0; i < initials.length; i += 1) {
        const initial = initials[i];
        if (initial === victimInitial || initial === murdererInitial) {
          continue;
        }
        if (this.puzzle.roomAt(assignment[initial]) === victimRoom) {
          return false;
        }
      }

      if (assignment[murdererInitial]) {
        return this.puzzle.roomAt(assignment[murdererInitial]) === victimRoom;
      }
      return true;
    }
  }

  class CSPSolver {
    constructor(puzzle) {
      this.puzzle = puzzle;
      this.engine = new ConstraintEngine(puzzle);
      this.initialDomains = this.buildInitialDomains();
    }

    buildInitialDomains() {
      const domains = {};
      this.puzzle.characterInitials().forEach((initial) => {
        domains[initial] = this.puzzle.occupiableCells().filter((coord) => {
          return this.engine.personConstraintOk(initial, coord, {});
        });
      });
      return domains;
    }

    domainsFor(assignment) {
      return this.propagateConstraints(cloneAssignment(assignment), cloneDomains(this.initialDomains));
    }

    hasSolution(assignment) {
      const propagated = this.domainsFor(assignment);
      if (!propagated) {
        return false;
      }
      return Boolean(this.backtrack(cloneAssignment(assignment), propagated));
    }

    propagateConstraints(assignment, currentDomains) {
      const propagated = cloneDomains(currentDomains);
      let changed = true;

      while (changed) {
        changed = false;
        if (!this.engine.assignmentConsistent(assignment)) {
          return null;
        }

        const assignedRows = new Set(Object.values(assignment).map((coord) => coord[0]));
        const assignedCols = new Set(Object.values(assignment).map((coord) => coord[1]));
        const assignedKeys = new Set(Object.values(assignment).map(coordKey));

        const initials = this.puzzle.characterInitials();
        for (let i = 0; i < initials.length; i += 1) {
          const initial = initials[i];
          if (assignment[initial]) {
            propagated[initial] = [assignment[initial].slice()];
            continue;
          }

          const validCoords = [];
          for (let j = 0; j < propagated[initial].length; j += 1) {
            const candidate = propagated[initial][j];
            if (assignedKeys.has(coordKey(candidate)) || assignedRows.has(candidate[0]) || assignedCols.has(candidate[1])) {
              continue;
            }
            const tentative = cloneAssignment(assignment);
            tentative[initial] = candidate.slice();
            if (this.engine.assignmentConsistent(tentative)) {
              validCoords.push(candidate.slice());
            }
          }

          if (!domainsEqual(validCoords, propagated[initial])) {
            propagated[initial] = validCoords;
            changed = true;
          }
          if (validCoords.length === 0) {
            return null;
          }
        }

        const forced = {};
        initials.forEach((initial) => {
          if (!assignment[initial] && propagated[initial].length === 1) {
            forced[initial] = propagated[initial][0].slice();
          }
        });

        Object.keys(forced).forEach((initial) => {
          const tentative = cloneAssignment(assignment);
          tentative[initial] = forced[initial].slice();
          if (!this.engine.assignmentConsistent(tentative)) {
            changed = false;
            return;
          }
          assignment[initial] = forced[initial].slice();
          changed = true;
        });

        if (!this.engine.assignmentConsistent(assignment)) {
          return null;
        }
      }

      return propagated;
    }

    backtrack(assignment, domains) {
      if (Object.keys(assignment).length === this.puzzle.characterInitials().length) {
        return this.engine.assignmentConsistent(assignment) ? cloneAssignment(assignment) : null;
      }

      const nextInitial = this.selectUnassignedVariable(assignment, domains);
      if (!nextInitial) {
        return null;
      }

      const candidates = sortedCoords(domains[nextInitial]);
      for (let i = 0; i < candidates.length; i += 1) {
        const candidate = candidates[i];
        const tentative = cloneAssignment(assignment);
        tentative[nextInitial] = candidate.slice();
        if (!this.engine.assignmentConsistent(tentative)) {
          continue;
        }
        const propagated = this.propagateConstraints(tentative, domains);
        if (!propagated) {
          continue;
        }
        const solved = this.backtrack(tentative, propagated);
        if (solved) {
          return solved;
        }
      }
      return null;
    }

    selectUnassignedVariable(assignment, domains) {
      const unassigned = this.puzzle.characterInitials().filter((initial) => !assignment[initial]);
      if (unassigned.length === 0) {
        return null;
      }
      return unassigned.reduce((best, initial) => {
        return domains[initial].length < domains[best].length ? initial : best;
      }, unassigned[0]);
    }
  }

  class BoardState {
    constructor(rawPuzzle) {
      this.puzzle = new PuzzleAdapter(rawPuzzle);
      this.assignment = {};
      this.solver = new CSPSolver(this.puzzle);
      this.domains = this.solver.domainsFor({}) || {};
      this.message = "Selecciona una inicial y colocala en la matriz.";
      this.messageIsPositive = true;
      this.finalAnswerMessage = "";
      this.finalAnswerIsCorrect = false;
      this.murdererAnswer = "";
    }

    reset() {
      this.assignment = {};
      this.domains = this.solver.domainsFor({}) || {};
      this.message = "Selecciona una inicial y colocala en la matriz.";
      this.messageIsPositive = true;
      this.finalAnswerMessage = "";
      this.finalAnswerIsCorrect = false;
      this.murdererAnswer = "";
    }

    blockedRows() {
      return new Set(Object.values(this.assignment).map((coord) => coord[0]));
    }

    blockedCols() {
      return new Set(Object.values(this.assignment).map((coord) => coord[1]));
    }

    canUseInitial(initial) {
      return Boolean(this.puzzle.characters[initial]);
    }

    placedInitialAt(coord) {
      const initials = Object.keys(this.assignment);
      for (let i = 0; i < initials.length; i += 1) {
        const initial = initials[i];
        if (sameCoord(this.assignment[initial], coord)) {
          return initial;
        }
      }
      return null;
    }

    place(initial, targetCoord) {
      if (!this.canUseInitial(initial)) {
        return this.applyMessage(false, "Esa inicial no existe en este caso.");
      }

      if (this.puzzle.isBlockedCell(targetCoord)) {
        return this.applyMessage(false, "Esa casilla no se puede ocupar.");
      }

      const existingInitial = this.placedInitialAt(targetCoord);
      if (existingInitial && existingInitial !== initial) {
        const name = this.puzzle.characters[existingInitial].name;
        return this.applyMessage(false, "Esa casilla ya esta ocupada por " + name + ".");
      }

      const tentativeBase = cloneAssignment(this.assignment);
      delete tentativeBase[initial];

      const solutionCoord = this.puzzle.solution[initial];
      if (!sameCoord(solutionCoord, targetCoord)) {
        return this.applyMessage(false, hintForMove(this.puzzle, this.solver, tentativeBase, initial, targetCoord));
      }

      const tentative = cloneAssignment(tentativeBase);
      tentative[initial] = targetCoord.slice();
      const propagated = this.solver.domainsFor(tentative);
      if (!propagated || !this.solver.hasSolution(tentative)) {
        return this.applyMessage(false, hintForMove(this.puzzle, this.solver, tentativeBase, initial, targetCoord));
      }

      this.assignment = tentative;
      this.domains = propagated;
      this.finalAnswerMessage = "";
      this.finalAnswerIsCorrect = false;

      const characterName = this.puzzle.characters[initial].name;
      if (this.isComplete()) {
        return this.applyMessage(true, "Todos ubicados. Escribe quien es el asesino.");
      }
      return this.applyMessage(true, characterName + " encaja con las pistas.");
    }

    removeAt(coord) {
      const initial = this.placedInitialAt(coord);
      if (!initial) {
        return this.applyMessage(false, "No hay una inicial para borrar en esa celda.");
      }
      delete this.assignment[initial];
      this.domains = this.solver.domainsFor(this.assignment) || {};
      this.finalAnswerMessage = "";
      this.finalAnswerIsCorrect = false;
      this.murdererAnswer = "";
      const name = this.puzzle.characters[initial].name;
      return this.applyMessage(true, name + " fue retirado del tablero.");
    }

    isComplete() {
      return Object.keys(this.assignment).length === this.puzzle.characterInitials().length;
    }

    validateMurderer(candidateAnswer) {
      const murdererCharacter = this.puzzle.characters[this.puzzle.murderer];
      const victimCharacter = this.puzzle.characters[this.puzzle.victim];
      const expected = murdererCharacter.name.toLowerCase();
      const received = candidateAnswer.trim().toLowerCase();
      this.murdererAnswer = candidateAnswer;

      if (received === expected) {
        this.finalAnswerIsCorrect = true;
        this.finalAnswerMessage = "Correcto: " + murdererCharacter.name + " quedo a solas con " + victimCharacter.name + ".";
        return { accepted: true, message: this.finalAnswerMessage };
      }

      this.finalAnswerIsCorrect = false;
      this.finalAnswerMessage = finalAnswerHint(victimCharacter.name, candidateAnswer);
      return { accepted: false, message: this.finalAnswerMessage };
    }

    applyMessage(accepted, message) {
      this.message = message;
      this.messageIsPositive = accepted;
      return { accepted, message };
    }
  }

  function hintForMove(puzzle, solver, assignment, initial, targetCoord) {
    const engine = new ConstraintEngine(puzzle);

    if (puzzle.isBlockedCell(targetCoord)) {
      return "Esa casilla no se puede ocupar.";
    }

    const assignedInitials = Object.keys(assignment);
    for (let i = 0; i < assignedInitials.length; i += 1) {
      const otherInitial = assignedInitials[i];
      const otherCoord = assignment[otherInitial];
      if (sameCoord(otherCoord, targetCoord)) {
        const occupiedName = puzzle.characters[otherInitial].name;
        return "Esa casilla ya esta ocupada por " + occupiedName + ".";
      }
      if (otherCoord[0] === targetCoord[0]) {
        return "No puede repetirse fila: esa fila ya esta bloqueada.";
      }
      if (otherCoord[1] === targetCoord[1]) {
        return "No puede repetirse columna: esa columna ya esta bloqueada.";
      }
    }

    const tentative = cloneAssignment(assignment);
    tentative[initial] = targetCoord.slice();

    if (!engine.personConstraintOk(initial, targetCoord, tentative)) {
      return ruleHint(puzzle, initial);
    }

    const propagated = solver.domainsFor(tentative);
    if (!propagated) {
      const stranded = firstStrandedCharacter(puzzle, solver, tentative);
      if (stranded) {
        return "Ese movimiento deja sin opciones validas a " + stranded + ".";
      }
      return "Ese movimiento contradice las pistas al hacer forward checking.";
    }

    const forcedName = forcedCharacterName(puzzle, assignment, solver);
    if (forcedName) {
      return "Solo queda una casilla valida para " + forcedName + ".";
    }

    return "Al cruzar todas las pistas, esa casilla queda descartada.";
  }

  function ruleHint(puzzle, initial) {
    const character = puzzle.characters[initial];
    const template = RULE_HINTS_BY_RULE[character.rule] || "{name} no cumple su pista en esa casilla.";
    return template.replace("{name}", character.name);
  }

  function firstStrandedCharacter(puzzle, solver, assignment) {
    const propagated = solver.domainsFor(assignment);
    if (!propagated) {
      return null;
    }
    const initials = puzzle.characterInitials();
    for (let i = 0; i < initials.length; i += 1) {
      const initial = initials[i];
      if (!assignment[initial] && (!propagated[initial] || propagated[initial].length === 0)) {
        return puzzle.characters[initial].name;
      }
    }
    return null;
  }

  function forcedCharacterName(puzzle, assignment, solver) {
    const propagated = solver.domainsFor(assignment);
    if (!propagated) {
      return null;
    }
    const initials = Object.keys(propagated);
    for (let i = 0; i < initials.length; i += 1) {
      const initial = initials[i];
      if (!assignment[initial] && propagated[initial].length === 1) {
        return puzzle.characters[initial].name;
      }
    }
    return null;
  }

  function finalAnswerHint(victimName, receivedAnswer) {
    if (!receivedAnswer.trim()) {
      return "Escribe el nombre del sospechoso que quedo a solas con " + victimName + ".";
    }
    return receivedAnswer.trim() + " no quedo como el unico sospechoso con " + victimName + ".";
  }

  window.MurdokuGameState = {
    BoardState,
    coordKey
  };
})();
