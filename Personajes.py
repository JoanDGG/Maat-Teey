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
                indice = self.equipo_nombres.index(gm.mochilas[mochila])
                self.carga += self.equipo[indice].boosteo
                break
        if("Shaed" in self.equipo_nombres and not gm.dia):
            self.condicion.update({'Invisible': 10})
            if(self.zona in gm.lugares_iluminados):
                self.condicion.pop("Invisible")
        elif("Shaed" in self.equipo_nombres and gm.dia):
            self.condicion.pop("Invisible")
        elif("Shaed mejorado" in self.equipo_nombres and not gm.dia):
            self.condicion.update({'Invisible': 10})
            if(self.zona in gm.lugares_iluminados):
                self.condicion.pop("Invisible")
        elif("Shaed mejorado" in self.equipo_nombres and gm.dia):
            self.condicion.pop("Invisible")
    
    def anadir_equipo(self, objeto:Objeto, indice: int):
        if(self.cartera_obj[objeto.nombre] > 1):
            self.cartera_obj[objeto.nombre] -= 1
        else:
            self.cartera_obj.pop(objeto.nombre)
        self.inventario.pop(indice)
        self.inventario_nombres.pop(indice)
        return True
    
    def quitar_equipo(self, objeto:Objeto):
        if(objeto.nombre not in self.cartera_obj.keys()):
            self.cartera_obj.update({objeto.nombre: 1})
        else:
            self.cartera_obj[objeto.nombre] += 1
        self.inventario.append(objeto)
        self.inventario_nombres.append(objeto.nombre)
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
            print("\n"+self.nombre + " murio, F")
            return self.is_ded()
        self.actualizar_stats()
        self.exceso_peso()
        return False
    
    def reclutar(self, asistente):
        while(self.espacio_asistentes < asistente.rango):
            print("No tienes espacio suficiente! (espacio faltante: "
                  + f"{asistente.rango - self.espacio_asistentes}) \nDeseas "
                  + "liberar a algun asistente?")
            for asistente_ya_reclutado in range(0, len(self.asistentes)):
                print(f"{asistente_ya_reclutado+1}: "
                      + f"{self.asistentes[asistente_ya_reclutado].apodo} \t"
                      + " espacio ocupado: "
                      + f"{self.asistentes[asistente_ya_reclutado].rango}")
            print(f"{len(self.asistentes)+1}: Ninguno")
            decision = int(input()) - 1
            if(decision == len(self.asistentes)):
                return False
            else:
                if(Juego.ubicar.count(self.zona) > 1): # Si no estas solo en la zona
                    decision = int(input("Deseas dejar libre al asistente o "
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
            decision = input("Quieres ponerle un nombre?(S/N)\n")
            if(decision == "S"):
                nombre = input("Como quieres llamarlo?\n")
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
        nuevo_asistente = Asistente(asistente.salud_max, asistente.fuerza,
                          asistente.resistencia, asistente.carisma_max,
                          asistente.inteligencia, asistente.sabiduria,
                          asistente.nombre, asistente.condicion,
                          asistente.dropeo, asistente.categoria,
                          asistente.rango, asistente.cantidad,
                          asistente.zona, self, nombre)
        self.asistentes.append(nuevo_asistente)
        return True
                
    
    def cambiar_dueno(self, asistente):
        personajes_temporal = []
        for personaje in gm.personajes:
            if(personaje.zona == self.zona):
                personajes_temporal.append(personaje)
        personajes_temporal.remove(self)
        
        if(personajes_temporal != []):
            print("Con quien vas a intercambiar asistentes?")
            for personaje_temporal in range(0, len(personajes_temporal)):
                print(f"{personaje_temporal+1}: "
                      + f"{personajes_temporal[personaje_temporal].nombre} "
                      + "\t espacio libre: "
                      + str(personajes_temporal[
                          personaje_temporal].espacio_asistentes))
            print(f"{len(personajes_temporal) + 1}: No pues ya no")
            nuevo_dueno = int(input()) - 1
            if(nuevo_dueno == len(personajes_temporal)):
                return False
            else:
                for asistente_temporal in range(0, len(
                        personajes_temporal[nuevo_dueno].asistentes)):
                    print(f"{asistente_temporal+1}: "
                          + str(personajes_temporal[
                              nuevo_dueno].asistentes[
                                  asistente_temporal].apodo)
                          + " \t espacio ocupado: "
                          + str(personajes_temporal[
                              nuevo_dueno].asistentes[
                              asistente_temporal].rango))
                print(f"{len(self.asistentes)+1}: Ninguno")
                asistente_intercambio = int(input()) - 1
                if(asistente_intercambio == len(personajes_temporal)):
                    resultado = personajes_temporal[nuevo_dueno].reclutar(
                        asistente)
                    if(resultado):
                        self.liberar(asistente)
                        return True
                    else:
                        return False
                else:
                    espacio_asistente_actual = asistente.rango
                    espacio_asistente_nuevo = personajes_temporal[
                        nuevo_dueno].asistentes[
                        asistente_intercambio].rango
                    if((self.espacio_asistentes + espacio_asistente_actual 
                        - espacio_asistente_nuevo >= 0) 
                       and ((personajes_temporal[
                           nuevo_dueno].espacio_asistentes 
                       + espacio_asistente_nuevo 
                       - espacio_asistente_actual) >= 0)):
                        asistente_actual = asistente
                        asistente_nuevo = personajes_temporal[
                            nuevo_dueno].asistentes[asistente_intercambio]
                        self.liberar(asistente)
                        personaje_intercambio = personajes_temporal[
                            nuevo_dueno]
                        asistentes = personaje_intercambio.asistentes[
                            asistente_intercambio]
                        personajes_temporal[nuevo_dueno].decision(asistentes)
                        personajes_temporal[nuevo_dueno].reclutar(
                            asistente_actual)
                        self.reclutar(asistente_nuevo)
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
        for zona in posibles:
            if zona not in conocidos:
                print(f"Felicidades! {self.nombre} ha descubierto {zona}!!")
                self.mapa[self.zona].append(zona)
                self.mapa.update({zona: [self.zona]})
                return self.mapa
        print(f"{self.nombre}, parece que "
              + "ya has descubierto todo de esta zona")
        return False
    
    def activar_habilidad(self, contexto_habilidad, omitidos = []):
        estadisticas = ["Salud", "Fuerza", "Resistencia", "Carisma",
                        "Inteligencia", "Sabiduria", "Energia"]
        if(contexto_habilidad != "anticipacion"):
            print("Que habilidad quieres activar? (0 para salir)")
            print("HABILIDAD\tCOSTO")
            for codigo_habilidad in self.arbol:
                for numero_habilidad in range(0, len(gm.habilidades[
                        contexto_habilidad])):
                    habilidad = list(gm.habilidades[
                        contexto_habilidad].keys())[numero_habilidad]
                    if(habilidad in self.arbol[codigo_habilidad][2] 
                       and self.arbol[codigo_habilidad][0] == 1):
                        gm_hab = gm.habilidades[contexto_habilidad]
                        gm_hab = gm_hab[list(gm.habilidades[
                            contexto_habilidad].keys())[
                            numero_habilidad]]
                        print(f"{codigo_habilidad}: "
                              + f"{self.arbol[codigo_habilidad][2]}:\t"
                              + str(gm.habilidades[contexto_habilidad][
                                  list(gm.habilidades[
                                      contexto_habilidad].keys())[
                                      numero_habilidad]]))
            codigo_habilidad = input()
            if(codigo_habilidad == "0"):
                return [False, False]
            elif(codigo_habilidad not in self.arbol):
                return [False, False]
            print(self.arbol)
        else:
            contexto_habilidad = "Turno enemigo"
            codigo_habilidad = "B1"
            
# =============================================================================
#         Costo de habilidad en llave, en self.arbol[hab][2] 
#         (nombre de la habilidad)
# =============================================================================
        costo = gm.habilidades[
            contexto_habilidad][list(gm.habilidades[
                contexto_habilidad].keys())[
                gm.habilidades[
                contexto_habilidad][list(gm.habilidades[
                    contexto_habilidad].keys()).index(self.arbol[
                        codigo_habilidad][2])]]]
        print(f"Habilidad: {self.arbol[codigo_habilidad][2]}\n Costo: "
              + f"{costo}")
        
        if(self.energia < costo):
            print("Estas muy cansado para esto")
            return [False, False]
        else:
            print(f"Se ha activado {self.arbol[codigo_habilidad][2]}")
            self.energia -= costo
            
            if(self.arbol[codigo_habilidad][2] == "Sabiduria del mas alla"):
                gm.anadir_obj_manual(gm.norman, "Nota de consejo sabia")
                
            elif(self.arbol[codigo_habilidad][2] == "Pociones"):
                lista = []
                for crafteo in gm.crafteos:
                    for objeto in self.inventario_nombres:
                        if objeto in crafteo:
                            lista.append(crafteo)
                for receta in lista:
                    print(receta + ": " + gm.crafteos[receta])
                    
            elif(self.arbol[codigo_habilidad][2] == "Boosteo"):
                print("A quien deseas boostear?")
                for personaje in range(0, len(gm.personajes)):
                    print(f"{personaje + 1}: "
                          + f"{gm.personajes[personaje].nombre}")
                
                objetivo = int(input()) - 1
                
                print("Que estadistica deseas boostear?")
                for estadistica in range(0, len(estadisticas)):
                    print(f"{estadistica + 1}: {estadisticas[estadistica]}")
                estadistica_a_boostear = int(input()) - 1
                
                boosteo = int(input("Cuanto boosteo quieres darle? (max 9)"))

                if(self.energia < boosteo):
                    boosteo = self.energia
                if(estadistica_a_boostear == 0):
                    gm.personajes[objetivo].cambiar_hp(boosteo)
                else:
                    condicion = (estadisticas[estadistica_a_boostear] 
                                 + str(boosteo))
                    gm.personajes[objetivo].condicion.update({condicion: 3})
                    if(estadistica_a_boostear == 1):
                        gm.personajes[objetivo].fuerza += boosteo
                    elif(estadistica_a_boostear == 2):
                        gm.personajes[objetivo].resistencia += boosteo
                    elif(estadistica_a_boostear == 3):
                        gm.personajes[objetivo].carisma += boosteo
                    elif(estadistica_a_boostear == 4):
                        gm.personajes[objetivo].inteligencia += boosteo
                    elif(estadistica_a_boostear == 5):
                        gm.personajes[objetivo].sabiduria += boosteo
                    elif(estadistica_a_boostear == 6):
                        gm.personajes[objetivo].energia += boosteo
 
            elif(self.arbol[codigo_habilidad][2] == "Disfraz"):
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
                
            elif(self.arbol[codigo_habilidad][2] == "Carisma absoluta"):
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
                
            elif(self.arbol[codigo_habilidad][2] == "Grito de guerra"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    objetivo = self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)][enemigo]
                    objetivo.enfermar("Confundido", 3)
                    omitidos.append(objetivo)
                    
            elif(self.arbol[codigo_habilidad][2] == "Habilidad animal"):
                animales = []
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    objetivo = self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)][enemigo]
                    if(objetivo.categoria == "Animal"):
                        animales.append(objetivo)
                
                print("A quien te vas a ratear?")
                
                for animal in range(0, len(animales)):
                    print(f"{animal + 1}: animales[animal].nombre")
                victima = animales[int(input()) - 1]
                
                print("Que estadistica deseas copiar?")
                for estadistica in range(0, len(estadisticas)):
                    print(f"{estadistica + 1}: {estadisticas[estadistica]}")
                decision_estadistica = estadisticas[int(input()) - 1]
                
                if(decision_estadistica == "Salud"):
                    self.cambiar_hp(victima.salud)
                elif(decision_estadistica == "Fuerza"):
                    if(victima.fuerza > self.fuerza):
                        self.condicion.update({decision_estadistica 
                                               + str(victima.fuerza 
                                                     - self.fuerza): 3})
                        self.fuerza = victima.fuerza
                    else:
                        self.condicion.update({decision_estadistica 
                                               + str(victima.fuerza): 3})
                        self.fuerza += victima.fuerza
                elif(decision_estadistica == "Resistencia"):
                    if(victima.resistencia > self.resistencia):
                        self.condicion.update({decision_estadistica 
                                               + str(victima.resistencia 
                                                     - self.resistencia): 3})
                        self.resistencia = victima.resistencia
                    else:
                        self.condicion.update({decision_estadistica
                                               + str(victima.resistencia): 3})
                        self.resistencia += victima.resistencia
                elif(decision_estadistica == "Carisma"):
                    if(victima.carisma > self.carisma):
                        self.condicion.update({decision_estadistica
                                               + str(victima.carisma 
                                                     - self.carisma): 3})
                        self.carisma = victima.carisma
                    else:
                        self.condicion.update({decision_estadistica
                                               + str(victima.carisma): 3})
                        self.carisma += victima.carisma
                elif(decision_estadistica == "Inteligencia"):
                    if(victima.inteligencia > self.inteligencia):
                        self.condicion.update({decision_estadistica
                                               + str(victima.inteligencia 
                                                     - self.inteligencia): 3})
                        self.inteligencia = victima.inteligencia
                    else:
                        self.condicion.update({decision_estadistica
                                               + str(victima.inteligencia): 3})
                        self.inteligencia += victima.inteligencia
                elif(decision_estadistica == "Sabiduria"):
                    if(victima.sabiduria > self.sabiduria):
                        self.condicion.update({decision_estadistica 
                                               + str(victima.sabiduria 
                                                     - self.sabiduria): 3})
                        self.sabiduria = victima.sabiduria
                    else:
                        self.condicion.update({decision_estadistica
                                               + str(victima.sabiduria): 3})
                        self.sabiduria += victima.sabiduria
                elif(decision_estadistica == "Energia"):
                    if(victima.energia > self.energia):
                        self.condicion.update({decision_estadistica 
                                               + str(victima.energia 
                                                     - self.energia): 3})
                        self.energia = victima.energia
                    else:
                        self.condicion.update({decision_estadistica
                                               + str(victima.energia): 3})
                        self.energia += victima.energia
            elif(self.arbol[codigo_habilidad][2] == "Invocar animal"):
                oso = Asistente(65, 19, 19, 19, 5, 17, "Oso", "Saludable",
                                "Pelaje", "Animal", 5, 1, self.zona,
                                self, "Oso")
                oso.condicion.update({"Lealtad": 5})
                self.asistentes.append(gm.nuevo)
            elif(self.arbol[codigo_habilidad][2] == "Special curry"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    enemigo.enfermar("Quemado", 3)
            elif(self.arbol[codigo_habilidad][2] == "Kaio ken" 
                 and contexto_habilidad == "Turno personaje"):
                self.condicion.update({"Kaio Ken": 3})
            elif(self.arbol[codigo_habilidad][2] == "Ultra instinto" 
                 and contexto_habilidad == "Turno personaje"):
                self.condicion.update({"Ultra instinto": 3})
            elif(self.arbol[codigo_habilidad][2] == "Analitico"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(enemigo.stats())
            elif(self.arbol[codigo_habilidad][2] == "Momazo"):
                print("A quien vas a trollear?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                omitidos.append(objetivo)
            elif(self.arbol[codigo_habilidad][2] == "Meme de enemigos"):
                print("A quien vas buliear?")
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    print(f"{enemigo + 1}: "
                          + str(self.ubicacion.enemigos_activos[
                              self.ubicacion.zonas.index(self.zona)][
                                  enemigo].nombre))
                objetivo = self.ubicacion.enemigos_activos[
                    self.ubicacion.zonas.index(self.zona)][int(input())-1]
                objetivo.carisma -= Juego.dados(1, objetivo.carisma//2)
            elif(self.arbol[codigo_habilidad][2] == "Lord meme"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    enemigo.carisma -= Juego.dados(1, objetivo.carisma//2)
                    omitidos.append(enemigo)                
            elif(self.arbol[codigo_habilidad][2] == "Robots"):
                robot = Asistente(25, 11, 7, 9, 15, 15, "Robot", "Saludable",
                                  "Tornillo", "Robot", 2, 1, self.zona, self,
                                  "Robot")
                robot.condicion.update({"Lealtad": 5})
                self.asistentes.append(gm.nuevo)
            elif(self.arbol[codigo_habilidad][2] == "Llamar al viento"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    self.atacar(enemigo, 2)
                for personaje in range(0, len(gm.personajes)):
                    if(personaje.zona == self.zona and personaje != self):
                        self.atacar(personaje, 2)
            elif(self.arbol[codigo_habilidad][2] == "Mente dormida"):
                eleccion_objetivos = int(input("Deseas atacar a todos (0)"
                                               + " o a uno "
                                     + "(1)?\n"))
                if(eleccion_objetivos == 0):
                    for enemigo in range(0, len(
                            self.ubicacion.enemigos_activos[
                                self.ubicacion.zonas.index(self.zona)])):
                        self.atacar(enemigo, 1.5)
                else:
                    print("A quien vas a atacar?")
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
            elif(self.arbol[codigo_habilidad][2] == "Anticipacion"):
                return [True, False]
            elif(self.arbol[codigo_habilidad][2] == "Explorador" 
                 and contexto_habilidad == "Iniciar pelea"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                        print(str(self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)][
                                enemigo].nombre))
            elif(self.arbol[codigo_habilidad][2] == "Smash ball"):
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
                self.energia -= gm.habilidades[contexto_habilidad][self.arbol[
                    codigo_habilidad][2]]
                return [True, [objetivo, dano, arma]]
            elif(self.arbol[codigo_habilidad][2] == "Artesano"):
                crafteo = self.craftear()
                quitar = False
                for objeto in self.inventario_nombres:
                    for ingrediente in crafteo[1]:
                        if(ingrediente.nombre == objeto):
                            self.inventario.pop(
                                self.inventario_nombres.index(objeto))
                            quitar = True
                if(quitar):
                    Juego.maquina(crafteo[2], self)
            elif(self.arbol[codigo_habilidad][2] == "Alquimista"):
                print("Que quieres mejorar?")
                for objeto in range(0, len(self.inventario_nombres)):
                    print("{objeto + 1}: self.inventario_nombres[objeto]")
                objeto = self.inventario[int(input()) - 1]
                Juego.maquina(objeto.nombre, self, 0.5)
        self.energia -= gm.habilidades[contexto_habilidad][
            self.arbol[codigo_habilidad][2]]
        return [True, False]
    
    def equipar(self, objeto: Objeto):
        lugares = []
        lugar = ""
        espalda = ""
        for equipo in self.equipo:
            if(equipo.nombre in gm.cabeza):
                lugares.append("cabeza")
            elif(equipo.nombre in gm.cara):
                lugares.append("cara")
            elif(equipo.nombre in gm.cuello):
                lugares.append("cuello")
            elif(equipo.nombre in gm.torso):
                lugares.append("torso")
            elif(equipo.nombre in gm.espalda):
                lugares.append("espalda")
                espalda = equipo
            elif(equipo.nombre in gm.piernas):
                lugares.append("piernas")
            elif(equipo.nombre in gm.pies):
                lugares.append("pies")
            elif(equipo.nombre in gm.cuerpo_completo):
                lugares.append("cuerpo_completo")
        if(objeto.nombre in gm.cabeza):
            lugar = "cabeza"
        elif(objeto.nombre in gm.cara):
            lugar = "cara"
        elif(objeto.nombre in gm.cuello):
            lugar = "cuello"
        elif(objeto.nombre in gm.torso):
            lugar = "torso"
        elif(objeto.nombre in gm.espalda):
            lugar = "espalda"
        elif(objeto.nombre in gm.piernas):
            lugar = "piernas"
        elif(objeto.nombre in gm.pies):
            lugar = "pies"
        elif(objeto.nombre in gm.cuerpo_completo):
            lugar = "cuerpo_completo"
        if(objeto.nombre in gm.cuerpo_completo):
            for equipo in range(0, len(self.equipo)):
                print(self.equipo[0].nombre)
                indice = self.equipo.index(self.equipo[0])
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
            indice = lugares.index(lugar)
            if(self.equipo[indice].estadistica == "F"):
                self.fuerza -= self.equipo[indice].boosteo
            elif(self.equipo[indice].estadistica == "R"):
                self.resistencia -= self.equipo[indice].boosteo
            elif(self.equipo[indice].estadistica == "C"):
                self.carisma -= self.equipo[indice].boosteo
            elif(self.equipo[indice].estadistica == "I"):
                self.inteligencia -= self.equipo[indice].boosteo
            elif(self.equipo[indice].estadistica == "S"):
                self.sabiduria -= self.equipo[indice].boosteo
            elif(self.equipo[indice].estadistica == "V"):
                self.velocidad -= self.equipo[indice].boosteo
            print(f"{self.nombre} se ha quitado {self.equipo[indice].nombre}")
            self.quitar_equipo(self.equipo[indice])
            self.equipo.pop(indice)
            self.equipo_nombres.pop(indice)
        
        self.equipo.append(objeto)
        self.equipo_nombres.append(objeto.nombre)
        indice = self.inventario.index(objeto)
        if(objeto.estadistica == "F"):
            self.fuerza += objeto.boosteo
        elif(objeto.estadistica == "R"):
            self.resistencia += objeto.boosteo
        elif(objeto.estadistica == "C"):
            self.carisma += objeto.boosteo
        elif(objeto.estadistica == "I"):
            self.inteligencia += objeto.boosteo
        elif(objeto.estadistica == "S"):
            self.sabiduria += objeto.boosteo
        elif(objeto.estadistica == "V"):
            if(self.zona in gm.agua):
                self.velocidad += objeto.boosteo
        print(f"{objeto.nombre} equipado !!")
        if("Shaed" in objeto.nombre):
            self.condicion.update({'Invisible': 10})
        self.anadir_equipo(objeto, indice)
        
        self.actualizar_stats()
        print("--------------------------------------------------------------")
    
    def desequipar(self):
        print("Que objeto quieres desequiparte?")
        for equipo in range(0, len(self.equipo_nombres)):
            print(f"{equipo+1}: {self.equipo_nombres[equipo]} | "
                  + f"{self.equipo[equipo].estadistica}: "
                  + f"{self.equipo[equipo].boosteo}")
        print(f"{len(self.equipo_nombres)+1}: Salir")    
        objeto = int(input())
        if(objeto == len(self.equipo_nombres)+1):
            return False
        if(self.equipo[objeto-1].estadistica == "F"):
            self.fuerza -= self.equipo[objeto-1].boosteo
        elif(self.equipo[objeto-1].estadistica == "R"):
            self.resistencia -= self.equipo[objeto-1].boosteo
        elif(self.equipo[objeto-1].estadistica == "C"):
            self.carisma -= self.equipo[objeto-1].boosteo
        elif(self.equipo[objeto-1].estadistica == "I"):
            self.inteligencia -= self.equipo[objeto-1].boosteo
        elif(self.equipo[objeto-1].estadistica == "S"):
            self.sabiduria -= self.equipo[objeto-1].boosteo
        elif(self.equipo[objeto-1].estadistica == "V"):
            if(self.zona in gm.agua):
                self.velocidad -= self.equipo[objeto-1].boosteo
        print(f"{self.nombre} se ha quitado {equipo.nombre}")
        self.quitar_equipo(equipo)
        self.equipo.pop(objeto-1)
        self.equipo_nombres.pop(objeto-1)
        
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
        for numero in range(1, 4):
            print("\t\t\t        |\t\t  |")
            codigo_habilidad = "A"+str(numero)
            if(self.arbol[codigo_habilidad][0] == 0):
                print(f"{self.arbol[codigo_habilidad][1]}\t\t\t      |"
                      + f"{codigo_habilidad}|\t", end="")
            else:
                print(f"{self.arbol[codigo_habilidad][1]}\t\t\t      |"
                      + f"{self.arbol[codigo_habilidad][2]}|\t", end="")
            codigo_habilidad = "B"+str(numero)
            if(self.arbol[codigo_habilidad][0] == 0):
                print(f"\t|{codigo_habilidad}|")
            else:
                print(f"\t|{self.arbol[codigo_habilidad][2]}|")
        seleccion_habilidad = input("Que habilidad deseas desbloquear? "
                          + "(0 para salir)\n")
        if(seleccion_habilidad == "0"):
            return False
        elif(seleccion_habilidad not in self.arbol.keys()):
            print("Eso no existe")
            self.arbol_habilidades()
        elif(int(seleccion_habilidad[1]) > 1):
            for nivel_habilidad in range(1, int(seleccion_habilidad[1])+1):
                if(self.arbol[
                        seleccion_habilidad[0]+str(nivel_habilidad)][0] == 0):
                    print("No te quieras adelantar >:(")
                    repetir = True
                    break
            if(repetir):
                self.arbol_habilidades()
        elif(self.arbol[seleccion_habilidad][1] > self.puntos_habilidad):
            print("No tienes puntos de habilidad suficientes")
            self.arbol_habilidades()
        else:
            print(f"Has desbloqueado {self.arbol[seleccion_habilidad][2]}!!")
            self.arbol[seleccion_habilidad][0] = 1
            self.puntos_habilidad -= self.arbol[seleccion_habilidad][1]
            if(self.arbol[seleccion_habilidad][2] == "Super Sayain"):
                self.condicion.update({"Super Sayain": self.fuerza})
            return True
            
    def subir_salud_max(self):
        #DEBUG
#    print("----------------------------------------Metodo subir salud maxima")
        self.salud_max+=15
        self.energia_max+=4
        print("Tu salud y energia han aumentado!!")
        self.actualizar_stats()
        return True
    
    def is_ded(self):
        #DEBUG
#        print("------------------------------------------------Metodo is_ded")
        zonas = self.ubicacion.zonas
        zona = zonas.index(self.zona)
        self.condicion = {"Muerto": 1}
        gm.personajes_muertos.append(self)
        gm.personajes.remove(self)
        objeto = Juego.tranformar_objeto("Cadaver de "+self.nombre)
        objeto.stats()
        self.ubicacion.objetos_activos[zona].append(objeto)
#        self.ubicacion.cantidades_objetos_activos[z].append(1)
        self.ubicacion.objetos[zona].append(objeto.nombre)
        self.ubicacion.cantidades[zona].append(1)
        
        if(self != gm.personaje_malo):
            for objeto_inventario in self.inventario:
                self.ubicacion.objetos_activos[zona].append(objeto_inventario)
                if(objeto_inventario.nombre not in self.ubicacion.objetos[
                        zona]):
                    self.ubicacion.objetos[zona].append(
                        objeto_inventario.nombre)
                    self.ubicacion.cantidades[zona].append(1)
                else:
                    indice = self.ubicacion.objetos[zona].index(
                        objeto_inventario.nombre)
                    self.ubicacion.cantidades[zona][indice] += 1
            self.inventario = []
            self.inventario_nombres = []
            for equipo in self.equipo:
                self.ubicacion.objetos_activos[zona].append(equipo)
                if(equipo.nombre not in self.ubicacion.objetos[zona]):
                    self.ubicacion.objetos[zona].append(equipo.nombre)
                    self.ubicacion.cantidades[zona].append(1)
                else:
                    indice = self.ubicacion.objetos[zona].index(equipo.nombre)
                    self.ubicacion.cantidades[zona][indice] += 1
            self.equipo = []
            self.equipo_nombres = []
            self.cartera_obj = {}
            self.cartera = 0
        return True
    
    def usar_maquina(self):
        print("Que objeto deseas insertar?(0 para salir)")
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
        
        objeto = int(input())-1
        if(objeto == -1):
            return False
        for llave in self.cartera_obj:
            if(objeto == 0):
                break
            objeto -= 1
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
            zona = zonas.index(self.zona)
            for lista_objetos in range (0, len(objetos)):
                objetos_nombres.append([])
                for objeto in range (0, len(objetos[lista_objetos])):
                    objetos_nombres[lista_objetos].append(objetos[
                        lista_objetos][objeto].nombre)
    #        print(objetos_nombres)
    #        print(objeto.nombre)
            objeto = objetos_nombres[zona].index(objeto.nombre)
    #        print(self.ubicacion.objetos[z])
            indice = self.ubicacion.objetos[zona].index(objeto.nombre)
            self.ubicacion.cantidades[zona][indice] -= 1
    #        self.ubicacion.cantidades_objetos_activos[z][j] -= 1
            objeto = objetos[zona][objeto]
            if(objeto.nombre == "Cartucho de magnum"):
                for bala in range(0, 16):
                    gm.anadir_obj_manual("Bala de magnum", self)
                return True
            elif(objeto.nombre == "Cartucho de sniper"):
                for bala in range(0, 6):
                    gm.anadir_obj_manual("Bala de sniper", self)
                return True
# =============================================================================
#              print(self.ubicacion.cantidades_objetos_activos()[z][j])
#              print(self.ubicacion.cantidades_objetos_activos()[z])
#              print(f'\nFelicidades!! Obtuviste {objeto.nombre}, quedan
#              {self.ubicacion.cantidades()[z][h]} restantes')
# =============================================================================
            indice_nombre = objetos_nombres[zona].index(objeto.nombre)
            objetos_nombres[zona].remove(objeto.nombre)
            if(self.ubicacion.cantidades[zona][indice] <= 0):
                self.ubicacion.objetos_activos[zona].pop(indice_nombre)
                self.ubicacion.objetos[zona].pop(indice)
                self.ubicacion.cantidades[zona].pop(indice)
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
        
    def usar_obj(self, objetivo = None, objeto = None):
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
            for objeto_inventario in range(0, len(self.inventario)):
                if(self.inventario[objeto_inventario].estadistica != "F" 
                   or "Pocion" in self.inventario_nombres[objeto_inventario]):
                    objetos_permitidos.append(self.inventario[
                        objeto_inventario].nombre)
            
            print("Que quieres usar?")
            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
            contador=0
            for objeto in self.cartera_obj:
                if(objeto in objetos_permitidos):
                    print(f"{contador+1}, \t{objeto:.<24s}: "
                          + f"{self.cartera_obj[objeto]} "
                          + "| \t\t"
                          + str(self.inventario[self.inventario_nombres.index(
                                  objeto)].estadistica)
                          + "| \t"
                          + str(self.inventario[self.inventario_nombres.index(
                              objeto)].boosteo))
                    contador+=1
            
            contador = int(input())-1
            for objeto in self.cartera_obj:
                if(objeto in objetos_permitidos):
                    if(contador == 0):
                        break
                    contador -= 1
            objeto = self.inventario[self.inventario_nombres.index(objeto)]
            
        if(objeto.nombre not in self.inventario_nombres):
            print("Pues no tienes eso shavo")
            return False
        
        for nombre in range(0, len(gm.Dfnombres_o)):
            if(gm.Dfnombres_o.iloc[nombre,0] == objeto.nombre):
                break
            
        zonas = self.ubicacion.zonas
        zona = zonas.index(self.zona)
        if(objetivo == None):
            print("Con quien lo quieres usar?")
            for personaje in range(0, len(gm.personajes)):
                if(gm.personajes[personaje].zona == self.zona):
                    print(f"{personaje+1}: {gm.personajes[personaje].nombre}")
            objetivo = gm.personajes[int(input())-1]
        if(type(objetivo) == str):
            for personaje_muerto in gm.personajes_muertos:
                if(personaje_muerto.nombre in objetivo):
                    objetivo = personaje_muerto
                    break
            limite_nivel = 13 + 5 * (objetivo.nivel)
        elif(objeto in gm.personajes):
            for personaje in gm.personajes:
                if(personaje.nombre == objetivo):
                    objetivo = personaje
                    break
            limite_nivel = 13 + 5 * (objetivo.nivel)
        elif(objetivo in self.ubicacion.enemigos_activos[zona]):
            for enemigo in self.ubicacion.enemigos_activos[zona]:
                if(enemigo.nombre == objetivo):
                    objetivo = enemigo
                    break
        elif(type(objetivo) == list):
            objetivos = [[],[]]
            for objetivo_individual in objetivo:
                if(objetivo_individual in gm.personajes):
                    objetivos[0].append(objetivo_individual)
                elif(objetivo_individual in self.ubicacion.enemigos_activos[
                        zona]):
                    objetivos[1].append(objetivo_individual)
            if(objetivos == [[],[]]):
                print("No se encontraron los target")
                return False
        else:
            print("No se encontro el target")
            return False
            
        # -----------------------------------------------------Objetos perrones
        Dfestadisticas_objetos = gm.Dfestadisticas_objetos.iloc[nombre,0]
        
        cantidad = int(gm.Dfboosteos_objetos.iloc[nombre,0])
        
        if("Sustancia" in objeto.nombre):
            indice = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, indice)
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
            for contador_mapa in range(0, 3):
                self.explorar()
        
        elif(objeto.nombre == "GPS"):
            lugares_conocidos = self.mapa[self.zona]
            lugares_posibles = gm.mapa_master[self.zona]
            print("Utilizando GPS... existen "
                  + f"{len(lugares_posibles) - len(lugares_conocidos)}"
                  + " lugares sin descubrir")
        
        elif(objeto.nombre == "Brujula"):
            if(self.ubicacion.nombre == "campamento"):
                print("La brujula esta vuelta loca...")
            else:
                lugares_conocidos = self.mapa[self.zona]
                for lugar_conocido in lugares_conocidos:
                    if(lugar_conocido in gm.jefes.values()):
                        print(f"Dentro de {lugar_conocido} se siente "
                              + "una presencia"
                              + " muy maligna...")
                        break
        
        elif(objeto.nombre == "Carnada") and (objetivo.nombre 
                                              not in gm.jefes.keys()):
            print(type(objetivo.condicion))
            objetivo.condicion.update({"Oloroso": 2})
            lugares_conocidos = gm.mapa_master[self.zona]
            print(gm.carneables)
            for lugar_conocido in lugares_conocidos:
                for objeto_lugar in range(0, len(gm.objetos_lugares)):
                    zonas_lugar = gm.objetos_lugares[objeto_lugar].zonas
                    if(lugar_conocido in zonas_lugar):
                        lugar = gm.objetos_lugares[objeto_lugar]
                        break
                # ----------------------------lugar = objeto lugar de la zona c
                for enemigo in lugar.enemigos_activos[
                        lugar.zonas.index(lugar_conocido)]:
                    print(enemigo.nombre)
                    if(enemigo.nombre in gm.carneables):
                        lugar.enemigos_activos[
                            lugar.zonas.index(lugar_conocido)].remove(enemigo)
                        self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)].append(
                                enemigo)
                        enemigo.condicion.update({"Atraido": 2})
                        enemigo.zona = self.zona
                        print(f"La carnada ha atraido a un {enemigo.nombre} "
                              + "salvaje...")
                        break
        
        elif(objeto.nombre == "Control universal"):
            if("Pila" in self.inventario_nombres):
                if(objetivo.nombre in robots):
                    self.peso -= gm.Dfespacios_objetos.iloc[nombre,0]
                    indice = self.inventario_nombres.index("Pila")
                    self.inventario.pop(indice)
                    self.inventario_nombres.pop(indice)
                    return {"Control universal": objetivo.defender()}
                self.peso -= gm.Dfespacios_objeto.iloc[nombre,0]
                indice = self.inventario_nombres.index("Pila")
                self.inventario.pop(indice)
                self.inventario_nombres.pop(indice)
                print("Felicidades!! Has gastado una pila a lo tonto :D")
                return True
            print("Oh no! Tu control ya no tiene bateria!! :(")
            return True
        
        elif(objeto.nombre == "Alcohol"):
            if(objetivo.nombre in borrachos):
                self.peso -= gm.Dfespacios_objetos.iloc[nombre,0]
                indice = self.inventario_nombres.index("Alcohol")
                self.inventario.pop(indice)
                self.inventario_nombres.pop(indice)
                return {"Alcohol": objetivo.defender()}
            print("Al enemigo no le interesa tu alcohol barato...")
            return True
        
        elif(objeto.nombre == "Binoculares" or objeto.nombre == "Sniper"):
            print("A donde deseas mirar?")
            for zona in range(0, len(self.mapa[self.zona])):
                print(f"{zona+1}: {self.mapa[self.zona][zona]}")
            zona = int(input())
            zona = self.mapa[self.zona][zona - 1]
            for lugar in range(0, len(gm.objetos_lugares)):
                zonas_lugar = gm.objetos_lugar[lugar].zonas
                if(zona in lugar):
                    ubicacion = gm.objetos_lugar[lugar]
                    break
            indice = ubicacion.zonas.index(zona)
            for enemigo in ubicacion.enemigos_activos[indice]:
                print(f"Puedes ver un {enemigo.nombre} salvaje acechando"
                      + " a lo lejos...")
            if("Sniper" in objeto.nombre 
               and "Bala de sniper" in self.inventario_nombres):
                print("A quien quieres dispararle los sesos con el sniper?")
                print("INDICE \t NOMBRE \t SALUD")
                print("0: Nadie")
                for enemigo in range (0, len(ubicacion.enemigos_activos[
                        indice])):
                    print(f"{enemigo+1}: "
                          + str(ubicacion.enemigos_activos[indice][
                              enemigo].nombre)
                          + "\t"
                          + str(ubicacion.enemigos_activos[indice][
                              enemigo].salud))
                objetivo = int(input())-1
                objetivo = ubicacion.enemigos_activos[indice][objetivo]
                if(objetivo <= -1):
                    return False
                else:
                    print("Tirando dados...")
                    tirada = gm.dados(1, 10)[0]
                    print("Tiraste "+str(tirada))
                    dano = self.fuerza + int(objeto.boosteo) + tirada
                    tirada = gm.dados(1, 10)[0]
                    if(tirada >= 4):
                        dano = 0
                        print("Has fallado tu ataque!")
                    objetivo.cambiar_hp(-dano, self)
                    indice = self.inventario_nombres.index("Bala de sniper")
                    self.anadir_equipo(self.inventario[indice], indice)
            else:
                print("No tienes municion :o")
                return False
            return True
        
        elif("humana" in objeto.nombre):
            self.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0])
            if(self.salud > self.salud_max):
                self.salud = self.salud_max
            self.actualizar_stats()
            if(self.is_wendigo):
                self.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0]*4)
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
                indice = self.inventario_nombres.index(objeto.nombre)
                self.inventario.pop(indice)
                for objeto_inventario in self.inventario:
                    if("Carne" in objeto_inventario.nombre):
                        carnes.append(objeto_inventario)
                    self.ubicacion.objetos_activos[zona].append(
                        objeto_inventario)
                    self.ubicacion.objetos[zona].append(
                        objeto_inventario.nombre)
                    self.ubicacion.cantidades[zona].append(1)
                self.inventario = []
                self.inventario_nombres = []
                for equipo in self.equipo:
                    self.ubicacion.objetos_activos[zona].append(equipo)
                    self.ubicacion.objetos[zona].append(equipo.nombre)
                    self.ubicacion.cantidades[zona].append(1)
                self.equipo = []
                self.equipo_nombres = []
                self.cartera_obj = {}
                self.cartera = 0
                for carne in carnes:
                    print(carne.nombre)
                    self.anadir_obj(carne)
                self.actualizar_stats()
                return True
        
        elif("Gasolina" in objeto.nombre or "Aceite" in objeto.nombre 
             or "Alcohol" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Le has hechado gasolina a todos tus companeros, "
                      + "maravillosa jugada! :D")
                for objetivo in objetivos[0]:
                    if("Quemado" in objetivo.condicion):
                        objetivo.enfermar("Quemado", 3)
                    else:
                        objetivo.condicion.update({"Engasolinado": 2})
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Te has resbalado y echado gasolina tu solo, "
                      + "que egoista...")
                if("Quemado" in self.condicion):
                    self.enfermar("Quemado", 3)
                else:
                    self.condicion.update({"Engasolinado": 2})
            elif(tirada <= 10):#-------------------------------------Un enemigo
                objetivo = objetivos[1][Juego.dados(1, len(objetivos[1]))[0]-1]
                print(f"Le has hechado gasolina a {objetivo.nombre}, no se ve"
                      + " muy feliz...")
                if("Quemado" in objetivo.condicion):
                    objetivo.enfermar("Quemado", 3)
                else:
                    objetivo.condicion.update({"Engasolinado": 2})
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Has banado el suelo con gasolina!")
            elif(tirada <= 18):#------------------------------------------Todos
                print("Haces un mortal triple y riegas gasolina a todos")
                for objetivo in objetivos:
                    for objetivo_individual in objetivo:
                        if("Quemado" in objetivo_individual.condicion):
                            objetivo_individual.enfermar("Quemado", 3)
                        else:
                            objetivo_individual.condicion.update(
                                {"Engasolinado": 2})
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("No se como le hiciste, pero banaste a todos tus "
                      + "rivales")
                for objetivo in objetivos[1]:
                    if("Quemado" in objetivo.condicion):
                        objetivo.enfermar("Quemado", 3)
                    else:
                        objetivo.condicion.update({"Engasolinado": 2})
        
        elif("Fosforo" in objeto.nombre or "Antorcha" in objeto.nombre 
             or "Encendedor" in objeto.nombre):
            for objetivo in objetivos:
                for objetivo_individual in objetivo:
                    if("Engasolinado" in objetivo_individual.condicion):
                        objetivo_individual.enfermar("Quemado", 3)
        
        elif("Lodo" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Le has hechado lodo a todos tus companeros, "
                      + "maravillosa jugada! :D")
                for objetivo in objetivos[0]:
                    objetivo.condicion.update({"Cegado": 1})
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Te has resbalado y echado lodo tu solo, que egoista...")
                self.condicion.update({"Cegado": 1})
            elif(tirada <= 10):#-------------------------------------Un enemigo
                objetivo = objetivos[1][Juego.dados(1, len(objetivos[1]))[0]-1]
                print(f"Le has hechado lodo a {objetivo.nombre}, no se ve "
                      + "muy feliz...")
                objetivo.condicion.update({"Cegado": 1})
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Has banado el suelo con lodo!")
            elif(tirada <= 18):#------------------------------------------Todos
                print("Haces un mortal triple y riegas lodo a todos")
                for objetivo in objetivos:
                    for objetivo_individual in objetivo:
                        objetivo_individual.condicion.update({"Cegado": 1})
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("No se como le hiciste, pero banaste a todos "
                      + "tus rivales")
                for objetivo in objetivos[1]:
                    objetivo.condicion.update({"Cegado": 1})
        
        elif("Dinamita" in objeto.nombre):
            tirada = Juego.dados(1, 20)[0]
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Has activado la dinamita en donde se encuentran tu y "
                      + "tus companeros exitosamente")
                for objetivo in objetivos[0]:
                    objetivo.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0])
                    objetivo.actualizar_stats()
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Has activado la dinamita... pero has olvidarlo "
                      + "lanzarla")
                self.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0])
                self.actualizar_stats()
            elif(tirada <= 10):#-------------------------------------Un enemigo
                objetivo = objetivos[1][Juego.dados(1, len(objetivos[1]))[0]-1]
                print(f"Le has lanzado la dinamita a {objetivo.nombre} "
                      + "de una manera "
                      + "muy radical")
                objetivo.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0])
                objetivo.actualizar_stats()
            elif(tirada <= 15):#------------------------------------------Nadie
                print("Lanzaste la dinamita muy lejos y exploto la casa de "
                      + "tu abuela")
            elif(tirada <= 18):#------------------------------------------Todos
                print("La explosion fue mucho mas grande de lo que "
                      + "esperabas...")
                for objetivo in objetivos:
                    for objetivo_indivual in objetivo:
                        objetivo_individual.cambiar_hp(
                            gm.Dfboosteos_objetos.iloc[
                            nombre,0])
                        objetivo_individual.actualizar_stats()
            elif(tirada <= 20):#-----------------------------Todos los enemigos
                print("Lanzaste la dinamita justo donde querias!")
                for objetivo in objetivos[1]:
                    objetivo.cambiar_hp(gm.Dfboosteos_objetos.iloc[nombre,0])
                    objetivo.actualizar_stats()
        
        elif("Botella" in objeto.nombre and "Quemado" in self.condicion):
            self.condicion.pop("Quemado")
            self.curar()
            indice = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, indice)
            self.actualizar_stats()
            print(f"\n{self.nombre} ha usado con exito {objeto.nombre}, "
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
                objetivo.stats()
            else:
                print(f"Fuerza de {objetivo.nombre}: {objetivo.fuerza}")
        
        elif("Escudo" in objeto.nombre):
            self.resistencia += objeto.boosteo
            defensa = self.defender()
            self.resistencia -= objeto.boosteo
            if(objetivo in gm.personajes):
                return {"Escudo": defensa}
            else:
                objetivo.condicion.update({"Bloqueado": defensa})
                print("ENEMIGO BLOQUEADO!!")
        
        elif("Trampa de osos" == objeto.nombre or "Jaula" in objeto.nombre):
            zona = self.ubicacion.zonas.index(self.zona)
            self.ubicacion.jaulas[zona].update({objeto.nombre: {objeto: ""}})
            self.ubicacion.objetos_activos[zona].append(objeto)
        
        elif("SCP 427" == objeto.nombre):
            gm.personajes.remove(self)
            gm.personajes_muertos.append(self)
            asistente_nuevo = Asistente(self.salud_max, self.fuerza,
                                        self.resistencia,
                              self.carisma_max, self.inteligencia,
                              self.sabiduria, self.nombre, self.condicion,
                              self.inventario, "SCP", self.nivel, 1,
                              self.zona, self, self.nombre + " SCP")
            asistente_nuevo.condicion.update({"Temporal": 1})
            asistente_nuevo.salud_max *= 4
            asistente_nuevo.salud = self.salud_max
            asistente_nuevo.fuerza *= 4
            asistente_nuevo.resistencia *= 4
            asistente_nuevo.carisma /= 2
            asistente_nuevo.inteligencia /= 2
            asistente_nuevo.sabiduria /= 2
            asistente_nuevo.actualizar_stats()
            self.asistentes.append(asistente_nuevo)
        
        elif("Curita wendiguito" in objeto.nombre):
            objetivo.is_wendigo = False
            objetivo.salud_max /= 3
            objetivo.salud = self.salud_max
            objetivo.fuerza /= 3
            objetivo.resistencia /= 3
            objetivo.carisma *= 2
            objetivo.inteligencia *= 2
            objetivo.sabiduria *= 2
            objetivo.actualizar_stats()
            
        elif("Pocion" in objeto.nombre):
            if(Dfestadisticas_objetos == 'H'):
                objetivo.salud += cantidad
                if(objetivo.salud > limite_nivel):
                    objetivo.salud = limite_nivel
            elif(Dfestadisticas_objetos =='F'):
                objetivo.fuerza += cantidad
                if("Super Sayain" in self.condicion):
                        self.condicion["Super Sayain"] += cantidad
                if(objetivo.fuerza > limite_nivel):
                    objetivo.fuerza = limite_nivel
            elif(Dfestadisticas_objetos=='R'):
                objetivo.resistencia += cantidad
                if(objetivo.resistencia > limite_nivel):
                    objetivo.resistencia = limite_nivel
            elif(Dfestadisticas_objetos=='C'):
                objetivo.carisma += cantidad
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
