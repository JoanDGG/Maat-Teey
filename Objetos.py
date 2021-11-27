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
        texto = (f"\n\t{self.nombre} \n "
                +f"Boosteo: {self.boosteo} \t| Estadistica: {self.estadistica}"
                +f" \nPeso: {self.peso} \t| Usos: {self.usos} \n "
                +f"Cantidad: {self.cantidad}\t| Precio: {self.precio}")
        return texto

# =============================================================================
#obj = Objeto("nombre", 0, "tu caca", 3.0, 8, 1, -3)
#print(obj)
# =============================================================================
