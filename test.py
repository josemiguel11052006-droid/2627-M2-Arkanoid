from pathlib import Path

def prueba():
    ruta = Path("niveles/demo.txt")
    texto = ruta.read_text(encoding = "utf-8")
    filas = texto.strip().splitlines()
    for fila in filas:
        if len(filas[0]) != len(fila):
                raise ValueError("El número de caracteres por fila debe ser igual")
        print (fila)
if __name__ == "__main__":
    prueba()