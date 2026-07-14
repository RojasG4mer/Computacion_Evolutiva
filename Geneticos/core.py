import random
from typing import Callable, Tuple

class AlgoritmoGenetico:
    def __init__(self, 
                 n_bits: int, 
                 intervalo: Tuple[float, float], 
                 tamano_poblacion: int, 
                 generaciones_totales: int, 
                 probabilidad_mutacion: float,
                 funcion_aptitud: Callable,
                 funcion_decodificacion: Callable,
                 funcion_seleccion: Callable,
                 funcion_cruza: Callable,
                 funcion_mutacion: Callable):
        
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
        self.historial_mejores = [] 
        self.log_texto = "" # <--- NUEVO: Aquí guardaremos todo el texto
        
    def _log(self, mensaje=""):
        """Imprime en terminal y guarda en el registro para el PDF."""
        print(mensaje)
        self.log_texto += str(mensaje) + "\n"

    def inicializar_poblacion(self):
        self.poblacion_actual = [[random.randint(0, 1) for _ in range(self.n_bits)] 
                                 for _ in range(self.tamano_poblacion)] 
        
    def _evaluar_generacion(self):
        datos_poblacion = []
        suma_aptitudes = 0
        
        for bits in self.poblacion_actual:
            decimal = self.decodificar(bits, self.intervalo[0], self.intervalo[1]) 
            aptitud = self.evaluar_aptitud(decimal) 
            suma_aptitudes += aptitud
            datos_poblacion.append({"bits": bits, "decimal": decimal, "aptitud": aptitud})
            
        for ind in datos_poblacion:
            ind["probabilidad"] = ind["aptitud"] / suma_aptitudes if suma_aptitudes > 0 else 0 
            
        return datos_poblacion

    def ejecutar(self):
        self.inicializar_poblacion()
        mejor_global = None
        self.log_texto = "" # Reiniciamos el log
        
        for gen in range(self.generaciones): 
            self._log(f"\n--- GENERACIÓN {gen + 1} ---") 
            
            # 1. EVALUACIÓN
            datos = self._evaluar_generacion()
            self._log("1. Evaluación:") 
            for d in datos:
                self._log(f"   Bits: {d['bits']} | Decimal: {d['decimal']:.2f} | Aptitud: {d['aptitud']:.2f} | Probabilidad: {d['probabilidad']:.4f}") 
            
            mejor_gen = max(datos, key=lambda x: x['aptitud'])
            self.historial_mejores.append(mejor_gen)
            if mejor_global is None or mejor_gen['aptitud'] > mejor_global['aptitud']:
                mejor_global = mejor_gen
                
            # 2. SELECCIÓN
            num_padres = int(self.tamano_poblacion / 2) 
            padres = self.seleccionar(datos, num_padres) 
            self._log("\n2. Selección (Padres elegidos para reproducirse):") 
            for p in padres: self._log(f"   {p['bits']}") 
            
            # 3. CRUZA
            siguiente_generacion = []
            self._log("\n3. Cruza:") 
            for i in range(num_padres):
                p1 = padres[i]['bits'].copy() 
                p2 = padres[i+1]['bits'].copy() if (i+1) < num_padres else padres[0]['bits'].copy() 
                
                hijo1, hijo2 = self.cruzar(p1, p2, self.n_bits) 
                siguiente_generacion.extend([hijo1, hijo2]) 
                self._log(f"   Cruzando {p1} y {p2} -> Hijos: {hijo1}, {hijo2}") 
                
            # 4. MUTACIÓN
            self._log("\n4. Mutación:") 
            for i in range(len(siguiente_generacion)):
                if random.random() < self.prob_mutacion: 
                    antes = siguiente_generacion[i].copy() 
                    siguiente_generacion[i] = self.mutar(siguiente_generacion[i]) 
                    self._log(f"   ¡Mutación! El individuo {i} cambió de {antes} a {siguiente_generacion[i]}") 
                    
            self.poblacion_actual = siguiente_generacion 
            self._log("-" * 50) 
            
        self._log("\n================== RESULTADO FINAL ==================") 
        self._log(f"El mejor individuo encontrado tras {self.generaciones} generaciones es:") 
        self._log(f"Bits: {mejor_global['bits']}") 
        self._log(f"Valor Decimal: {mejor_global['decimal']:.2f}") 
        self._log(f"Aptitud Alcanzada: {mejor_global['aptitud']:.2f}") 
        
        # AHORA DEVOLVEMOS AMBOS: El historial (para graficas/tablas) y el texto
        return self.historial_mejores, self.log_texto