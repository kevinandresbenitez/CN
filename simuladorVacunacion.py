import random
import math
import heapq
from collections import deque
from typing import List, Optional, Dict, Any, Tuple

from persona import Persona
from calendario import Calendario
from cabina import Cabina

class SimuladorVacunacion:

    def __init__(self, calendario: Calendario, constantes: Dict[str, Any]):
        self.num_cabinas = constantes['CABINAS']
        self.calendario = calendario
        self.cabinas: List[Cabina] = [Cabina(i) for i in range(self.num_cabinas)]
        self.cola: deque[Persona] = deque()
        self.tiempo_actual: float = 0.0
        self.cola_eventos: List[Tuple[float, str, Any]] = []
        
        self.TASA_LLEGADAS = constantes['TASA_LLEGADAS']
        self.TIEMPO_SERVICIO = constantes['TIEMPO_SERVICIO']
        self.TIEMPO_DIA = constantes['TIEMPO_DIA']
        self.PROB_ABANDONO = constantes['PROB_ABANDONO']
        self.TASA_ASISTENCIA = constantes['TASA_ASISTENCIA']
        self.COSTOS = {
            "FIJO_CABINA": constantes['COSTO_FIJO_CABINA'],
            "DOSIS": constantes['COSTO_DOSIS'],
            "REPROG": constantes['COSTO_REPROG'],
            "ESPERA": constantes['COSTO_ESPERA'],
        }

        self.estadisticas: Dict[str, Any] = {}

        # Agrego esto para fijar secuencia aleatoria
        self.rand_asistencia = random.Random(42)
        self.rand_abandono = random.Random(45)


    def _buscar_cabina_libre(self) -> Optional[Cabina]:
        for cabina in self.cabinas:
            if cabina.estaLibre():
                return cabina
        return None


    def _programar_evento(self, tiempo: float, tipo: str, data: Any):
        heapq.heappush(self.cola_eventos, (tiempo, tipo, data))

    def _procesar_evento_llegada(self, persona: Persona, nombre_dia: str):
        cabina_libre = self._buscar_cabina_libre()
        
        if cabina_libre:
            cabina_libre.asignar(persona, self.tiempo_actual, persona.tiempo_servicio)

            # Programamos su futuro evento de salida
            if cabina_libre.tiempo_liberacion is not None:
                self._programar_evento(cabina_libre.tiempo_liberacion, "SALIDA", cabina_libre)
        else:

            # Estimar tiempo de espera de persona
            tiempo_espera_estimado = (len(self.cola) * self.TIEMPO_SERVICIO) / self.num_cabinas
            TIEMPO_MAX_TOLERADO = 150


            # No hay cabinas. La persona mira la cola y decide.
            if tiempo_espera_estimado > TIEMPO_MAX_TOLERADO and self.rand_abandono.random() < self.PROB_ABANDONO:
                # Abandona
                persona.abandono = True
                self.estadisticas['abandonos'] += 1
                self.calendario.registrar_reprogramado(persona, nombre_dia)
            else:
                # Se une a la cola 
                self.cola.append(persona)
                self.estadisticas['cola_maxima'] = max(self.estadisticas['cola_maxima'], len(self.cola))

    def _procesar_evento_salida(self, cabina: Cabina, nombre_dia: str):
     
        # Liberar la cabina y obtener la persona
        persona_vacunada = cabina.liberar(self.tiempo_actual)
        
        # Registrar estadísticas
        self.estadisticas['vacunados'] += 1
        self.estadisticas['tiempo_espera_total'] += persona_vacunada.tiempo_espera()
        self.estadisticas['tiempo_sistema_total'] += persona_vacunada.tiempo_sistema()
        
        # Informar al calendario que la persona se vacunó
        self.calendario.registrar_vacunado(persona_vacunada, nombre_dia)
        
        # Llamar al siguiente en la cola (si hay)
        if self.cola:
            siguiente_persona = self.cola.popleft()
            cabina.asignar(siguiente_persona, self.tiempo_actual, siguiente_persona.tiempo_servicio)
            
            if cabina.tiempo_liberacion is not None:
                self._programar_evento(cabina.tiempo_liberacion, "SALIDA", cabina)

    def simular_dia(self, nombre_dia: str) -> Dict[str, Any]:
        
        self.tiempo_actual = 0.0
        self.cola.clear()
        self.cola_eventos = []
        for cabina in self.cabinas:
            cabina.limpiarCabina() 
        
        self.estadisticas = {
            'llegadas_atendidas': 0, 'abandonos': 0, 'vacunados': 0,
            'cola_maxima': 0, 'tiempo_espera_total': 0.0, 'tiempo_sistema_total': 0.0, 'reprogramados':0
        }
        
        pacientes_potenciales_hoy = list(self.calendario.obtener_pacientes_para_hoy(nombre_dia))
        tiempo_prox_llegada = 0.0

        for persona in pacientes_potenciales_hoy:
            
            # Cada persona tiene una probabilidad de asistir
            if self.rand_asistencia.random() < self.TASA_ASISTENCIA:
                tiempo_prox_llegada += persona.tiempo_entre_llegada

                #Termina el dia
                if tiempo_prox_llegada > self.TIEMPO_DIA:
                    break 
            
                persona.tiempo_llegada = tiempo_prox_llegada
                self._programar_evento(tiempo_prox_llegada, "LLEGADA", persona)
            else:
                # No asiste. Se queda en la lista 'sinVacunar' para
                # la próxima semana.
                pass
        
        # Simulación de Eventos 
        while self.cola_eventos:
            (tiempo, tipo_evento, data) = heapq.heappop(self.cola_eventos)
            self.tiempo_actual = tiempo

             # Si finalizo el dia
            if tiempo > self.TIEMPO_DIA:
                heapq.heappush(self.cola_eventos, (tiempo, tipo_evento, data))
                break    

            if tipo_evento == "LLEGADA":
                self.estadisticas['llegadas_atendidas'] += 1
                self._procesar_evento_llegada(data, nombre_dia)
            elif tipo_evento == "SALIDA":
                self._procesar_evento_salida(data, nombre_dia)



        
        #  Fin del Día reprogramar personas de la cola 
        if self.cola:
            self.estadisticas['reprogramados'] += len(self.cola)
            for persona in self.cola:
                self.calendario.registrar_reprogramado(persona, nombre_dia)
            self.cola.clear()
        
        costo_fijo = self.COSTOS['FIJO_CABINA'] * self.num_cabinas
        costo_dosis = self.estadisticas['vacunados'] * self.COSTOS['DOSIS']
        costo_reprog = self.estadisticas['abandonos'] * self.COSTOS['REPROG']
        costo_espera = self.estadisticas['tiempo_espera_total'] * self.COSTOS['ESPERA']
        self.estadisticas['costo_total_dia'] = costo_fijo + costo_dosis + costo_reprog + costo_espera
        
        if self.estadisticas['vacunados'] > 0:
            self.estadisticas['tiempo_espera_promedio'] = self.estadisticas['tiempo_espera_total'] / self.estadisticas['vacunados']
            self.estadisticas['costo_por_vacunado'] = self.estadisticas['costo_total_dia'] / self.estadisticas['vacunados']
        else:
            self.estadisticas['tiempo_espera_promedio'] = 0.0
            self.estadisticas['costo_por_vacunado'] = 0.0
            
        return self.estadisticas