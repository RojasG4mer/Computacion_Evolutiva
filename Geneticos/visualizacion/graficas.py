import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np

def configurar_estilo():
    """Configura un estilo limpio y formal."""
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'legend.fontsize': 10,
        'figure.dpi': 300,        
        'savefig.bbox': 'tight'   
    })

# ==========================================
# REPORTE AUTOMÁTICO DINÁMICO (4 VISTAS)
# ==========================================
def generar_reporte_completo_pdf(historial_pob, log_texto, configuracion, funcion_raw, intervalo, titulo_base="Reporte AG", nombre_archivo="reporte.pdf"):
    
    total_gen = len(historial_pob)
    
    # Lógica dinámica de saltos
    paso = 1 if total_gen <= 10 else total_gen // 10
    indices_snapshots = list(range(paso - 1, total_gen, paso))
    if indices_snapshots[-1] != total_gen - 1:
        indices_snapshots[-1] = total_gen - 1

    colores_6 = ['#e6194b', '#3cb44b', '#ffe119', '#e6beff', '#f58231', '#911eb4']

    # Pre-calculamos la malla matemática de la función
    X_grid = np.linspace(intervalo[0], intervalo[1], 50)
    Y_grid = np.linspace(intervalo[0], intervalo[1], 50)
    X_mesh, Y_mesh = np.meshgrid(X_grid, Y_grid)
    Z_mesh = np.zeros_like(X_mesh)
    
    for i in range(X_mesh.shape[0]):
        for j in range(X_mesh.shape[1]):
            Z_mesh[i,j] = funcion_raw((X_mesh[i,j], Y_mesh[i,j]))

    # Pre-calculamos la silueta máxima y mínima del terreno para proyectarla al fondo
    # (Esto creará una sombra gris muy útil en las vistas laterales)
    Z_min_X = np.min(Z_mesh, axis=0) 
    Z_max_X = np.max(Z_mesh, axis=0)
    Z_min_Y = np.min(Z_mesh, axis=1) 
    Z_max_Y = np.max(Z_mesh, axis=1)

    def dibujar_entorno(fig, titulo_general):
        """Prepara el lienzo 2x2 con las 4 vistas."""
        ax_2d = fig.add_subplot(221)
        ax_3d = fig.add_subplot(222, projection='3d')
        ax_xz = fig.add_subplot(223)
        ax_yz = fig.add_subplot(224)
        
        # 1. Vista Superior 2D (Topográfica)
        ax_2d.contourf(X_mesh, Y_mesh, Z_mesh, levels=40, cmap='viridis', alpha=0.8)
        ax_2d.set_title("Vista Superior (X, Y)", weight='bold')
        ax_2d.set_xlabel('Eje X')
        ax_2d.set_ylabel('Eje Y')
        ax_2d.grid(True, linestyle=':', alpha=0.5)

        # 2. Vista de Perfil 3D Completa
        ax_3d.plot_surface(X_mesh, Y_mesh, Z_mesh, cmap='viridis', alpha=0.5, edgecolor='none')
        ax_3d.set_title("Perspectiva 3D", weight='bold')
        ax_3d.set_xlabel('Eje X')
        ax_3d.set_ylabel('Eje Y')
        ax_3d.set_zlabel('Aptitud (Z)')
        ax_3d.view_init(elev=25, azim=45) 

        # 3. Vista Lateral XZ
        ax_xz.fill_between(X_grid, Z_min_X, Z_max_X, color='gray', alpha=0.2, label='Perfil del Terreno')
        ax_xz.set_title("Vista Lateral (X vs Elevación Z)", weight='bold')
        ax_xz.set_xlabel('Eje X')
        ax_xz.set_ylabel('Aptitud (Z)')
        ax_xz.grid(True, linestyle=':', alpha=0.7)

        # 4. Vista Frontal YZ
        ax_yz.fill_between(Y_grid, Z_min_Y, Z_max_Y, color='gray', alpha=0.2, label='Perfil del Terreno')
        ax_yz.set_title("Vista Frontal (Y vs Elevación Z)", weight='bold')
        ax_yz.set_xlabel('Eje Y')
        ax_yz.set_ylabel('Aptitud (Z)')
        ax_yz.grid(True, linestyle=':', alpha=0.7)

        fig.suptitle(titulo_general, weight='bold', fontsize=18, y=1.03)
        return ax_2d, ax_3d, ax_xz, ax_yz

    with PdfPages(nombre_archivo) as pdf:
        
        # --- PÁGINA 1: PORTADA ---
        fig_portada, ax_portada = plt.subplots(figsize=(8.5, 11))
        ax_portada.axis('off')
        texto_portada = "REPORTE DE EJECUCIÓN\nALGORITMO GENÉTICO EN ESPACIO 2D Y 3D\n" + "="*45 + "\n\nMÉTODOS UTILIZADOS:\n\n"
        for parametro, valor in configuracion.items():
            texto_portada += f"  > {parametro}:\t{valor.upper()}\n"
        texto_portada += f"  > Generaciones:\t{total_gen}\n\n" + "="*45 + "\nCentro de Investigaciones en Óptica"
        ax_portada.text(0.1, 0.8, texto_portada, transform=ax_portada.transAxes, fontsize=14, family='monospace', verticalalignment='top')
        pdf.savefig(fig_portada)
        plt.close(fig_portada)

        # --- PÁGINA 2: GRÁFICAS INICIALES (Gen 1) ---
        fig = plt.figure(figsize=(14, 12)) # Lienzo más alto para soportar las 4 vistas
        ax_2d, ax_3d, ax_xz, ax_yz = dibujar_entorno(fig, "Generación 1: Posición Inicial de los 6 Mejores")
        
        top6_ini = historial_pob[0][:6]
        for i, ind in enumerate(top6_ini):
            x_val, y_val = ind['decimal']
            z_val = funcion_raw((x_val, y_val))
            c = colores_6[i % len(colores_6)]
            
            ax_2d.scatter(x_val, y_val, color=c, s=100, edgecolors='black', zorder=5)
            ax_3d.scatter(x_val, y_val, z_val, color=c, s=150, edgecolors='black', depthshade=False, label=f'Indiv. {i+1}')
            ax_xz.scatter(x_val, z_val, color=c, s=120, edgecolors='black', zorder=5)
            ax_yz.scatter(y_val, z_val, color=c, s=120, edgecolors='black', zorder=5)
            
        ax_3d.legend(loc='upper left', fontsize=9, bbox_to_anchor=(1.05, 1))
        fig.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # --- PÁGINAS MEDIAS: LOS SALTOS DE AVANCE ---
        for idx in indices_snapshots:
            fig = plt.figure(figsize=(14, 12))
            gen_num = idx + 1
            ax_2d, ax_3d, ax_xz, ax_yz = dibujar_entorno(fig, f"Progreso: Generación {gen_num}")
            
            top6_gen = historial_pob[idx][:6]
            for i, ind in enumerate(top6_gen):
                x_val, y_val = ind['decimal']
                z_val = funcion_raw((x_val, y_val))
                c = colores_6[i % len(colores_6)]
                
                ax_2d.scatter(x_val, y_val, color=c, s=100, edgecolors='black', zorder=5)
                ax_3d.scatter(x_val, y_val, z_val, color=c, s=150, edgecolors='black', depthshade=False)
                ax_xz.scatter(x_val, z_val, color=c, s=120, edgecolors='black', zorder=5)
                ax_yz.scatter(y_val, z_val, color=c, s=120, edgecolors='black', zorder=5)
                
            fig.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

        # --- PÁGINA PENÚLTIMA: TABLA DE LOS PASOS ---
        datos_tabla = []
        for i in indices_snapshots:
            mejor = historial_pob[i][0]
            str_dec = f"X: {mejor['decimal'][0]:.2f}, Y: {mejor['decimal'][1]:.2f}"
            datos_tabla.append({'Gen': i + 1, 'Mejores Bits': str(mejor['bits']), 'Coordenadas (X, Y)': str_dec, 'Aptitud': round(mejor['aptitud'], 4)})
        
        df_tabla = pd.DataFrame(datos_tabla)
        fig_tab, ax_tab = plt.subplots(figsize=(8, max(4, len(df_tabla) * 0.4)))
        ax_tab.axis('tight')
        ax_tab.axis('off')
        ax_tab.set_title(f"Posición del Mejor Individuo por Salto", weight='bold', pad=20)
        
        tabla = ax_tab.table(cellText=df_tabla.values, colLabels=df_tabla.columns, loc='center', cellLoc='center')
        tabla.scale(1, 1.5)
        tabla.set_fontsize(9)
        for (row, col), cell in tabla.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#2c5282') 
            elif row % 2 == 0:
                cell.set_facecolor('#f7fafc')
        pdf.savefig(fig_tab, bbox_inches='tight')
        plt.close(fig_tab)

        # --- PÁGINA FINAL: COMPARATIVA INICIO VS FIN ---
        fig = plt.figure(figsize=(14, 12))
        ax_2d, ax_3d, ax_xz, ax_yz = dibujar_entorno(fig, f"Comparativa: Iniciales (Tache) vs Finales Gen {total_gen} (Círculo)")
        
        # Iniciales como cruces transparentes
        for i, ind in enumerate(top6_ini):
            x_val, y_val = ind['decimal']
            z_val = funcion_raw((x_val, y_val))
            c = colores_6[i % len(colores_6)]
            
            ax_2d.scatter(x_val, y_val, color=c, alpha=0.4, marker='x', s=100, zorder=5)
            ax_3d.scatter(x_val, y_val, z_val, color=c, alpha=0.4, marker='x', s=100)
            ax_xz.scatter(x_val, z_val, color=c, alpha=0.4, marker='x', s=100, zorder=5)
            ax_yz.scatter(y_val, z_val, color=c, alpha=0.4, marker='x', s=100, zorder=5)
            
        # Finales como esferas grandes
        top6_fin = historial_pob[-1][:6]
        for i, ind in enumerate(top6_fin):
            x_val, y_val = ind['decimal']
            z_val = funcion_raw((x_val, y_val))
            c = colores_6[i % len(colores_6)]
            
            ax_2d.scatter(x_val, y_val, color=c, s=150, edgecolors='black', zorder=6)
            ax_3d.scatter(x_val, y_val, z_val, color=c, s=200, edgecolors='black', depthshade=False, label=f'Final {i+1}')
            ax_xz.scatter(x_val, z_val, color=c, s=150, edgecolors='black', zorder=6)
            ax_yz.scatter(y_val, z_val, color=c, s=150, edgecolors='black', zorder=6)
            
        ax_3d.legend(loc='upper left', fontsize=9, bbox_to_anchor=(1.05, 1))
        fig.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # --- LOG TEXTO ---
        lineas = log_texto.split('\n')
        lineas_por_pagina = 65 
        for i in range(0, len(lineas), lineas_por_pagina):
            fig_texto, ax_texto = plt.subplots(figsize=(8.5, 11))
            ax_texto.axis('off')
            bloque_texto = '\n'.join(lineas[i : i + lineas_por_pagina])
            ax_texto.text(0.02, 0.98, bloque_texto, transform=ax_texto.transAxes, fontsize=7.5, family='monospace', verticalalignment='top')
            pdf.savefig(fig_texto)
            plt.close(fig_texto)