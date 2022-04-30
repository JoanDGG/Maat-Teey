# -*- coding: ISO-8859-1 -*-
from Enemigos import Enemigo
import random

class Asistente(Enemigo):
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int,
                 inteligencia:int, sabiduria:int, nombre:str, condicion:dict,
                 dropeo:str, categoria:str, rango:int, cantidad:int, zona:str,
                 dueno, apodo:str):
        super().__init__(salud, fuerza, resistencia, carisma, inteligencia,
                         sabiduria, nombre, condicion, dropeo, categoria,
                         rango, cantidad, zona)
        self.dueno = dueno
        self.apodo = apodo

    def bautizo(self):
        archivo = open("Nombres.txt", "r")
        texto = archivo.read()
        nombres = texto.split(",")
        archivo.close()
        nombre = random.choice(nombres).split()[0].replace('"', '')
        self.apodo = nombre
    
    def is_ded(self):
        self.dueno.asistentes.remove(self)
        mensaje = input("Escribe un mensaje de despedida "
                        + "(Enter para continuar)\n")
        if(mensaje == ""):
            mensaje = "F"
        print(f"\n\tAdios... {self.nombre}... {mensaje}\n")
        self.dueno.in_memoriam.update({self.apodo: mensaje})
        if(self.salud <= 0):
            self.dropear()
            self.salud = 0
        return True
    
    def __str__(self):
        salud_index = super().__str__().find("Salud")
        dropeos_index = super().__str__().find("Dropeos")
        texto = (f"\n{self.apodo:.^50} \n " 
                + super().__str__()[salud_index:dropeos_index - 4] 
                + f" | Especie: {self.nombre} \n Dueno: {self.dueno.nombre} \n "
                + super().__str__()[dropeos_index:])
        return texto

# =============================================================================
#compa = Asistente(15, 14, 13, 10, 11, 15, "Aguila", "Saludable", "%Esencia velocidad II/Esencia sabiduria II", "Animal", 3, 1, "Cabana", )
#print(compa)
# =============================================================================
