# Murdoku

Videojuego de puzzle logico detectivesco inspirado en Sudoku + misterio.

## Requisitos

- Python 3
- Pygame

Instalacion:

```bash
pip install -r requirements.txt
```

Ejecucion:

```bash
python main.py
```

## Fase actual

Incluye:

- Menu principal
- Pantalla de reglas
- Nivel 1 funcional
- Transicion al nivel 2 funcional
- Imagen del caso como referencia visual
- Matriz logica 6x6 separada
- Validacion con CSP, backtracking, forward checking, propagacion y MRV
- Hints rule-based, sin IA generativa, OCR ni APIs externas

## Controles

Selecciona una inicial con el mouse o con el teclado (`A`, `B`, `C`, `D`, `E`, `V`) y haz clic en una casilla de la matriz. Al completar todas las letras, escribe el nombre del asesino y pulsa `Enter` o `Validar`.
