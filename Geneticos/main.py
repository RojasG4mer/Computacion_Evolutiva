from core import AlgoritmoGenetico
import operadores as op
import visualizacion as vis

# ==========================================
# 1. PANEL DE CONFIGURACIÓN (TIPO APP)
# ==========================================
METODO_CODIFICACION = "gray"      # ¡Aquí eliges "binario" o "gray"!
METODO_APTITUD      = "polinomial"
METODO_SELECCION    = "ruleta" 
METODO_CRUZA        = "un_punto"
METODO_MUTACION     = "un_bit"

# ==========================================
# 2. INSTANCIACIÓN DEL ALGORITMO
# ==========================================
print("==================================================")
print(f" INICIANDO ALGORITMO GENÉTICO ")
print(f" Conf: {METODO_CODIFICACION.upper()} | {METODO_SELECCION} | {METODO_CRUZA} | {METODO_MUTACION}")
print("==================================================\n")

app_genetica = AlgoritmoGenetico(
    n_bits = 6, #[cite: 1]
    intervalo = (0, 63), #[cite: 1]
    tamano_poblacion = 6, #[cite: 1]
    generaciones_totales = 3, #[cite: 1]
    probabilidad_mutacion = 0.15, #[cite: 1]
    
    # Inyección de módulos:
    funcion_aptitud = op.APTITUD[METODO_APTITUD],
    
    # --- AQUÍ INYECTAMOS LA CODIFICACIÓN DINÁMICA ---
    funcion_decodificacion = op.CODIFICACION[METODO_CODIFICACION], 
    
    funcion_seleccion = op.SELECCION[METODO_SELECCION],
    funcion_cruza = op.CRUZA[METODO_CRUZA],
    funcion_mutacion = op.MUTACION[METODO_MUTACION]
)

# ==========================================
# 3. EJECUCIÓN Y RESULTADOS
# ==========================================
# Ahora recibimos dos variables de la app
historial_resultados, registro_texto = app_genetica.ejecutar()

titulo_reporte = f"Reporte AG - {METODO_CODIFICACION.capitalize()} | {METODO_SELECCION.capitalize()}"
nombre_pdf = f"reporte_{METODO_CODIFICACION}_{METODO_SELECCION}.pdf"

# Le mandamos ambas cosas a nuestro visualizador
vis.generar_reporte_completo_pdf(
    historial=historial_resultados,
    log_texto=registro_texto,       # <--- Añadimos el texto
    titulo_base=titulo_reporte,
    nombre_archivo=nombre_pdf
)

print(f"\n¡Se ha generado el documento '{nombre_pdf}'!")