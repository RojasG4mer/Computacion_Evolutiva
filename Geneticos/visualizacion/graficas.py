import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd


def configurar_estilo():
    """Configura un estilo limpio y formal, excelente para reportes científicos."""
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'legend.fontsize': 10,
        'figure.dpi': 300,        # Alta resolución para exportar a PDF/LaTeX
        'savefig.bbox': 'tight'   # Evita que se corten los bordes al guardar
    })

def graficar_evolucion(historial, titulo="Evolución de la Aptitud", nombre_archivo="evolucion.png"):
    """
    Grafica cómo mejora la aptitud a lo largo de las generaciones.
    """
    configurar_estilo()
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Extraer las aptitudes del historial
    aptitudes = [gen['aptitud'] for gen in historial]
    generaciones = list(range(1, len(aptitudes) + 1))
    
    # Crear la gráfica
    ax.plot(generaciones, aptitudes, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label='Mejor Aptitud')
    
    # Línea punteada de aptitud (como lo pide tu instrucción)
    aptitud_max = max(aptitudes)
    ax.axhline(y=aptitud_max, color='r', linestyle='--', alpha=0.6, label=f'Aptitud Máxima ({aptitud_max:.2f})')
    
    ax.set_title(titulo)
    ax.set_xlabel("Generación")
    ax.set_ylabel("Aptitud")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    
    # Guardar automáticamente la imagen
    plt.savefig(nombre_archivo)
    plt.show()

def graficar_comparativa_algoritmos(diccionario_historiales, titulo="Comparativa de Algoritmos"):
    """
    Ideal para comparar Cauchy, Lineal y Polinomial en la misma gráfica.
    Recibe un diccionario: {"Polinomial": historial1, "Cauchy": historial2}
    """
    configurar_estilo()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for nombre_algoritmo, historial in diccionario_historiales.items():
        aptitudes = [gen['aptitud'] for gen in historial]
        ax.plot(aptitudes, marker='.', linestyle='-', linewidth=2, label=nombre_algoritmo)
        
    ax.set_title(titulo)
    ax.set_xlabel("Generación")
    ax.set_ylabel("Mejor Aptitud")
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()
    
    plt.savefig("comparativa_algoritmos.png")
    plt.show()

def generar_reporte_completo_pdf(historial, log_texto, titulo_base="Reporte de Algoritmo Genético", nombre_archivo="reporte_completo.pdf"):
    df = pd.DataFrame(historial)
    df.index = df.index + 1
    df.index.name = "Generación"
    
    df_tabla = df.copy()
    df_tabla['decimal'] = df_tabla['decimal'].round(4)
    df_tabla['aptitud'] = df_tabla['aptitud'].round(4)
    
    with PdfPages(nombre_archivo) as pdf:
        
        # --- PÁGINA 1: LA GRÁFICA DE EVOLUCIÓN ---
        fig_graf, ax_graf = plt.subplots(figsize=(8, 5))
        ax_graf.plot(df.index, df['aptitud'], marker='o', linestyle='-', color='#1f77b4', linewidth=2)
        aptitud_max = df['aptitud'].max()
        ax_graf.axhline(y=aptitud_max, color='r', linestyle='--', alpha=0.6, label=f'Máxima ({aptitud_max:.2f})')
        ax_graf.set_title(f"{titulo_base} - Evolución", weight='bold')
        ax_graf.set_xlabel("Generación")
        ax_graf.set_ylabel("Mejor Aptitud")
        ax_graf.grid(True, linestyle=':', alpha=0.7)
        ax_graf.legend()
        pdf.savefig(fig_graf, bbox_inches='tight')
        plt.close(fig_graf)
        
        # --- PÁGINA 2: LA TABLA RESUMEN ---
        alto_figura = max(4, len(df_tabla) * 0.4)
        fig_tab, ax_tab = plt.subplots(figsize=(8, alto_figura))
        ax_tab.axis('tight')
        ax_tab.axis('off')
        ax_tab.set_title(f"{titulo_base} - Tabla de Resultados", weight='bold', pad=20)
        
        datos = df_tabla.reset_index().values
        columnas = df_tabla.reset_index().columns.str.capitalize()
        tabla = ax_tab.table(cellText=datos, colLabels=columnas, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        tabla.set_fontsize(10)
        
        for (row, col), cell in tabla.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#2c5282') 
            elif row % 2 == 0:
                cell.set_facecolor('#f7fafc')
        pdf.savefig(fig_tab, bbox_inches='tight')
        plt.close(fig_tab)

        # --- PÁGINAS EXTRA: EL REGISTRO DETALLADO (LOG) ---
        lineas = log_texto.split('\n')
        # Aumentamos la cantidad de líneas por página (antes 55, ahora 65)
        lineas_por_pagina = 65 
        
        for i in range(0, len(lineas), lineas_por_pagina):
            # Mantenemos el tamaño carta estándar (8.5 x 11 pulgadas)
            fig_texto, ax_texto = plt.subplots(figsize=(8.5, 11))
            ax_texto.axis('off')
            
            bloque_texto = '\n'.join(lineas[i : i + lineas_por_pagina])
            
            # --- AJUSTE DE MÁRGENES Y FUENTE ---
            # 0.02 = Margen izquierdo más pequeño (antes 0.05)
            # 0.98 = Margen superior más alto (antes 0.95)
            # fontsize = 7.5 (antes 9, permite que líneas de 120 caracteres quepan)
            ax_texto.text(0.005, 0.98, bloque_texto, 
                          transform=ax_texto.transAxes, 
                          fontsize=8.5, 
                          family='monospace', 
                          verticalalignment='top')
            
            pdf.savefig(fig_texto)
            plt.close(fig_texto)

        # --- METADATOS DEL DOCUMENTO ACADÉMICO ---
        d = pdf.infodict()
        d['Title'] = titulo_base
        d['Author'] = 'Jonathan Francisco Rojas Martínez'
        d['Subject'] = 'Reporte de ejecución de Algoritmos Genéticos'