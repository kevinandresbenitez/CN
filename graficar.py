import pandas as pd
import matplotlib.pyplot as plt

print("Generando gráficos desde 'reporte_simulacion.csv'...")

# Cargar los datos desde el CSV
try:
    datos = pd.read_csv("reporte_simulacion.csv")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'reporte_simulacion.csv'")
    print("Asegúrate de correr 'main.py' primero.")
    exit()

# --- 1. Gráfico: Vacunados Acumulados vs. Tiempo ---
plt.figure(figsize=(12, 6))
plt.plot(datos['dia_global'], datos['vacunados_acumulados'], label='Vacunados Acumulados')
plt.title('Vacunados Acumulados vs. Tiempo')
plt.xlabel('Día de la Campaña')
plt.ylabel('Total de Vacunados')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('grafico_vacunados_acumulados.png')
print("Gráfico 'vacunados_acumulados.png' guardado.")

# --- 2. Gráfico: Cola Máxima Diaria vs. Tiempo ---
plt.figure(figsize=(12, 6))
plt.plot(datos['dia_global'], datos['cola_maxima'], label='Cola Máxima Diaria', color='orange')
plt.title('Tamaño Máximo de la Cola vs. Tiempo')
plt.xlabel('Día de la Campaña')
plt.ylabel('Personas en Cola')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('grafico_cola_maxima.png')
print("Gráfico 'cola_maxima.png' guardado.")

# --- 3. Gráfico: Ocupación Diaria de Puestos ---
plt.figure(figsize=(12, 6))
plt.bar(datos['dia_global'], datos['ocupacion_prom_diaria'], label='Ocupación Diaria', color='green')
plt.title('Ocupación Promedio de Cabinas vs. Tiempo')
plt.xlabel('Día de la Campaña')
plt.ylabel('Ocupación Promedio (%)')
plt.axhline(y=100, color='red', linestyle='--', label='Capacidad Máxima (100%)')
plt.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('grafico_ocupacion_diaria.png')
print("Gráfico 'ocupacion_diaria.png' guardado.")

print("\n¡Gráficos generados exitosamente!")
# plt.show() # Descomentá esta línea si querés que los gráficos se muestren en pantalla