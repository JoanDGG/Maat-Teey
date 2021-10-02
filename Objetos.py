lecturas = ["Nota de consejo", "Fragmento de libro de secretos", "Archivo de doctor", "Manual de supervivencia"]

class Objeto:
    
    def __init__(self, nombre:str, boosteo:int, estadistica:str, peso:float, usos:int, cantidad:int, precio:int):
        self.nombre = nombre
        self.boosteo = boosteo
        if(self.nombre not in lecturas):
            self.boosteo = int(boosteo)
        self.estadistica = estadistica
        self.peso = peso
        self.usos = usos
        self.cantidad = cantidad
        self.precio = precio
        
    def nombre(self):
      return self._nombre

    def stats(self):
        print(f'\n\t{self.nombre} \n Boosteo: {self.boosteo} \t| Estadistica: {self.estadistica} \n Peso: {self.peso} \t| Usos: {self.usos} \n Cantidad: {self.cantidad}\t Precio: {self.precio}')
