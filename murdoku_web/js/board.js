(function () {
  "use strict";

  class BoardRenderer {
    constructor(rootElement) {
      this.rootElement = rootElement;
    }

    render(options) {
      const state = options.state;
      const puzzle = state.puzzle;
      const selectedCell = options.selectedCell;
      const selectedInitial = options.selectedInitial;
      const blockedRows = state.blockedRows();
      const blockedCols = state.blockedCols();

      this.rootElement.innerHTML = "";
      const grid = document.createElement("div");
      grid.className = "board-grid";
      grid.style.setProperty("--board-size", String(puzzle.size));
      grid.style.minWidth = "min(100%, " + (38 + puzzle.size * 46) + "px)";

      const corner = document.createElement("div");
      corner.className = "corner-label";
      corner.setAttribute("aria-hidden", "true");
      grid.appendChild(corner);

      for (let col = 0; col < puzzle.size; col += 1) {
        const label = document.createElement("div");
        label.className = "axis-label";
        label.textContent = String(col + 1);
        grid.appendChild(label);
      }

      for (let row = 0; row < puzzle.size; row += 1) {
        const rowLabel = document.createElement("div");
        rowLabel.className = "axis-label";
        rowLabel.textContent = String(row + 1);
        grid.appendChild(rowLabel);

        for (let col = 0; col < puzzle.size; col += 1) {
          const coord = [row, col];
          const cell = document.createElement("button");
          const placedInitial = state.placedInitialAt(coord);
          cell.type = "button";
          cell.className = "cell-button";
          cell.dataset.row = String(row);
          cell.dataset.col = String(col);
          cell.setAttribute("aria-label", "Fila " + (row + 1) + ", columna " + (col + 1));

          if (blockedRows.has(row) || blockedCols.has(col)) {
            cell.classList.add("is-row-col-blocked");
          }
          if (puzzle.isBlockedCell(coord)) {
            cell.classList.add("is-map-blocked");
          }
          if (placedInitial) {
            cell.textContent = placedInitial;
            cell.classList.add("has-value");
          }
          if (selectedCell && selectedCell[0] === row && selectedCell[1] === col) {
            cell.classList.add("is-selected-cell");
          }
          if (selectedInitial) {
            cell.dataset.selectedInitial = selectedInitial;
          }

          cell.addEventListener("click", () => {
            options.onCellClick(coord);
          });
          grid.appendChild(cell);
        }
      }

      this.rootElement.appendChild(grid);
    }
  }

  window.MurdokuBoard = {
    BoardRenderer
  };
})();
