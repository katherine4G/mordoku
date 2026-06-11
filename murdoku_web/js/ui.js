(function () {
  "use strict";

  class MurdokuUI {
    constructor() {
      this.screens = {
        menu: document.getElementById("menuScreen"),
        rules: document.getElementById("rulesScreen"),
        game: document.getElementById("gameScreen")
      };

      this.refs = {
        playButton: document.getElementById("playButton"),
        rulesButton: document.getElementById("rulesButton"),
        rulesBackButton: document.getElementById("rulesBackButton"),
        menuButton: document.getElementById("menuButton"),
        resetButton: document.getElementById("resetButton"),
        levelSelect: document.getElementById("levelSelect"),
        caseTitle: document.getElementById("caseTitle"),
        caseSummary: document.getElementById("caseSummary"),
        caseImage: document.getElementById("caseImage"),
        levelCounter: document.getElementById("levelCounter"),
        characterButtons: document.getElementById("characterButtons"),
        clueList: document.getElementById("clueList"),
        selectedText: document.getElementById("selectedText"),
        messageBox: document.getElementById("messageBox"),
        clearButton: document.getElementById("clearButton"),
        answerForm: document.getElementById("answerForm"),
        murdererInput: document.getElementById("murdererInput"),
        answerMessage: document.getElementById("answerMessage"),
        nextLevelButton: document.getElementById("nextLevelButton")
      };
    }

    showScreen(screenName) {
      Object.keys(this.screens).forEach((name) => {
        this.screens[name].classList.toggle("is-active", name === screenName);
      });
    }

    renderLevelOptions(levels, currentIndex) {
      this.refs.levelSelect.innerHTML = "";
      levels.forEach((level, index) => {
        const option = document.createElement("option");
        option.value = String(index);
        option.textContent = String(index + 1) + "/" + levels.length;
        option.selected = index === currentIndex;
        this.refs.levelSelect.appendChild(option);
      });
    }

    renderGame(options) {
      const state = options.state;
      const puzzle = state.puzzle;
      const selectedInitial = options.selectedInitial;
      const currentIndex = options.currentIndex;
      const totalLevels = options.totalLevels;

      this.refs.caseTitle.textContent = puzzle.title;
      this.refs.caseSummary.textContent = puzzle.summary;
      this.refs.caseImage.src = puzzle.image;
      this.refs.levelCounter.textContent = "Nivel " + (currentIndex + 1) + "/" + totalLevels;
      this.refs.selectedText.textContent = selectedInitial ? "Seleccionado: " + selectedInitial : "Selecciona una inicial";
      this.renderCharacters(state, selectedInitial, options.onCharacterSelect);
      this.renderClues(state);
      this.renderMessage(state.message, state.messageIsPositive);
      this.renderAnswerPanel(state, currentIndex, totalLevels);
    }

    renderCharacters(state, selectedInitial, onCharacterSelect) {
      const puzzle = state.puzzle;
      this.refs.characterButtons.innerHTML = "";
      puzzle.characterInitials().forEach((initial) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "character-button";
        button.textContent = initial;
        button.title = puzzle.characters[initial].name;
        if (selectedInitial === initial) {
          button.classList.add("is-selected");
        }
        if (state.assignment[initial]) {
          button.classList.add("is-placed");
        }
        button.addEventListener("click", () => onCharacterSelect(initial));
        this.refs.characterButtons.appendChild(button);
      });
    }

    renderClues(state) {
      const puzzle = state.puzzle;
      this.refs.clueList.innerHTML = "";
      puzzle.characterInitials().forEach((initial) => {
        const character = puzzle.characters[initial];
        const clue = document.createElement("div");
        clue.className = "clue-item";
        clue.innerHTML = "<strong>" + initial + " " + character.name + ":</strong> " + character.clue;
        this.refs.clueList.appendChild(clue);
      });
    }

    renderMessage(message, isPositive) {
      this.refs.messageBox.textContent = message;
      this.refs.messageBox.classList.toggle("is-bad", !isPositive);
    }

    renderAnswerPanel(state, currentIndex, totalLevels) {
      const visible = state.isComplete();
      this.refs.answerForm.classList.toggle("is-visible", visible);
      this.refs.murdererInput.value = state.murdererAnswer;
      this.refs.answerMessage.textContent = state.finalAnswerMessage;
      this.refs.answerMessage.classList.toggle("is-good", state.finalAnswerIsCorrect);

      const hasNext = currentIndex + 1 < totalLevels;
      this.refs.nextLevelButton.classList.toggle("is-hidden", !state.finalAnswerIsCorrect || !hasNext);
      this.refs.nextLevelButton.disabled = !state.finalAnswerIsCorrect || !hasNext;
    }
  }

  window.MurdokuUI = {
    MurdokuUI
  };
})();
