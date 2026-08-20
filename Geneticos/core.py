import random
from typing import Callable, Tuple

class AlgoritmoGenetico:
    def __init__(self, n_bits: int, intervalo: Tuple[float, float], tamano_poblacion: int, generaciones_totales: int, probabilidad_mutacion: float, funcion_aptitud: Callable, funcion_decodificacion: Callable, funcion_seleccion: Callable, funcion_cruza: Callable, funcion_mutacion: Callable):
        self.n_bits = n_bits 
        self.intervalo = intervalo 
        self.tamano_poblacion = tamano_poblacion 
        self.generaciones = generaciones_totales 
        self.prob_mutacion = probabilidad_mutacion 
        self.evaluar_aptitud = funcion_aptitud
        self.decodificar = funcion_decodificacion
        self.seleccionar = funcion_seleccion
        self.cruzar = funcion_cruza
        self.mutar = funcion_mutacion
        self.poblacion_actual = []
        self.historial_completo = [] 
        self.log_texto = "" 
        
    def _log(self, mensaje=""):
        print(mensaje)
        self.log_texto += str(mensaje) + "\n"

    def inicializar_poblacion(self):
        self.poblacion_actual = [[random.randint(0, 1) for _ in range(self.n_bits)] for _ in range(self.tamano_poblacion)] 
        
    def _evaluar_generacion(self):
        datos_poblacion = []
        suma_aptitudes = 0
        
        for bits in self.poblacion_actual:
            valores_decimales = self.decodificar(bits, self.intervalo[0], self.intervalo[1]) 
            aptitud = self.evaluar_aptitud(valores_decimales) 
            suma_aptitudes += aptitud
            datos_poblacion.append({"bits": bits, "decimal": valores_decimales, "aptitud": aptitud})
            
        for ind in datos_poblacion:
            ind["probabilidad"] = ind["aptitud"] / suma_aptitudes if suma_aptitudes > 0 else 0 
            
        return datos_poblacion

    def ejecutar(self):
        self.inicializar_poblacion()
        mejor_global = None
        self.log_texto = "" 
        self.historial_completo = []
        
        for gen in range(self.generaciones): 
            self._log(f"\n--- GENERACIÓN {gen + 1} ---") 
            
            datos = self._evaluar_generacion()
            self._log("1. Evaluación:") 
            for d in datos:
                # Imprimimos 2 dimensiones (x, y) si existe, si no 1 dimension
                val_str = f"({d['decimal'][0]:.2f}, {d['decimal'][1]:.2f})" if isinstance(d['decimal'], tuple) else f"{d['decimal']:.2f}"
                self._log(f"   Bits: {d['bits']} | Dec: {val_str} | Aptitud: {d['aptitud']:.2f} | Probabilidad: {d['probabilidad']:.4f}") 
            
            datos_ordenados = sorted(datos, key=lambda x: x['aptitud'], reverse=True)
            self.historial_completo.append(datos_ordenados)
            mejor_gen = datos_ordenados[0]
            
            if mejor_global is None or mejor_gen['aptitud'] > mejor_global['aptitud']:
                mejor_global = mejor_gen
                
            num_padres = int(self.tamano_poblacion / 2) 
            padres = self.seleccionar(datos, num_padres) 
            self._log("\n2. Selección:") 
            for p in padres: self._log(f"   {p['bits']}") 
            
            # rECUERDA Al elite, sino luego no converge
            elite = mejor_gen['bits'].copy()
            siguiente_generacion = [elite] 
            
            self._log("\n3. Cruza:") 
            for i in range(num_padres):
                p1, p2 = padres[i]['bits'].copy(), padres[i+1]['bits'].copy() if (i+1) < num_padres else padres[0]['bits'].copy() 
                hijo1, hijo2 = self.cruzar(p1, p2, self.n_bits) 
                siguiente_generacion.extend([hijo1, hijo2]) 
                self._log(f"   Cruzando {p1} y {p2} -> Hijos: {hijo1}, {hijo2}") 
                
            # Recortamos la población al tamaño original (por haber agregado al élite extra)
            siguiente_generacion = siguiente_generacion[:self.tamano_poblacion]
                
            self._log("\n4. Mutación:") 


            for i in range(1, len(siguiente_generacion)):
                if random.random() < self.prob_mutacion: 
                    antes = siguiente_generacion[i].copy() 
                    siguiente_generacion[i] = self.mutar(siguiente_generacion[i]) 
                    self._log(f"   ¡Mutación! {antes} -> {siguiente_generacion[i]}") 
                    
            self.poblacion_actual = siguiente_generacion 
            self._log("-" * 50) 
            
        val_str = f"({mejor_global['decimal'][0]:.2f}, {mejor_global['decimal'][1]:.2f})" if isinstance(mejor_global['decimal'], tuple) else f"{mejor_global['decimal']:.2f}"
        self._log("\n================== RESULTADO FINAL ==================") 
        self._log(f"Bits: {mejor_global['bits']}\nValor (X, Y): {val_str}\nAptitud Alcanzada: {mejor_global['aptitud']:.2f}") 
        
        return self.historial_completo, self.log_texto