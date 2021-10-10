# -*- coding: ISO-8859-1 -*-
import Game_Manager as gm

class Individuo:
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int,
                 inteligencia:int, sabiduria:int, nombre:str, condicion:dict):
        self.salud = salud
        self.fuerza = fuerza
        self.resistencia = resistencia
        self.carisma = carisma
        self.inteligencia = inteligencia
        self.sabiduria = sabiduria
        self.nombre = nombre
        self.condicion = condicion
        self.salud_max = salud
        self.carisma_max = carisma
        self.energia_max = 0
        self.energia = self.energia_max
            
    def cambiar_hp(self, hp:int):
        #DEBUG
#    print("------------------------------------------------Metodo cambiar hp")
        self.salud += round(hp)
        if(self.salud <= 0):
            print("\n"+self.nombre + " murió, F")
            return self.is_ded()
        return False
    
    def efecto(self):
        #DEBUG
#    print("----------------------------------------------------Metodo efecto")
        if("Envenenado III" in self.condicion):
            self.cambiar_hp(-self.salud_max*.15)
        elif("Envenenado II" in self.condicion):
            self.cambiar_hp(-self.salud_max*.1)
        elif("Envenenado I" in self.condicion):
            self.cambiar_hp(-self.salud_max*.05)
        if("Quemado" in self.condicion):
            self.cambiar_hp(-self.salud_max*self.condicion["Quemado"]*.05)
        if("Acelerado" in self.condicion):
            self.velocidad *= 1.2
        for c in self.condicion:
            if(c != "Saludable" and c != "Muerto" and c != "Bloqueado" 
               and c != "Temporal" and c != "Super Sayain"):
                self.condicion[c] -= 1
            if(self.condicion[c] == 0 or c == "Bloqueado"):
                if(c == "Indefenso"):
                    self.carisma = self.carisma_max
                elif("Fuerza" in c):
                    self.fuerza -= int(c[-1])
                elif("Resistencia" in c):
                    self.resistencia -= int(c[-1])
                elif("Carisma" in c):
                    self.carisma -= int(c[-1])
                elif("Inteligencia" in c):
                    self.inteligencia -= int(c[-1])
                elif("Sabiduria" in c):
                    self.sabiduria -= int(c[-1])
                elif("Energia" in c):
                    self.energia -= int(c[-1])
                self.condicion.pop(c)
                self.curar()
        return True
    
    def stats(self):
        espacio = 18-(len(str(int(self.energia_max))))
        espacio2 = 19-(len(str(int(self.salud_max))))
        a = f"\n{self.nombre:.^50} \n Salud: {int(self.salud)}/"
        + f"{int(self.salud_max):<{espacio2}} | Fuerza: {int(self.fuerza)}"
        + f" \n Resistencia: {int(self.resistencia):<14} | "
        + f"Carisma/Hostilidad: {int(self.carisma)} \n Inteligencia: "
        + f"{int(self.inteligencia):<13} | Sabiduria: {int(self.sabiduria)} "
        + f"\n Velocidad: {int(self.velocidad):<16} | Condicion: "
        + f"{self.condicion}\n Energia: {int(self.energia)}/"
        + f"{int(self.energia_max):<{espacio}}"
        return a
    
    def is_ded(self):
        #DEBUG
#    print("------------------------------------------Metodo is_ded individuo")
        return True
    
    def curar(self):
        if("Envenenado III" not in self.condicion and "Envenenado II" 
           not in self.condicion and "Envenenado I" not in self.condicion 
           and "Quemado" not in self.condicion):
            self.condicion.update({"Saludable": 1})
            return True
        return False
    
    def enfermar(self, condicion: str, duracion: int):
        if("Saludable" in self.condicion):
            self.condicion.pop("Saludable")
        self.condicion.update({condicion: duracion})
        return True
    
    def defender(self):
        #DEBUG
#    print("--------------------------------------------------Metodo defender")
        self.condicion.update({"Defendiendose": 1})
        self.energia += self.energia_max * .3
        print("Has recuperado el 30% de energia")
        if(self.energia > self.energia_max):
            self.energia = self.energia_max
        return self.resistencia + gm.dados(1, 10)[0]