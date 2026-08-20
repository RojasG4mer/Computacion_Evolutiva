import os
from core import AlgoritmoGenetico
import operadores as op
import visualizacion as vis

carpeta_reportes = "Reportes_Automaticos"
if not os.path.exists(carpeta_reportes):
    os.makedirs(carpeta_reportes)

# ==========================================
# Parametros iniciales
# ==========================================
N_BITS = 24       
TAMANO_POBLACION = 10   
GENERACIONES = 100
PROB_MUTACION = 0.2

METODO_APTITUD = "de_jong_1" 
INTERVALO = (-10, 10)
funcion_matematica_pura = op.APTITUD[METODO_APTITUD]

# Minimiza y maximiza:


def funcion_fitness(valores):
    # valores de la Funcion original
    resultado_crudo = funcion_matematica_pura(valores)
    # Inverso es minimo, normal es maximo
    aptitud = 1.0 / (resultado_crudo + 1e-6)
    return aptitud

# ¡Nota el "_2d" en las codificaciones!
lista_codificacion = ["binario_2d"]
lista_seleccion = ["boltzmann"] 
lista_cruza = ["un_punto"]
lista_mutacion = ["un_bit"]

total_combinaciones = len(lista_codificacion) * len(lista_seleccion) * len(lista_cruza) * len(lista_mutacion)
print(f"Generando {total_combinaciones} reportes en 3D...\n")

contador = 1

for cod in lista_codificacion:
    for sel in lista_seleccion:
        for cru in lista_cruza:
            for mut in lista_mutacion:
                print(f"Ejecutando [{contador}/{total_combinaciones}]: {cod} | {sel} | {cru} | {mut}")
                
                app = AlgoritmoGenetico(
                    n_bits = N_BITS,
                    intervalo = INTERVALO,
                    tamano_poblacion = TAMANO_POBLACION,
                    generaciones_totales = GENERACIONES,
                    probabilidad_mutacion = PROB_MUTACION,
                    funcion_aptitud = funcion_fitness,
                    funcion_decodificacion = op.CODIFICACION[cod],
                    funcion_seleccion = op.SELECCION[sel],
                    funcion_cruza = op.CRUZA[cru],
                    funcion_mutacion = op.MUTACION[mut]
                )
                
                historial_completo, log_texto = app.ejecutar()
                
                diccionario_config = {
                    "Aptitud 3D": METODO_APTITUD,
                    "Codificación": cod,
                    "Selección": sel,
                    "Cruza": cru,
                    "Mutación": mut
                }
                
                nombre_pdf = f"{carpeta_reportes}/MIN_{cod}_{sel}_{cru}_{mut}.pdf"
                
                vis.generar_reporte_completo_pdf(
                    historial_pob = historial_completo,
                    log_texto = log_texto,
                    configuracion = diccionario_config,
                    funcion_raw = funcion_matematica_pura,
                    intervalo = INTERVALO,
                    titulo_base = f"Boltzman 2 - {cod.upper()}",
                    nombre_archivo = nombre_pdf
                )
                contador += 1

print("\n¡PROCESO FINALIZADO!")