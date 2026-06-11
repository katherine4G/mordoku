(function () {
  "use strict";

  const levels = window.MURDOKU_LEVELS;
  const ui = new window.MurdokuUI.MurdokuUI();
  const board = new window.MurdokuBoard.BoardRenderer(document.getElementById("boardRoot"));

  let currentIndex = 0;
  let state = new window.MurdokuGameState.BoardState(levels[currentIndex]);
  let selectedInitial = null;
  let selectedCell = null;

  function startLevel(index) {
    currentIndex = index;
    state = new window.MurdokuGameState.BoardState(levels[currentIndex]);
    selectedInitial = null;
    selectedCell = null;
    ui.renderLevelOptions(levels, currentIndex);
    ui.showScreen("game");
    render();
  }

  function render() {
    ui.renderGame({
      state,
      selectedInitial,
      currentIndex,
      totalLevels: levels.length,
      onCharacterSelect: handleCharacterSelect
    });
    board.render({
      state,
      selectedInitial,
      selectedCell,
      onCellClick: handleCellClick
    });
  }

  function handleCharacterSelect(initial) {
    selectedInitial = initial;
    state.applyMessage(true, state.puzzle.characters[initial].name + " seleccionado.");
    render();
  }

  function handleCellClick(coord) {
    selectedCell = coord.slice();
    if (selectedInitial) {
      const result = state.place(selectedInitial, coord);
      if (result.accepted) {
        selectedInitial = null;
      }
      render();
      return;
    }

    const placedInitial = state.placedInitialAt(coord);
    if (placedInitial) {
      selectedInitial = placedInitial;
      state.applyMessage(true, placedInitial + " seleccionado. Puedes moverlo o borrar la celda.");
    } else {
      state.applyMessage(false, "Primero selecciona una inicial.");
    }
    render();
  }

  function clearSelectedCell() {
    if (!selectedCell) {
      state.applyMessage(false, "Selecciona una celda para borrar.");
      render();
      return;
    }
    const removed = state.placedInitialAt(selectedCell);
    const result = state.removeAt(selectedCell);
    if (result.accepted && selectedInitial === removed) {
      selectedInitial = null;
    }
    render();
  }

  function submitAnswer(event) {
    event.preventDefault();
    state.validateMurderer(ui.refs.murdererInput.value);
    render();
    ui.refs.murdererInput.focus();
  }

  function handleKeydown(event) {
    if (!ui.screens.game.classList.contains("is-active")) {
      return;
    }
    const target = event.target;
    const isTextInput = target && (target.tagName === "INPUT" || target.tagName === "SELECT");
    if (isTextInput) {
      return;
    }

    if (event.key === "Escape") {
      ui.showScreen("menu");
      return;
    }
    if ((event.key === "Backspace" || event.key === "Delete") && selectedCell) {
      event.preventDefault();
      clearSelectedCell();
      return;
    }

    const typed = event.key.toUpperCase();
    if (state.puzzle.characters[typed]) {
      selectedInitial = typed;
      state.applyMessage(true, state.puzzle.characters[typed].name + " seleccionado.");
      render();
    }
  }

  ui.refs.playButton.addEventListener("click", () => startLevel(0));
  ui.refs.rulesButton.addEventListener("click", () => ui.showScreen("rules"));
  ui.refs.rulesBackButton.addEventListener("click", () => ui.showScreen("menu"));
  ui.refs.menuButton.addEventListener("click", () => ui.showScreen("menu"));
  ui.refs.resetButton.addEventListener("click", () => startLevel(currentIndex));
  ui.refs.clearButton.addEventListener("click", clearSelectedCell);
  ui.refs.answerForm.addEventListener("submit", submitAnswer);
  ui.refs.levelSelect.addEventListener("change", (event) => startLevel(Number(event.target.value)));
  ui.refs.nextLevelButton.addEventListener("click", () => {
    if (currentIndex + 1 < levels.length) {
      startLevel(currentIndex + 1);
    }
  });
  document.addEventListener("keydown", handleKeydown);

  ui.renderLevelOptions(levels, currentIndex);
  ui.showScreen("menu");
})();
