import math

from typing import Optional
from collections import deque

from persona import Persona
from cabina import Cabina
from calendario import Calendario
from simuladorVacunacion import SimuladorVacunacion


CONSTANTES = {
    "CABINAS": 10,
    "POBLACION_TOTAL": 180000,
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
    print("="*60)
    print("SIMULACIÓN DE CAMPAÑA DE VACUNACIÓN")
    print("="*60)

    # Inicializar calendario
    calendario = Calendario()
    calendario.inicializar_poblacion(CONSTANTES["POBLACION_TOTAL"])

    # Inicializar simulacion
    simulacion = SimuladorVacunacion(calendario,CONSTANTES)
  
    # Contadores Globales
    dia_global = 0
    semana = 0
    costo_total_campana = 0.0
    
    # Chequear si ya terminamos
    while calendario.total_vacunados() < CONSTANTES["POBLACION_TOTAL"]:
        semana +=1
        print(f"\n--- Semana {semana} ---")

        #Contadores Semanales 
        vacunados_semana = 0
        abandonos_semana = 0
        costo_semana = 0.0
        cola_max_semana = 0
        espera_total_semana = 0.0
        dias_operativos_semana = 0

        for nombre_dia in calendario.dias:
            dia_global += 1
            dias_operativos_semana += 1
            
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
            
            # 3. Acumular para el resumen SEMANAL
            vacunados_semana += stats_dia['vacunados']
            abandonos_semana += stats_dia['abandonos']
            costo_semana += stats_dia['costo_total_dia']
            cola_max_semana = max(cola_max_semana, stats_dia['cola_maxima'])
            espera_total_semana += stats_dia['tiempo_espera_total']
        
            # 4. Reportar resultados del día
            print(f"  Resultados: Vacunados: {stats_dia['vacunados']}, "
                  f"Abandonos: {stats_dia['abandonos']}, "
                  f"Cola Máx: {stats_dia['cola_maxima']}, "
                  f"Espera Prom: {stats_dia['tiempo_espera_promedio']:.2f} min, "
                  f"Costo: ${stats_dia['costo_total_dia']:,.2f}")
        
        # Reporte al final de la semana
        espera_prom_semana = 0.0
        if vacunados_semana > 0:
            # Calculamos el promedio ponderado de la semana
            espera_prom_semana = espera_total_semana / vacunados_semana
            
        print(f"\n--- Resumen Semana {semana} ---")
        print(f"  Días operativos: {dias_operativos_semana}")
        print(f"  Nuevos vacunados: {vacunados_semana}")
        print(f"  Nuevos abandonos: {abandonos_semana}")
        print(f"  Pico de cola semanal: {cola_max_semana} personas")
        print(f"  Espera prom. semanal: {espera_prom_semana:.2f} min")
        print(f"  Costo semanal: ${costo_semana:,.2f}")
        print(f"  Total acumulado: {calendario.total_vacunados()} / {CONSTANTES['POBLACION_TOTAL']}")

    # --- INICIO NUEVO RESUMEN FINAL ---
    print("\n" + "="*60)
    print("SIMULACIÓN FINALIZADA - RESUMEN TOTAL")
    print("="*60)
    
    # Corregimos los días si terminamos a mitad de semana
    dias_reales = dia_global - (len(calendario.dias) - dias_operativos_semana)
    
    print(f"  Tiempo total: {dias_reales} días ({semana} semanas)")
    print(f"  Población objetivo: {CONSTANTES['POBLACION_TOTAL']}")
    print(f"  Vacunados finales: {calendario.total_vacunados()}")
    print(f"  Costo total de la campaña: ${costo_total_campana:,.2f}")
    
    costo_prom_por_persona = 0.0
    if calendario.total_vacunados() > 0:
         costo_prom_por_persona = costo_total_campana / calendario.total_vacunados()
    print(f"  Costo promedio por vacunado: ${costo_prom_por_persona:,.2f}")
    # --- FIN NUEVO RESUMEN FINAL ---



    
