import numpy as np

def ruleta(datos_poblacion, num_seleccionados):
    probabilidades = [d["probabilidad"] for d in datos_poblacion]
    indices = np.random.choice(len(datos_poblacion), size=num_seleccionados, p=probabilidades)
    return [datos_poblacion[i] for i in indices]

def torneo(datos_poblacion, num_seleccionados, k=3):
    # Aquí puedes programar un método de selección por torneo fácilmente
    seleccionados = []
    for _ in range(num_seleccionados):
        aspirantes = np.random.choice(datos_poblacion, size=k, replace=False)
        ganador = max(aspirantes, key=lambda x: x["aptitud"])
        seleccionados.append(ganador)
    return seleccionados