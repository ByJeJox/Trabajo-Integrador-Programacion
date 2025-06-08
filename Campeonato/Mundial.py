# Simulación de Torneo de la Copa del Mundo usando árboles con listas anidadas
import random
# Implementación del torneo como árbol binario usando listas
def crear_arbol(valor):
    return [valor, [], []]

def insertar_izquierda(nodo, nuevo_valor):
    if not nodo[1]:  # Solo inserta si no hay hijo izquierdo
        nodo[1] = [nuevo_valor, [], []]

def insertar_derecha(nodo, nuevo_valor):
    if not nodo[2]:  # Solo inserta si no hay hijo derecho
        nodo[2] = [nuevo_valor, [], []]

# Definir los grupos del torneo con equipos en una lista anidada
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

# Crear una lista vacía para almacenar los equipos que avanzan a la fase eliminatoria
clasificados = []

# Recorrer cada grupo en la lista 'grupos'
for grupo in grupos:
    print(f"\n{grupo[0]}:")  # Muestra el nombre del grupo
    for i, equipo in enumerate(grupo[1], 1):  # Itera sobre los equipos en cada grupo, asignando números
        print(f"{i}. {equipo}")  # Imprime cada equipo con su número correspondiente

    seleccionados = []  # Lista temporal para almacenar los equipos seleccionados
    while len(seleccionados) < 2:  # Asegurar que se seleccionen exactamente 2 equipos por grupo
        try:
            seleccion = int(input(f"Selecciona un equipo que avanza en {grupo[0]} (1-4): ")) - 1
            
            # Verifica si el número ingresado está dentro del rango permitido
            if seleccion not in range(4):
                print(" Opción inválida. Ingresa un número entre 1 y 4.")  # Mensaje de error si la selección no es válida
                continue  # Repite la solicitud si hubo un error
            
            # Evita la selección repetida del mismo equipo
            if grupo[1][seleccion] in seleccionados:
                print(" Ya seleccionaste este equipo. Elige otro.")  # Mensaje de advertencia
                continue  # Repite la solicitud si hubo un error
            
            seleccionados.append(grupo[1][seleccion])  # Agrega el equipo a la lista de seleccionados
        
        except ValueError:  # Maneja errores si el usuario ingresa algo que no es un número
            print(" Entrada inválida. Ingresa un número.")

    clasificados.extend(seleccionados)  # Agrega los equipos seleccionados a la lista principal de clasificados

# Muestra los equipos clasificados después de que el usuario ha seleccionado todos los grupos
print("\nEquipos clasificados a la fase eliminatoria:")
print(clasificados)



def generar_arbol(eliminatorias):
    if len(eliminatorias) == 1:
        return crear_arbol(eliminatorias[0])
    
    mitad = len(eliminatorias) // 2
    nodo = crear_arbol("Torneo")  # Nodo raíz
    nodo[1] = generar_arbol(eliminatorias[:mitad]) 
    nodo[2] = generar_arbol(eliminatorias[mitad:])
    
    return nodo

def imprimir_arbol(arbol, nivel=0):
    if arbol:  # Verifica que el nodo exista
        imprimir_arbol(arbol[2], nivel + 1)  # Imprime primero el hijo derecho
        if isinstance(arbol[0], list):  # Si el nodo contiene dos equipos, los muestra juntos
            print('   ' * nivel + f"[{arbol[0][0]} vs {arbol[0][1]}]")
        else:
            print('   ' * nivel + f"[{arbol[0]}]")  # Muestra la final u otro nodo de un solo equipo
        imprimir_arbol(arbol[1], nivel + 1)  # Luego imprime el hijo izquierdo


# Preguntar al usuario si quiere elegir los ganadores manualmente o automáticamente
modo_juego = input("\n¿Quieres asignar los ganadores manualmente (M) o automáticamente (A)? ").strip().upper()

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

    # Aquí el usuario selecciona al equipo que avanza según el modo de juego
    nodo[0] = seleccionar_ganador([eliminatorias[0], eliminatorias[1]])
    
    return nodo

def mostrar_puestos(arbol):
    print("\n ¡El torneo ha terminado! ")
    print(f" Campeón: {arbol[0]}")  # El nodo raíz es el campeón

    # Obtener subcampeón (el otro equipo en la final)
    subcampeon = arbol[1][0] if arbol[1][0] != arbol[0] else arbol[2][0]
    print(f" Subcampeón: {subcampeon}")

    # Obtener tercer y cuarto puesto (perdedores en semifinales)
    tercer_puesto = arbol[1][1][0] if arbol[1][1] else arbol[2][1][0]
    cuarto_puesto = arbol[1][2][0] if arbol[1][2] else arbol[2][2][0]
    print(f" Tercer lugar: {tercer_puesto}")
    print(f" Cuarto lugar: {cuarto_puesto}")


arbol = generar_arbol(clasificados)  # Generamos el árbol de eliminatorias

ver_puestos = input("\nTenemos un ganador, ¿quieres ver los puestos finales? (S/N): ").strip().upper()
if ver_puestos == "S":
    mostrar_puestos(arbol)


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

while True:
    try:
        opcion = int(input("Selecciona una opción (1-3): "))
        if opcion in [1, 2, 3]:
            break
        else:
            print("⚠️ Opción inválida. Ingresa un número entre 1 y 3.")
    except ValueError:
        print("⚠️ Entrada inválida. Ingresa un número.")

print("\n🔎 Recorrido del árbol:")
if opcion == 1:
    preorden(arbol)
elif opcion == 2:
    inorden(arbol)
else:
    postorden(arbol)

print("\n✅ Recorrido completado.")

def buscar(arbol, pais):
    """Busca un país en el árbol del torneo"""
    if isinstance(arbol, str):
        return arbol == pais
    else:
        return any(buscar(nodo, pais) for nodo in arbol)

