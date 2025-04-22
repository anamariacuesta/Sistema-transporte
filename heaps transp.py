

from dataclasses import dataclass
from datetime import datetime
from DataStructs.List import arlt
from Utils.error import error_handler as err
from DataStructs.Trees.heap import new_heap, insert, delete_min, get_min, is_empty
from tabulate import tabulate

@dataclass
class Ruta:
    id: int
    nombre: str
    origen: str
    destino: str
    densidad_pasajeros: float
    retraso_acumulado: int
    importancia_conexion: float
    recursos_disponibles: int
    ultima_actualizacion: datetime

    def calcular_prioridad(self):
        FACTOR_DEMANDA = 10
        FACTOR_RETRASO = 5
        FACTOR_CONECTIVIDAD = 3
        FACTOR_RECURSOS = 2

        return (self.densidad_pasajeros * FACTOR_DEMANDA) + \
               (self.retraso_acumulado * FACTOR_RETRASO) + \
               (self.importancia_conexion * FACTOR_CONECTIVIDAD) - \
               (self.recursos_disponibles * FACTOR_RECURSOS)

class SistemaTransporte:
    def __init__(self):
        self.rutas = {}
        self.heap_rutas_criticas = new_heap(lambda r1, r2: -1 if r1.calcular_prioridad() > r2.calcular_prioridad() else (1 if r1.calcular_prioridad() < r2.calcular_prioridad() else 0)
)


    def agregar_ruta(self, ruta):
        self.rutas[ruta.id] = ruta
        insert(self.heap_rutas_criticas, ruta)

    def actualizar_ruta(self, id_ruta, **kwargs):
        if id_ruta not in self.rutas:
            return False

        ruta = self.rutas[id_ruta]

        # Actualizamos los atributos que se pasaron como kwargs
        for attr, value in kwargs.items():
            if hasattr(ruta, attr):
                setattr(ruta, attr, value)

        ruta.ultima_actualizacion = datetime.now()

        # Se reconstruye el heap excluyendo la ruta actualizada
        cmp_func = self.heap_rutas_criticas["cmp_function"]
        nueva_heap = new_heap(cmp_func)

        for i in range(self.heap_rutas_criticas["size"]):
            r = arlt.get_element(self.heap_rutas_criticas["elements"], i)
            if r is not None and r.id != id_ruta:
                insert(nueva_heap, r)

        # Se inserta la ruta actualizada nuevamente
        insert(nueva_heap, ruta)

        # Se reemplaza el heap antiguo
        self.heap_rutas_criticas = nueva_heap

        return True


    def obtener_ruta_mas_critica(self):
        if is_empty(self.heap_rutas_criticas):
            return None
        return get_min(self.heap_rutas_criticas)

    def procesar_ruta_critica(self):
        if is_empty(self.heap_rutas_criticas):
            return None
        return delete_min(self.heap_rutas_criticas)

    def simular_evento_trafico(self, id_ruta, retraso_adicional):
        if id_ruta in self.rutas:
            ruta = self.rutas[id_ruta]
            return self.actualizar_ruta(id_ruta, retraso_acumulado=ruta.retraso_acumulado + retraso_adicional)
        return False

    def generar_plan_optimizacion(self):
        plan = []
        copia = [arlt.get_element(self.heap_rutas_criticas["elements"], i)
                 for i in range(self.heap_rutas_criticas["size"])]
        copia.sort(key=lambda r: r.calcular_prioridad())

        for i in range(min(5, len(copia))):
            ruta = copia[i]
            accion = self._determinar_accion_optimizacion(ruta)
            plan.append((ruta, accion))

        return plan

    def _determinar_accion_optimizacion(self, ruta):
        if ruta.densidad_pasajeros > 0.8 and ruta.recursos_disponibles < 5:
            return "Aumentar frecuencia de vehículos"
        elif ruta.retraso_acumulado > 10:
            return "Implementar ruta express"
        elif ruta.importancia_conexion > 0.7 and ruta.retraso_acumulado > 5:
            return "Priorizar sincronización de conexiones"
        else:
            return "Monitoreo continuo"

# Demostración
def demostrar_sistema():
    sistema = SistemaTransporte()
    now = datetime.now()

    rutas = [
        Ruta(1, "Línea 1", "Terminal Norte", "Centro", 0.9, 8, 0.8, 3, now),
        Ruta(2, "Línea 2", "Centro", "Terminal Sur", 0.7, 3, 0.9, 4, now),
        Ruta(3, "Línea 3", "Terminal Este", "Terminal Oeste", 0.5, 12, 0.6, 2, now),
        Ruta(4, "Línea 4", "Plaza Central", "Aeropuerto", 0.8, 15, 0.9, 1, now),
        Ruta(5, "Línea 5", "Universidad", "Centro Comercial", 0.4, 2, 0.3, 5, now),
        Ruta(6, "Línea 6", "Barrio Norte", "Parque Industrial", 0.6, 7, 0.5, 3, now),
    ]

    for ruta in rutas:
        sistema.agregar_ruta(ruta)

    print("Estado inicial de las rutas:")
    for ruta in rutas:
        print(f"Ruta {ruta.nombre}: Prioridad = {ruta.calcular_prioridad():.2f}")

    print("\nRuta más crítica:")
    ruta_critica = sistema.obtener_ruta_mas_critica()
    print(f"ID: {ruta_critica.id}, Nombre: {ruta_critica.nombre}, Prioridad: {ruta_critica.calcular_prioridad():.2f}")

    print("\nSimulando accidente en la Línea 2...")
    sistema.simular_evento_trafico(2, 10)

    print("\nRuta más crítica después del evento:")
    ruta_critica = sistema.obtener_ruta_mas_critica()
    print(f"ID: {ruta_critica.id}, Nombre: {ruta_critica.nombre}, Prioridad: {ruta_critica.calcular_prioridad():.2f}")

    print("\nPlan de optimización generado:")
    plan = sistema.generar_plan_optimizacion()
    for ruta, accion in plan:
        print(f"Ruta {ruta.nombre} - Acción: {accion} - Prioridad: {ruta.calcular_prioridad():.2f}")

if __name__ == "__main__":
    demostrar_sistema()

def simular_dia_operativo():
    sistema = SistemaTransporte()
    now = datetime.now()

    # Inicializar rutas base
    rutas = [
        Ruta(1, "Línea 1", "Terminal Norte", "Centro", 0.7, 5, 0.6, 3, now),
        Ruta(2, "Línea 2", "Centro", "Terminal Sur", 0.5, 2, 0.8, 4, now),
        Ruta(3, "Línea 3", "Terminal Este", "Terminal Oeste", 0.6, 3, 0.5, 2, now),
        Ruta(4, "Línea 4", "Plaza Central", "Aeropuerto", 0.4, 1, 0.9, 2, now),
        Ruta(5, "Línea 5", "Universidad", "Centro Comercial", 0.3, 0, 0.3, 5, now),
        Ruta(6, "Línea 6", "Barrio Norte", "Parque Industrial", 0.6, 4, 0.5, 3, now),
    ]

    for ruta in rutas:
        sistema.agregar_ruta(ruta)

    eventos = [
        ("08:00", "hora pico", [(1, 0.9), (2, 0.85), (5, 0.8)]),  # aumenta densidad de pasajeros
        ("09:30", "accidente", [(3, 15)]),  # accidente en Línea 3
        ("11:00", "refuerzo", [(1, 5)]),  # se asignan más vehículos a Línea 1
        ("13:00", "evento", [(4, 0.75)]),  # aumento de densidad por evento cerca del aeropuerto
        ("15:00", "conectividad", [(2, 0.95)]),  # se vuelve más importante para conexión
        ("17:00", "hora pico", [(1, 0.95), (2, 0.9), (6, 0.85)]),
        ("19:00", "congestión", [(1, 8), (2, 5)]),  # aumentan los retrasos
        ("21:00", "desaceleración", [(1, 0.5), (2, 0.4), (5, 0.2)]),  # baja la densidad en la noche
    ]

    print("\n=== Simulación de un día operativo ===\n")
    for hora, tipo_evento, cambios in eventos:
        print(f"\n[{hora}] Evento: {tipo_evento}")
        for id_ruta, valor in cambios:
            if tipo_evento in ["hora pico", "evento", "desaceleración"]:
                sistema.actualizar_ruta(id_ruta, densidad_pasajeros=valor)
            elif tipo_evento == "accidente":
                sistema.simular_evento_trafico(id_ruta, valor)
            elif tipo_evento == "refuerzo":
                ruta = sistema.rutas[id_ruta]
                sistema.actualizar_ruta(id_ruta, recursos_disponibles=ruta.recursos_disponibles + valor)
            elif tipo_evento == "conectividad":
                sistema.actualizar_ruta(id_ruta, importancia_conexion=valor)
            elif tipo_evento == "congestión":
                sistema.simular_evento_trafico(id_ruta, valor)

        # Mostrar la ruta más crítica después de cada evento
        ruta_critica = sistema.obtener_ruta_mas_critica()
        if ruta_critica:
            print(f"Ruta más crítica: {ruta_critica.nombre} - Prioridad = {ruta_critica.calcular_prioridad():.2f}")

        # Mostrar plan de optimización tras evento
        plan = sistema.generar_plan_optimizacion()
        headers = ["Ruta", "Acción sugerida", "Prioridad"]
        tabla = [
            [ruta.nombre, accion, f"{ruta.calcular_prioridad():.2f}"]
            for ruta, accion in plan
        ]
        print(tabulate(tabla, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    # demostrar_sistema()
    simular_dia_operativo()
