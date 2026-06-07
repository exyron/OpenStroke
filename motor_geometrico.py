import math


class ReconocedorGestos:
    def __init__(self, num_puntos=64, tamano_cuadrado=250.0):
        self.num_puntos = num_puntos
        self.tamano_cuadrado = tamano_cuadrado

    def calcular_longitud(self, puntos):
        d = 0.0
        for i in range(1, len(puntos)):
            d += math.hypot(puntos[i][0] - puntos[i - 1][0], puntos[i][1] - puntos[i - 1][1])
        return d

    def remuestrear(self, puntos):
        if not puntos or len(puntos) < 2: return []
        I = self.calcular_longitud(puntos) / (self.num_puntos - 1)
        D = 0.0
        nuevos_puntos = [puntos[0]]
        puntos_temp = puntos.copy()
        i = 1

        while i < len(puntos_temp):
            p1 = puntos_temp[i - 1]
            p2 = puntos_temp[i]
            d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])

            if (D + d) >= I:
                qx = p1[0] + ((I - D) / d) * (p2[0] - p1[0])
                qy = p1[1] + ((I - D) / d) * (p2[1] - p1[1])
                q = [qx, qy]
                nuevos_puntos.append(q)
                puntos_temp.insert(i, q)
                D = 0.0
            else:
                D += d
            i += 1

        if len(nuevos_puntos) == self.num_puntos - 1:
            nuevos_puntos.append(puntos[-1])
        return nuevos_puntos[:self.num_puntos]

    def escalar(self, puntos):
        # 1. Buscamos los extremos del trazo
        min_x = min(p[0] for p in puntos)
        max_x = max(p[0] for p in puntos)
        min_y = min(p[1] for p in puntos)
        max_y = max(p[1] for p in puntos)

        # 2. Calculamos el ancho y alto del "cuadro" que contiene el gesto
        ancho = max(max_x - min_x, 1.0)  # Evitamos división por cero
        alto = max(max_y - min_y, 1.0)

        # 3. Escalamos todos los puntos para que quepan en un cuadro de 100x100
        # Esto hace que el tamaño relativo sea lo que importa, no el absoluto
        factor = 100.0 / max(ancho, alto)
        return [[p[0] * factor, p[1] * factor] for p in puntos]

    def trasladar_al_origen(self, puntos):
        # 1. Calculamos el centroide (el centro exacto de la forma)
        sum_x = sum(p[0] for p in puntos)
        sum_y = sum(p[1] for p in puntos)
        centroide_x = sum_x / len(puntos)
        centroide_y = sum_y / len(puntos)

        # 2. Restamos el centroide a cada punto para que el nuevo centro sea (0,0)
        return [[p[0] - centroide_x, p[1] - centroide_y] for p in puntos]

        # --- PEGA AQUÍ EL NUEVO MÉTODO ---
    def alinear_punto_inicio(self, puntos):
        # Calcula la distancia al origen para encontrar el punto más cercano al "centro"
        # o al eje X, ayudando a normalizar el inicio del trazo
        distancias = [math.hypot(p[0], p[1]) for p in puntos]
        indice_min = distancias.index(min(distancias))
        return puntos[indice_min:] + puntos[:indice_min]
    # ==========================================
    # NUEVA IA: LÓGICA DE FORMAS Y ÁNGULOS
    # ==========================================
    def calcular_proporcion(self, puntos):
        """Calcula si la forma es cuadrada, muy alargada o muy ancha."""
        if not puntos: return 1.0
        min_x = min(p[0] for p in puntos)
        max_x = max(p[0] for p in puntos)
        min_y = min(p[1] for p in puntos)
        max_y = max(p[1] for p in puntos)
        ancho = max_x - min_x
        alto = max_y - min_y
        if alto < 0.01: return 999.0  # Evita la división por cero en líneas horizontales
        return ancho / alto

    def calcular_indice_curvatura(self, puntos):
        """Diferencia líneas rectas (\\) de formas con esquinas (L) o curvas."""
        if len(puntos) < 2: return 1.0
        longitud_total = self.calcular_longitud(puntos)

        # Distancia en línea recta como el vuelo de un pájaro (Inicio a Fin)
        distancia_vuelo = math.hypot(puntos[-1][0] - puntos[0][0], puntos[-1][1] - puntos[0][1])

        if distancia_vuelo < 0.01: return longitud_total  # Para formas cerradas (como un círculo)
        return longitud_total / distancia_vuelo
    # ==========================================
    def procesar_trazo(self, puntos_crudos):
        if len(puntos_crudos) < 10: return []

        # 1. Túnel de lavado (Suavizado)
        puntos_limpios = self.optimizar_trazo(puntos_crudos)

        # 2. Normalización estándar
        p1 = self.remuestrear(puntos_limpios)
        p2 = self.escalar(p1)
        p3 = self.trasladar_al_origen(p2)

        # 3. NUEVA ALINEACIÓN DE INICIO (El paso crucial)
        p4 = self.alinear_punto_inicio(p3)

        return p4

    def calcular_distancia_trazo(self, trazo_dibujado, trazo_plantilla):
        # ANTES del bucle, miramos qué estamos comparando
        print(f"DEBUG: Comparando trazo[0] {trazo_dibujado[0]} con plantilla[0] {trazo_plantilla[0]}")
        if len(trazo_dibujado) != len(trazo_plantilla): return float('inf')

        # 1. Distancia Euclidiana Clásica (El algoritmo base)
        distancia_total = 0.0
        for i in range(len(trazo_dibujado)):
            distancia_total += math.hypot(trazo_dibujado[i][0] - trazo_plantilla[i][0],
                                          trazo_dibujado[i][1] - trazo_plantilla[i][1])
        distancia_base = distancia_total / len(trazo_dibujado)

        # ACTIVACIÓN DE LA INTELIGENCIA GEOMÉTRICA
        prop_dibujo = self.calcular_proporcion(trazo_dibujado)
        prop_plantilla = self.calcular_proporcion(trazo_plantilla)
        diferencia_proporcion = abs(prop_dibujo - prop_plantilla)

        curv_dibujo = self.calcular_indice_curvatura(trazo_dibujado)
        curv_plantilla = self.calcular_indice_curvatura(trazo_plantilla)
        diferencia_curvatura = abs(curv_dibujo - curv_plantilla)

        # RELAJAMOS EL CASTIGO (Modo Flexible)
        multiplicador_castigo = 1.0

        # Reducimos el peso de las esquinas y la proporción a la mitad
        multiplicador_castigo += (diferencia_curvatura * 1.25)
        if diferencia_proporcion < 100:
            multiplicador_castigo += (diferencia_proporcion * 0.25)

        return distancia_base * multiplicador_castigo

    def reconocer(self, puntos_crudos, diccionario_plantillas, umbral_porcentaje):

        # 1. Procesamos y vemos cuántos puntos quedan
        trazo_limpio = self.procesar_trazo(puntos_crudos)
        print(f"DEBUG: Tras procesado, el trazo tiene {len(trazo_limpio)} puntos")

        if not trazo_limpio or not diccionario_plantillas:
            return None, float('inf')

        mejor_coincidencia = None
        menor_distancia = float('inf')

        for nombre_plantilla, puntos_plantilla in diccionario_plantillas.items():
            distancia = self.calcular_distancia_trazo(trazo_limpio, puntos_plantilla)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_coincidencia = nombre_plantilla

        umbral_aceptacion = self.tamano_cuadrado * umbral_porcentaje
        if menor_distancia < umbral_aceptacion:
            return mejor_coincidencia, menor_distancia
        else:
            return None, menor_distancia

    def optimizar_trazo(self, puntos):
        """
        Fase 1: El Túnel de Lavado.
        Suaviza el trazo mediante una media móvil simple para eliminar jitter.
        """
        if len(puntos) < 3: return puntos

        suavizado = [puntos[0]]
        for i in range(1, len(puntos) - 1):
            # Calculamos la media entre el punto anterior, el actual y el siguiente
            x = (puntos[i - 1][0] + puntos[i][0] + puntos[i + 1][0]) / 3
            y = (puntos[i - 1][1] + puntos[i][1] + puntos[i + 1][1]) / 3
            suavizado.append([x, y])
        suavizado.append(puntos[-1])
        return suavizado