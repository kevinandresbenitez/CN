import math
import statistics  # <-- IMPORTANTE
from typing import Optional

from calendario import Calendario
from simuladorVacunacion import SimuladorVacunacion

CONSTANTES = {
    "CABINAS": 5,
    "POBLACION_TOTAL": 20000,
    "TASA_LLEGADAS": 30,
    "TIEMPO_SERVICIO": 3,
    "HORAS_TRABAJO": 10,
    "TIEMPO_DIA": 10 * 60,
    "PROB_ABANDONO": 0.2,
    "TASA_ASISTENCIA": 0.8, 


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
    calendario.inicializar_poblacion(CONSTANTES["POBLACION_TOTAL"], CONSTANTES["TASA_LLEGADAS"],CONSTANTES["TIEMPO_SERVICIO"])

    # Inicializar simulacion
    simulacion = SimuladorVacunacion(calendario,CONSTANTES)
  
    # --- Contadores Globales ---
    dia_global = 0
    semana = 0
    costo_total_campana = 0.0
    proximo_hito_porcentaje = 10
    
    total_abandonos_voluntarios = 0
    total_abandonos_cierre = 0
    total_vacunados_campana = 0
    lista_espera_global = []
    lista_servicio_global = []
    
    # Chequear si ya terminamos
    while calendario.total_vacunados() < CONSTANTES["POBLACION_TOTAL"]:
        semana +=1
        print(f"\n--- Semana {semana} ---")

        # --- Contadores Semanales  ---
        vacunados_semana = 0
        abandonos_voluntarios_semana = 0
        abandonos_cierre_semana = 0
        costo_semana = 0.0
        cola_max_semana = 0
        dias_operativos_semana = 0
        
        lista_espera_semana = []
        lista_servicio_semana = []

        #Bucle de semana
        for nombre_dia in calendario.dias:
            dia_global += 1
            
            # Chequeo por si terminamos a mitad de semana
            if calendario.total_vacunados() >= CONSTANTES["POBLACION_TOTAL"]:
                print(f"Día {dia_global} ({nombre_dia.capitalize()}): Campaña completada.")
                break
            
            dias_operativos_semana += 1
            print(f"Día {dia_global} ({nombre_dia.capitalize()}):")
            
            # 1. Preparar el día (mueve reprogramados de la semana anterior)
            calendario.preparar_dia_siguiente(nombre_dia)
            
            # 2. Simular el día y obtener estadísticas
            stats_dia = simulacion.simular_dia(nombre_dia)
            costo_total_campana += stats_dia['costo_total_dia']
            
            # 3. Acumular para el resumen SEMANAL
            vacunados_semana += stats_dia['vacunados']
            abandonos_voluntarios_semana += stats_dia['abandonos']
            abandonos_cierre_semana += stats_dia['reprogramados'] 
            costo_semana += stats_dia['costo_total_dia']
            cola_max_semana = max(cola_max_semana, stats_dia['cola_maxima'])
            
            # Acumulamos las listas para el reporte semanal
            lista_espera_semana.extend(stats_dia['tiempos_de_espera'])
            lista_servicio_semana.extend(stats_dia['tiempos_de_servicio'])
        
            # 4. Reportar resultados del día 
            print(f"  Resultados: Vacunados: {stats_dia['vacunados']}, "
                  f"Abandonos: {stats_dia['abandonos']}, "
                  f"Reprogramados al cierre: {stats_dia['reprogramados']}, "
                  f"Tasa de Abandono: {stats_dia['tasa_abandono']:.1f}%  Tasa de Reprogramados: {stats_dia['tasa_reprogramados']:.1f}%")
            
            print(f"    Cola:     Max: {stats_dia['cola_maxima']}, Min: {stats_dia['cola_minima']}")
            
            print(f"    Espera:   Prom: {stats_dia['espera_prom']:.2f} min, "
                  f"Max: {stats_dia['espera_max']:.2f} min, "
                  f"Min: {stats_dia['espera_min']:.2f} min")
            
            print(f"    Servicio: Prom: {stats_dia['servicio_prom']:.2f} min, "
                  f"Max: {stats_dia['servicio_max']:.2f} min, "
                  f"Min: {stats_dia['servicio_min']:.2f} min")

            print(f"    Costo: ${stats_dia['costo_total_dia']:,.2f}")
            
            
            #Mostrar hitos
            porcentaje_actual = (calendario.total_vacunados() / CONSTANTES["POBLACION_TOTAL"]) * 100
            if(porcentaje_actual >= proximo_hito_porcentaje):
                print(f"  >>> HITO: Se superó el {proximo_hito_porcentaje}% de la población el Día {dia_global} (Semana {semana})")
                proximo_hito_porcentaje +=10
        
        # --- Reporte al final de la semana (NUEVO) ---
        
        # --- Cálculo de estadísticas semanales (con las listas) ---
        espera_prom_semana = 0.0
        espera_max_semana = 0.0
        espera_min_semana = 0.0
        servicio_prom_semana = 0.0
        servicio_max_semana = 0.0
        servicio_min_semana = 0.0
        tasa_abandono_semana = 0.0
        
        abandonos_totales_semana = abandonos_voluntarios_semana + abandonos_cierre_semana
        denominador_tasa_semana = abandonos_totales_semana + vacunados_semana
        
        tasa_abandono_semana = 0.0
        tasa_reprogramados_semana = 0.0

        if denominador_tasa_semana > 0:
            tasa_abandono_semana = (abandonos_voluntarios_semana / denominador_tasa_semana) * 100
            tasa_reprogramados_semana = (abandonos_cierre_semana / denominador_tasa_semana) * 100

        if vacunados_semana > 0:
            espera_prom_semana = statistics.mean(lista_espera_semana)
            espera_max_semana = max(lista_espera_semana)
            espera_min_semana = min(lista_espera_semana)
            
            servicio_prom_semana = statistics.mean(lista_servicio_semana)
            servicio_max_semana = max(lista_servicio_semana)
            servicio_min_semana = min(lista_servicio_semana)

        # --- Acumuladores globales ---
        total_abandonos_voluntarios += abandonos_voluntarios_semana
        total_abandonos_cierre += abandonos_cierre_semana
        total_vacunados_campana += vacunados_semana
        lista_espera_global.extend(lista_espera_semana)
        lista_servicio_global.extend(lista_servicio_semana)
            
        # --- Impresión del resumen semanal ---
        print(f"\n--- Resumen Semana {semana} ---")
        print(f"  Días operativos: {dias_operativos_semana}")
        print(f"  Nuevos vacunados: {vacunados_semana}")
        print(f"  Abandonos (Voluntarios): {abandonos_voluntarios_semana}")
        print(f"  Abandonos (Cierre): {abandonos_cierre_semana}")
        print(f"  Tasa Abandono Semanal: {tasa_abandono_semana:.1f}%")
        print(f"  Tasa Reprogramados Semanal: {tasa_reprogramados_semana:.1f}%")
        print(f"  Pico de cola semanal: {cola_max_semana} personas")
        print(f"  Espera prom. semanal: {espera_prom_semana:.2f} min (Max: {espera_max_semana:.2f}, Min: {espera_min_semana:.2f})")
        print(f"  Servicio prom. semanal: {servicio_prom_semana:.2f} min (Max: {servicio_max_semana:.2f}, Min: {servicio_min_semana:.2f})")
        print(f"  Costo semanal: ${costo_semana:,.2f}")
        print(f"  Total acumulado: {calendario.total_vacunados()} / {CONSTANTES['POBLACION_TOTAL']}")

    # --- Reporte final de la simulacion ---
    print("\n" + "="*60)
    print("SIMULACIÓN FINALIZADA - RESUMEN TOTAL")
    print("="*60)
    
    # Corregimos los días si terminamos a mitad de semana
    dias_reales = dia_global - (len(calendario.dias) - dias_operativos_semana)
    
    print(f"  Tiempo total: {dias_reales} días ({semana} semanas)")
    print(f"  Cantidad de cabinas utilizadas: {CONSTANTES['CABINAS']}")
    print(f"  Población objetivo: {CONSTANTES['POBLACION_TOTAL']}")
    print(f"  Vacunados finales: {calendario.total_vacunados()}")
    
    # --- Reporte Final Detallado (NUEVO) ---
    print(f"  Abandonos Voluntarios Totales: {total_abandonos_voluntarios}")
    print(f"  Abandonos por Cierre Totales: {total_abandonos_cierre}")

    # --- Cálculo de estadísticas globales ---
    espera_prom_global = 0.0
    espera_max_global = 0.0
    espera_min_global = 0.0
    servicio_prom_global = 0.0
    servicio_max_global = 0.0
    servicio_min_global = 0.0
    tasa_abandono_global = 0.0
    
    abandonos_globales = total_abandonos_voluntarios + total_abandonos_cierre
    denominador_tasa_global = abandonos_globales + total_vacunados_campana

    tasa_abandono_global = 0.0
    tasa_reprogramados_global = 0.0

    if denominador_tasa_global > 0:
            tasa_abandono_global = (total_abandonos_voluntarios / denominador_tasa_global) * 100
            tasa_reprogramados_global = (total_abandonos_cierre / denominador_tasa_global) * 100
    
    if total_vacunados_campana > 0:
        espera_prom_global = statistics.mean(lista_espera_global)
        espera_max_global = max(lista_espera_global)
        espera_min_global = min(lista_espera_global)
        
        servicio_prom_global = statistics.mean(lista_servicio_global)
        servicio_max_global = max(lista_servicio_global)
        servicio_min_global = min(lista_servicio_global)

    
    print(f"  Tasa de Abandono Total: {tasa_abandono_global:.2f}%")
    print(f"  Tasa de Reprogramados Total: {tasa_reprogramados_global:.2f}%")
    print(f"  Estadísticas de Espera (Global):")
    print(f"    Promedio: {espera_prom_global:.2f} min")
    print(f"    Máxima:   {espera_max_global:.2f} min")
    print(f"    Mínima:   {espera_min_global:.2f} min")
    print(f"  Estadísticas de Servicio (Global):")
    print(f"    Promedio: {servicio_prom_global:.2f} min")
    print(f"    Máxima:   {servicio_max_global:.2f} min")
    print(f"    Mínima:   {servicio_min_global:.2f} min")

    print(f"  Costo total de la campaña: ${costo_total_campana:,.2f}")
    
    costo_prom_por_persona = 0.0
    if calendario.total_vacunados() > 0:
         costo_prom_por_persona = costo_total_campana / calendario.total_vacunados()
    print(f"  Costo promedio por vacunado: ${costo_prom_por_persona:,.2f}")