import random
import math

from typing import Optional
from collections import deque

from persona import Persona
from cabina import Cabina
from calendario import Calendario
from simuladorVacunacion import SimuladorVacunacion


CONSTANTES = {
    "CABINAS": 5,
    "POBLACION_TOTAL": 10000,
    "TASA_LLEGADAS": 30,
    "TIEMPO_SERVICIO": 3,
    "HORAS_TRABAJO": 10,
    "TIEMPO_DIA": 10 * 60,
    "PROB_ABANDONO": 0.2,
    "TASA_ASISTENCIA": 0.8, 

    # La gente solo considerará abandonar si la cola es mayor a esto.
    "COLA_PACIENCIA": 50, 

    "COSTO_FIJO_CABINA": 55000,
    "COSTO_DOSIS": 2000,
    "COSTO_REPROG": 300,
    "COSTO_ESPERA": 3,
}


if __name__ == "__main__":
    random.seed(42)
    
    print("="*60)
    print("SIMULACIÓN DE CAMPAÑA DE VACUNACIÓN")
    print("="*60)

    # Inicializar calendario
    calendario = Calendario()
    calendario.inicializar_poblacion(CONSTANTES["POBLACION_TOTAL"])

    # Inicializar simulacion
    simulacion = SimuladorVacunacion(calendario,CONSTANTES)
  
    # Contadores
    dia_global = 0
    semana = 0
    costo_total_campana = 0.0
    
    # Chequear si ya terminamos
    while calendario.total_vacunados() < CONSTANTES["POBLACION_TOTAL"]:
        semana +=1
        print(f"\n--- Semana {semana} ---")

        for nombre_dia in calendario.dias:
            dia_global += 1
            
            # Chequeo por si terminamos a mitad de semana
            if calendario.total_vacunados() >= CONSTANTES["POBLACION_TOTAL"]:
                print(f"Día {dia_global} ({nombre_dia.capitalize()}): Campaña completada.")
                break
            
            print(f"Día {dia_global} ({nombre_dia.capitalize()}):")
            
            # 1. Preparar el día (mueve reprogramados de la semana anterior)
            calendario.preparar_dia_siguiente(nombre_dia)
            
            # 2. Simular el día y obtener estadísticas
            stats_dia = simulacion.simular_dia(nombre_dia)
            costo_total_campana += stats_dia['costo_total_dia']
            
            # 3. Reportar resultados del día ("lindo")
            print(f"  Resultados: Vacunados: {stats_dia['vacunados']}, "
                  f"Abandonos: {stats_dia['abandonos']}, "
                  f"Cola Máx: {stats_dia['cola_maxima']}, "
                  f"Espera Prom: {stats_dia['tiempo_espera_promedio']:.2f} min, "
                  f"Costo: ${stats_dia['costo_total_dia']:,.2f}")
        
        # Reporte al final de la semana
        print(f"--- Fin Semana {semana}: Total Vacunados {calendario.total_vacunados()} / {CONSTANTES["POBLACION_TOTAL"]} ---") 





    
