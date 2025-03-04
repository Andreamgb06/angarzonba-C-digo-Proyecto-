import random

class Tablero:
    """
    Clase que representa el tablero del juego de Parchís.
    Contiene la información de las casillas, seguros, salidas y llegadas.
    """
    def __init__(self):
        # Inicializa 68 casillas normales en el tablero principal
        self.casillas = [{"tipo": "normal", "ocupantes": []} for _ in range(68)]
        # Posiciones de las casillas seguras
        self.seguros = [12, 26, 40, 54]
        # Posiciones de las casillas de salida para cada color
        self.salidas = {"rojo": 5, "azul": 19, "verde": 33, "amarillo": 47}
        # Rangos de las casillas de llegada para cada color
        self.llegadas = {"rojo": range(69, 77), "azul": range(77, 85), 
                         "verde": range(85, 93), "amarillo": range(93, 101)}
        # Configura las casillas especiales en el tablero
        self.configurar_tablero()

    def configurar_tablero(self):
        """Configura las casillas de seguro y salida en el tablero."""
        # Marca las casillas seguras
        for i in self.seguros:
            self.casillas[i]["tipo"] = "seguro"
        # Marca las casillas de salida y su color
        for color, pos in self.salidas.items():
            self.casillas[pos]["tipo"] = "salida"
            self.casillas[pos]["color"] = color
    
    def seguro(self, posicion):
        """Verifica si una posición es una casilla segura."""
        if posicion < 68:
            return self.casillas[posicion]["tipo"] == "seguro"
        return False
    
    def salida(self, posicion):
        """Verifica si una posición es una casilla de salida."""
        if posicion < 68:
            return self.casillas[posicion]["tipo"] == "salida"
        return False

    def color_salida(self, posicion):
        """Devuelve el color de la casilla de salida, si aplica."""
        if posicion < 68 and self.salida(posicion):
            return self.casillas[posicion]["color"]
        return None
    
    def casilla_internas(self, color, avance):
        """
        Determina la posición en las casillas internas (llegada) 
        para un color y un avance específicos.
        """
        for i, pos in enumerate(self.llegadas[color]):
            if avance == i:
                return pos
        return None
    
    def bloqueo(self, posicion):
        """
        Verifica si hay un bloqueo en la posición (2 fichas del mismo color).
        """
        if posicion >= 68:
            return False
        ocupantes = self.casillas[posicion]["ocupantes"]
        if len(ocupantes) < 2:
            return False
        if ocupantes[0].color == ocupantes[1].color:
            return True
        return False

    def agregar_ficha(self, ficha, posicion):
        """
        Agrega una ficha a una casilla y maneja la lógica de capturas.
        Retorna True si se capturó una ficha, False en caso contrario.
        """
        if posicion >= 68:
            return False
        ocupantes = self.casillas[posicion]["ocupantes"]
        
        # Si no hay ocupantes, simplemente agrega la ficha
        if not ocupantes:
            ocupantes.append(ficha)
            return False
            
        # Si hay una ficha existente
        if len(ocupantes) == 1:
            ficha_existente = ocupantes[0]
            
            # Caso especial: misma salida para fichas del mismo color
            if self.salida(posicion) and ficha_existente.color == ficha.color:
                ocupantes.remove(ficha_existente)
                ocupantes.append(ficha)
                return True
                
            # En casillas seguras o de salida se pueden apilar hasta 2 fichas
            if self.seguro(posicion) or self.salida(posicion):
                if len(ocupantes) < 2:
                    ocupantes.append(ficha)
                return False
                
            # Si son del mismo color, se pueden apilar hasta 2 fichas
            if ficha_existente.color == ficha.color:
                if len(ocupantes) < 2:
                    ocupantes.append(ficha)
                return False
                
            # Si son de distinto color, se captura la ficha existente
            ocupantes.remove(ficha_existente)
            ficha_existente.reiniciar()
            ocupantes.append(ficha)
            return True
            
        # Si ya hay dos ocupantes, no se puede agregar más fichas
        if len(ocupantes) == 2:
            return False  # CORRECCIÓN: Faltaba el return aquí
            
    def quitar_ficha(self, ficha):
        """Elimina una ficha de su posición actual en el tablero."""
        if ficha.posicion is None or ficha.carcel:
            return
        if ficha.posicion < 68:
            if ficha in self.casillas[ficha.posicion]["ocupantes"]:
                self.casillas[ficha.posicion]["ocupantes"].remove(ficha)

    def vertablero(self):
        """Muestra una representación visual del tablero en la consola."""
        print("Tablero:")
        for fila in range(7):
            for col in range(10):
                i = fila * 10 + col
                if i >= len(self.casillas):
                    break
                casilla = self.casillas[i]
                tipo = "S" if casilla["tipo"] == "seguro" else "N"
                if casilla["tipo"] == "salida":
                    tipo = f"{casilla.get('color', '')[0].upper()}"
                ocupantes_str = " ".join([ficha.color[0].upper() for ficha in casilla["ocupantes"]])
                if not ocupantes_str:
                    ocupantes_str = " "
                print(f"[{tipo}{ocupantes_str}]", end=" ")
            print()
        print("\nFin del Tablero\n")
        
class Dados:
    """
    Clase para manejar los dados del juego.
    Permite lanzar dos dados o forzar valores específicos en modo desarrollador.
    """
    def __init__(self, modo_desarrollador=False):
        self.d1 = 0
        self.d2 = 0
        self.modo_desarrollador = modo_desarrollador
        self.forzar_manual = False

    def lanzar(self):
        """
        Lanza los dados. Si está en modo desarrollador y forzar_manual,
        permite al usuario ingresar los valores.
        """
        if self.modo_desarrollador and self.forzar_manual:
            try:
                self.d1 = int(input("Ingresa por favor el valor del primer dado (1-6): "))
                while self.d1 < 1 or self.d1 > 6:
                    self.d1 = int(input("Valor inválido. intenta de nuevo: primer dado (1-6): "))
                self.d2 = int(input("Ingresa por favor el valor del segundo dado (1-6): "))
                while self.d2 < 1 or self.d2 > 6:
                    self.d2 = int(input("Valor inválido. Intenta de nuevo: segundo dado (1-6): "))
            except ValueError:
                print("Entrada inválida. Usando valores aleatorios.")
                self.d1 = random.randint(1, 6)
                self.d2 = random.randint(1, 6)
        else:
            self.d1 = random.randint(1, 6)
            self.d2 = random.randint(1, 6)
        return self.d1, self.d2
           
class Ficha:
    """
    Clase que representa una ficha del juego.
    Cada ficha tiene un color, un ID, y un estado (en cárcel o en juego).
    """
    def __init__(self, color, id_ficha):
        self.color = color
        self.id = id_ficha
        self.carcel = True  # Todas las fichas empiezan en la cárcel
        self.posicion = None
        self.llegada = None
        self.ultima_movida = None

    def mover(self, nueva_posicion):
        """Mueve la ficha a una nueva posición y actualiza su estado."""
        self.posicion = nueva_posicion
        self.carcel = False
        self.ultima_movida = True
        
        # Verifica si la ficha ha llegado a su zona final
        if self.color == "rojo" and nueva_posicion >= 69 and nueva_posicion < 77:
            self.llegada = True
        elif self.color == "azul" and nueva_posicion >= 77 and nueva_posicion < 85:
            self.llegada = True
        elif self.color == "verde" and nueva_posicion >= 85 and nueva_posicion < 93:
            self.llegada = True
        elif self.color == "amarillo" and nueva_posicion >= 93 and nueva_posicion < 101:
            self.llegada = True

    def reiniciar(self):
        """Devuelve la ficha a la cárcel."""
        self.carcel = True
        self.posicion = None
        self.ultima_movida = False
        self.llegada = False
    
    def __str__(self):
        """Representación de texto de la ficha."""
        if self.carcel:
            estado = "en la cárcel"
        elif self.llegada:
            estado = f"en la posición {self.posicion} (llegada)"
        else:
            estado = f"en la posición {self.posicion}"
        return f"Ficha {self.id} de color {self.color} {estado}"

class Jugador:
    """
    Clase que representa a un jugador.
    Cada jugador tiene un nombre, un color, y 4 fichas.
    """
    def __init__(self, nombre, color, tablero):
        self.nombre = nombre
        self.color = color
        self.tablero = tablero
        self.fichas = [Ficha(color, i) for i in range(4)]
        self.pares_consecutivos = 0
        self.movimientos_extra = 0
        self.ultima_ficha_movida = None

    def fichas_carcel(self):
        """Devuelve una lista de las fichas que están en la cárcel."""
        return [ficha for ficha in self.fichas if ficha.carcel]

    def fichasactivas(self):
        """Devuelve una lista de las fichas que están en juego."""
        return [ficha for ficha in self.fichas if not ficha.carcel]

    def marcar_ultima_ficha(self, ficha_elegida):
        """Marca la última ficha movida por el jugador."""
        for ficha in self.fichas:
            ficha.ultima_movida = False
        if ficha_elegida:
            ficha_elegida.ultima_movida = True
            self.ultima_ficha_movida = ficha_elegida

    def ganador(self):
        """Verifica si el jugador ha ganado (todas sus fichas en llegada)."""
        return all(ficha.llegada for ficha in self.fichas)

    def puede_mover_ficha(self, ficha, avance):
        """
        Verifica si una ficha puede moverse un número determinado de casillas.
        Comprueba si hay bloqueos en el camino o si el movimiento es válido.
        """
        if ficha.carcel:
            return False
            
        posicionact = ficha.posicion
        
        # Verifica si hay bloqueos en el camino
        for i in range(1, avance + 1):
            pos_intermedia = (posicionact + i) % 68
            if self.tablero.bloqueo(pos_intermedia):
                return False
                
        # Caso para fichas en el tablero principal
        if posicionact < 68:
            nueva_posicion = posicionact + avance
            # Si la ficha pasaría a la zona interna
            if nueva_posicion >= 68:
                avance_interno = nueva_posicion - 68
                # Solo puede avanzar hasta 7 casillas internas (0-7)
                if avance_interno < 8:
                    return True
                else:
                    return False
            else:
                return True
        # Caso para fichas ya en zona interna
        else:
            # Encuentra el índice actual en la zona interna
            for i, pos in enumerate(self.tablero.llegadas[self.color]):
                if pos == posicionact:
                    indice_actual = i
                    break
            nuevo_indice = indice_actual + avance
            # Solo puede avanzar hasta el final de la zona interna
            if nuevo_indice < 8:
                return True
            else:
                return False
        return False

class Juego:
    """
    Clase principal que maneja la lógica del juego.
    Coordina turnos, jugadores, tablero y dados.
    """
    def __init__(self, modo_desarrollador=False):
        self.tablero = Tablero()
        self.dados = Dados(modo_desarrollador)
        self.jugadores = []
        self.turnoact = 0
        self.modo_desarrollador = modo_desarrollador

    def solicitar_ficha(self, mensaje, fichasact):
        """
        Solicita al usuario que elija una ficha.
        Retorna el índice de la ficha o None si no elige ninguna.
        """
        while True:
            try:
                ficha_idx = int(input(mensaje)) - 1
                if ficha_idx == -1:
                    return None  # El usuario decidió pasar
                if 0 <= ficha_idx < len(fichasact):
                    return ficha_idx
                print("Número fuera de rango. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

    def agregarjugador(self, nombre, color):
        """Agrega un nuevo jugador al juego."""
        if color not in ["rojo", "azul", "verde", "amarillo"]:
            print("Color inválido, por favor elige entre rojo, azul, verde o amarillo.")
            return False
        if any(jugador.color == color for jugador in self.jugadores):
            print("Ya hay un jugador con ese color.")
            return False
        self.jugadores.append(Jugador(nombre, color, self.tablero))
        print(f"Jugador {nombre} agregado con éxito con el color {color}.")
        return True
        
    def cambiodeturno(self):
        """Cambia al siguiente jugador."""
        self.turnoact = (self.turnoact + 1) % len(self.jugadores)
    
    def manejar_pares_consecutivos(self, jugador, d1, d2):
        """
        Maneja la lógica de los pares consecutivos.
        Si un jugador saca 3 pares consecutivos, su última ficha movida vuelve a la cárcel.
        """
        if d1 == d2:
            jugador.pares_consecutivos += 1
            print(f"¡Felicidades sacaste par!, recuerda que llevas {jugador.pares_consecutivos} pares consecutivos.")
            if jugador.pares_consecutivos == 3:
                print("Sacaste tres pares seguidos :(, tu ultima ficha movida se irá a la cárcel.")
                if jugador.ultima_ficha_movida:
                    self.tablero.quitar_ficha(jugador.ultima_ficha_movida)  # CORRECCIÓN: Quitar la ficha del tablero
                    jugador.ultima_ficha_movida.reiniciar()
                jugador.pares_consecutivos = 0
                return False
            return True
        else:
            jugador.pares_consecutivos = 0
            return False
            
    def sacar_ficha_carcel(self, jugador, d1, d2):
        """
        Intenta sacar una ficha de la cárcel si se obtiene un 5 en los dados.
        Retorna True si se sacó una ficha, False en caso contrario.
        """
        fichas_carcel = jugador.fichas_carcel()
        if not fichas_carcel:
            print("No tienes fichas en la cárcel.")
            return False
            
        # Se puede sacar una ficha si alguno de los dados es 5 o si su suma es 5
        cinco = d1 == 5 or d2 == 5 or d1 + d2 == 5
        if not cinco:
            return False
            
        pos_salida = self.tablero.salidas[jugador.color]
        ocupantes = self.tablero.casillas[pos_salida]["ocupantes"]
        
        # Comprobar si la casilla de salida está bloqueada por fichas del mismo color
        if len(ocupantes) >= 2 and all(ficha.color == jugador.color for ficha in ocupantes):
            print("No puedes sacar la ficha de la cárcel, ya hay dos fichas en la salida.")
            return False
            
        ficha = fichas_carcel[0]
        self.tablero.quitar_ficha(ficha)
        ficha.mover(pos_salida)
        captura = self.tablero.agregar_ficha(ficha, pos_salida)
        print(f"Ficha {ficha.id} de color {ficha.color} salió de la cárcel a la posición {pos_salida}.")
        
        if captura:
            jugador.movimientos_extra = 20
            print("¡Capturaste una ficha enemiga, ahora tienes 20 movimientos extra!")
        return True
        
    def mover_ficha(self, jugador, ficha_idx, avance):
        """
        Mueve una ficha un número determinado de casillas.
        Maneja la lógica de capturas y llegadas.
        """
        fichasact = jugador.fichasactivas()
        if ficha_idx < 0 or ficha_idx >= len(fichasact):
            print("Ficha inválida.")
            return False
            
        ficha = fichasact[ficha_idx]
        if not jugador.puede_mover_ficha(ficha, avance):
            print(f"No puedes mover la ficha {ficha.id} {avance} casillas.")  # CORRECCIÓN: f-string
            return False
            
        self.tablero.quitar_ficha(ficha)
        posicionact = ficha.posicion
        
        # Caso para fichas en el tablero principal
        if posicionact < 68:
            nueva_posicion = posicionact + avance
            # Si la ficha pasa a la zona interna
            if nueva_posicion >= 68:
                avance_interno = nueva_posicion - 68
                nueva_posicion = self.tablero.casilla_internas(jugador.color, avance_interno)
                ficha.mover(nueva_posicion)
                print(f"Ficha {ficha.id} de color {ficha.color} ha llegado a su casilla interna {nueva_posicion}.")
                jugador.movimientos_extra = 10
                print("¡Felicidades!, ahora tienes 10 movimientos extra.")
            # Si se queda en el tablero principal
            else:
                ficha.mover(nueva_posicion)
                captura = self.tablero.agregar_ficha(ficha, nueva_posicion)
                print(f"Ficha {ficha.id} de color {ficha.color} se ha movido a la posición {nueva_posicion}.")
                if captura:
                    jugador.movimientos_extra = 20
                    print("¡Capturaste una ficha enemiga, ahora tienes 20 movimientos extra!")
        # Caso para fichas ya en zona interna
        else:
            # Encuentra el índice actual en la zona interna
            for i, pos in enumerate(self.tablero.llegadas[jugador.color]):
                if pos == posicionact:
                    indice_actual = i
                    break
            nuevo_indice = indice_actual + avance
            nueva_posicion = self.tablero.casilla_internas(jugador.color, nuevo_indice)
            ficha.mover(nueva_posicion)
            print(f"Ficha {ficha.id} de color {ficha.color} movida a la casilla interna {nueva_posicion}.")
            
        jugador.marcar_ultima_ficha(ficha)
        return True

    def jugarturno(self):
        """
        Ejecuta un turno completo de un jugador.
        Retorna True si el jugador ha ganado, False en caso contrario.
        """
        jugador = self.jugadores[self.turnoact]
        print(f"\nTurno del jugador {jugador.nombre}, color {jugador.color}")
        print("Estado de las fichas:")
        for ficha in jugador.fichas:
            print(f"Ficha {ficha.id}: {ficha}")
            
        d1, d2 = self.dados.lanzar()
        print(f"Dados: {d1}, {d2}")
        
        # Maneja pares consecutivos
        repetir_turno = self.manejar_pares_consecutivos(jugador, d1, d2)
        
        # Intenta sacar una ficha de la cárcel
        ficha_sacada = self.sacar_ficha_carcel(jugador, d1, d2)
        
        # Si no sacó una ficha, puede mover las fichas activas
        if not ficha_sacada:
            fichasact = jugador.fichasactivas()
            if not fichasact:
                print("No tienes fichas para mover.")
            else:
                print("Fichas activas:")
                for i, ficha in enumerate(fichasact):
                    print(f"{i + 1}: {ficha}")
                    
                # Mover con el primer dado
                ficha_idx = self.solicitar_ficha(f"Elige una ficha para mover {d1} casillas (1-{len(fichasact)}, 0 para pasar): ", fichasact)
                if ficha_idx is not None:
                    self.mover_ficha(jugador, ficha_idx, d1)
                    
                # Actualizar lista de fichas activas para el segundo dado
                fichasact = jugador.fichasactivas()
                
                # Mover con el segundo dado
                ficha_idx = self.solicitar_ficha(f"Elige una ficha para mover {d2} casillas (1-{len(fichasact)}, 0 para pasar): ", fichasact)
                if ficha_idx is not None:
                    self.mover_ficha(jugador, ficha_idx, d2)
        
        # Maneja los movimientos extra
        while jugador.movimientos_extra > 0:
            fichasact = jugador.fichasactivas()
            if not fichasact:
                print("No tienes fichas para usar tus movimientos extra.")
                jugador.movimientos_extra = 0
                break
                
            print(f"Te quedan {jugador.movimientos_extra} movimientos extra.")
            print("Fichas disponibles para mover:")
            for i, ficha in enumerate(fichasact):
                print(f"{i + 1}: {ficha}")
                
            try:
                ficha_idx = int(input(f"Elige una ficha para mover (1-{len(fichasact)}, 0 para pasar): ")) - 1
                if ficha_idx < 0:
                    jugador.movimientos_extra = 0
                    break
                if self.mover_ficha(jugador, ficha_idx, 1):  # Los movimientos extra son de 1 en 1
                    jugador.movimientos_extra -= 1
            except ValueError:
                print("Entrada inválida. Perdiste un movimiento extra.")
                jugador.movimientos_extra -= 1
                
        self.tablero.vertablero()
        
        # Verifica si el jugador ha ganado
        if jugador.ganador():
            print(f"¡El jugador {jugador.nombre}, color {jugador.color} es el ganador!")
            return True
            
        # Cambia de turno si no sacó par
        if not repetir_turno:
            self.cambiodeturno()
        return False
        
    def configurar_juego(self):
        """Configura el juego: modo, jugadores, colores, etc."""
        print("Configuración del juego:")
        
        # Configurar modo desarrollador
        modo = input("¿Quieres activar el modo desarrollador? (si/no): ").lower()
        self.modo_desarrollador = modo == "si"
        self.dados = Dados(self.modo_desarrollador)
        
        if self.modo_desarrollador:
            manual = input("¿Quieres forzar los valores de los dados? (si/no): ").lower()
            self.dados.forzar_manual = manual == "si"
            
        # Configurar número de jugadores
        try:
            num_jugadores = int(input("Número de jugadores (2-4): "))
            while num_jugadores < 2 or num_jugadores > 4:
                num_jugadores = int(input("Número inválido. Número de jugadores (2-4): "))
        except ValueError:
            print("Entrada inválida. Se usarán 2 jugadores por defecto.")
            num_jugadores = 2
            
        # Configurar jugadores
        colores_disponibles = ["rojo", "azul", "verde", "amarillo"]
        for i in range(num_jugadores):
            nombre = input(f"Nombre del jugador {i + 1}: ")
            print("Colores disponibles:", ", ".join(colores_disponibles))
            color = input("Elige un color: ").lower()
            while color not in colores_disponibles:
                color = input(f"Color no válido. Por favor elige un color entre {', '.join(colores_disponibles)}: ").lower()
            self.agregarjugador(nombre, color)
            colores_disponibles.remove(color)  # CORRECCIÓN: Eliminar el color elegido de la lista
            
        print("\n¡Juego configurado! Comencemos...")

    def jugar(self):
        """Ejecuta el juego completo."""
        if not self.jugadores:
            self.configurar_juego()
            
        juego_terminado = False
        while not juego_terminado:
            juego_terminado = self.jugarturno()
            
            if not juego_terminado:
                continuar = input("¿Quieres continuar jugando? (si/no): ").lower()
                if continuar == "no":
                    juego_terminado = True
                    print("Gracias por jugar, ¡hasta la próxima!")
                    break
                    
            if juego_terminado:
                ganador = self.jugadores[self.turnoact]
                print(f"¡Felicidades {ganador.nombre}, eres el ganador!")

def main():
    """Función principal para iniciar el juego."""
    juego = Juego()
    juego.jugar()

# Ejecutar el juego
if __name__ == "__main__":
    main()