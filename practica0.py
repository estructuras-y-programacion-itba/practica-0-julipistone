import csv
import random

def crear_archivo(nombre): ### crea archivo en modo write, y escribe la estructura del juego. 1
    
    ##Cada 'casilla' es una lista y deja dos espacios vacios para que los jugadores vayan completando.
    with open(nombre, 'w', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['jugadas', 'jugador1', 'jugador2'])
        escritor.writerow(['generala', ' ', ' '])
        escritor.writerow(['poker', ' ', ' '])
        escritor.writerow(['full', ' ', ' '])
        escritor.writerow(['escalera', ' ', ' '])
        for i in range(1,7):
            escritor.writerow([i, ' ', ' '])

crear_archivo('jugadas.csv') ##llama a la funcion y crea el archivo


def tirar_dados(cantidad): ### genera una lista con los dados que se tiraron 'aleatorios'. 'cantidad' son los dados a tirar
    dados = []
    for i in range(cantidad):
        dados.append(random.randint(1,6))
    return dados

def pedir_posiciones(): ## como lo dice, pide las posiciones de la lista_dados con la que el jugador se quiere quedar.
    posiciones = []
    seguir = True

    while seguir == True:
        entrada = input("Ingresar posicion a conservar (0 a 4, Enter para terminar): ")

        if entrada == "": ## si hay un vacio de entrada, termina la jugada
            seguir = False
        else:
            pos = int(entrada)

            if pos < 0 or pos > 4: ##valida que este dentro de las posiciones
                print("Posicion invalida")
            elif pos in posiciones: ##valida que no se repita la pos
                print("Esa posicion ya fue ingresada")
            else:
                posiciones.append(pos) ##apendea a la lista

    return posiciones 

def nueva_tirada(dados_actuales, posiciones): ##recorre la lista de pos y se guarda los dados que eligio el jugador en una nueva lista. 
    ##tira los dados restantes. 
    dados_guardados = []

    for pos in posiciones:
        dados_guardados.append(dados_actuales[pos])

    faltan = 5 - len(dados_guardados)
    dados_nuevos = tirar_dados(faltan) ## aca cuenta cuantos dados quedan por tirar y utiliza la funcion tirar dados. cantidad=faltan

    return dados_guardados + dados_nuevos

def turno(): ## maneja las tres tiradas de cada turno del jugador
    dados = tirar_dados(5)
    primera_tirada = dados[:]   # guarda la primera tirada
    print("Tirada 1:", dados)

    tirada = 1
    posiciones = pedir_posiciones() ## hasta aca es la primer jugada. muestra los primeros 5 dados, pide pos al jugador

    while tirada < 3 and posiciones != []: 
        dados = nueva_tirada(dados, posiciones) ## usa la funcion nueva_tirada.
        tirada += 1
        print("Tirada", tirada, ":", dados)

        if tirada < 3:
            posiciones = pedir_posiciones()
        else:
            posiciones = [] ### aca no vuelve a pedir pos, ya queda la ult lista

    return dados, primera_tirada 

def elegir_jugada(): ## pide al jugador donde anotar
    jugada = input("Elegir donde anotar: ")
    return jugada

def calcular_suma(lista_final, numero): ## suma los numsss del jugador donde quiere anotar
    suma = 0
    for dado in lista_final:
        if dado == numero:
            suma = suma + dado
    return suma

def es_generala(lista_final): ## chequea que sea generala
    primero = lista_final[0]
    iguales = True

    for dado in lista_final: ## setea que iguales=true y despues recorre toda la lista. Si un dado no es igual al primero, setea iguales=false
        if dado != primero:
            iguales = False

    return iguales

def es_poker(lista_final): ## chequea que sea poker
    i = 0

    while i < len(lista_final):
        contador = 0

        for dado in lista_final:
            if dado == lista_final[i]:
                contador += 1

        if contador >= 4:
            return True

        i += 1

    return False

def es_full(lista_final):
    i = 0
    tiene_tres = False
    tiene_dos = False

    while i < len(lista_final):
        contador = 0

        for dado in lista_final:
            if dado == lista_final[i]:
                contador += 1

        if contador == 3:
            tiene_tres = True
        if contador == 2:
            tiene_dos = True

        i += 1

    if tiene_tres and tiene_dos:
        return True
    else:
        return False

def es_escalera(lista_final):
    lista_ordenada = sorted(lista_final)

    if lista_ordenada == [1,2,3,4,5] or lista_ordenada == [2,3,4,5,6]:
        return True
    else:
        return False
    
def bonus_primera_tirada(jugada, primera_tirada): #anota los bonus de la primera tirada

    if jugada == 'generala' and es_generala(primera_tirada): #el True avisa que el juego debe terminar 
        return 30, True

    elif jugada == 'poker' and es_poker(primera_tirada):
        return 5, False

    elif jugada == 'full' and es_full(primera_tirada):
        return 5, False

    elif jugada == 'escalera' and es_escalera(primera_tirada):
        return 5, False

    else:
        return 0, False

def calcular_puntos(jugada, lista_final): ## en esta jugada calcula los puntos y valida que la lista cumpla lo que el juagdor quiere anotar
    if jugada == 'generala':
        if es_generala(lista_final):
            return 50
        else:
            return 0
    elif jugada == 'poker':
        if es_poker(lista_final):
            return 40
        else:
            return 0
    elif jugada == 'full':
        if es_full(lista_final):
            return 30
        else:
            return 0
    elif jugada == 'escalera':
        if es_escalera(lista_final):
            return 20
        else:
            return 0
    else:
        numero = int(jugada)
        return calcular_suma(lista_final, numero)


def anotar_jugada(nombre, jugada, lista_final, jugador): ##anota en el csv lo que el jugadro quiere anotar
    tablero = [] ## crea una lista vacia, para pasar todas las filas del csv y crear una lista de listas
    anotado = False

    with open(nombre, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            tablero.append(fila) ## aca crea la lista de listas

    if jugador == 1: ## se fija que jugadro es y designa la columna
        columna = 1
    else:
        columna = 2

    while anotado == False: ## no este ocupada ese casilla
        i = 0
        encontrada = False ## se fija que encuentre la jugada en el tablero

        while i < len(tablero) and encontrada == False:
            if str(tablero[i][0]) == jugada: ## la jugada es lo que elige el jugador en donde anotar y se fija si existe en el tablero(la primera columna)
                encontrada = True

                if tablero[i][columna] == ' ': ## chequea que no este completado
                    puntos = calcular_puntos(jugada, lista_final)
                    tablero[i][columna] = puntos ##lo reemplaza
                    anotado = True 
                else: ## si esta ocupada
                    print("Esa jugada ya esta ocupada. Tenes que elegir otra.")
                    jugada = elegir_jugada()

            i = i + 1

        if encontrada == False: ## si no encuentra la juagda
            print("Jugada invalida. Elegi otra.")
            jugada = elegir_jugada()

    with open(nombre, 'w', encoding='utf-8') as archivo: ## reescribe el archivo con los datos nyevos
        escritor = csv.writer(archivo)
        for fila in tablero:
            escritor.writerow(fila)

    return puntos

def jugar_un_turno(jugador): ## ejecuta el turno de cada jugador
    print()
    if jugador == 1:
        print("Jugador 1:")
    else:
        print("Jugador 2:")

    lista_final,primera_tirada = turno() ## ejecuta el turno y guarda la lista final de dados y la primera tirada para los bonus
    print(lista_final)
    jugada = elegir_jugada()
    puntos = anotar_jugada('jugadas.csv', jugada, lista_final, jugador)
    bonus, fin = bonus_primera_tirada(jugada, primera_tirada) ## chequea si hay bonus por la primera tirada y si el juego debe terminar por generala en la primera tirada
    puntos = puntos + bonus
    return puntos, fin


jugador = 1 ## setea estos valores para arrancar con jugador1  y ronda 1
ronda = 1

puntos_jugador1 = 0 ## setea puntos=0
puntos_jugador2 = 0

fin_del_juego = False

while ronda <= 10 and fin_del_juego == False:

    puntos, fin = jugar_un_turno(jugador)

    if jugador == 1:
        puntos_jugador1 = puntos_jugador1 + puntos

        if fin:
            fin_del_juego = True
        else:
            jugador = 2

    else:
        puntos_jugador2 = puntos_jugador2 + puntos

        if fin:
            fin_del_juego = True
        else:
            jugador = 1
            ronda = ronda + 1

print()
print("Puntaje final:")
print("Jugador 1:", puntos_jugador1)
print("Jugador 2:", puntos_jugador2)

### se fija quien gano
if puntos_jugador1 > puntos_jugador2:
    print("Gano el Jugador 1 con", puntos_jugador1, "puntos")
elif puntos_jugador2 > puntos_jugador1:
    print("Gano el Jugador 2 con", puntos_jugador2, "puntos")
else:
    print("Empate en", puntos_jugador1, "puntos")