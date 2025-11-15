
from persona import Persona
from typing import Optional

class Cabina:

    def __init__(self, id_cabina: int):
        self.id = id_cabina
        self.ocupada = False
        self.persona_actual: Optional[Persona] = None
        self.tiempo_liberacion: Optional[float] = None
        self.personas_atendidas = 0
        self.tiempo_ocupacion_total = 0.0
    

    def limpiarCabina(self):
        self.ocupada = False
        self.persona_actual: Optional[Persona] = None
        self.tiempo_liberacion: Optional[float] = None
        self.personas_atendidas = 0
        self.tiempo_ocupacion_total = 0.0

    def estaLibre(self):
        return not self.ocupada

    def asignar(self, persona: Persona, tiempo_actual: float, tiempo_servicio: float):
        self.ocupada = True
        self.persona_actual = persona
        persona.tiempo_inicio_servicio = tiempo_actual
        self.tiempo_liberacion = tiempo_actual + tiempo_servicio
    
    def liberar(self, tiempo_actual: float) -> Persona:
        persona = self.persona_actual
        if persona:
            persona.tiempo_fin_servicio = tiempo_actual
            persona.vacunaciones+=1
            self.personas_atendidas += 1
            self.tiempo_ocupacion_total += (tiempo_actual - persona.tiempo_inicio_servicio)
        
        self.ocupada = False
        self.persona_actual = None
        self.tiempo_liberacion = None
        return persona


