from dataclasses import dataclass
from typing import Optional
@dataclass
class Persona:
    dni: int
    vacunaciones: int = 0
    abandono: bool = False

    tiempo_llegada: Optional[float] = None
    tiempo_inicio_servicio: Optional[float] = None
    tiempo_fin_servicio: Optional[float] = None
    
    tiempo_servicio:int = None
    tiempo_entre_llegada:int = None

    def tiempo_espera(self) -> float:
        if self.tiempo_inicio_servicio is not None:
            return max(0.0, self.tiempo_inicio_servicio - self.tiempo_llegada)
        return 0
    
    def tiempo_sistema(self) -> float:
        if self.tiempo_fin_servicio is not None:
            return self.tiempo_fin_servicio - self.tiempo_llegada
        return 0