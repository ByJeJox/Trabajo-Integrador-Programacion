import random

# Implementación del torneo como arbol binario usando listas
def crear_arbol(valor):
    return [valor, [], []]

# Función para insertar un nuevo nodo en el subárbol izquierdo
# Solo lo hace si el espacio está vacío, sin sobrescribir nodos existentes
def insertar_izquierda(nodo, nuevo_valor):
    if not nodo[1]:  # Verifica si el nodo no tiene hijo izquierdo
        nodo[1] = [nuevo_valor, [], []] # Si el hijo izquierdo está vacío, inserta el nuevo valor como un nuevo nodo

def insertar_derecha(nodo, nuevo_valor):
    if not nodo[2]:  
        nodo[2] = [nuevo_valor, [], []]

# Definimos los grupos del torneo con equipos en una lista anidada
grupos = [
    ["Grupo A", ["Argentina", "Brasil", "Uruguay", "Chile"]],
    ["Grupo B", ["Francia", "España", "Alemania", "Italia"]],
    ["Grupo C", ["Inglaterra", "Portugal", "Países Bajos", "Bélgica"]],
    ["Grupo D", ["México", "EEUU", "Colombia", "Perú"]],
    ["Grupo E", ["Japón", "Corea del Sur", "Australia", "Arabia Saudita"]],
    ["Grupo F", ["Senegal", "Nigeria", "Argelia", "Marruecos"]],
    ["Grupo G", ["Costa Rica", "Panamá", "Honduras", "El Salvador"]],
    ["Grupo H", ["Rusia", "Polonia", "Suecia", "Dinamarca"]]
]

# Creamos una lista vacia para almacenar los equipos que avanzan a la fase eliminatoria
clasificados = []

# Recorrer cada grupo en la lista 'grupos'
for grupo in grupos:
    print(f"\n{grupo[0]}:")  # Muestra el nombre del grupo
    for i, equipo in enumerate(grupo[1], 1):  # Itera sobre los equipos en cada grupo, asignando numeros
        print(f"{i}. {equipo}")  # Imprime el número del equipo seguido de su nombre

    seleccionados = []  # Lista temporal para almacenar los equipos seleccionados
    while len(seleccionados) < 2:  # Se seleccionan 2 equipos por grupo
        try:
            seleccion = int(input(f"Selecciona un equipo que avanza en {grupo[0]} (1-4): ")) - 1
            
            # Verifica si el numero ingresado esta dentro del rango permitido
            if seleccion not in range(4):
                print(" Opción inválida. Ingresa un número entre 1 y 4.")  # Mensaje de error
                continue  # Repite la solicitud si hubo un error
            
            # Evita la seleccion repetida del mismo equipo
            if grupo[1][seleccion] in seleccionados:
                print(" Ya seleccionaste este equipo. Elige otro.")  # Mensaje de advertencia
                continue  # Repite la solicitud si hubo un error
            
            seleccionados.append(grupo[1][seleccion])  # Agrega el equipo a la lista de seleccionados
        
        except ValueError:  # Maneja errores si el usuario ingresa algo que no es un numero
            print(" Entrada inválida. Ingresa un número.")

    clasificados.extend(seleccionados)  # Agrega los equipos seleccionados a la lista principal de clasificados

# Muestra los equipos clasificados después de que el usuario ha seleccionado todos los grupos
print("\nEquipos clasificados a la fase eliminatoria:")
print(clasificados)

def generar_arbol(eliminatorias):
    if len(eliminatorias) == 1:
        return crear_arbol(eliminatorias[0])  # Último equipo, el campeón

    mitad = len(eliminatorias) // 2
    nodo = crear_arbol("Partido")  # Nodo que representará el enfrentamiento
    
    # Generar los enfrentamientos en la primera mitad y segunda mitad
    nodo[1] = generar_arbol(eliminatorias[:mitad])  
    nodo[2] = generar_arbol(eliminatorias[mitad:])  

    # 🔹 Seleccionar el ganador correctamente y evitar duplicaciones
    ganador = seleccionar_ganador([nodo[1][0], nodo[2][0]])
    nodo[0] = ganador  # Asignar el ganador al nodo actual

    return nodo

def imprimir_arbol_por_niveles(arbol, nivel=0, lista=None, pos=0):
    """Genera una representación en listas para imprimir correctamente el árbol en niveles descendentes."""
    if lista is None:
        lista = {}

    if arbol:
        if nivel not in lista:
            lista[nivel] = []  # Creamos el nivel si todavia no existe
        lista[nivel].append(arbol[0])  # Agregamos el nodo al nivel correspondiente

        imprimir_arbol_por_niveles(arbol[1], nivel + 1, lista, pos * 2)
        imprimir_arbol_por_niveles(arbol[2], nivel + 1, lista, pos * 2 + 1)

    if nivel == 0:
        for k in sorted(lista.keys()):
            print(" ".join([f"[{e}]" for e in lista[k]]))  # Imprime cada nivel correctamente alineado

def imprimir_arbol_horizontal(arbol, indent="", ultimo=True):
    """
    Imprime el árbol de forma horizontal estilo bracket de torneo,
    con conexiones visuales entre nodos.
    """
    if not arbol or arbol == []:
        return
    
    print(indent, end='')
    if ultimo:
        print("└── ", end='')
        indent += "    "
    else:
        print("├── ", end='')
        indent += "│   "
    
    print(arbol[0])  # Imprime el nodo actual
    
    # Primero hijo izquierdo, si existe
    if arbol[1]:
        imprimir_arbol_horizontal(arbol[1], indent, arbol[2] == [])
    # Luego hijo derecho, siempre último si existe
    if arbol[2]:
        imprimir_arbol_horizontal(arbol[2], indent, True)



# Preguntar al usuario si quiere elegir los ganadores manualmente o automáticamente
while True:
    modo_juego = input("\n¿Quieres asignar los ganadores manualmente (M) o automáticamente (A)? ").strip().upper()
    if modo_juego in ["M", "A"]:
        break
    else:
        print("Opción inválida. Ingresa 'M' para manual o 'A' para automático.")

def seleccionar_ganador(equipos):
    if modo_juego == "A":  # Modo automático
        ganador = random.choice(equipos)
        print(f"\nGanador automático: {ganador}")
        return ganador
    else:  # Modo manual
        print(f"\nEnfrentamiento: {equipos[0]} vs {equipos[1]}")
        print("1. " + equipos[0])
        print("2. " + equipos[1])
    
    while True:
            try:
                seleccion = int(input("Selecciona el equipo que gana (1-2): "))
                if seleccion in [1, 2]:
                    return equipos[seleccion - 1]  # Retorna el equipo ganador
                else:
                    print("Opción inválida. Ingresa 1 o 2.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

def generar_arbol(eliminatorias):
    if len(eliminatorias) == 1:
        return crear_arbol(eliminatorias[0])  # Último equipo, el campeón

    mitad = len(eliminatorias) // 2
    nodo = crear_arbol("Partido")  # Nodo que representará el enfrentamiento
    nodo[1] = generar_arbol(eliminatorias[:mitad])  # Primera mitad
    nodo[2] = generar_arbol(eliminatorias[mitad:])  # Segunda mitad

    # Seleccionar el ganador entre los ganadores de las ramas
    nodo[0] = seleccionar_ganador([nodo[1][0], nodo[2][0]])
    
    return nodo

def mostrar_puestos(arbol):
    print("\n ¡El torneo ha terminado! ")
    print(f" Campeón: {arbol[0]}")  # El nodo raíz es el campeón

    # Subcampeón: el que perdió la final
    finalistas = [arbol[1][0], arbol[2][0]]
    subcampeon = finalistas[0] if finalistas[1] == arbol[0] else finalistas[1]
    print(f" Subcampeón: {subcampeon}")

    # Semifinalistas: los que perdieron en semifinales
    # Accedemos a los nodos de semifinales
    semifinalistas = []
    for lado in [arbol[1], arbol[2]]:
        if lado[1] and lado[2]:
            semifinalistas.append(lado[1][0] if lado[2][0] == lado[0] else lado[2][0])

    if len(semifinalistas) == 2:
        print(f" Tercer lugar: {semifinalistas[0]}")
        print(f" Cuarto lugar: {semifinalistas[1]}")
    else:
        print(" No se pudo determinar tercer y cuarto puesto correctamente.")


arbol = generar_arbol(clasificados)  # Generamos el árbol de eliminatorias

# Preguntar si quiere ver los puestos finales, validando entrada S/N
while True:
    ver_puestos = input("\nTenemos un ganador, ¿quieres ver los puestos finales? (S/N): ").strip().upper()
    if ver_puestos in ["S", "N"]:
        break
    else:
        print("Opción inválida. Ingresa 'S' para sí o 'N' para no.")

if ver_puestos == "S":
    mostrar_puestos(arbol)

# Preguntar si quiere imprimir el árbol, validando entrada S/N
while True:
    ver_arbol = input("\n¿Quieres imprimir el árbol por niveles y de forma horizontal? (S/N): ").strip().upper()
    if ver_arbol in ["S", "N"]:
        break
    else:
        print("Opción inválida. Ingresa 'S' para sí o 'N' para no.")
if ver_arbol == "S":
    print("\nÁrbol horizontal:")
    imprimir_arbol_horizontal(arbol)
    print("\nÁrbol por niveles:")
    imprimir_arbol_por_niveles(arbol)


# Recorridos del Árbol
def preorden(arbol):
    if arbol:
        print(arbol[0], end=" ")
        preorden(arbol[1])
        preorden(arbol[2])

def inorden(arbol):
    if arbol:
        inorden(arbol[1])
        print(arbol[0], end=" ")
        inorden(arbol[2])

def postorden(arbol):
    if arbol:
        postorden(arbol[1])
        postorden(arbol[2])
        print(arbol[0], end=" ")

# Preguntar al usuario cómo quiere recorrer el árbol
print("\n¿Cómo quieres recorrer el árbol?")
print("1. Preorden")
print("2. Inorden")
print("3. Postorden")
print("4. Salir")

while True:
    try:
        opcion = int(input("Selecciona una opción (1-4): "))
        if opcion in [1, 2, 3, 4]:
            break
        else:
            print("Opción inválida. Ingresa un número entre 1 y 4.")
    except ValueError:
        print("Entrada inválida. Ingresa un número.")

while opcion != 4:
    print("\n🔎 Recorrido del árbol:")
    if opcion == 1:
        preorden(arbol)
    elif opcion == 2:
        inorden(arbol)
    elif opcion == 3:
        postorden(arbol)
    print("\nRecorrido completado.")

    print("\n¿Cómo quieres recorrer el árbol?")
    print("1. Preorden")
    print("2. Inorden")
    print("3. Postorden")
    print("4. Salir")
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-4): "))
            if opcion in [1, 2, 3, 4]:
                break
            else:
                print("Opción inválida. Ingresa un número entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Ingresa un número.")

print("Gracias por jugar al torneo de la Copa del Mundo") 