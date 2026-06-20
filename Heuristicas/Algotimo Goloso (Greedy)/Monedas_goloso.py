import numpy as np

def algoritmo_goloso_monedas(cantidad_pesos):
    print(f"--- Solución Algoritmo Goloso para {cantidad_pesos} Pesos ---")
    
    # Convertimos los valores disponibles a centavos para operar con precisión
    # 2 pesos (200), 1 peso (100), 50, 20, 10 y 5 centavos.
    # El orden debe ser descendente para tomar el candidato más "prometedor" primero (el que más abarca con menos monedas).
    denominaciones_centavos = np.array([200, 100, 50, 20, 10, 5])
    
    # Convertimos la cantidad solicitada a centavos
    cantidad_restante = int(round(cantidad_pesos * 100))
    
    solucion = []
    
    # Iniciamos el ciclo mientras la cantidad no sea cero
    while cantidad_restante > 0:
        moneda_seleccionada = None
        
        # Buscar la moneda más grande que no exceda el restante
        for moneda in denominaciones_centavos:
            # Factibilidad: es válido tomar esta moneda?
            if moneda <= cantidad_restante:
                moneda_seleccionada = moneda
                break # Ya lo encontramos
        
        if moneda_seleccionada is None:
            print("No se puede encontrar una solución exacta con las denominaciones actuales.")
            break
            
        # Añadir a la solución y restar a la cantidad pendiente
        solucion.append(moneda_seleccionada / 100.0) # Guardamos el formato en pesos
        cantidad_restante -= moneda_seleccionada
        
    # Agrupar e imprimir resultados
    valores_unicos, conteos = np.unique(solucion, return_counts=True)
    
    print("Desglose óptimo de monedas a entregar:")
    for valor, cantidad in zip(reversed(valores_unicos), reversed(conteos)):
        if valor >= 1.0:
            print(f"- {cantidad} moneda(s) de {int(valor)} Peso(s)")
        else:
            print(f"- {cantidad} moneda(s) de {int(valor * 100)} centavos")

algoritmo_goloso_monedas(15.31)