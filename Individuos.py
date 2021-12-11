# -*- coding: ISO-8859-1 -*-
import Game_Manager as gm

class Individuo:
    
    def __init__(self, salud:int, fuerza:int, resistencia:int, carisma:int,
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
    
    def curar(self):
        if("Envenenado III" not in self.condicion and "Envenenado II" 
           not in self.condicion and "Envenenado I" not in self.condicion 
           and "Quemado" not in self.condicion):
            self.condicion.update({"Saludable": 1})
            return True
        return False
    
    def defender(self):
        #DEBUG
#    print("--------------------------------------------------Metodo defender")
        self.condicion.update({"Defendiendose": 1})
        self.energia += self.energia_max * .3
        print("Has recuperado el 30% de energia")
        if(self.energia > self.energia_max):
            self.energia = self.energia_max
        defensa = self.resistencia + gm.dados(1, 10)[0]
        return defensa
    
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
        for condicion in self.condicion:
            if(condicion != "Saludable" and condicion != "Muerto" 
               and condicion != "Bloqueado" 
               and condicion != "Temporal" and condicion != "Super Sayain"):
                self.condicion[condicion] -= 1
            if(self.condicion[condicion] == 0 or condicion == "Bloqueado"):
                if(condicion == "Indefenso"):
                    self.carisma = self.carisma_max
                elif("Fuerza" in condicion):
                    self.fuerza -= int(condicion[-1])
                elif("Resistencia" in condicion):
                    self.resistencia -= int(condicion[-1])
                elif("Carisma" in condicion):
                    self.carisma -= int(condicion[-1])
                elif("Inteligencia" in condicion):
                    self.inteligencia -= int(condicion[-1])
                elif("Sabiduria" in condicion):
                    self.sabiduria -= int(condicion[-1])
                elif("Energia" in condicion):
                    self.energia -= int(condicion[-1])
                self.condicion.pop(condicion)
                self.curar()
        return True
    
    def enfermar(self, condicion: str, duracion: int):
        if("Saludable" in self.condicion):
            self.condicion.pop("Saludable")
        self.condicion.update({condicion: duracion})
        return True
    
    def stats(self):
        espacio_en_texto = 18-(len(str(int(self.energia_max))))
        espacio_en_texto_2 = 19-(len(str(int(self.salud_max))))
        texto = (f"\n{self.nombre:.^50} \n Salud: {int(self.salud)}/"
        + f"{int(self.salud_max):<{espacio_en_texto_2}} | Fuerza: "
        + f"{int(self.fuerza)}"
        + f" \n Resistencia: {int(self.resistencia):<14} | "
        + f"Carisma/Hostilidad: {int(self.carisma)} \n Inteligencia: "
        + f"{int(self.inteligencia):<13} | Sabiduria: {int(self.sabiduria)} "
        + f"\n Velocidad: {int(self.velocidad):<16} | Condicion: "
        + f"{self.condicion}\n Energia: {int(self.energia)}/"
        + f"{int(self.energia_max):<{espacio_en_texto}}")
        return texto