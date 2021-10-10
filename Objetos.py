lecturas = ["Nota de consejo", "Fragmento de libro de secretos", 
            "Archivo de doctor", "Manual de supervivencia"]

class Objeto:
    
    def __init__(self, nombre:str, boosteo:int, estadistica:str, peso:float, 
                 usos:int, cantidad:int, precio:int):
        self.nombre = nombre
        self.boosteo = boosteo
        if(self.nombre not in lecturas):
            self.boosteo = int(boosteo)
        self.estadistica = estadistica
        self.peso = peso
        self.usos = usos
        self.cantidad = cantidad
        self.precio = precio
        
    def __str__(self):
        return (f"\n\t{self.nombre} \n "
                + f"Boosteo: {self.boosteo} \t| Estadistica: {self.estadistica} \n "
                + f"Peso: {self.peso} \t| Usos: {self.usos} \n "
                + f"Cantidad: {self.cantidad}\t| Precio: {self.precio}")

# =============================================================================
#obj = Objeto("nombre", 0, "tu caca", 3.0, 8, 1, -3)
#print(obj)
# =============================================================================
