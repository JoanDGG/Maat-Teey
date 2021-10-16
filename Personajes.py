# -*- coding: ISO-8859-1 -*-
from Individuos import Individuo
from Objetos import Objeto
from Lugares import Lugar
from Asistentes import Asistente
import numpy as np

class Personaje(Individuo):
    
    def __init__(self, salud: int, fuerza:int, resistencia:int, carisma:int,
                 inteligencia:int, sabiduria:int, nombre:str, condicion:dict,
                 peso:int, inventario:list, ubicacion: Lugar, zona:str,
                 nivel:int, mapa: dict, cartera: int, energia: int,
                 arbol: dict):
        super().__init__(salud, fuerza, resistencia, carisma, inteligencia,
                         sabiduria, nombre, condicion)
        self.inventario = inventario
        self.inventario_nombres = []
        self.masa_corporal = self.resistencia*(self.salud_max/self.salud)
        for i in (self.inventario):
            self.inventario_nombres.append(i.nombre)
        self.peso = 0
        for i in self.inventario:
            self.peso += i.peso
        self.peso = round(self.peso) + self.masa_corporal
        self.ubicacion = ubicacion
        self.nivel = nivel
        self.zona = zona
        self.velocidad = round((self.fuerza/self.peso)*self.nivel)
        self.carga = round(self.resistencia*(self.salud/self.salud_max)
                           + (self.inteligencia+self.fuerza)/2)
        self.mapa = mapa
        self.cartera = cartera
        self.puntos_habilidad = 0
        self.energia = energia
        self.energia_max = energia
        self.arbol = arbol
        self.viaje_astral = False
        self.equipo = []
        self.equipo_nombres= []
        for equipo in (self.equipo):
            self.equipo_nombres.append(equipo.nombre)
        self.cartera_obj = {}
        self.is_wendigo = False
        self.lugar_previo = "Cabana"
        self.asistentes = []
        self.espacio_asistentes = 7
    
    def efecto(self):
        super().efecto()
        for asistente in self.asistentes:
            if("Lealtad" in asistente.condicion 
               and asistente.condicion["Lealtad"] == 0):
                self.asistentes.remove(asistente)
        self.actualizar_stats()
    
    def actualizar_stats(self):
        self.masa_corporal = self.resistencia*(self.salud_max/self.salud)
        self.peso = 0
        for objeto in self.inventario:
            self.peso += objeto.peso
        self.peso = round(self.peso) + self.masa_corporal
        if("Super Sayain" in self.condicion):
            if(self.fuerza != self.condicion["Super Sayain"] * 1.5):
                self.fuerza *= 1.5
        self.velocidad = round((self.fuerza/self.peso)*self.nivel)
        self.carga = round(self.resistencia*(self.salud/self.salud_max)
                           + (self.inteligencia+self.fuerza)/2)
        if(self.arbol["B1"][0] == 1):
            self.carga += self.energia_max
        for mochila in range(0, len(gm.mochilas)):
            if(gm.mochilas[mochila] in self.equipo_nombres):
                indio = self.equipo_nombres.index(gm.mochilas[mochila])
                self.carga += self.equipo[indio].boosteo
                break
        if("Shaed" in self.equipo_nombres and not gm.dia):
            self.condicion.update({'Invisible': 10})
            if(self.zona in gm.iluminados):
                self.condicion.pop("Invisible")
        elif("Shaed" in self.equipo_nombres and gm.dia):
            self.condicion.pop("Invisible")
        elif("Shaed mejorado" in self.equipo_nombres and not gm.dia):
            self.condicion.update({'Invisible': 10})
            if(self.zona in gm.iluminados):
                self.condicion.pop("Invisible")
        elif("Shaed mejorado" in self.equipo_nombres and gm.dia):
            self.condicion.pop("Invisible")
    
    def anadir_equipo(self, o:Objeto, index: int):
        if(self.cartera_obj[o.nombre] > 1):
            self.cartera_obj[o.nombre] -= 1
        else:
            self.cartera_obj.pop(o.nombre)
        self.inventario.pop(index)
        self.inventario_nombres.pop(index)
        return True
    
    def quitar_equipo(self, o:Objeto):
        if(o.nombre not in self.cartera_obj.keys()):
            self.cartera_obj.update({o.nombre: 1})
        else:
            self.cartera_obj[o.nombre] += 1
        self.inventario.append(o)
        self.inventario_nombres.append(o.nombre)
        return True
    
    def energetizar(self):
        if(self.energia <= 0 or self.salud == self.salud_max):
            print("Pues no se pudo")
            return False
        while(self.energia > 0 and self.salud < self.salud_max):
            self.salud += (self.energia/self.energia_max)*self.salud_max
            self.energia -= 1
        if(self.salud > self.salud_max):
            self.salud = self.salud_max
        return True
    
    def cambiar_hp(self, hp:int, atacante:Individuo):
        #DEBUG
#    print("------------------------------------------------Metodo cambiar hp")
        self.salud += round(hp)
        if(self.salud <= 0):
            print("\n"+self.nombre + " muri�, F")
            return self.is_ded()
        self.actualizar_stats()
        self.exceso_peso()
        return False
    
    def reclutar(self, asistente):
        while(self.espacio_asistentes < asistente.rango):
            print("No tienes espacio suficiente! (espacio faltante: "
                  + f"{asistente.rango - self.espacio_asistentes}) \n�Deseas "
                  + "liberar a algun asistente?")
            for a in range(0, len(self.asistentes)):
                print(f"{a+1}: {self.asistentes[a].apodo} \t espacio ocupado: "
                      + f"{self.asistentes[a].rango}")
            print(f"{len(self.asistentes)+1}: Ninguno")
            decision = int(input()) - 1
            if(decision == len(self.asistentes)):
                return False
            else:
                if(Juego.ubicar.count(self.zona) > 1): # Si no estas solo en la zona
                    decision = int(input("�Deseas dejar libre al asistente o "
                                         + "darselo a alguien?\n 1: Dejarlo "
                                         + "libre \n 2: Cambiar de dueno\n"))
                    if(decision == 1):
                        self.asistentes[decision].is_ded()
                    elif(decision == 2):
                        self.cambiar_dueno(self.asistentes[decision])
        # reclutado
        print("Asistente adquirido!")
        from Enemigos import Enemigo
        if(type(asistente) == Enemigo):
            decision = input("�Quieres ponerle un nombre?(S/N)\n")
            if(decision == "S"):
                nombre = input("�Como quieres llamarlo?\n")
    #        else:
                #Generador de nombres 2000
        elif(issubclass(asistente, Enemigo)): # Si ya tiene apodo
            nombre = asistente.apodo
        print(f"Felicidades! {nombre} se ha unido a tu aventura!!")
        agresividad_max = (((Juego.oso_marino.carisma 
                             + Juego.oso_marino.fuerza)
                           -(Juego.oso_marino.inteligencia 
                             + Juego.oso_marino.resistencia))+4)
        suma = (asistente.salud_max + asistente.fuerza + asistente.resistencia
        + asistente.carisma_max + asistente.inteligencia + asistente.sabiduria)
        boosteo = ((asistente.salud/asistente.salud_maxima 
                   - asistente.agresividad/agresividad_max) * suma / 4)
        for punto in range(0, boosteo):
            tirada = Juego.dados(1, 6)[0]
            if(tirada == 1):
                asistente.salud_max += 5
            elif(tirada == 2):
                asistente.fuerza += 1
            elif(tirada == 3):
                asistente.resistencia += 1
            elif(tirada == 4):
                asistente.carisma_max += 1
            elif(tirada == 5):
                asistente.inteligencia += 1
            elif(tirada == 6):
                asistente.sabiduria += 1
        
        zona = self.ubicacion.zonas.index(self.zona)
        self.ubicacion.enemigos_activos[zona].remove(asistente)
        nuevo = Asistente(asistente.salud_max, asistente.fuerza,
                          asistente.resistencia, asistente.carisma_max,
                          asistente.inteligencia, asistente.sabiduria,
                          asistente.nombre, asistente.condicion,
                          asistente.dropeo, asistente.categoria,
                          asistente.rango, asistente.cantidad,
                          asistente.zona, self, nombre)
        self.asistentes.append(nuevo)
        return True
                
    
    def cambiar_dueno(self, asistente):
        personajes_temp = []
        for p in gm.personajes:
            if(p.zona == self.zona):
                personajes_temp.append(p)
        personajes_temp.remove(self)
        
        if(personajes_temp != []):
            print("�Con quien vas a intercambiar asistentes?")
            for p in range(0, len(personajes_temp)):
                print(f"{p+1}: {personajes_temp[p].nombre} \t espacio libre: "
                      + f"{personajes_temp[p].espacio_asistentes}")
            print(f"{len(personajes_temp) + 1}: No pues ya no")
            decision = int(input()) - 1
            if(decision == len(personajes_temp)):
                return False
            else:
                for a in range(0, len(personajes_temp[decision].asistentes)):
                    print(f"{a+1}: "
                          + f"{personajes_temp[decision].asistentes[a].apodo}"
                          + " \t espacio ocupado: "
                          + f"{personajes_temp[decision].asistentes[a].rango}")
                print(f"{len(self.asistentes)+1}: Ninguno")
                decision2 = int(input()) - 1
                if(decision2 == len(personajes_temp)):
                    resultado = personajes_temp[decision].reclutar(asistente)
                    if(resultado):
                        self.liberar(asistente)
                        return True
                    else:
                        return False
                else:
                    espacio1 = asistente.rango
                    espacio2 = personajes_temp[decision].asistentes[decision2]
                    espacio2 = espacio2.rango
                    if(self.espacio_asistentes + espacio1 - espacio2 >= 0 
                       and ((personajes_temp[decision].espacio_asistentes 
                       + espacio2 - espacio1) >= 0)):
                        a1 = asistente
                        a2 = personajes_temp[decision].asistentes[decision2]
                        self.liberar(asistente)
                        person = personajes_temp[decision]
                        asistentes = person.asistentes[decision2]
                        personajes_temp[decision].decision(asistentes)
                        personajes_temp[decision].reclutar(a1)
                        self.reclutar(a2)
                        return True
                    else:
                        print("No se puede shavo")
                        return False
        else:
            print("Estas solito no hay nadie aqui a tu lado")
            return False
    
    
    def liberar(self, asistente):
        self.asistentes.remove(asistente)
        self.espacio_asistentes += asistente.rango
        return True
    
    
    def explorar(self):
        conocidos = self.mapa[self.zona]
        posibles = gm.mapa_master[self.zona]
        for z in posibles:
            if z not in conocidos:
                print(f"Felicidades! {self.nombre} ha descubierto {z}!!")
                self.mapa[self.zona].append(z)
                self.mapa.update({z: [self.zona]})
                return self.mapa
        print(f"{self.nombre}, parece que "
              + "ya has descubierto todo de esta zona")
        return False
    
    def activar_habilidad(self, llave, cancel = []):
        estadisticas = ["Salud", "Fuerza", "Resistencia", "Carisma",
                        "Inteligencia", "Sabiduria", "Energia"]
        if(llave != "anticipacion"):
            print("�Que habilidad quieres activar? (0 para salir)")
            print("HABILIDAD\tCOSTO")
            for a in self.arbol:
                for n in range(0, len(gm.habilidades[llave])):
                    habilidad = list(gm.habilidades[llave].keys())[n]
                    if(habilidad in self.arbol[a][2] 
                       and self.arbol[a][0] == 1):
                        gm_hab = gm.habilidades[llave]
                        gm_hab = gm_hab[list(gm.habilidades[llave].keys())[n]]
                        print(f"{a}: {self.arbol[a][2]}:\t"
                              + f"{gm_hab}")
            hab = input()
            if(hab == "0"):
                return [False, False]
            elif(hab not in self.arbol):
                return [False, False]
            print(self.arbol)
        else:
            llave = "Turno enemigo"
            hab = "Anticipacion"
            
# =============================================================================
#         Costo de habilidad en llave, en self.arbol[hab][2] 
#         (nombre de la habilidad)
# =============================================================================
        costo = gm.habilidades[
            llave][list(gm.habilidades[llave].keys())[gm.habilidades[
                llave][list(gm.habilidades[
                    llave].keys()).index(self.arbol[hab][2])]]]
        print(f"Habilidad: {self.arbol[hab][2]}\n Costo: {costo}")
        
        if(self.energia < costo):
            print("Estas muy cansado para esto")
            return [False, False]
        else:
            print(f"Se ha activado {self.arbol[hab][2]}")
            self.energia -= costo
            
            if(self.arbol[a][2] == "Sabiduria del mas alla"):
                gm.anadir_obj_manual(gm.norman, "Nota de consejo sabia")
                
            elif(self.arbol[a][2] == "Pociones"):
                lista = []
                for i in gm.crafteos:
                    for o in self.inventario:
                        if o in i:
                            lista.append(i)
                for o in lista:
                    print(o + ": " + gm.crafteos[o])
                    
            elif(self.arbol[a][2] == "Boosteo"):
                print("�A quien deseas boostear?")
                for p in range(0, len(gm.personajes)):
                    print(f"{p + 1}: {gm.personajes[p].nombre}")
                
                objetivo = int(input()) - 1
                
                print("�Que estadistica deseas boostear?")
                for e in range(0, len(estadisticas)):
                    print(f"{e + 1}: {estadisticas[e]}")
                decision = int(input()) - 1
                
                cantidad = int(input("�Cu�nto boosteo quieres darle? (max 9)"))

                if(self.energia < cantidad):
                    cantidad = self.energia
                if(decision == 0):
                    gm.personajes[objetivo].cambiar_hp(cantidad)
                else:
                    condicion = estadisticas[decision] + str(cantidad)
                    gm.personajes[objetivo].condicion.update({condicion: 3})
                    if(decision == 1):
                        gm.personajes[objetivo].fuerza += cantidad
                    elif(decision == 2):
                        gm.personajes[objetivo].resistencia += cantidad
                    elif(decision == 3):
                        gm.personajes[objetivo].carisma += cantidad
                    elif(decision == 4):
                        gm.personajes[objetivo].inteligencia += cantidad
                    elif(decision == 5):
                        gm.personajes[objetivo].sabiduria += cantidad
                    elif(decision == 6):
                        gm.personajes[objetivo].energia += cantidad
 
            elif(self.arbol[a][2] == "Disfraz"):
                print("�De quien te vas a disfrazar?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                objetivo.enfermar("Confundido", 3)
                
            elif(self.arbol[a][2] == "Carisma absoluta"):
                print("�A quien vas a pacificar?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                objetivo.mover_enemigo(self.zona)
                
            elif(self.arbol[a][2] == "Grito de guerra"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    objetivo = self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)][enemigo]
                    objetivo.enfermar("Confundido", 3)
                    cancel.append(objetivo)
                    
            elif(self.arbol[a][2] == "Habilidad animal"):
                animales = []
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    objetivo = self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)][enemigo]
                    if(objetivo.categoria == "Animal"):
                        animales.append(objetivo)
                
                print("�A quien te vas a ratear?")
                
                for animal in range(0, len(animales)):
                    print(f"{animal + 1}: animales[animal].nombre")
                victima = animales[int(input()) - 1]
                
                print("�Que estadistica deseas copiar?")
                for e in range(0, len(estadisticas)):
                    print(f"{e + 1}: {estadisticas[e]}")
                decision = estadisticas[int(input()) - 1]
                
                if(decision == "Salud"):
                    self.cambiar_hp(victima.salud)
                elif(decision == "Fuerza"):
                    if(victima.fuerza > self.fuerza):
                        self.condicion.update({decision 
                                               + str(victima.fuerza 
                                                     - self.fuerza): 3})
                        self.fuerza = victima.fuerza
                    else:
                        self.condicion.update({decision 
                                               + str(victima.fuerza): 3})
                        self.fuerza += victima.fuerza
                elif(decision == "Resistencia"):
                    if(victima.resistencia > self.resistencia):
                        self.condicion.update({decision 
                                               + str(victima.resistencia 
                                                     - self.resistencia): 3})
                        self.resistencia = victima.resistencia
                    else:
                        self.condicion.update({decision
                                               + str(victima.resistencia): 3})
                        self.resistencia += victima.resistencia
                elif(decision == "Carisma"):
                    if(victima.carisma > self.carisma):
                        self.condicion.update({decision
                                               + str(victima.carisma 
                                                     - self.carisma): 3})
                        self.carisma = victima.carisma
                    else:
                        self.condicion.update({decision
                                               + str(victima.carisma): 3})
                        self.carisma += victima.carisma
                elif(decision == "Inteligencia"):
                    if(victima.inteligencia > self.inteligencia):
                        self.condicion.update({decision
                                               + str(victima.inteligencia 
                                                     - self.inteligencia): 3})
                        self.inteligencia = victima.inteligencia
                    else:
                        self.condicion.update({decision
                                               + str(victima.inteligencia): 3})
                        self.inteligencia += victima.inteligencia
                elif(decision == "Sabiduria"):
                    if(victima.sabiduria > self.sabiduria):
                        self.condicion.update({decision 
                                               + str(victima.sabiduria 
                                                     - self.sabiduria): 3})
                        self.sabiduria = victima.sabiduria
                    else:
                        self.condicion.update({decision
                                               + str(victima.sabiduria): 3})
                        self.sabiduria += victima.sabiduria
                elif(decision == "Energia"):
                    if(victima.energia > self.energia):
                        self.condicion.update({decision 
                                               + str(victima.energia 
                                                     - self.energia): 3})
                        self.energia = victima.energia
                    else:
                        self.condicion.update({decision 
                                               + str(victima.energia): 3})
                        self.energia += victima.energia
            elif(self.arbol[a][2] == "Invocar animal"):
                oso = Asistente(65, 19, 19, 19, 5, 17, "Oso", "Saludable",
                                "Pelaje", "Animal", 5, 1, self.zona,
                                self, "Oso")
                oso.condicion.update({"Lealtad": 5})
                self.asistentes.append(gm.nuevo)
            elif(self.arbol[a][2] == "Special curry"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    enemigo.enfermar("Quemado", 3)
            elif(self.arbol[a][2] == "Kaio ken" 
                 and llave == "Turno personaje"):
                self.condicion.update({"Kaio Ken": 3})
            elif(self.arbol[a][2] == "Ultra instinto" 
                 and llave == "Turno personaje"):
                self.condicion.update({"Ultra instinto": 3})
            elif(self.arbol[a][2] == "Analitico"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(enemigo.stats())
            elif(self.arbol[a][2] == "Momazo"):
                print("�A quien vas a trollear?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                cancel.append(objetivo)
            elif(self.arbol[a][2] == "Meme de enemigos"):
                print("�A quien vas buliear?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                objetivo.carisma -= Juego.dados(1, objetivo.carisma//2)
            elif(self.arbol[a][2] == "Lord meme"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    enemigo.carisma -= Juego.dados(1, objetivo.carisma//2)
                    cancel.append(enemigo)                
            elif(self.arbol[a][2] == "Robots"):
                robot = Asistente(25, 11, 7, 9, 15, 15, "Robot", "Saludable",
                                  "Tornillo", "Robot", 2, 1, self.zona, self,
                                  "Robot")
                robot.condicion.update({"Lealtad": 5})
                self.asistentes.append(gm.nuevo)
            elif(self.arbol[a][2] == "Llamar al viento"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    self.atacar(enemigo, 2)
                for p in range(0, len(gm.personajes)):
                    if(p.zona == self.zona and p != self):
                        self.atacar(p, 2)
            elif(self.arbol[a][2] == "Mente dormida"):
                eleccion = int(input("�Deseas atacar a todos (0) o a uno "
                                     + "(1)?\n"))
                if(eleccion == 0):
                    for enemigo in range(0, len(
                            self.ubicacion.enemigos_activos[
                                self.ubicacion.zonas.index(self.zona)])):
                        self.atacar(enemigo, 1.5)
                else:
                    print("�A quien vas a atacar?")
                    for enemigo in range(0, len(
                            self.ubicacion.enemigos_activos[
                                self.ubicacion.zonas.index(self.zona)])):
                        print(f"{enemigo + 1}: "
                              + str(self.ubicacion.enemigos_activos[
                                  self.ubicacion.zonas.index(self.zona)][
                                      enemigo].nombre))
                    objetivo = self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)][int(input())-1]
                    self.atacar(objetivo, 3)
            elif(self.arbol[a][2] == "Anticipacion"):
                return [True, False]
            elif(self.arbol[a][2] == "Explorador" 
                 and llave == "Iniciar pelea"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                        print(str(self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)][
                                enemigo].nombre))
            elif(self.arbol[a][2] == "Smash ball"):
                tirada = Juego.dados(1, 2)
                if(tirada == 1):
                    objetivo, dano, arma = gm.atacar(
                        self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)], 5)
                else:
                    objetivo, dano, arma = gm.atacar(
                        self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)])
                    self.cambiar_hp(-dano * 3)
                    dano = 0
                # aplicar el ataque en turno personaje
                self.energia -= gm.habilidades[llave][self.arbol[a][2]]
                return [True, [objetivo, dano, arma]]
            elif(self.arbol[a][2] == "Artesano"):
                resultado = self.craftear()
                quitar = False
                for obj in self.inventario_nombres:
                    for ing in resultado[1]:
                        if(ing.nombre == obj):
                            self.inventario.pop(
                                self.inventario_nombres.index(obj))
                            quitar = True
                if(quitar):
                    Juego.maquina(resultado[2], self)
            elif(self.arbol[a][2] == "Alquimista"):
                print("Que quieres mejorar?")
                for obj in range(0, len(self.inventario_nombres)):
                    print("{obj + 1}: self.inventario_nombres[obj]")
                objeto = self.inventario[int(input()) - 1]
                Juego.maquina(objeto.nombre, self, 0.5)
        self.energia -= gm.habilidades[llave][self.arbol[a][2]]
        return [True, False]
    
    def equipar(self, o: Objeto):
        lugares = []
        lugar = ""
        espalda = ""
        for e in self.equipo:
            if(e.nombre in gm.cabeza):
                lugares.append("cabeza")
            elif(e.nombre in gm.cara):
                lugares.append("cara")
            elif(e.nombre in gm.cuello):
                lugares.append("cuello")
            elif(e.nombre in gm.torso):
                lugares.append("torso")
            elif(e.nombre in gm.espalda):
                lugares.append("espalda")
                espalda = e
            elif(e.nombre in gm.piernas):
                lugares.append("piernas")
            elif(e.nombre in gm.pies):
                lugares.append("pies")
            elif(e.nombre in gm.cuerpo_completo):
                lugares.append("cuerpo_completo")
        if(o.nombre in gm.cabeza):
            lugar = "cabeza"
        elif(o.nombre in gm.cara):
            lugar = "cara"
        elif(o.nombre in gm.cuello):
            lugar = "cuello"
        elif(o.nombre in gm.torso):
            lugar = "torso"
        elif(o.nombre in gm.espalda):
            lugar = "espalda"
        elif(o.nombre in gm.piernas):
            lugar = "piernas"
        elif(o.nombre in gm.pies):
            lugar = "pies"
        elif(o.nombre in gm.cuerpo_completo):
            lugar = "cuerpo_completo"
        if(o.nombre in gm.cuerpo_completo):
            for e in range(0, len(self.equipo)):
                print(self.equipo[0].nombre)
                indio = self.equipo.index(self.equipo[0])
                if(self.equipo[0].estadistica == "F"):
                    self.fuerza -= self.equipo[0].boosteo
                elif(self.equipo[0].estadistica == "R"):
                    self.resistencia -= self.equipo[0].boosteo
                elif(self.equipo[0].estadistica == "C"):
                    self.carisma -= self.equipo[0].boosteo
                elif(self.equipo[0].estadistica == "I"):
                    self.inteligencia -= self.equipo[0].boosteo
                elif(self.equipo[0].estadistica == "S"):
                    self.sabiduria -= self.equipo[0].boosteo
                elif(self.equipo[0].estadistica == "V"):
                    if(self.zona in gm.agua):
                        self.velocidad -= self.equipo[0].boosteo
                print(f"{self.nombre} se ha quitado {self.equipo[0].nombre}")
                self.quitar_equipo(self.equipo[0])
                self.equipo.pop(0)
                self.equipo_nombres.pop(0)
            if(espalda != ""):
                self.equipar(espalda)
        elif(lugar in lugares):
            indio = lugares.index(lugar)
            if(self.equipo[indio].estadistica == "F"):
                self.fuerza -= self.equipo[indio].boosteo
            elif(self.equipo[indio].estadistica == "R"):
                self.resistencia -= self.equipo[indio].boosteo
            elif(self.equipo[indio].estadistica == "C"):
                self.carisma -= self.equipo[indio].boosteo
            elif(self.equipo[indio].estadistica == "I"):
                self.inteligencia -= self.equipo[indio].boosteo
            elif(self.equipo[indio].estadistica == "S"):
                self.sabiduria -= self.equipo[indio].boosteo
            elif(self.equipo[indio].estadistica == "V"):
                self.velocidad -= self.equipo[indio].boosteo
            print(f"{self.nombre} se ha quitado {self.equipo[indio].nombre}")
            self.quitar_equipo(self.equipo[indio])
            self.equipo.pop(indio)
            self.equipo_nombres.pop(indio)
        
        self.equipo.append(o)
        self.equipo_nombres.append(o.nombre)
        indie = self.inventario.index(o)
        if(o.estadistica == "F"):
            self.fuerza += o.boosteo
        elif(o.estadistica == "R"):
            self.resistencia += o.boosteo
        elif(o.estadistica == "C"):
            self.carisma += o.boosteo
        elif(o.estadistica == "I"):
            self.inteligencia += o.boosteo
        elif(o.estadistica == "S"):
            self.sabiduria += o.boosteo
        elif(o.estadistica == "V"):
            if(self.zona in gm.agua):
                self.velocidad += o.boosteo
        print(f"{o.nombre} equipado !!")
        if("Shaed" in o.nombre):
            self.condicion.update({'Invisible': 10})
        self.anadir_equipo(o, indie)
        
        self.actualizar_stats()
        print("--------------------------------------------------------------")
    
    def desequipar(self):
        print("�Que objeto quieres desequiparte?")
        for e in range(0, len(self.equipo_nombres)):
            print(f"{e+1}: {self.equipo_nombres[e]} | "
                  + f"{self.equipo[e].estadistica}: {self.equipo[e].boosteo}")
        print(f"{len(self.equipo_nombres)+1}: Salir")    
        o = int(input())
        if(o == len(self.equipo_nombres)+1):
            return False
        if(self.equipo[o-1].estadistica == "F"):
            self.fuerza -= self.equipo[o-1].boosteo
        elif(self.equipo[o-1].estadistica == "R"):
            self.resistencia -= self.equipo[o-1].boosteo
        elif(self.equipo[o-1].estadistica == "C"):
            self.carisma -= self.equipo[o-1].boosteo
        elif(self.equipo[o-1].estadistica == "I"):
            self.inteligencia -= self.equipo[o-1].boosteo
        elif(self.equipo[o-1].estadistica == "S"):
            self.sabiduria -= self.equipo[o-1].boosteo
        elif(self.equipo[o-1].estadistica == "V"):
            if(self.zona in gm.agua):
                self.velocidad -= self.equipo[o-1].boosteo
        print(f"{self.nombre} se ha quitado {e.nombre}")
        self.quitar_equipo(e)
        self.equipo.pop(o-1)
        self.equipo_nombres.pop(o-1)
        
        self.actualizar_stats()
        print("--------------------------------------------------------------")
        return True
    
    def arbol_habilidades(self):
        print('{:-^70}'.format('Arbol de habilidades'))
        print(f"Puntos de habilidad disponibles: {self.puntos_habilidad}")
        print("COSTO\t\t\t\t    __________ \t\t\t\t\n\t\t\t\t   | "
              + f"{self.nombre} |\n\t\t\t\t    __________ \t\t\t\t\n")
        print("\t\t\t\t/\t\t  \\")
        repetir = False
        for i in range(1, 4):
            print("\t\t\t        |\t\t  |")
            llave = "A"+str(i)
            if(self.arbol[llave][0] == 0):
                print(f"{self.arbol[llave][1]}\t\t\t      |{llave}|\t", end="")
            else:
                print(f"{self.arbol[llave][1]}\t\t\t      |"
                      + f"{self.arbol[llave][2]}|\t", end="")
            llave = "B"+str(i)
            if(self.arbol[llave][0] == 0):
                print(f"\t|{llave}|")
            else:
                print(f"\t|{self.arbol[llave][2]}|")
        seleccion = input("�Que habilidad deseas desbloquear? "
                          + "(0 para salir)\n")
        if(seleccion == "0"):
            return False
        elif(seleccion not in self.arbol.keys()):
            print("Eso no existe")
            self.arbol_habilidades()
        elif(int(seleccion[1]) > 1):
            for j in range(1, int(seleccion[1])+1):
                if(self.arbol[seleccion[0]+str(j)][0] == 0):
                    print("No te quieras adelantar >:(")
                    repetir = True
                    break
            if(repetir):
                self.arbol_habilidades()
        elif(self.arbol[seleccion][1] > self.puntos_habilidad):
            print("No tienes puntos de habilidad suficientes")
            self.arbol_habilidades()
        else:
            print(f"Has desbloqueado {self.arbol[seleccion][2]}!!")
            self.arbol[seleccion][0] = 1
            self.puntos_habilidad -= self.arbol[seleccion][1]
            if(self.arbol[seleccion][2] == "Super Sayain"):
                self.condicion.update({"Super Sayain": self.fuerza})
            return True
            
    def subir_salud_max(self):
        #DEBUG
#    print("----------------------------------------Metodo subir salud maxima")
        self.salud_max+=15
        self.energia_max+=4
        print("Tu salud y energ�a han aumentado!!")
        self.actualizar_stats()
        return True
    
    def is_ded(self):
        #DEBUG
#        print("------------------------------------------------Metodo is_ded")
        zonas = self.ubicacion.zonas
        z = zonas.index(self.zona)
        self.condicion = {"Muerto": 1}
        gm.personajes_muertos.append(self)
        gm.personajes.remove(self)
        o = Juego.tranformar_objeto("Cadaver de "+self.nombre)
        o.stats()
        self.ubicacion.objetos_activos[z].append(o)
#        self.ubicacion.cantidades_objetos_activos[z].append(1)
        self.ubicacion.objetos[z].append(o.nombre)
        self.ubicacion.cantidades[z].append(1)
        
        if(self != gm.personaje_malo):
            for i in self.inventario:
                self.ubicacion.objetos_activos[z].append(i)
                if(i.nombre not in self.ubicacion.objetos[z]):
                    self.ubicacion.objetos[z].append(i.nombre)
                    self.ubicacion.cantidades[z].append(1)
                else:
                    indi = self.ubicacion.objetos[z].index(i.nombre)
                    self.ubicacion.cantidades[z][indi] += 1
            self.inventario = []
            self.inventario_nombres = []
            for e in self.equipo:
                self.ubicacion.objetos_activos[z].append(e)
                if(e.nombre not in self.ubicacion.objetos[z]):
                    self.ubicacion.objetos[z].append(e.nombre)
                    self.ubicacion.cantidades[z].append(1)
                else:
                    indi = self.ubicacion.objetos[z].index(e.nombre)
                    self.ubicacion.cantidades[z][indi] += 1
            self.equipo = []
            self.equipo_nombres = []
            self.cartera_obj = {}
            self.cartera = 0
        return True
    
    def usar_maquina(self):
        print("�Que objeto deseas insertar?(0 para salir)")
        print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
        i=0
        for llave in self.cartera_obj:
            print(f"{i+1}, \t{llave:.<24s}: {self.cartera_obj[llave]} | "
                  + "\t\t"
                  + str(self.inventario[
                      self.inventario_nombres.index(llave)].estadistica)
                  + "| \t"
                  + str(self.inventario[
                      self.inventario_nombres.index(llave)].boosteo))
            i+=1
        
        obj = int(input())-1
        if(obj == -1):
            return False
        for llave in self.cartera_obj:
            if(obj == 0):
                break
            obj -= 1
        objeto = self.inventario[self.inventario_nombres.index(llave)]
        return Juego.maquina(objeto.nombre, self)
    
    def anadir_obj(self, objeto):
        #DEBUG
#        print("-----------------------------------------Metodo anadir objeto")
        if(self.is_wendigo):
            if(type(objeto) == int):
                print("Nel")
                return False
            if("Carne" not in objeto.nombre):
                print("Nel")
                return False
                
        if(type(objeto) == Objeto):
            objetos = self.ubicacion.objetos_activos
            objetos_nombres = []
            zonas = self.ubicacion.zonas
            z = zonas.index(self.zona)
            for i in range (0, len(objetos)):
                objetos_nombres.append([])
                for j in range (0, len(objetos[i])):
                    objetos_nombres[i].append(objetos[i][j].nombre)
    #        print(objetos_nombres)
    #        print(objeto.nombre)
            j = objetos_nombres[z].index(objeto.nombre)
    #        print(self.ubicacion.objetos[z])
            h = self.ubicacion.objetos[z].index(objeto.nombre)
            self.ubicacion.cantidades[z][h] -= 1
    #        self.ubicacion.cantidades_objetos_activos[z][j] -= 1
            objeto = objetos[z][j]
            if(objeto.nombre == "Cartucho de magnum"):
                for b in range(0, 16):
                    gm.anadir_obj_manual("Bala de magnum", self)
                return True
            elif(objeto.nombre == "Cartucho de sniper"):
                for b in range(0, 6):
                    gm.anadir_obj_manual("Bala de sniper", self)
                return True
# =============================================================================
#              print(self.ubicacion.cantidades_objetos_activos()[z][j])
#              print(self.ubicacion.cantidades_objetos_activos()[z])
#              print(f'\nFelicidades!! Obtuviste {objeto.nombre}, quedan
#              {self.ubicacion.cantidades()[z][h]} restantes')
# =============================================================================
            ind = objetos_nombres[z].index(objeto.nombre)
            objetos_nombres[z].remove(objeto.nombre)
            if(self.ubicacion.cantidades[z][h] <= 0):
                self.ubicacion.objetos_activos[z].pop(ind)
                self.ubicacion.objetos[z].pop(h)
                self.ubicacion.cantidades[z].pop(h)
    #            self.ubicacion.cantidades_objetos_activos[z].pop(ind)
            self.quitar_equipo(objeto)
            
            self.actualizar_stats()
            self.exceso_peso()
            print(f"Has encontrado {objeto.nombre}!!")
        else:
            print(f"Has encontrado {objeto} dineros en el suelo!!")
            self.cartera += objeto
        self.stats()
        return True
        
    def usar_obj(self, target = None, objeto = None):
        robots = ["Sub Bismark"]
        borrachos = ["Alumno Pasio", "Mentor Pasio", "Policia",
                     "Guardabosques", "Pueblerino", "Obrero", "Burgues"]
        #DEBUG
#    print("-----------------------------------------------Metodo usar objeto")
        self.energia += self.energia_max * 0.2
        print("Has recuperado el 20% de energia")
        if(self.energia > self.energia_max):
            self.energia = self.energia_max
            
        if(len(self.inventario) <= 0):
            print("Stas pobre")
            return False
        
        if(objeto == None):
            objetos_permitidos = []
            for i in range(0, len(self.inventario)):
                if(self.inventario[i].estadistica != "F" 
                   or "Pocion" in self.inventario_nombres[i]):
                    objetos_permitidos.append(self.inventario[i].nombre)
            
            print("�Que quieres usar?")
            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
            i=0
            for llave in self.cartera_obj:
                if(llave in objetos_permitidos):
                    print(f"{i+1}, \t{llave:.<24s}: {self.cartera_obj[llave]} "
                          + "| \t\t"
                          + str(self.inventario[self.inventario_nombres.index(
                                  llave)].estadistica)
                          + "| \t"
                          + str(self.inventario[self.inventario_nombres.index(
                              llave)].boosteo))
                    i+=1
            
            obj = int(input())-1
            for llave in self.cartera_obj:
                if(llave in objetos_permitidos):
                    if(obj == 0):
                        break
                    obj -= 1
            objeto = self.inventario[self.inventario_nombres.index(llave)]
            
        if(objeto.nombre not in self.inventario_nombres):
            print("Pues no tienes eso shavo")
            return False
        
        for i in range(0, len(gm.Dfnombres_o)):
            if(gm.Dfnombres_o.iloc[i,0] == objeto.nombre):
                break
            
        zonas = self.ubicacion.zonas
        z = zonas.index(self.zona)
        if(target == None):
            print("�Con qui�n lo quieres usar?")
            for p in range(0, len(gm.personajes)):
                if(gm.personajes[p].zona == self.zona):
                    print(f"{p+1}: {gm.personajes[p].nombre}")
            target = gm.personajes[int(input())-1]
        if(type(target) == str):
            for y in gm.personajes_muertos:
                if(y.nombre in target):
                    target = y
                    break
            limite = 13 + 5 * (target.nivel)
        elif(target in gm.personajes):
            for y in gm.personajes:
                if(y.nombre == target):
                    target = y
                    break
            limite = 13 + 5 * (target.nivel)
        elif(target in self.ubicacion.enemigos_activos[z]):
            for y in self.ubicacion.enemigos_activos[z]:
                if(y.nombre == target):
                    target = y
                    break
        elif(type(target) == list):
            targets = [[],[]]
            for t in target:
                if(t in gm.personajes):
                    targets[0].append(t)
                elif(t in self.ubicacion.enemigos_activos[z]):
                    targets[1].append(t)
            if(targets == [[],[]]):
                print("No se encontraron los target")
                return False
        else:
            print("No se encontr� el target")
            return False
            
        # -----------------------------------------------------Objetos perrones
        Dfstat_o = gm.Dfstats_o.iloc[i,0]
        
        cantidad = int(gm.Dfboosts_o.iloc[i,0])
        
        if("Sustancia" in objeto.nombre):
            ind = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, ind)
            pociones = ["Pocion fuerza", "Pocion resistencia",
                        "Pocion carisma", "Pocion inteligencia",
                        "Pocion sabiduria", "Pocion invisibilidad",
                        "Pocion velocidad", "Pocion energia", "Veneno"]
            pocion = pociones[Juego.dados(1, len(pociones))[0]-1]
            if("III" in objeto.nombre):
                pocion += " III"
            elif("II" in objeto.nombre):
                pocion += " II"
            else:
                pocion += " I"
            objeto = Juego.transformar_objeto(pocion)
            self.quitar_equipo(objeto)
            
        if(objeto.nombre in gm.equipables):
            self.equipar(objeto)
            return True
        
        elif(objeto.nombre == "Mapa"):
            for m in range(0, 3):
                self.explorar()
        
        elif(objeto.nombre == "GPS"):
            conocidos = self.mapa[self.zona]
            posibles = gm.mapa_master[self.zona]
            print(f"Utilizando GPS... existen {len(posibles) - len(conocidos)}"
                  + " lugares sin descubrir")
        
        elif(objeto.nombre == "Brujula"):
            if(self.ubicacion.nombre == "campamento"):
                print("La brujula esta vuelta loca...")
            else:
                conocidos = self.mapa[self.zona]
                for j in conocidos:
                    if(j in gm.jefes.values()):
                        print(f"Dentro de {j} se siente una presencia"
                              + " muy maligna...")
                        break
        
        elif(objeto.nombre == "Carnada") and (target.nombre 
                                              not in gm.jefes.keys()):
            print(type(target.condicion))
            target.condicion.update({"Oloroso": 2})
            conocidos = gm.mapa_master[self.zona]
            print(gm.carneables)
            for c in conocidos:
                for l in range(0, len(gm.lugares_o)):
                    lug = gm.lugares_o[l].zonas
                    if(c in lug):
                        lugar = gm.lugares_o[l]
                        break
                # ----------------------------lugar = objeto lugar de la zona c
                for e in lugar.enemigos_activos[lugar.zonas.index(c)]:
                    print(e.nombre)
                    if(e.nombre in gm.carneables):
                        lugar.enemigos_activos[
                            lugar.zonas.index(c)].remove(e)
                        self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)].append(e)
                        e.condicion.update({"Atraido": 2})
                        e.zona = self.zona
                        print(f"La carnada ha atraido a un {e.nombre} "
                              + "salvaje...")
                        break
        
        elif(objeto.nombre == "Control universal"):
            if("Pila" in self.inventario_nombres):
                if(target.nombre in robots):
                    self.peso -= gm.Dfespacios_o.iloc[i,0]
                    indio = self.inventario_nombres.index("Pila")
                    self.inventario.pop(indio)
                    self.inventario_nombres.pop(indio)
                    return {"Control universal": target.defender()}
                self.peso -= gm.Dfespacios_o.iloc[i,0]
                indio = self.inventario_nombres.index("Pila")
                self.inventario.pop(indio)
                self.inventario_nombres.pop(indio)
                print("Felicidades!! Has gastado una pila a lo tonto :D")
                return True
            print("Oh no! Tu control ya no tiene bateria!! :(")
            return True
        
        elif(objeto.nombre == "Alcohol"):
            if(target.nombre in borrachos):
                self.peso -= gm.Dfespacios_o.iloc[i,0]
                indio = self.inventario_nombres.index("Alcohol")
                self.inventario.pop(indio)
                self.inventario_nombres.pop(indio)
                return {"Alcohol": target.defender()}
            print("Al enemigo no le interesa tu alcohol barato...")
            return True
        
        elif(objeto.nombre == "Binoculares" or objeto.nombre == "Sniper"):
            print("�A donde deseas mirar?")
            for i in range(0, len(self.mapa[self.zona])):
                print(f"{i+1}: {self.mapa[self.zona][i]}")
            zona = int(input())
            zona= self.mapa[self.zona][zona - 1]
            for l in range(0, len(gm.lugares_o)):
                lug = gm.lugares_o[l].zonas
                if(zona in lug):
                    ubicacion = gm.lugares_o[l]
                    break
            indio = ubicacion.zonas.index(zona)
            for e in ubicacion.enemigos_activos[indio]:
                print(f"Puedes ver un {e.nombre} salvaje acechando"
                      + " a lo lejos...")
            if("Sniper" in objeto.nombre 
               and "Bala de sniper" in self.inventario_nombres):
                print("�A quien quieres dispararle los sesos con el sniper?")
                print("INDICE \t NOMBRE \t SALUD")
                print("0: Nadie")
                for i in range (0, len(ubicacion.enemigos_activos[indio])):
                    print(f"{i+1}: "
                          + str(ubicacion.enemigos_activos[indio][i].nombre)
                          + "\t"
                          + str(ubicacion.enemigos_activos[indio][i].salud))
                ind = int(input())-1
                objetivo = ubicacion.enemigos_activos[indio][ind]
                if(ind <= -1):
                    return False
                else:
                    print("Tirando dados...")
                    da2 = gm.dados(1, 10)[0]
                    print("Tiraste "+str(da2))
                    dano = self.fuerza + int(objeto.boosteo) + da2
                    tirada = gm.dados(1, 10)[0]
                    if(tirada >= 4):
                        dano = 0
                        print("Has fallado tu ataque!")
                    objetivo.cambiar_hp(-dano, self)
                    indio = self.inventario_nombres.index("Bala de sniper")
                    self.anadir_equipo(self.inventario[indio], indio)
            else:
                print("No tienes municion :o")
                return False
            return True
        
        elif("humana" in objeto.nombre):
            self.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
            if(self.salud > self.salud_max):
                self.salud = self.salud_max
            self.actualizar_stats()
            if(self.is_wendigo):
                self.cambiar_hp(gm.Dfboosts_o.iloc[i,0]*4)
                if(self.salud > self.salud_max):
                    self.salud = self.salud_max
                self.actualizar_stats()
            if(self.ubicacion == gm.montana):
                print("Descripcion perra de conversion a Wendigo wuuuu")
                self.is_wendigo = True
                self.salud_max *= 3
                self.salud = self.salud_max
                self.fuerza *= 3
                self.resistencia *= 3
                self.carisma /= 2
                self.inteligencia /= 2
                self.sabiduria /= 2
                carnes = []
                ind = self.inventario_nombres.index(objeto.nombre)
                self.inventario.pop(ind)
                for i in self.inventario:
                    if("Carne" in i.nombre):
                        carnes.append(i)
                    self.ubicacion.objetos_activos[z].append(i)
                    self.ubicacion.objetos[z].append(i.nombre)
                    self.ubicacion.cantidades[z].append(1)
                self.inventario = []
                self.inventario_nombres = []
                for e in self.equipo:
                    self.ubicacion.objetos_activos[z].append(e)
                    self.ubicacion.objetos[z].append(e.nombre)
                    self.ubicacion.cantidades[z].append(1)
                self.equipo = []
                self.equipo_nombres = []
                self.cartera_obj = {}
                self.cartera = 0
                for c in carnes:
                    print(c.nombre)
                    self.anadir_obj(c)
                self.actualizar_stats()
                return True
        
        elif("Gasolina" in objeto.nombre or "Aceite" in objeto.nombre 
             or "Alcohol" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Le has hechado gasolina a todos tus companeros, "
                      + "maravillosa jugada! :D")
                for t in targets[0]:
                    if("Quemado" in t.condicion):
                        t.enfermar("Quemado", 3)
                    else:
                        t.condicion.update({"Engasolinado": 2})
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Te has resbalado y echado gasolina tu solo, "
                      + "que egoista...")
                if("Quemado" in self.condicion):
                    self.enfermar("Quemado", 3)
                else:
                    self.condicion.update({"Engasolinado": 2})
            elif(tirada <= 10):#-------------------------------------Un enemigo
                t = targets[1][Juego.dados(1, len(targets[1]))[0]-1]
                print(f"Le has hechado gasolina a {t.nombre}, no se ve"
                      + " muy feliz...")
                if("Quemado" in t.condicion):
                    t.enfermar("Quemado", 3)
                else:
                    t.condicion.update({"Engasolinado": 2})
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Has banado el suelo con gasolina!")
            elif(tirada <= 18):#------------------------------------------Todos
                print("Haces un mortal triple y riegas gasolina a todos")
                for f in targets:
                    for t in f:
                        if("Quemado" in t.condicion):
                            t.enfermar("Quemado", 3)
                        else:
                            t.condicion.update({"Engasolinado": 2})
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("No se como le hiciste, pero banaste a todos tus "
                      + "rivales")
                for t in targets[1]:
                    if("Quemado" in t.condicion):
                        t.enfermar("Quemado", 3)
                    else:
                        t.condicion.update({"Engasolinado": 2})
        
        elif("Fosforo" in objeto.nombre or "Antorcha" in objeto.nombre 
             or "Encendedor" in objeto.nombre):
            for f in targets:
                for t in f:
                    if("Engasolinado" in t.condicion):
                        t.enfermar("Quemado", 3)
        
        elif("Lodo" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Le has hechado lodo a todos tus companeros, "
                      + "maravillosa jugada! :D")
                for t in targets[0]:
                    t.condicion.update({"Cegado": 1})
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Te has resbalado y echado lodo tu solo, que egoista...")
                self.condicion.update({"Cegado": 1})
            elif(tirada <= 10):#-------------------------------------Un enemigo
                t = targets[1][Juego.dados(1, len(targets[1]))[0]-1]
                print(f"Le has hechado lodo a {t.nombre}, no se ve "
                      + "muy feliz...")
                t.condicion.update({"Cegado": 1})
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Has banado el suelo con lodo!")
            elif(tirada <= 18):#------------------------------------------Todos
                print("Haces un mortal triple y riegas lodo a todos")
                for f in targets:
                    for t in f:
                        t.condicion.update({"Cegado": 1})
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("No se como le hiciste, pero banaste a todos "
                      + "tus rivales")
                for t in targets[1]:
                    t.condicion.update({"Cegado": 1})
        
        elif("Dinamita" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Has activado la dinamita en donde se encuentran tu y "
                      + "tus companeros exitosamente")
                for t in targets[0]:
                    t.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
                    t.actualizar_stats()
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Has activado la dinamita... pero has olvidarlo "
                      + "lanzarla")
                self.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
                self.actualizar_stats()
            elif(tirada <= 10):#-------------------------------------Un enemigo
                t = targets[1][Juego.dados(1, len(targets[1]))[0]-1]
                print(f"Le has lanzado la dinamita a {t.nombre} de una manera "
                      + "muy radical")
                t.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
                t.actualizar_stats()
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Lanzaste la dinamita muy lejos y exploto la casa de "
                      + "tu abuela")
            elif(tirada <= 18):#------------------------------------------Todos
                print("La explosion fue mucho mas grande de lo que "
                      + "esperabas...")
                for f in targets:
                    for t in f:
                        t.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
                        t.actualizar_stats()
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("Lanzaste la dinamita justo donde querias!")
                for t in targets[1]:
                    t.cambiar_hp(gm.Dfboosts_o.iloc[i,0])
                    t.actualizar_stats()
        
        elif("Botella" in objeto.nombre and "Quemado" in self.condicion):
            self.condicion.pop("Quemado")
            self.curar()
            ind = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, ind)
            self.actualizar_stats()
            print(f"\n{self.nombre} ha usado con �xito {objeto.nombre}, "
                  + "es super efectivo!")
            return True
        
        elif("Nota de consejo" in objeto.nombre):
            print(objeto.boosteo)
            return True
        
        elif("Cana" == objeto.nombre and self.ubicacion.nombre == "Puerto"):
            self.buscar(None, "Mar")
            
        elif("Cana mejorada" == objeto.nombre 
             and self.ubicacion.nombre == "Puerto"):
            self.buscar(None, "Profundidades")
        
        elif("Lector de poder" in objeto.nombre):
            if("mejorado" in objeto.nombre):
                target.stats()
            else:
                print(f"Fuerza de {target.nombre}: {target.fuerza}")
        
        elif("Escudo" in objeto.nombre):
            self.resistencia += objeto.boosteo
            defensa = self.defender()
            self.resistencia -= objeto.boosteo
            if(target in gm.personajes):
                return {"Escudo": defensa}
            else:
                target.condicion.update({"Bloqueado": defensa})
                print("ENEMIGO BLOQUEADO!!")
        
        elif("Trampa de osos" == objeto.nombre or "Jaula" in objeto.nombre):
            z = self.ubicacion.zonas.index(self.zona)
            self.ubicacion.jaulas[z].update({objeto.nombre: {objeto: ""}})
            self.ubicacion.objetos_activos[z].append(objeto)
        
        elif("SCP 427" == objeto.nombre):
            gm.personajes.remove(self)
            gm.personajes_muertos.append(self)
            nuevo = Asistente(self.salud_max, self.fuerza, self.resistencia,
                              self.carisma_max, self.inteligencia,
                              self.sabiduria, self.nombre, self.condicion,
                              self.inventario, "SCP", self.nivel, 1,
                              self.zona, self, self.nombre + " SCP")
            nuevo.condicion.update({"Temporal": 1})
            nuevo.salud_max *= 4
            nuevo.salud = self.salud_max
            nuevo.fuerza *= 4
            nuevo.resistencia *= 4
            nuevo.carisma /= 2
            nuevo.inteligencia /= 2
            nuevo.sabiduria /= 2
            nuevo.actualizar_stats()
            self.asistentes.append(nuevo)
        
        elif("Curita wendiguito" in objeto.nombre):
            target.is_wendigo = False
            target.salud_max /= 3
            target.salud = self.salud_max
            target.fuerza /= 3
            target.resistencia /= 3
            target.carisma *= 2
            target.inteligencia *= 2
            target.sabiduria *= 2
            target.actualizar_stats()
            
        elif("Pocion" in objeto.nombre):
            if(Dfstat_o== 'H'):
                target.salud += cantidad
                if(target.salud > limite):
                    target.salud = limite
            elif(Dfstat_o=='F'):
                target.fuerza += cantidad
                if("Super Sayain" in self.condicion):
                        self.condicion["Super Sayain"] += cantidad
                if(target.fuerza > limite):
                    target.fuerza = limite
            elif(Dfstat_o=='R'):
                target.resistencia += cantidad
                if(target.resistencia > limite):
                    target.resistencia = limite
            elif(Dfstat_o=='C'):
                target.carisma += cantidad
                if(target.carisma > limite):
                    target.carisma = limite
            elif(Dfstat_o=='I'):
                target.inteligencia += cantidad
                if(target.inteligencia > limite):
                    target.inteligencia = limite
            elif(Dfstat_o=='S'):
                target.sabiduria += cantidad
                if(target.sabiduria > limite):
                    target.sabiduria = limite
            elif(Dfstat_o=='V'):
                target.condicion.update({"Acelerado": cantidad})
            elif(gm.Dfstat_o=='E' and target in gm.personajes):
                target.energia += cantidad
                if(target.energia > limite):
                    target.energia = limite
        
        else:
            if(Dfstat_o== 'H'):
                if(self.nombre == "Turati" and self.arbol["B1"][0] == 1):
                    gm.cantidad = (int(gm.cantidad 
                                       * np.random.randint(10, 21) / 10))
                target.salud += cantidad
                if(target.salud > target.salud_max):
                    target.salud = target.salud_max
            elif(Dfstat_o=='Saludable III'):
                if ('Envenenado III' in target.condicion):
                    target.condicion.pop('Envenenado III')
                    target.curar()
            elif(Dfstat_o=='Saludable II'):
                if ('Envenenado II' in target.condicion):
                    target.condicion.pop('Envenenado II')
                    target.curar()
            elif(Dfstat_o=='Saludable I'):
                if ('Envenenado I' in target.condicion):
                    target.condicion.pop('Envenenado I')
                    target.curar()
            elif(Dfstat_o=='Envenenado I'):
                if (('Envenenado III' not in target.condicion) 
                    and ('Envenenado II' not in target.condicion)):
                    target.enfermar('Envenenado I', cantidad)
            elif(Dfstat_o=='Envenenado II'):
                if ('Envenenado III' not in target.condicion):
                    target.enfermar('Envenenado II', cantidad)
                    if('Envenenado I' in target.condicion):
                        target.condicion.pop('Envenenado I')
            elif(Dfstat_o=='Envenenado III'):
                target.enfermar('Envenenado III', cantidad)
                if('Envenenado I' in target.condicion):
                    target.condicion.pop('Envenenado I')
                elif('Envenenado II' in target.condicion):
                    target.condicion.pop('Envenenado II')
            elif(Dfstat_o=='Confusion'):
                target.enfermar('Confundido', cantidad)
            elif(Dfstat_o=='Cuarto salud'):
                target.salud += target.salud_max/4
                if(target.salud > target.salud_max):
                    target.salud = target.salud_max
            elif(Dfstat_o=='Mitad salud'):
                target.salud += target.salud_max/2
                if(target.salud > target.salud_max):
                    target.salud = target.salud_max
            elif(Dfstat_o=='Tres cuartos salud'):
                target.salud += target.salud_max*3/4
                if(target.salud > target.salud_max):
                    target.salud = target.salud_max
            elif(Dfstat_o=='Salud maxima'):
                target.condicion = {"Saludable": 1}
                target.salud = target.salud_max
            elif(Dfstat_o=='Revivir'):
                if(target.salud <= 0 and target in gm.personajes_muertos 
                   and (("Cadaver de "+target.nombre) 
                        in self.inventario_nombres)):
                    gm.personajes_muertos.remove(target)
                    gm.personajes.append(target)
                    target.salud = target.salud_max/2
                    ind = self.inventario_nombres.index(
                        "Cadaver de "+target.nombre)
                    self.inventario_nombres.remove("Cadaver de "+target.nombre)
                    self.inventario.pop(ind)
                    target.condicion = {"Saludable": 1}
            elif(Dfstat_o=='Invisible'):
                target.condicion.update({'Invisible': 3})
            elif(Dfstat_o=='Habilidad'):
                if(objeto.usos == 1):
                    target.puntos_habilidad += 1
                    print(objeto.boosteo)
                    objeto.usos -= 1
                    return True
                print(objeto.boosteo)
                
        if(objeto.usos == 1 and "Pistola laser" not in objeto.nombre):
            ind = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, ind)
        self.actualizar_stats()
        print(f"\n{self.nombre} ha usado con �xito {objeto.nombre}, "
              + "es super efectivo!")
        return True
    
    def craftear(self):
        seguir = True
        ingredientes = []
        while(seguir):
            print("�Que quieres usar?")
            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
            i=0
            for llave in self.cartera_obj:
                print(f"{i+1}, \t{llave:.<24s}: {self.cartera_obj[llave]} | "
                      + "\t\t"
                      + str(self.inventario[
                          self.inventario_nombres.index(llave)].estadistica)
                      + "| \t"
                      + str(self.inventario[
                          self.inventario_nombres.index(llave)].boosteo))
                i+=1
            print(f"{i+1}: Terminar")
            obj = int(input())-1
            if(obj == i): # Terminando
                ingredientes.sort()
                for craft in gm.crafteos:
                    crafteo = list(craft)
                    if("Amuleto" in ingredientes):
                        nuevo = Asistente(19, 15, 3, 15, 5, 9,
                                          ("Golem de " 
                                           + ingredientes[-1].nombre),
                                          {"Saludable": 1}, ["Amuleto"],
                                          "Monstruo", len(ingredientes), 1,
                                          self.zona, self, "Golem")
                        for ing in ingredientes:
                            estadistica = ing.estadistica
                            boosteo = ing.boosteo
                            if(estadistica == "F"):
                                nuevo.fuerza += boosteo
                            elif(estadistica == "R"):
                                nuevo.resistencia += boosteo
                            elif(estadistica == "C"):
                                nuevo.carisma += boosteo
                            elif(estadistica == "I"):
                                nuevo.inteligencia += boosteo
                            elif(estadistica == "S"):
                                nuevo.sabiduria += boosteo
                        self.reclutar(nuevo)
                        return True
                    crafteo.sort()
                    if(crafteo == ingredientes):
                        print("Crafteo exitoso!")
                        gm.anadir_obj_manual(gm.crafteos[craft], self)
                        for i in ingredientes:
                            self.inventario.remove(i)
                            self.inventario_nombres.remove(i.nombre)
                    else:
                        print("Crafteo no disponible")
                        return False
                seguir = False
            else:
                objeto = self.inventario[obj]
                ingredientes.append(objeto)
        return [True, ingredientes, gm.crafteos[craft]]
    
    def __str__(self):
        texto = (super().stats() + f"| Peso: {self.peso} \n Nivel: "
              + f"{self.nivel:<20} | Ubicacion: {self.ubicacion.nombre} \n "
              + f"Zona: {self.zona:<21} | Carga: {self.carga} \n Saldo: "
              + f"{self.cartera:<20} \n Equipo: \n {self.equipo_nombres}\n "
              + f"Inventario: \n {self.cartera_obj}")
        if(self.is_wendigo):
            texto += ("ESTATUS: WENDIGO")
        return texto
    
    def moverse(self, zona = None):
        #DEBUG
#    print("---------------------------------------------------Metodo moverse")
        self.lugar_previo = self.zona

        ubicaciones = []
        zonas = self.ubicacion.zonas
        z = zonas.index(self.zona)
        if(zona == None):
            print("�A donde deseas moverte?")
            for i in range(0, len(self.mapa[self.zona])):
                print(f"{i+1}: {self.mapa[self.zona][i]}")
            zona = int(input())
            zona= self.mapa[self.zona][zona - 1]
        
        lugar = gm.buscaLugar(zona)
        
        values = self.mapa.values()
        
        for i in gm.personajes:
            ubicaciones.append(i.ubicacion.nombre)
        
        zonas_vistas = []
        for p in gm.personajes:
            if(p == self):
                continue
            for m in p.mapa[p.zona]:
                zonas_vistas.append(m)
            zonas_vistas.append(p.zona)
        zonas_vistas.append(zona)
        zonas_vistas.append(self.zona)
        
#        if(ubicacion not in ubicaciones):
##            eliminar(self.ubicacion.objetos_activos)
#            self.ubicacion.objetos_activos = []
#            for i in range(0, len(self.ubicacion.zonas)):
#                self.ubicacion.objetos_activos.append([])
#            Juego.generar_objetos(lugar)
        
        for zone in gm.master.mapa[zona]:
            if(zone not in zonas_vistas):
                for luga in range(0, len(gm.lugares_o)):
                    lug = gm.lugares_o[luga].zonas
                    print(zone)
                    print(lug)
                    if(zone in lug):
                        ubicacion_zone = gm.lugares_o[luga]
                        break
                Juego.generar_enemigos_zona(ubicacion_zone, zone)
                Juego.generar_objetos_zona(ubicacion_zone, zone)
        
        if(lugar.nombre == "Edificio Abandonado"):
            if('Submarino' not in [
                    x for v in values for x in v if type(v)==list] 
                    or 'Submarino' not in values):
                lugar = gm.fondo_del_mar
                zona = "Submarino"
            if(self.viaje_astral != True and self == gm.personaje_malo):
                self.viaje_astral = True
                lugar = gm.viaje_astral
                zona = "camion" #----------------------------------------------
        if(zona == "Profundidades" 
           and "Pin de bob esponja" in self.equipo_nombres):
            print("Escuchas a lo lejos una voz que dice: ""EsToY LiStO"" "
                  + "seguido de una risa infantil...")
        if(zona == "Sala principal"):
            Juego.dificultad = 2
        
        for zonaa in self.mapa[zona]:
            zonas_vistas.append(zonaa)
        
        for zapo in self.mapa[self.zona]:
            for luga in range(0, len(gm.lugares_o)):
                lug = gm.lugares_o[luga].zonas
                if(zapo in lug):
                    ubicacion_zapo = gm.lugares_o[luga]
                    break
            zonas = ubicacion_zapo.zonas
            z = zonas.index(zapo)
            if(zapo not in zonas_vistas):
                gm.eliminar(ubicacion_zapo.enemigos_activos[z])
                gm.eliminar(ubicacion_zapo.objetos_activos[z])
                ubicacion_zapo.enemigos_activos[z] = []
                ubicacion_zapo.objetos_activos[z] = []
                print(f"enemigos y objetos eliminados de: {zapo}")
        
        if(self.zona in gm.agua 
           and "Traje de buzo mejorado" in self.equipo_nombres 
           and zona not in gm.agua):
            self.velocidad -= self.equipo[
                self.equipo_nombres.index("Traje de buzo mejorado")].boosteo
        elif(self.zona not in gm.agua 
             and "Traje de buzo mejorado" in self.equipo_nombres 
             and zona in gm.agua):
            self.velocidad += self.equipo[self.equipo_nombres.index(
                "Traje de buzo mejorado")].boosteo
        
        print(lugar.jaulas)
        
        self.ubicacion = lugar
        self.zona = zona
        
        for asistente in self.asistentes:
            asistente.zona = zona
        
        zonas = self.ubicacion.zonas
        z = zonas.index(self.zona)
        print(f"{self.nombre} se ha movido a {lugar.nombre} en {zona}")
#        print(self.ubicacion.enemigos_activos)
#        print(self.ubicacion.objetos_activos)
        return True
    
    def buscar(self, objeto = None, zona = None):
        #DEBUG
#    print("----------------------------------------------------Metodo buscar")
        scp = ["SCP 079", "SCP 053", "SCP 682"]
        ultra_raros = ["Diamante", "Nota amenazante", "Tridente",
                       "Esencia de bida"]
        raros = ["Planta azul", "Planta blanca", "Planta roja",
                 "Planta verde", "Planta morada", "Planta amarilla",
                 "Sniper", "Dinamita", "Oro", "SCP 079", "SCP 500"]
        iluminacion = ["Fosforo","Encendedor", "Antorcha", "Lupa", "Telefono",
                       "Telefono con senal infinita", "Linterna",
                       "Casco con linterna"]
        
        
        if(zona == None):
            lugar = self.ubicacion
            zonas = self.ubicacion.zonas
            z = zonas.index(self.zona)
        else:
            for l in range(0, len(gm.lugares_o)):
                lug = gm.lugares_o[l].zonas
                if(zona in lug):
                    break
            lugar = gm.lugares_o[l]
            zonas = lugar.zonas
            z = zonas.index(zona)
        n = Juego.dados(1, 100)[0]
        mul = 1
        
        if(lugar.nombre == "Fondo del mar"):
            iluminacion = iluminacion[3:]
            
        if(lugar == self.ubicacion and self.zona not in gm.iluminados):
            print("�Quieres usar algun objeto para ayudarte a buscar?")
            for il in range(0, len(iluminacion)):
                if(iluminacion[il] in self.inventario_nombres):
                    print(f"{il+1}: iluminacion[il]")
            print(f"{len(iluminacion)+1}: Nada")
            ob = int(input())-1
            
            if(ob < len(iluminacion)):
                for i in range(0, len(gm.Dfnombres_o)):
                    if(gm.Dfnombres_o.iloc[i,0] == iluminacion[ob]):
                        break
                if(gm.Dfusos_o.iloc[i,0] == 1):
                    self.peso -= gm.Dfespacios_o.iloc[i,0]
                    ind = self.inventario_nombres.index(objeto.nombre)
                    self.inventario_nombres.remove(objeto.nombre)
                    self.inventario.pop(ind)
                mul = (ob+1)*2
                n+=mul
        
        if(self.nombre == "Ruben" and self.arbol["A3"][0] == 1):
            n += 20
        elif(self.nombre == "Norman" and self.arbol["A1"][0] == 1):
            n += 10
        
        obj = ""
        print("Buscando...")
        if(objeto == None):
            #---------------------------------------------------------aleatorio
            tirada = gm.dados(1, len(lugar.objetos_activos[z]))[0]
            objeto = lugar.objetos_activos[z][tirada-1]
        else:
            encontrado = False
            for h in range(0, len(lugar.objetos_activos[z])):
                if(objeto == lugar.objetos_activos[z][h].nombre):
                    encontrado = True
                    break
            if(not encontrado):
                print("Aqui no existe shavo")
                return False                
            objeto = lugar.objetos_activos[z][h]
            
        print(objeto.nombre)
        if(objeto.nombre == "SCP 053"):
            print("No nel no puedes jaja salu3")
        if(objeto.nombre in scp):
            #------------------------------dialogo scp, crear objeto pertinente
            print("\nDi lo tuyo...\n")
            if(objeto.nombre == "SCP 079"):
                obj = Objeto("Tecla", "--", "--", 0, 1, 1, 0)
                gm.anadir_obj_manual(obj, self)
                print("(texto de la compu)")
                gm.anadir_obj_manual("Nota de consejo", self)
                return True
            elif(objeto.nombre == "SCP 682"):
                obj = Objeto("Escama", "--", "--", 0, 1, 1, 0)
                gm.anadir_obj_manual(obj, self)
                return True
        elif(objeto.nombre in ultra_raros):
            #--------------------------------busca objeto con probabilidad baja
            if(n >= 80):
                obj = objeto
        elif(objeto.nombre in raros):
            #-------------------------------busca objeto con probabilidad media
            if(n >= 45):
                obj = objeto
        else:
            #--------------------------------busca objeto con probabilidad alta
            if(n >= 15):
                obj = objeto
#        print()
#        for i in self.ubicacion.objetos_activos[z]:
#            print(i.nombre, end = ", ")
#        print()
        if(obj == ""):
            print("Que mala suerte shavo, no encontraste el amor de tu bida")
        elif(objeto.nombre == "Dinero"):
            self.anadir_obj(1)
        else:
            for h in range(0, len(lugar.objetos_activos[z])):
                if(objeto.nombre == lugar.objetos_activos[z][h]):
                    break
            
            if(self.ubicacion != lugar):
                lugar.cantidades[z][h] -= 1
                if(lugar.cantidades[z][h] <= 0):
                    lugar.objetos_activos[z].pop(ind)
                gm.anadir_obj_manual(objeto.nombre, self)
                return True
            
            self.anadir_obj(objeto)
            if(self.zona == "Mercado"):
                # lista personajes
                p_presentes = []
                for p in gm.personajes:
                    if(p.zona == self.zona):
                        p_presentes.append(p)
                # mult enemigos
                mult = 1
                if(objeto.precio <= 6):
                    mult += objeto.precio/10
                elif(objeto.precio < 300):
                    mult += 0.8
                else:
                    mult*=2
                
                e_presentes = []
                for e in self.ubicacion.enemigos_activos[z]:
                    e.salud *= mult
                    e.fuerza *= mult
                    e.resistencia *= mult
                    e.carisma *= mult
                    e.inteligencia *= mult
                    e.sabiduria *= mult
                    e_presentes.append(e)
                    
                Juego.iniciar_pelea(p_presentes, e_presentes, [], self, mult)
    
    def atacar(self, e_presentes, mult = 1):
        #DEBUG
#    print("------------------------------------------Metodo atacar personaje")
        nada = Objeto("Puno", 0, "F", 0, 1, 2, 0)
        if(len(e_presentes) > 1):
            print("\n�Qui�n ser� tu victima?")
            print("INDICE \t NOMBRE \t SALUD")
            for i in range (0, len(e_presentes)):
                print(f"{i+1}: "
                      + f"{e_presentes[i].nombre}\t{e_presentes[i].salud}")
            objetivo = e_presentes[int(input())-1]
        else:
            objetivo = e_presentes[0]
        print("Deseas usar algun objeto?")
        objetos_permitidos = []
        for i in range(0, len(self.inventario)):
            if(self.inventario[i].estadistica == "F"):
                objetos_permitidos.append(self.inventario[i])
        print("0: A puno cerrado")
        for i in range(0, len(objetos_permitidos)):
            print(f"{i+1}: {objetos_permitidos[i].nombre}")
        sel = int(input())
        if(sel == 0):
            arma = nada
        elif(sel > len(objetos_permitidos) or sel < 0):
            print("No es valido")
            arma = nada
        else:
            arma = objetos_permitidos[sel-1]
        print("Tirando dados...")
        da2 = Juego.dados(1, 10)[0]
        print("Tiraste "+str(da2))
        
        if(self.nombre == "Turati" and self.arbol["A2"][0] == 1):
            tirada = Juego.dados(1, 10)
            if(tirada == 1):
                mult *= 2
        elif(self.nombre == "Sebas" and "Kaio Ken" in self.condicion):
            mult *= 2
        elif(self.nombre == "Ruben" and self.arbol["A1"][0] == 1 
             and objetivo.categoria == "Animal"):
            mult *= 2
        dano = self.fuerza*mult + int(arma.boosteo) + da2
        
        if("Pistola laser" in arma.nombre):
            arma.uso += 3
            if("mejorada" in arma.nombre):
                if(arma.uso >= 6):
                    return False
            else:
                if(arma.uso >= 4):
                    return False
        
        if(arma.nombre == "Magnum"):
            if("Bala de magnum" not in self.inventario_nombres):
                print("No tienes municion :o")
                dano = 0
            else:
                indio = self.inventario_nombres.index("Bala de magnum")
                self.anadir_equipo(self.inventario[indio], indio)
                
        elif(arma.nombre == "Sniper") or (arma.nombre == "Rifle"):
            if("Bala de sniper" not in self.inventario_nombres):
                print("No tienes municion :o")
                dano = 0
            else:
                indio = self.inventario_nombres.index("Bala de sniper")
                self.anadir_equipo(self.inventario[indio], indio)
                
        elif(arma.nombre == "Arco") or (arma.nombre == "Arco mejorado"):
            if(("Flecha" not in self.inventario_nombres) 
               and ("Flecha emplumada" not in self.inventario_nombres) 
               and ("Flecha primitiva" not in self.inventario_nombres)):
                print("No pues estas mongolo")
                dano = 0
            else:
                print("�Que flecha quieres usar?")
                for i in range(0, len(self.inventario_nombres)):
                    if("Flecha" in self.inventario_nombres[i]):
                        print(f"{i+1}: {self.inventario_nombres[i]}")
                f = int(input())-1
                flecha = self.inventario[f].boosteo
                dano += flecha
                indio = self.inventario_nombres[f]
                self.anadir_equipo(self.inventario[f], f)
        if("Cegado" in self.condicion):
            tirada = Juego.dados(1, 10)[0]
            if(tirada >= 8):
                dano = 0
                print("Has fallado tu ataque!")
        
        # Funcion subir energia
        self.energia += self.energia_max * 0.2
        print("Has recuperado el 20% de energia")
        if(self.energia > self.energia_max):
            self.energia = self.energia_max
        
        self.actualizar_stats()
        return [objetivo, dano, arma]
    
    def atacar_carisma(self, enemigo):
        ataque = int(input("�C�mo quieres atacar?\n1: Intimidar\n2: "
                           + "Tranquilizar\n3: Persuadir"))-1
        dano = self.carisma + Juego.dados(1, self.carisma_max/10)[0]
        for h in range (0, len(gm.Dfnombres_e)):
            if(gm.Dfnombres_e.iloc[h,0] == enemigo.nombre):
                if(ataque == 0):
                    dano -= gm.Dfintimidar_e.iloc[h,0]
                elif(ataque == 1):
                    dano -= gm.Dftranquilizar_e.iloc[h,0]
                elif(ataque == 2):
                    dano -= gm.Dfpersuadir_e.iloc[h,0]
        return[enemigo, dano]
        
    
    def huir(self, e_presentes): #-------------------------e_presentes = turnos
        for e in range(0, len(e_presentes)):
            if(type(e_presentes[e]) == gm.Enemigo):
                break
        if(self.velocidad > e_presentes[e].velocidad):
            return True
        else:
            prob = (self.velocidad/e_presentes[e].velocidad)*100
            tirada = Juego.dados(1, 100)[0]
            if(tirada <= prob):
                return True
            else:
                return False
    
    def comprar(self):
        if(self.zona != "Mercado"):
            print("Comprale a tu abuela")
            return False
        else:
            print("�Que quieres comprar?\nNOMBRE \t PRECIO")
            for i in range (0, len(self.ubicacion.objetos_activos[0])):
                print(f"{i+1}: "
                      + f"{self.ubicacion.objetos_activos[0][i].nombre}: "
                      + f"\t{self.ubicacion.objetos_activos[0][i].precio}")
            objeto = int(input())
            if(self.inventario_nombres.count("Dinero") 
               >= self.ubicacion.objetos_activos[0][objeto-1].precio):
                print("Compra realizada!")
                pago = self.ubicacion.objetos_activos[0][objeto-1].precio
                self.anadir_obj(-pago)
                self.anadir_obj(self.ubicacion.objetos_activos[0][objeto-1])
            else:
                decision = input("Oh no! No alcanzan los dineros :( "
                                 + "�Quieres vender algo? (S/N) \n")
                if(decision == "S"):
                    vend = self.vender(self.ubicacion.objetos_activos[0][
                        objeto-1].precio)
                    if(vend):
                        print("Compra realizada!")
                        pago = self.ubicacion.objetos_activos[0][
                            objeto-1].precio
                        self.anadir_obj(-pago)
                        self.anadir_obj(self.ubicacion.objetos_activos[0][
                            objeto-1])
                else:
                    print("Weno pues estas pobre")
                    return False
        return True
    
    def vender(self, pobre = None):
        if(self.zona != "Mercado"):
            print("Vendele a tu abuela")
            return False
        else:
            print("�Que quieres vender?\nNOMBRE \t PRECIO")
            for i in range(0, len(self.inventario)):
                print(f"{i+1}: {self.inventario_nombres[i]} "
                      + f"{round(self.inventario[i].precio*.6)}")
            indio = int(input())-1
            objeto = self.inventario[indio]
            if(objeto.nombre == "Nota de consejo" or objeto.precio == 0):
                print("No compramos basura")
                return False
            pago = int(round(objeto.precio*.6))
            if(pobre != None):
                if(pobre > pago):
                    print("Con eso no te va a alcanzar vato loko")
                    return False            
            self.anadir_obj(pago)
            self.inventario.pop(indio)
            self.inventario_nombres.pop(indio)
            return True
    
    def exceso_peso(self):
        #DEBUG
#    print("-----------------------------------------------Metodo exceso peso")
        if(self.peso > self.carga):
            if(self.inventario != []):
                print(f"{self.nombre} estas muy gordo :(")
                self.tirar_objeto()
            else:
                self.carga = self.peso
    
    def tirar_objeto(self):
        #DEBUG
#    print("-----------------------------------------------------Tirar objeto")
        self.energia += self.energia_max * 0.2
        print("Has recuperado el 20% de energia")
        if(self.energia > self.energia_max):
            self.energia = self.energia_max
            
        if(len(self.inventario) <= 0):
            print("Stas pobre")
            return False
        print("�Que quieres tirar?")
        print("INDICE \t NOMBRE \t CANTIDAD \t PESO")
        i=0
        for llave in self.cartera_obj:
            print(f"{i+1},\t {llave:.<24s}: {self.cartera_obj[llave]} | "
                  + str(self.inventario[
                      self.inventario_nombres.index(llave)].peso))
            i+=1
        objeto = int(input())-1
        if("Confundido" in self.condicion):
            objeto = Juego.dados(1, len(self.cartera_obj))[0]-1
            
        for llave in self.cartera_obj:
            if(objeto == 0):
                break
            objeto -= 1
        
        print(f"{self.nombre} se ha desecho de {llave}, descanse en paz "
              + f"{llave}, F")
        zonas = self.ubicacion.zonas
        i = zonas.index(self.zona)
        indio = self.inventario_nombres.index(llave)
        obj = self.inventario[indio]
        
        self.ubicacion.objetos_activos[i].append(obj)
        if(obj.nombre not in self.ubicacion.objetos[i]):
            self.ubicacion.objetos[i].append(obj.nombre)
            self.ubicacion.cantidades[i].append(1)
        else:
            indi = self.ubicacion.objetos[i].index(obj.nombre)
            self.ubicacion.cantidades[i][indi] += 1
        
        self.anadir_equipo(obj, indio)
        
        self.actualizar_stats()
        return True
    
    def subir_nivel(self):
        #DEBUG
#    print("-----------------------------------------------Metodo subir nivel")
        self.nivel += 1
        self.puntos_habilidad += 1
        self.subir_salud_max()
        if(self.nivel == 2 or self.nivel == 5 or self.nivel == 8):
            print(f"\n{self.nombre}: " + "SUBISTE DE NIVEL!!\n")
            contador=5
            for i in range(0, 5):
                print("�Que estadistica deseas mejorar? Tienes: "
                      + str(contador-i) +" puntos disponibles")
                sel = int(input("\nFuerza(1)\nResistencia(2)\nCarisma(3)\n"
                                + "Inteligencia(4)\nSabiduria(5)\n"))
                if(sel == 1):        
                    self.fuerza+=1
                    if("Super Sayain" in self.condicion):
                        self.condicion["Super Sayain"] += 1
                elif(sel == 2):
                    self.resistencia+=1
                elif(sel == 3):
                    self.carisma+=1
                elif(sel == 4):
                    self.inteligencia+=1
                elif(sel == 5):
                    self.sabiduria+=1
            self.salud = self.salud_max
            self.actualizar_stats()
        else:
            self.actualizar_stats()
            print("\nSUBISTE DE NIVEL!!\n")
        print(self.stats())
        return ""

from Juegos import Juego
import Game_Manager as gm

gm.mirek   = Personaje(27, 14, 13, 15, 16, 18, "Mirek",
                       {"Saludable": 1}, 20, [], gm.campamento, "Cabana", 1,
                       gm.mapa_mirek, 0, 10, gm.arbol_mirek)
gm.bugatti = Personaje(39, 8, 7, 18, 16, 9,    "Turati", {"Saludable": 1}, 25,
                       [], gm.campamento, "Cabana", 1, gm.mapa_bugatti, 0, 10,
                       gm.arbol_bugatti)
gm.ruben   = Personaje(27, 13, 18, 8, 11, 15,  "Ruben",  {"Saludable": 1}, 20,
                       [], gm.campamento, "Cabana", 1, gm.mapa_ruben, 0, 10,
                       gm.arbol_ruben)
gm.sebas   = Personaje(29, 18, 8, 19, 7, 17,   "Sebas",  {"Saludable": 1}, 25,
                       [], gm.campamento, "Cabana", 1, gm.mapa_sebas, 0, 10,
                       gm.arbol_sebas)
gm.norman  = Personaje(31, 7, 20, 19, 18, 12,  "Norman", {"Saludable": 1}, 15,
                       [], gm.campamento, "Cabana", 1, gm.mapa_norman, 0, 10,
                       gm.arbol_norman)

gm.master  = Personaje(420, 5, 69, 69, 69, 69,  "Tu dios", {"Saludable": 1},
                       69, [], gm.bosque, "Aire libre", 69, gm.mapa_master,
                       666, 420, gm.arbol_norman)
gm.ninja   = Personaje(420, 69, 69, 69, 69, 69,  "Tu segundo dios",
                       {"Saludable": 1}, 69, [], gm.bosque, "Aire libre",
                       69, gm.mapa_master, 666, 420, gm.arbol_norman)
