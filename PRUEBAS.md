# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido (demo.txt) y nivel inexistente (inexistente.txt);

- nivel con filas de distinta longitud(distinta_longitud.txt), filas vacias en principio fin y medio(filas_vacias);

- paleta en ambos límites de la pantalla (linea 86 y 87, funcion max y min cuando llega a la izquierda y derecha respectivamente sin permitir el desborde de la paleta)

- rebote contra pared, paleta y cada tipo de bloque (en actualizar bola se establecen condiciones cambiando la direccion de la bola en relacion con el impacto);

- pérdida de una vida y reinicio de la bola (Condicion establecida en actualizar bola si la posicion y de la pelota supera el alto de la pantalla es decir esta por debajo del limite);

- victoria al eliminar el último bloque y derrota al agotar vidas (si la funcion self.blocks es falso es decir no quedan bloques has ganado, y si cuando cae la bola por abajo y resta vida no te quedan, has perdido);

- salida limpia con Escape y al cerrar la ventana (Controlando con un while cuando se esta ejecutando si se pulsa la tecla esc o se cierra la ventana, deja de correr).

Una mejora opcional no debe romper ninguno de estos casos.

Tras buscar información hemos identificado que para ejecutar el codigo en windows debemos añadir la variable de entorno $env:SDL_VIDEODRIVER="windows"; python arkanoid_game.py niveles/*.txt
    - Siendo * el nombre del nivel (hemos testeado con inexistente.txt, que no existe, demo.txt que es que venia, y distinta_longitud.txt y filas_vacias.txt para comprobar brechas de funcionamiento en nuestro juego)
    - Se puede ejecutar desde la terminal de VS Code, powershel o cmd
Otra solucion serian:
    - Añadir la variable de entorno de manera permanente
    - Ejecutar desde un kernel Linux, bien un SO anfitrion a traves de una virtualización en nuestra máquina o usando alternativas como WLS o Docker que corren imagenes Linux dentro de nuestro windows