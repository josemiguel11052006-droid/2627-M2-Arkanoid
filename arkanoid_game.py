"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    
    # - Comprueba que `self.level_path` existe y es fichero.
    if not self.level_path.is_file():
        raise ValueError ( "No existe o no es un fichero")
    
        # leemos el fichero de texto y lo guardamos en la variable texto
    texto = self.level_path.read_text(encoding = "utf-8")
    
        # separamos el texto por lineas dentro de una tupla
    filas = []
    for linea in texto.splitlines():
        if linea.strip():
            filas.append(linea.rstrip())
    
    # Comprobamos que haya filas o que el contenido de las filas sea valido
    if not filas:
        raise ValueError("El nivel esta vacio, o no tiene ningun simbolo valido")
        
        # recorremos la tupla para comprobar que todas las lineas tienen la misma longitud    
        # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    for fila in filas:
        # Si la linea no esta vacia
        if len(filas[0]) != len(fila):
                
                # Comparamos la primera linea, el primer elemento con todos los demas, que los recorre el for
            raise ValueError("El número de caracteres por fila debe ser igual")       
        
        # - Guarda el resultado en `self.layout` y devuélvelo.
        self.layout.append(fila)
    return self.layout
            

@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    self.paddle = self.crear_rect(0, 0, *self.PADDLE_SIZE)
    self.paddle.midbottom=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT-self.PADDLE_OFFSET)
    
    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    self.score = 0
    self.lives = 3
    self.end_message = ""    
    
    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    self.reiniciar_bola()
    

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    
    # - Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    self.blocks = []
    self.block_colors = []
    self.block_symbols = []
    
    # - Recorre `self.layout` para detectar símbolos de bloque.
    # - Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
    # funcion enumerate genera indice para las filas self.layout y despues para recorrer las columnas de cada fila
    for numero_fila, fila in enumerate(self.layout):
        
        for columna, simbolo in enumerate(fila):
            
            # Comprobamos que el simbolo es valido
            if simbolo in self.BLOCK_COLORS:
                
                # obtenemos posicion del bloque con los indice en los que nos encontramos
                posicion_bloque = self.calcular_posicion_bloque(numero_fila, columna)
                
                # añadimos el bloque a la posicin
                self.blocks.append(posicion_bloque)
                
                # ajustamos el color del bloque segun su simbolo 
                self.block_colors.append(self.BLOCK_COLORS[simbolo])

                # guardamos el simbolo para despues saber su puntuacion segun cual sea
                self.block_symbols.append(simbolo)
            

@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    
    # - Obtén el estado de teclas con `self.obtener_estado_teclas()`.
    estado_teclas = self.obtener_estado_teclas()
    
    # - Desplaza la paleta con `self.PADDLE_SPEED` si se pulsan las teclas izquierda/derecha. 
    # [flecha izq o letra a]
    if estado_teclas[self.KEY_LEFT] or estado_teclas[self.KEY_A]:
        self.paddle.x -= self.PADDLE_SPEED

    # [flecha der o letra d]
    if estado_teclas[self.KEY_RIGHT] or estado_teclas[self.KEY_D]:
        self.paddle.x += self.PADDLE_SPEED
        
    # - Limita la posición de la paleta para que no salga de la pantalla.
    # evita que desborde devolviendo 0 siempre que el limite izquiero vaya a ser menor
    self.paddle.left = max(0, self.paddle.left)
    
    # evita que desborde devolviendo el ancho siempre que el limite derecho vaya a ser mayor
    self.paddle.right = min(self.SCREEN_WIDTH, self.paddle.right)


@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
    # - Suma `self.ball_velocity` a `self.ball_pos` y genera `ball_rect` con `self.obtener_rect_bola()`.
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()
    # - Gestiona rebotes con paredes, paleta y bloques, modificando velocidad y puntuación.
    
    # Rebote con la pared de la izquierda
    if ball_rect.left < 0:
        self.ball_pos.x = self.BALL_RADIUS
        self.ball_velocity.x = abs(self.ball_velocity.x)
        
    # Rebote con la pared de la derecha
    if ball_rect.right > self.SCREEN_WIDTH:
        self.ball_pos.x = self.SCREEN_WIDTH - self.BALL_RADIUS
        self.ball_velocity.x = -abs(self.ball_velocity.x)
        
    # Rebore con el techo
    if ball_rect.top < 0:
        self.ball_pos.y = self.BALL_RADIUS
        self.ball_velocity.y = abs(self.ball_velocity.y)
    
    # Se vuelve a obtener el rectangulo, sino se queda la pelota pillada en el techo
    ball_rect = self.obtener_rect_bola()    
    
    # Resta vida si la bola cae por arriba
    if ball_rect.bottom > self.SCREEN_HEIGHT: 
        self.lives -= 1
        
        # Si no te quedan mas vidas, pierdes
        if self.lives <= 0 : 
            self.end_message = "¡Has perdido!"
        
        # Si te quedan mas vidas sigues jugando con una vida menos
        else :
            self.reiniciar_bola()
        return
    
        
    # choque contra bloque
    # esta funcion obtiene el indice si tras comprobar impactos de la pelota con algun bloque coinciden
    indice = ball_rect.collidelist(self.blocks)
    
    # si ha habido impacto elimina el bloque y cambia la direccion de la bola
    if indice != -1:
        simbolo = self.block_symbols[indice]
        self.score += self.BLOCK_POINTS[simbolo]
        del self.blocks[indice]
        del self.block_colors[indice]
        del self.block_symbols[indice]
        self.ball_velocity.y = -self.ball_velocity.y
        
    # choque contra la pala
    
    # si ha habido impacto con la pala cuando la bola desciende, porque sino la bola se queda imantada en la pala
    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:
        self.ball_pos.y -= ball_rect.bottom - self.paddle.top
        desplazamiento = (self.ball_pos.x - self.paddle.centerx) / (self.paddle.width / 2)
        desplazamiento = max(-1.0, min(1.0, desplazamiento))
        self.ball_velocity = Vector2(desplazamiento, -1.2).normalize() * self.BALL_SPEED
     
    # - Controla fin de nivel cuando no queden bloques y resta vidas si la bola cae.
    if not self.blocks:
        self.end_message = "¡Has ganado!"
    

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    
    # Rellenamos el fondo de la pantalla usando el color definido en arkanoid core
    self.screen.fill(self.BACKGROUND_COLOR)
    
    # Dibujar cada bloque obteniendo bloques y color correspondiente con las funciones correspondientes
    for bloque, color in zip(self.blocks, self.block_colors):
        self.dibujar_rectangulo(bloque, color)
        
    # - Pinta la paleta y la bola con las utilidades proporcionadas.
    
    # Dibujar la pala
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    
    # Dibujar la bola, transformamos a int porque en el eje x e y no deja añadir floats que es lo que devuelve
    self.dibujar_circulo((int(self.ball_pos.x), int(self.ball_pos.y)),self.BALL_RADIUS, self.BALL_COLOR)
    
    # - Muestra puntuación, vidas y mensajes usando `self.dibujar_texto`.
    
    # puntuacion
    self.dibujar_texto(f"PUNTUACION: {self.score}",(10,10))
    
    # mostrar vidas
    self.dibujar_texto(f"VIDAS: {self.lives}", (self.SCREEN_WIDTH - 110, 10))
    
    # cuando hay mensaje final se muestra en el centro de la pantalla
    if self.end_message:
        self.dibujar_texto(
            self.end_message,
            (self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2)
        )

@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    
    # - Inicializa recursos (`self.inicializar_pygame`, `self.cargar_nivel`, etc.).
    self.inicializar_pygame()
    self.cargar_nivel()
    self.crear_bloques()
    self.preparar_entidades()
    
    # - Procesa eventos de `self.iterar_eventos()` y llama a los métodos de actualización/dibujo.
    running = True
    # blucle para controlar cuando se esta ejecutando y cuando no, evita que se quede abierto en segundo plano tras cerrar
    while running:
        for evento in self.iterar_eventos():
            # METODOS DE CERRAR EL PROGRAMA DE MANERA LIMPIA
            if evento.type == self.EVENT_QUIT:
                running = False
            elif evento.type == self.EVENT_KEYDOWN and evento.key == self.KEY_ESCAPE:
                running = False
                
    # - Refresca la pantalla con `self.actualizar_pantalla()` y cierra con `self.finalizar_pygame()`.
        if not self.end_message: 
            self.procesar_input()
            self.actualizar_bola()
        self.dibujar_escena()
        self.actualizar_pantalla()
        self.clock.tick(self.FPS)

    self.finalizar_pygame()
        
    


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
