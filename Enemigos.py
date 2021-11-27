# -*- coding: ISO-8859-1 -*-
import Game_Manager as gm
from Individuos import Individuo

class Enemigo(Individuo):
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int,
                 inteligencia:int, sabiduria:int, nombre:str, condicion:dict,
                 dropeo:str, categoria:str, rango:int, cantidad:int, zona:str):
        super().__init__(salud, fuerza, resistencia, carisma, inteligencia,
                         sabiduria, nombre, condicion)
        self.dropeo = dropeo
        self.categoria = categoria
        self.rango = rango
        self.cantidad = cantidad
        self.peso = self.resistencia*(self.salud_max/self.salud)
        self.velocidad = round((self.fuerza/self.peso)*self.rango)
        self.agresividad = (((self.carisma+self.fuerza)-(
            self.inteligencia+self.resistencia))+4)
        self.energia_max = self.rango
        self.zona = zona
        if("Energio" in self.nombre):
            self.energia_max *= 2
        self.energia = self.energia_max
        
    def __str__(self):
        return(super().stats() + f"| Categoria: {self.categoria} \n Rango: "
              + f"{int(self.rango):<20} | Peso: {int(self.peso)} \n "
              + f"Agresividad: {int(self.agresividad):<15} \n Dropeos: "
              + f"\n {self.dropeo}")
    
    def actualizar_stats(self):
        self.peso = self.resistencia*(self.salud_max/self.salud)
        self.velocidad = round((self.fuerza/self.peso)*self.rango)
        self.agresividad = (((self.carisma+self.fuerza)-(
            self.inteligencia+self.resistencia))+4)
        
    def atacar(self, p_presentes, historial, turnos_aux, defensas):
        #DEBUG
#    print("----------------------------------------------------Metodo atacar")
        objetivo = ""
        dano = self.fuerza + gm.dados(1, 10)[0]
        no_faccion = self.no_faccion(turnos_aux, p_presentes)
        if(self.inteligencia <= 9):
            #-------------------------------------ataque aleatorio a cualquiera
            objetivos = turnos_aux
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            tirada = gm.dados(1, len(objetivos))[0]
            objetivo = objetivos[tirada-1]
        elif(self.inteligencia > 9 and self.inteligencia <= 19):
            #------------------------------ataque aleatorio a rival o el ultimo
            objetivos = no_faccion
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            tirada = gm.dados(1, len(objetivos))[0]
            objetivo = objetivos[tirada-1]
            
            # Si eres jefe, revisa si el atacante es personaje, si no, no
            for individuo in reversed(historial):                  
                if(individuo[1].nombre == self.nombre 
                   and (((self.nombre in gm.jefes) 
                         and(individuo[0] in gm.personajes)) 
                        or(self.nombre not in gm.jefes))):
                    objetivo = individuo[0]
                    break
                
        elif(self.inteligencia > 19):
            #-----------------------------------------ataque al rival mas debil
            objetivos = no_faccion
            if(self.nombre in gm.jefes):
                objetivos = p_presentes
            objetivo = objetivos[0]
            for individuo in objetivos:
                if(objetivo.salud > individuo.salud):
                    objetivo = individuo
        if("Alumno" in self.nombre 
           and "Simbolo comunidad" in objetivo.equipo_nombres):
            indice = objetivo.equipo_nombres.index("Simbolo comunidad")
            objetivo.equipo.pop(indice)
            objetivo.equipo_nombres.pop(indice)
            p_presentes.remove(objetivo)
            self.decidir(self, p_presentes, historial, turnos_aux, defensas)
        if(objetivo.nombre == "Mirek" and self.categoria == "Animal" 
           and objetivo.arbol["B1"][0] == 1):
            if(len(p_presentes) > 1):
                p_presentes.remove(objetivo)
                self.atacar(self, p_presentes, historial, turnos_aux, defensas)
            else:
                dano = 0
        elif(objetivo.nombre == "Sebas" 
             and "Ultra instinto" in objetivo.condicion):
            dano = 0
        elif(objetivo.nombre == "Sebas" 
             and "Kaio ken" in objetivo.condicion):
            dano *= 2
        if("Cegado" in self.condicion):
            tirada = gm.dados(1, 10)[0]
            if(tirada >= 8):
                dano = 0
                print(f"{self.nombre} ha fallado el ataque!")
        if(defensas[turnos_aux.index(objetivo)] > 0 and self.energia >= 1): 
            #---------------------------------------------Atacar si se defiende
            print(f"{self.nombre} ha usado un ataque de energia!")
            dano *= 1.25
            self.energia -= 1
        else:
            self.energia += self.energia_max * 0.2
            print("Has recuperado el 20% de energia")
            if(self.energia > self.energia_max):
                self.energia = self.energia_max
        if("Atraido" in self.condicion): # -----------------------------Carnada
            for personaje in turnos_aux:
                if("Oloroso" in personaje.condicion):
                    objetivo = personaje
                    break
        if("Bloqueado" in self.condicion):
            dano -= self.condicion["Bloqueado"]
            if(dano < 0):
                dano = 0
        self.condicion.update({"Atacando normal": 1})
        return [[objetivo], dano]
    
    def ataque_carisma(self, p_presentes = None, historial = None,
                       turnos_aux = None, defensas = None, objetivo = None):
        dano = self.carisma
        if(self.rango >= 5):
            dano *= 2
        if(objetivo == None):
            no_faccion = self.no_faccion(turnos_aux, p_presentes)
                        
            if(self.inteligencia <= 9):
                #---------------------------------ataque aleatorio a cualquiera
                objetivos = turnos_aux
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                tirada = gm.dados(1, len(objetivos))[0]
                objetivo = objetivos[tirada-1]
            elif(self.inteligencia > 9 and self.inteligencia <= 19):
                #--------------------------ataque aleatorio a rival o el ultimo
                objetivos = no_faccion
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                tirada = gm.dados(1, len(objetivos))[0]
                objetivo = objetivos[tirada-1]
                
                # Si eres jefe, revisa si el atacante es personaje, si no, no
                for individuo in reversed(historial): 
                    if(individuo[1].nombre == self.nombre 
                       and (((self.nombre in gm.jefes)
                             and (individuo[0] in gm.personajes)) 
                            or (self.nombre not in gm.jefes))):
                        objetivo = individuo[0]
                        break    
            elif(self.inteligencia > 19):
                #-------------------------------------ataque al rival mas debil
                objetivos = no_faccion
                if(self.nombre in gm.jefes):
                    objetivos = p_presentes
                objetivo = objetivos[0]
                for individuo in objetivos:
                    if(objetivo.carisma > individuo.carisma):
                        objetivo = individuo
        tirada = gm.dados(1, 10)[0]
        if(tirada >= 5):
            dano += 5
        elif(tirada >= 3):
            dano += 3
        else:
            dano += 1
        dano -= gm.dados(1, dano/10)[0]
        if(objetivo.nombre == "Mirek" and self.categoria == "Animal" 
           and objetivo.arbol["B1"][0] == 1):
            if(len(p_presentes) > 1):
                p_presentes.remove(objetivo)
                self.ataque_carisma(self, p_presentes, historial, turnos_aux,
                                    defensas)
            else:
                dano = 0
        if("Indefenso" in self.condicion):
            return [objetivo, 0]
        if("Indefenso" in objetivo.condicion):
            return self.atacar(self, p_presentes, historial, turnos_aux,
                               defensas)
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
    
    def cambiar_hp(self, hp:int, atacante: Individuo):
        #DEBUG
#    print("------------------------------------------------Metodo cambiar hp")
        self.salud += round(hp)
        if(self.salud <= 0):
            print("\n"+self.nombre + " murio, F")
            return self.is_ded(atacante)
        return False
    
    def decidir(self, p_presentes, historial, turnos_aux, defensas):
        #DEBUG
#    print("---------------------------------------------------Metodo decidir")
        porcentaje = 10 + 5*self.agresividad
        tirada = gm.dados(1, 100)[0]
        presentes = []
        for turno in range(0, len(turnos_aux)):
            if(turnos_aux[turno] in p_presentes):
                presentes.append(defensas[turno])
        
        if(tirada > porcentaje):
            if(self.salud/self.salud_max < .15 
               and self.carisma/self.carisma_max < .15):
                #Actualiza condicion en mover enemigo
                return self.huir(self, turnos_aux) 
            #Actualiza condicion en individuo defender
            return self.defender(self) 
        elif(self.carisma > self.fuerza):
            return self.ataque_carisma(self, p_presentes, historial,
                                          turnos_aux, defensas)
        else:
            if(presentes.count(0) > len(presentes)//2 
               and self.nombre in gm.jefes.keys() and self.energia >= 2):
                # --------------------Mayoria de objetivos posibles se defiende
                return self.ataque_especial(self, p_presentes)
            return self.atacar(self, p_presentes, historial, turnos_aux,
                                  defensas)
        
    def dropear(self):
        #DEBUG
#    print("---------------------------------------------------Metodo dropear")
        dropeos=["Owo"]
        dropeo_aleatorio=""
        if(self.dropeo == "--"):
            print("Dropeo Owo")
        elif(self.dropeo[0] == "%"):
            dropeo_aleatorio = gm.revisar_string(self.dropeo)
            if(dropeo_aleatorio[0].isdigit()):
                for dropeo_n in range(0, int(dropeo_aleatorio[0])):
                    dropeos.append(dropeo_aleatorio)
            else:
                dropeos.append(dropeo_aleatorio)
            print("Dropeo: " + dropeo_aleatorio + " y Owo")
        elif(self.dropeo == "Dialogo"):
            dropeos = None
            print("\nDi lo tuyo...\n")
        else:
            dropeos.append(self.dropeo)
            dropeo_carne_humana = ""
            if(self.categoria == "Humano"):
                dropeo_carne_humana = ", Carne humana"
                dropeos.append("Carne humana")
                
            print("Dropeo: " + self.dropeo + dropeo_carne_humana + " y Owo")
        return dropeos
        
    def efecto(self):
        super().efecto()
        self.actualizar_stats()
        
    def huir(self, turnos):
        for personaje in range(0, len(turnos)):
            if(turnos[personaje] in gm.personajes):
                break
        if(self.velocidad >= turnos[personaje].velocidad):
            return self.mover_enemigo(turnos[personaje].zona)
        else:
            prob = (self.velocidad/turnos[personaje].velocidad)*100
            tirada = gm.dados(1, 100)[0]
            if(tirada <= prob):
                return self.mover_enemigo(turnos[personaje].zona)
            else:
                return False
            
    def is_ded(self, atacante: Individuo):
        #DEBUG
#        print("------------------------------------------------Metodo is_ded")
        lugar = gm.busca_lugar(atacante.zona)
        zonas = lugar.zonas
        indice_zona = zonas.index(atacante.zona)
        indice = lugar.enemigos_activos[indice_zona].index(self)
        lugar.enemigos_activos[indice_zona].remove(self)
        lugar.cantidades_enemigos[indice_zona][indice] -= 1
        
        dropeos = self.dropear()
        
        for dropeo in dropeos:
            indice = lugar.zonas.index(self.zona)
            objeto = gm.transformar_objeto(dropeo)
            lugar.objetos_activos[indice].append(objeto)
            lugar.cantidades[indice].append(1)
            lugar.objetos[indice].append(objeto.nombre)
        return True
    
    def mover_enemigo(self, zona):
        self.condicion.update({"Huyendo": 1})
        origen = gm.buscaLugar(zona)
        zonas = gm.mapa_master[zona]
        tirada = gm.dados(1, len(zonas))[0]
        destino = gm.buscaLugar(zonas[tirada])
        origen.enemigos_activos[origen.indice_zona(zona)].remove(self)
        destino.enemigos_activos[destino.indice_zona(zonas[tirada
                                                           ])].append(self)
        return True
    
    def no_faccion(self, turnos_aux, p_presentes):
        no_faccion = []
        if("Confundido" in self.condicion):
            no_faccion = turnos_aux
        elif(issubclass(type(self), Enemigo)):
            for turno in turnos_aux:
                if(type(turno) == Enemigo):
                    no_faccion.append(turno)
        else:
            no_faccion = p_presentes.copy()
            for turno in turnos_aux:
                # Si sus categorias no son iguales
                #Si es animal y el otro tambien
                #Si es scp y el otro tambien
                #si el objetivo no es un jefe
                #si el objetivo no esta en la lista aun
                if((turno not in gm.personajes) 
                   and (turno.categoria != self.categoria) 
                   and (((self.categoria == "Animal") 
                         and (self.categoria == "Animal")) 
                        or ((self.categoria == "SCP") 
                            and (self.categoria == "SCP"))) 
                   and (turno.nombre not in gm.jefes.keys()) 
                   and (turno not in p_presentes)):
                    no_faccion.append(turno)
                    # animales, scp y no jefes
        return no_faccion