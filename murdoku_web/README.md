# Murdoku Web

Version web estatica del juego Murdoku. Esta carpeta no reemplaza ni elimina la version Python/Pygame.

## Como abrir el juego

Abre `index.html` directamente en el navegador. No requiere backend, servidor local ni frameworks.

## Archivos principales

- `index.html`: estructura de pantallas para menu, reglas y juego.
- `css/styles.css`: diseno responsive, tablero adaptable y estilo visual.
- `js/levels.js`: niveles migrados desde `data/puzzles.py`.
- `js/gameState.js`: reglas, estado del tablero, validacion y solucion CSP en JavaScript.
- `js/board.js`: render del tablero y celdas.
- `js/ui.js`: actualizacion de textos, botones, pistas y paneles.
- `js/main.js`: flujo principal, eventos y cambio de niveles.
- `assets/images/`: copia de las imagenes originales usadas por los casos.

## Partes migradas

- Menu principal.
- Pantalla de reglas.
- Carga de niveles.
- Tres casos disponibles del proyecto Python.
- Referencia visual del caso.
- Pistas por personaje.
- Tablero 6x6 y 9x9 responsive.
- Seleccion, ingreso, cambio y borrado de iniciales.
- Bloqueo visual de filas y columnas usadas.
- Validacion de movimientos con reglas del caso.
- Comprobacion del asesino al completar el tablero.
- Reinicio y avance al siguiente caso.

## Pendiente o incompleto

- No hay animaciones avanzadas.
- No hay guardado persistente de progreso.
- No hay editor de niveles.
- La version web usa la misma solucion fija de cada caso para aceptar ubicaciones.
