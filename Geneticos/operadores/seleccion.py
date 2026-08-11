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

def rango(datos_poblacion, num_seleccionados):
    # Aquí puedes programar un método de selección por rango fácilmente
    datos_ordenados = sorted(datos_poblacion, key=lambda x: x["aptitud"])
    total = len(datos_ordenados)
    probabilidades = [(i + 1) / total for i in range(total)]
    indices = np.random.choice(len(datos_ordenados), size=num_seleccionados, p=probabilidades)
    return [datos_ordenados[i] for i in indices]

def Boltzmann(datos_poblacion, num_seleccionados, temperatura=1.0):
    # Aquí puedes programar un método de selección por Boltzmann fácilmente
    aptitudes = np.array([d["aptitud"] for d in datos_poblacion])
    probabilidades = np.exp(aptitudes / temperatura)
    probabilidades /= np.sum(probabilidades)
    indices = np.random.choice(len(datos_poblacion), size=num_seleccionados, p=probabilidades)
    return [datos_poblacion[i] for i in indices]