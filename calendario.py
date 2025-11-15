


from persona import Persona
import random

class Calendario:

    DIA_ACTUAL:int = 0

    def __init__(self):
        self.dias:dict[str, dict[str, list[Persona]]] = {
                    "lunes": {"sinVacunar": [], "vacunados": [], "reprogramados": []},
                    "martes": {"sinVacunar": [], "vacunados": [], "reprogramados": []},
                    "miercoles": {"sinVacunar": [], "vacunados": [], "reprogramados": []},
                    "jueves": {"sinVacunar": [], "vacunados": [], "reprogramados": []},
                    "viernes": {"sinVacunar": [], "vacunados": [], "reprogramados": []}
        }

    def inicializar_poblacion(self, total_personas:int):
        """
        Crea las instancias de Persona y las distribuye en la lista 'sinVacunar'
        de cada día de forma equitativa.
        """
        num_dias = len(self.dias)
        lista_dnis = random.sample(range(10_000_000, 50_000_000), total_personas)

        mapeo_dias = {
            0: "lunes",
            1: "lunes",
            2: "martes",
            3: "martes",
            4: "miercoles",
            5: "miercoles",
            6: "jueves",
            7: "jueves",
            8: "viernes",
            9: "viernes"
        }

        for dni in lista_dnis:
            ultimo_digito = dni % 10
            dia_asignado = mapeo_dias[ultimo_digito]
            persona = Persona(dni=dni, tiempo_llegada=0.0)
            self.dias[dia_asignado]["sinVacunar"].append(persona)

        print("Población Inicializada")
        print("Personas asignadas:")
        print("lunes: " + str(len(self.dias["lunes"]["sinVacunar"])))
        print("martes: " + str(len(self.dias["martes"]["sinVacunar"])))
        print("miercoles: " + str(len(self.dias["miercoles"]["sinVacunar"])))
        print("jueves: " + str(len(self.dias["jueves"]["sinVacunar"])))
        print("viernes: " + str(len(self.dias["viernes"]["sinVacunar"])))
        print("="*60)
        
    def preparar_dia_siguiente(self, nombre_dia):
        lista_repro = self.dias[nombre_dia]["reprogramados"]
        lista_sin_vacunar = self.dias[nombre_dia]["sinVacunar"]
        if lista_repro:
            lista_sin_vacunar.extend(lista_repro)
            self.dias[nombre_dia]["reprogramados"] = []

    def obtener_pacientes_para_hoy(self, nombre_dia):
        return self.dias[nombre_dia]["sinVacunar"]

    def registrar_vacunado(self, persona: Persona, nombre_dia: str):
        try:
            self.dias[nombre_dia]["sinVacunar"].remove(persona)
            self.dias[nombre_dia]["vacunados"].append(persona)
        except ValueError:
            print(f"ADVERTENCIA: Persona {persona.dni} no estaba en 'sinVacunar' de {nombre_dia} para ser vacunada.")

    def registrar_reprogramado(self, persona: Persona, nombre_dia: str):
        try:
            self.dias[nombre_dia]["sinVacunar"].remove(persona)
            self.dias[nombre_dia]["reprogramados"].append(persona)
        except ValueError:
            print(f"ADVERTENCIA: Persona {persona.dni} no estaba en 'sinVacunar' de {nombre_dia} para ser reprogramada.")
      
    def total_vacunados(self):
        total = 0
        for dia in self.dias:
            total += len(self.dias[dia]["vacunados"])
        return total