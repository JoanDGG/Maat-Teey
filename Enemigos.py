# -*- coding: ISO-8859-1 -*-
import Game_Manager as gm
from Individuos import Individuo

class Enemigo(Individuo):
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int, inteligencia:int, sabiduria:int, nombre:str, condicion:dict, dropeo:str, categoria:str, rango:int, cantidad:int, zona:str):
        super().__init__(salud, fuerza, resistencia, carisma, inteligencia, sabiduria, nombre, condicion)
        self.dropeo = dropeo
        self.categoria = categoria
        self.rango = rango
        self.cantidad = cantidad
        self.peso = self.resistencia*(self.salud_max/self.salud)
        self.velocidad = round((self.fuerza/self.peso)*self.rango)
        self.agresividad = ((self.carisma+self.fuerza)-(self.inteligencia+self.resistencia))+4
        self.energia_max = self.rango
        self.zona = zona
        if("Energio" in self.nombre):
            self.energia_max *= 2
        self.energia = self.energia_max
    
    def efecto(self):
        super().efecto()
        self.actualizar_stats()
        
    def actualizar_stats(self):
        self.peso = self.resistencia*(self.salud_max/self.salud)
        self.velocidad = round((self.fuerza/self.peso)*self.rango)
        self.agresividad = ((self.carisma+self.fuerza)-(self.inteligencia+self.resistencia))+4
        
    def cambiar_hp(self, hp:int, atacante: Individuo):
        #DEBUG
#    print("-----------------------------------------------------Metodo cambiar hp")
        self.salud += round(hp)
        if(self.salud <= 0):
            print("\n"+self.nombre + " murió, F")
            return self.is_ded(atacante)
        return False
    
    def mover_enemigo(self, zona):
        self.condicion.update({"Huyendo": 1})
        origen = gm.buscaLugar(zona)
        zonas = gm.mapa_master[zona]
        tirada = gm.dados(1, len(zonas))[0]
        destino = gm.buscaLugar(zonas[tirada])
        origen.enemigos_activos()[origen.zonas().index(zona)].remove(self)
        destino.enemigos_activos()[destino.zonas().index(zonas[tirada])].append(self)
        return True
    
    def huir(self, turnos):
        for p in range(0, len(turnos)):
            if(turnos[p] in gm.personajes):
                break
        if(self.velocidad >= turnos[p].velocidad):
            return self.mover_enemigo(turnos[p].zona)
        else:
            prob = (self.velocidad/turnos[p].velocidad)*100
            tirada = gm.dados(1, 100)[0]
            if(tirada <= prob):
                return self.mover_enemigo(turnos[p].zona)
            else:
                return False
    
    def decidir(self, p_presentes, hist, turnos_aux, defensas):
        #DEBUG
#    print("--------------------------------------------------------Metodo decidir")
        porcentaje = 10 + 5*self.agresividad
        n = gm.dados(1, 100)[0]
        presentes = []
        for t in range(0, len(turnos_aux)):
            if(turnos_aux[t] in p_presentes):
                presentes.append(defensas[t])
        
        if(n > porcentaje):
            if(self.salud/self.salud_max < .15 and self.carisma/self.carisma_max < .15):
                return Enemigo.huir(self, turnos_aux) #Actualiza condicion en mover enemigo
            return Enemigo.defender(self) #Actualiza condicion en individuo defender
        elif(self.carisma > self.fuerza):
            return Enemigo.ataque_carisma(self, p_presentes, hist, turnos_aux, defensas)
        else:
            if(presentes.count(0) > len(presentes)//2 and self.nombre in gm.jefes.keys() and self.energia >= 2):
                # -------------------------Mayoria de objetivos posibles se defiende
                return Enemigo.ataque_especial(self, p_presentes)
            return Enemigo.atacar(self, p_presentes, hist, turnos_aux, defensas)
    
    def ataque_carisma(self, p_presentes = None, hist = None, turnos_aux = None, defensas = None, objetivo = None):
        dano = self.carisma
        if(self.rango >= 5):
            dano *= 2
        if(objetivo == None):
            if("Confundido" in self.condicion):
                no_faccion = turnos_aux
            elif(issubclass(type(self), Enemigo)):
                no_faccion = []
                for t in turnos_aux:
                    if(type(t) == Enemigo):
                        no_faccion.append(t)
            else:
                no_faccion = p_presentes.copy()
                for t in turnos_aux:
                    # Si sus categorias no son iguales             Si es animal y el otro tambien                                     Si es scp y el otro tambien                              si el objetivo no es un jefe    si el objetivo no esta en la lista aun
                    if(t not in gm.personajes) and (t.categoria != self.categoria) and (((self.categoria == "Animal") and (self.categoria == "Animal")) or ((self.categoria == "SCP") and (self.categoria == "SCP"))) and (t.nombre not in gm.jefes.keys()) and (t not in gm.p_presentes):
                        no_faccion.append(t)
                        # animales, scp y no jefes
                        
            if(self.inteligencia <= 9):
                #------------------------------------------ataque aleatorio a cualquiera
                objetivos = turnos_aux
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                n = gm.dados(1, len(objetivos))[0]
                objetivo = objetivos[n-1]
            elif(self.inteligencia > 9 and self.inteligencia <= 19):
                #-----------------------------------ataque aleatorio a rival o el ultimo
                objetivos = no_faccion
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                n = gm.dados(1, len(objetivos))[0]
                objetivo = objetivos[n-1]
                
                for i in reversed(hist):                  # Si eres jefe, revisa si el atacante es personaje, si no, no
                    if(i[1].nombre == self.nombre and (((self.nombre in gm.jefes)and(i[0] in gm.personajes))or(self.nombre not in gm.jefes))):
                        objetivo = i[0]
                        break    
            elif(self.inteligencia > 19):
                #----------------------------------------------ataque al rival mas debil
                objetivos = no_faccion
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                objetivo = objetivos[0]
                for i in objetivos:
                    if(objetivo.carisma > i.carisma):
                        objetivo = i
        tirada = gm.dados(1, 10)[0]
        if(tirada >= 5):
            dano += 5
        elif(tirada >= 3):
            dano += 3
        else:
            dano += 1
        dano -= gm.dados(1, dano/10)[0]
        if(objetivo.nombre == "Mirek" and self.categoria == "Animal" and objetivo.arbol["B1"][0] == 1):
            if(len(p_presentes) > 1):
                p_presentes.remove(objetivo)
                self.ataque_carisma(self, p_presentes, hist, turnos_aux, defensas)
            else:
                dano = 0
        if("Indefenso" in self.condicion):
            return [objetivo, 0]
        if("Indefenso" in objetivo.condicion):
            return self.atacar(self, p_presentes, hist, turnos_aux, defensas)
        self.condicion.update({"Atacando con carisma": 1})
        return [objetivo, dano]
    
    def ataque_especial(self, p_presentes):
        print(f"{self.nombre} ha usado su habilidad especial!!")
        dano = self.fuerza + gm.dados(1, 10)[0]
        if(len(p_presentes) == 1):
             dano *= 2
        
        if("Bloqueado" in self.condicion):
            dano -= self.condicion["Bloqueado"]
            if(dano < 0):
                dano = 0
        self.energia -= 2
        self.condicion.update({"Atacando especial": 1})
        return [p_presentes, dano]

    def atacar(self, p_presentes, hist, turnos_aux, defensas):
        #DEBUG
#    print("---------------------------------------------------------Metodo atacar")
        objetivo = ""
        dano = self.fuerza + gm.dados(1, 10)[0]
        no_faccion = []
        if("Confundido" in self.condicion):
            no_faccion = turnos_aux
        elif(issubclass(type(self), Enemigo)):
            for t in turnos_aux:
                if(type(t) == Enemigo):
                    no_faccion.append(t)
        else:
            no_faccion = p_presentes.copy()
            for t in turnos_aux:
                # Si sus categorias no son iguales             Si es animal y el otro tambien                                     Si es scp y el otro tambien                              si el objetivo no es un jefe    si el objetivo no esta en la lista aun
                if(t not in gm.personajes) and (t.categoria != self.categoria) and (((self.categoria == "Animal") and (self.categoria == "Animal")) or ((self.categoria == "SCP") and (self.categoria == "SCP"))) and (t.nombre not in gm.jefes.keys()) and (t not in p_presentes):
                    no_faccion.append(t)
                    # animales, scp y no jefes
        
        if(self.inteligencia <= 9):
            #------------------------------------------ataque aleatorio a cualquiera
            objetivos = turnos_aux
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            n = gm.dados(1, len(objetivos))[0]
            objetivo = objetivos[n-1]
        elif(self.inteligencia > 9 and self.inteligencia <= 19):
            #-----------------------------------ataque aleatorio a rival o el ultimo
            objetivos = no_faccion
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            n = gm.dados(1, len(objetivos))[0]
            objetivo = objetivos[n-1]
            
            for i in reversed(hist):                  # Si eres jefe, revisa si el atacante es personaje, si no, no
                if(i[1].nombre == self.nombre and (((self.nombre in gm.jefes)and(i[0] in gm.personajes))or(self.nombre not in gm.jefes))):
                    objetivo = i[0]
                    break
                
        elif(self.inteligencia > 19):
            #----------------------------------------------ataque al rival mas debil
            objetivos = no_faccion
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            objetivo = objetivos[0]
            for i in objetivos:
                if(objetivo.salud > i.salud):
                    objetivo = i
        if("Alumno" in self.nombre and "Simbolo comunidad" in objetivo.equipo_nombres):
            indio = objetivo.equipo_nombres.index("Simbolo comunidad")
            objetivo.equipo.pop(indio)
            objetivo.equipo_nombres.pop(indio)
            p_presentes.remove(objetivo)
            self.decidir(self, p_presentes, hist, turnos_aux, defensas)
        if(objetivo.nombre == "Mirek" and self.categoria == "Animal" and objetivo.arbol["B1"][0] == 1):
            if(len(p_presentes) > 1):
                p_presentes.remove(objetivo)
                self.atacar(self, p_presentes, hist, turnos_aux, defensas)
            else:
                dano = 0
        elif(objetivo.nombre == "Sebas" and "Ultra instinto" in objetivo.condicion):
            dano = 0
        elif(objetivo.nombre == "Sebas" and "Kaio ken" in objetivo.condicion):
            dano *= 2
        if("Cegado" in self.condicion):
            tirada = gm.dados(1, 10)[0]
            if(tirada >= 8):
                dano = 0
                print(f"{self.nombre} ha fallado el ataque!")
        if(defensas[turnos_aux.index(objetivo)] > 0 and self.energia >= 1): 
            #--------------------------------------------------Atacar si se defiende
            print(f"{self.nombre} ha usado un ataque de energia!")
            dano *= 1.25
            self.energia -= 1
        else:
            self.energia += self.energia_max * 0.2
            print("Has recuperado el 20% de energia")
            if(self.energia > self.energia_max):
                self.energia = self.energia_max
        if("Atraido" in self.condicion): # ----------------------------------Carnada
            for p in turnos_aux:
                if("Oloroso" in p.condicion):
                    objetivo = p
                    break
        if("Bloqueado" in self.condicion):
            dano -= self.condicion["Bloqueado"]
            if(dano < 0):
                dano = 0
        self.condicion.update({"Atacando normal": 1})
        return [[objetivo], dano]
    
    def dropear(self):
        #DEBUG
#    print("--------------------------------------------------------Metodo dropear")
        kk=["Owo"]
        s=""
        if(self.dropeo == "--"):
            print("Dropeo Owo")
            return kk
        elif(self.dropeo[0] == "%"):
            s = gm.revisar_string(self.dropeo)
            if(s[0].isdigit()):
                for i in range(0, int(s[0])):
                    kk.append(s)
            else:
                kk.append(s)
            print("Dropeo: " + s + " y Owo")
            return kk
        elif(self.dropeo == "Dialogo"):
            print("\nDi lo tuyo...\n")
        else:
            kk.append(self.dropeo)
            kkk = ""
            if(self.categoria == "Humano"):
                kkk = ", Carne humana"
                kk.append("Carne humana")
                
            print("Dropeo: " + self.dropeo + kkk + " y Owo")
            return kk
        
    def is_ded(self, atacante: Individuo):
        #DEBUG
#        print("-----------------------------------------------------Metodo is_ded")
        for l in range(0, len(gm.lugares_o)):
            lug = gm.lugares_o[l].zonas()
            if(atacante.zona in lug):
                lugar = gm.lugares_o[l]
                break
        zonas = lugar.zonas()
        i = zonas.index(atacante.zona)
        indio = lugar.enemigos_activos()[i].index(self)
        lugar.enemigos_activos()[i].remove(self)
        lugar.cantidades_enemigos()[i][indio] -= 1
        
        from Juegos import Juego
        kk = self.dropear()
        
        for k in kk:
            indio = lugar.zonas().index(self.zona)
            o = Juego.tranformar_objeto(k)
            lugar.objetos_activos()[indio].append(o)
            lugar.cantidades()[indio].append(1)
            lugar.objetos()[indio].append(o.nombre)
        return True

    def stats(self):
        print(super().stats() + f'| Categoria: {self.categoria} \n Rango: {int(self.rango):<20} | Peso: {int(self.peso)} \n Agresividad: {int(self.agresividad):<15} \n Dropeos: \n {self.dropeo}')
