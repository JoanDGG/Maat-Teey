# -*- coding: ISO-8859-1 -*-
from Enemigos import Enemigo

class Asistente(Enemigo):
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int, inteligencia:int, sabiduria:int, nombre:str, condicion:dict, dropeo:str, categoria:str, rango:int, cantidad:int, zona:str, dueno, apodo:str):
        super().__init__(salud, fuerza, resistencia, carisma, inteligencia, sabiduria, nombre, condicion, dropeo, categoria, rango, cantidad, zona)
        self.dueno = dueno
        self.apodo = apodo

    def is_ded(self):
        self.dueno.asistentes.remove(self)
        mensaje = input("Escribe un mensaje de despedida (Enter para continuar)")
        if(mensaje == ""):
            mensaje = "F"
        self.dueno.in_memoriam.update({self.apodo: mensaje})
        if(self.salud <= 0):
            self.dropear()
        return True
    