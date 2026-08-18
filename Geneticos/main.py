import os
from core import AlgoritmoGenetico
import operadores as op
import visualizacion as vis

carpeta_reportes = "Reportes_Automaticos"
if not os.path.exists(carpeta_reportes):
    os.makedirs(carpeta_reportes)

# ==========================================
# CONFIGURACIÓN DEL EXPERIMENTO (X, Y)
# ==========================================
N_BITS = 24             # ¡24 Bits! -> 12 bits para X y 12 bits para Y
TAMANO_POBLACION = 10   
GENERACIONES = 100      # 100 Generaciones (El PDF generará brincos de 10 en 10 automáticamente)
PROB_MUTACION = 0.15

METODO_APTITUD = "rastrigin" # Prueba "de_jong_1" o "rastrigin" (ambos son excelentes en 3D)
INTERVALO = (-5.12, 5.12)
funcion_matematica_pura = op.APTITUD[METODO_APTITUD]

# Envolvemos la función para invertirla hacia maximización del GA
def funcion_fitness(valores):
    # 'valores' trae la tupla (x, y) lista
    return op.minimizacion_fmin_inverso(funcion_matematica_pura(valores), f_min_t=0.0)

# ¡Nota el "_2d" en las codificaciones!
lista_codificacion = ["binario_2d", "gray_2d"]
lista_seleccion = ["ruleta", "torneo"] 
lista_cruza = ["un_punto", "uniforme"]
lista_mutacion = ["un_bit", "multiple"]

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
                
                nombre_pdf = f"{carpeta_reportes}/AG_3D_{cod}_{sel}_{cru}_{mut}.pdf"
                
                vis.generar_reporte_completo_pdf(
                    historial_pob = historial_completo,
                    log_texto = log_texto,
                    configuracion = diccionario_config,
                    funcion_raw = funcion_matematica_pura,
                    intervalo = INTERVALO,
                    titulo_base = f"Reporte AG 3D - {cod.upper()}",
                    nombre_archivo = nombre_pdf
                )
                contador += 1

print("\n¡PROCESO FINALIZADO!")