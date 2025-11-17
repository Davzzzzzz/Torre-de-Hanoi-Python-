import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Clase Disco que representa un disco individual en la Torre de Hanoi.
class Disco:
    def __init__(self, tamaño):
        self.tamaño = tamaño

# Clase Torre que representa una torre en la Torre de Hanoi.
class Torre:
    def __init__(self, nombre, discos=None):
        
        self.nombre = nombre
        self.discos = discos if discos else []  # Inicializa con una lista vacía si no se proporcionan discos.

    def agregar_disco(self, disco):
        
        if not self.discos or disco.tamaño < self.discos[-1].tamaño:
            self.discos.append(disco)
            return True
        return False

    def quitar_disco(self):
        
        if self.discos:
            return self.discos.pop()
        return None

# Función para mover un disco de una torre a otra.
def mover_disco(origen, destino):
    
    disco = origen.quitar_disco()  # Quita el disco de la torre de origen.
    if disco and destino.agregar_disco(disco):  # Intenta agregar el disco a la torre de destino.
        print(f"Moviendo disco {disco.tamaño} de {origen.nombre} a {destino.nombre}")
        return True
    return False

# Función recursiva para resolver la Torre de Hanoi utilizando paralelismo.
def resolver_hanoi(n, origen, auxiliar, destino, executor):
    
    if n == 1:
        # Caso base: si solo hay un disco, moverlo directamente al destino.
        return [executor.submit(mover_disco, origen, destino)]
    
    # Lista que almacenará las tareas futuras.
    futuras_tareas = []
    # Mover n-1 discos del origen al auxiliar utilizando la torre destino como apoyo.
    futuras_tareas.extend(resolver_hanoi(n-1, origen, destino, auxiliar, executor))
    # Mover el disco restante del origen al destino.
    futuras_tareas.append(executor.submit(mover_disco, origen, destino))
    # Mover los n-1 discos del auxiliar al destino utilizando la torre origen como apoyo.
    futuras_tareas.extend(resolver_hanoi(n-1, auxiliar, origen, destino, executor))
    
    return futuras_tareas

# Función para simular una carga de procesamiento en cada movimiento.
def simular_carga(tarea):
    
    time.sleep(random.uniform(0.1, 0.5))  # Introduce un retraso aleatorio entre 0.1 y 0.5 segundos.
    return tarea

# Función para obtener el número de discos de parte del usuario.
def obtener_numero_discos():
    
    while True:
        try:
            num_discos = int(input("Ingrese el número de discos para la Torre de Hanoi (mínimo 3): "))
            if num_discos >= 3:
                return num_discos
            else:
                print("Por favor, ingrese un número mayor o igual a 3.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

# Bloque principal para ejecutar el programa.
if __name__ == "__main__":
    num_discos = obtener_numero_discos()  # Obtener el número de discos del usuario.
    torres = [Torre(f"Torre_{i}") for i in range(3)]  # Inicializar las tres torres.

    # Colocar todos los discos en la primera torre en orden descendente de tamaño.
    for i in range(num_discos, 0, -1):
        torres[0].agregar_disco(Disco(i))

    # Mostrar el estado inicial de las torres.
    print("\nEstado inicial:")
    for torre in torres:
        print(f"{torre.nombre}: {[disco.tamaño for disco in torre.discos]}")

    # Usar ThreadPoolExecutor para simular un sistema distribuido con 3 hilos (nodos).
    with ThreadPoolExecutor(max_workers=3) as executor:
        inicio = time.time()  # Medir el tiempo de inicio.
        tareas = resolver_hanoi(num_discos, torres[0], torres[1], torres[2], executor)

        # Esperar a que se completen todas las tareas y aplicar la simulación de carga.
        for futuro in as_completed(tareas):
            simular_carga(futuro.result())

    fin = time.time()  # Medir el tiempo de finalización.

    # Mostrar el estado final de las torres.
    print("\nEstado final:")
    for torre in torres:
        print(f"{torre.nombre}: {[disco.tamaño for disco in torre.discos]}")

    # Mostrar el tiempo total de ejecución.
    print(f"\nTiempo total de ejecución: {fin - inicio:.2f} segundos")
