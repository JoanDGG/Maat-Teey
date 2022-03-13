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
        for objeto in (self.inventario):
            self.inventario_nombres.append(objeto.nombre)
        self.peso = 0
        for objeto in self.inventario:
            self.peso += objeto.peso
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
        self.in_memoriam = {}
    
    def __str__(self):
        texto = (super().stats() + f"| Peso: {self.peso} \n Nivel: "
              + f"{self.nivel:<20} | Ubicacion: {self.ubicacion.nombre} \n "
              + f"Zona: {self.zona:<21} | Carga: {self.carga} \n Saldo: "
              + f"{self.cartera:<20} \n Equipo: \n {self.equipo_nombres}\n "
              + f"Inventario: \n {self.cartera_obj}")
        if(self.is_wendigo):
            texto += ("ESTATUS: WENDIGO")
        return texto
    
    def activar_habilidad(self, contexto_habilidad, omitidos = []):
        estadisticas = ["Salud", "Fuerza", "Resistencia", "Carisma",
                        "Inteligencia", "Sabiduria", "Energia"]
        if(contexto_habilidad != "anticipacion"):
            print("Que habilidad quieres activar? (0 para salir)")
            print("HABILIDAD\tCOSTO")
            vacio = True
            for codigo_habilidad in self.arbol:
                for numero_habilidad in range(0, len(gm.habilidades[
                        contexto_habilidad])):
                    habilidad = list(gm.habilidades[
                        contexto_habilidad].keys())[numero_habilidad]
                    if(habilidad in self.arbol[codigo_habilidad][2] 
                       and self.arbol[codigo_habilidad][0] == 1):
                        vacio = False
                        print(f"{codigo_habilidad}: "
                              + f"{self.arbol[codigo_habilidad][2]}:\t"
                              + str(gm.habilidades[contexto_habilidad][
                                  list(gm.habilidades[
                                      contexto_habilidad].keys())[
                                      numero_habilidad]]))
            if(vacio):
                print("No hay ninguna habilidad activa actualmente\n")
                codigo_habilidad = "0"
            else:
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
                print("De quien te vas a disfrazar?")
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
                print("A quien vas a pacificar?")
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
                self.asistentes.append(oso)
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
                    print(enemigo)
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
                objetivo.carisma -= gm.dados(1, objetivo.carisma//2)
            elif(self.arbol[codigo_habilidad][2] == "Lord meme"):
                for enemigo in range(0, len(self.ubicacion.enemigos_activos[
                        self.ubicacion.zonas.index(self.zona)])):
                    enemigo.carisma -= gm.dados(1, objetivo.carisma//2)
                    omitidos.append(enemigo)                
            elif(self.arbol[codigo_habilidad][2] == "Robots"):
                robot = Asistente(25, 11, 7, 9, 15, 15, "Robot", "Saludable",
                                  "Tornillo", "Robot", 2, 1, self.zona, self,
                                  "Robot")
                robot.condicion.update({"Lealtad": 5})
                self.asistentes.append(robot)
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
                tirada = gm.dados(1, 2)
                if(tirada == 1):
                    objetivo, dano, arma = self.atacar(
                        self.ubicacion.enemigos_activos[
                            self.ubicacion.zonas.index(self.zona)], 5)
                else:
                    objetivo, dano, arma = self.atacar(
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
            self.condicion.update({"Invisible": 10})
            if(self.zona in gm.lugares_iluminados):
                self.condicion.pop("Invisible")
        elif("Shaed" in self.equipo_nombres and gm.dia):
            self.condicion.pop("Invisible")
        elif("Shaed mejorado" in self.equipo_nombres and not gm.dia):
            self.condicion.update({"Invisible": 10})
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
                for objeto_indice in range (0, len(objetos[lista_objetos])):
                    objetos_nombres[lista_objetos].append(objetos[
                        lista_objetos][objeto_indice].nombre)
    #        print(objetos_nombres)
    #        print(objeto.nombre)
            objeto_seleccionado_indice = objetos_nombres[zona].index(
                                                                 objeto.nombre)
            cantidad_seleccionado_indice = self.ubicacion.objetos[zona].index(
                                                                 objeto.nombre)
            self.ubicacion.cantidades_objetos[zona][
                                            cantidad_seleccionado_indice] -= 1
            objeto = objetos[zona][objeto_seleccionado_indice]
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
#              print(f"\nFelicidades!! Obtuviste {objeto.nombre}, quedan
#              {self.ubicacion.cantidades_objetos[z][h]} restantes")
# =============================================================================
            indice_nombre = objetos_nombres[zona].index(objeto.nombre)
            objetos_nombres[zona].remove(objeto.nombre)
            if(self.ubicacion.cantidades_objetos[zona][indice_nombre] <= 0):
                self.ubicacion.objetos_activos[zona].pop(indice_nombre)
                self.ubicacion.objetos[zona].pop(indice_nombre)
                self.ubicacion.cantidades_objetos[zona].pop(indice_nombre)
            self.quitar_equipo(objeto)
            
            self.actualizar_stats()
            self.exceso_peso()
            print(f"Has encontrado {objeto.nombre}!!")
        else:
            print(f"Has encontrado {objeto} dineros en el suelo!!")
            self.cartera += objeto
        print(self)
        return True
        
    def arbol_habilidades(self):
        print("{:-^70}".format("Arbol de habilidades"))
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
#            self.arbol_habilidades()
        else:
            print(f"Has desbloqueado {self.arbol[seleccion_habilidad][2]}!!")
            self.arbol[seleccion_habilidad][0] = 1
            self.puntos_habilidad -= self.arbol[seleccion_habilidad][1]
            if(self.arbol[seleccion_habilidad][2] == "Super Sayain"):
                self.condicion.update({"Super Sayain": self.fuerza})
            return True
    
    def atacar(self, enemigos_presentes, multiplicador = 1):
        #DEBUG
#    print("------------------------------------------Metodo atacar personaje")
        puno = Objeto("Puno", 0, "F", 0, 1, 2, 0)
        if(len(enemigos_presentes) > 1):
            print("\nQuien sera tu victima?")
            print("INDICE \t NOMBRE \t SALUD")
            for enemigo in range (0, len(enemigos_presentes)):
                print(f"{enemigo+1}: "
                      + f"{enemigos_presentes[enemigo].nombre}\t"
                      + f"{enemigos_presentes[enemigo].salud}")
            objetivo = enemigos_presentes[int(input())-1]
        else:
            objetivo = enemigos_presentes[0]
        print("Deseas usar algun objeto?")
        objetos_permitidos = []
        for objeto in range(0, len(self.inventario)):
            if(self.inventario[objeto].estadistica == "F"):
                objetos_permitidos.append(self.inventario[objeto])
        print("0: A puno cerrado")
        for objeto in range(0, len(objetos_permitidos)):
            print(f"{objeto+1}: {objetos_permitidos[objeto].nombre}")
        seleccionado = int(input())
        if(seleccionado == 0):
            arma = puno
        elif(seleccionado > len(objetos_permitidos) or seleccionado < 0):
            print("No es valido")
            arma = puno
        else:
            arma = objetos_permitidos[seleccionado-1]
        print("Tirando dados...")
        tirada_dano = gm.dados(1, 10)
        print("Tiraste "+str(tirada_dano))
        
        if(self.nombre == "Turati" and self.arbol["A2"][0] == 1):
            tirada = gm.dados(1, 10)
            if(tirada == 1):
                multiplicador *= 2
        elif(self.nombre == "Sebas" and "Kaio Ken" in self.condicion):
            multiplicador *= 2
        elif(self.nombre == "Ruben" and self.arbol["A1"][0] == 1 
             and objetivo.categoria == "Animal"):
            multiplicador *= 2
        dano = self.fuerza*multiplicador + int(arma.boosteo) + tirada_dano
        
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
                indice = self.inventario_nombres.index("Bala de magnum")
                self.anadir_equipo(self.inventario[indice], indice)
                
        elif(arma.nombre == "Sniper") or (arma.nombre == "Rifle"):
            if("Bala de sniper" not in self.inventario_nombres):
                print("No tienes municion :o")
                dano = 0
            else:
                indice = self.inventario_nombres.index("Bala de sniper")
                self.anadir_equipo(self.inventario[indice], indice)
                
        elif(arma.nombre == "Arco") or (arma.nombre == "Arco mejorado"):
            if(("Flecha" not in self.inventario_nombres) 
               and ("Flecha emplumada" not in self.inventario_nombres) 
               and ("Flecha primitiva" not in self.inventario_nombres)):
                print("No pues estas mongolo")
                dano = 0
            else:
                print("Que flecha quieres usar?")
                for objeto in range(0, len(self.inventario_nombres)):
                    if("Flecha" in self.inventario_nombres[objeto]):
                        print(f"{objeto+1}: {self.inventario_nombres[objeto]}")
                seleccionado = int(input())-1
                flecha = self.inventario[seleccionado].boosteo
                dano += flecha
                indice = self.inventario_nombres[seleccionado]
                self.anadir_equipo(self.inventario[seleccionado], seleccionado)
        if("Cegado" in self.condicion):
            tirada = gm.dados(1, 10)
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
        ataque = int(input("Como quieres atacar?\n1: Intimidar\n2: "
                           + "Tranquilizar\n3: Persuadir"))-1
        dano = self.carisma + gm.dados(1, self.carisma_max/10)
        for nombre in range (0, len(gm.Dfnombres_enemigos)):
            if(gm.Dfnombres_enemigos.iloc[nombre,0] == enemigo.nombre):
                if(ataque == 0):
                    dano -= gm.Dfintimidar_enemigos.iloc[nombre,0]
                elif(ataque == 1):
                    dano -= gm.Dftranquilizar_enemigos.iloc[nombre,0]
                elif(ataque == 2):
                    dano -= gm.Dfpersuadir_enemigos.iloc[nombre,0]
        return[enemigo, dano]
    
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
            indice_zona = zonas.index(self.zona)
        else:
            for indice_lugar in range(0, len(gm.objetos_lugares)):
                zonas_lugar = gm.objetos_lugares[indice_lugar].zonas
                if(zona in zonas_lugar):
                    break
            lugar = gm.objetos_lugares[indice_lugar]
            zonas = lugar.zonas
            indice_zona = zonas.index(zona)
        probabilidad = gm.dados(1, 100)
        multiplicador = 1
        
        if(lugar.nombre == "Fondo del mar"):
            iluminacion = iluminacion[3:]
            
        if(lugar == self.ubicacion and self.zona not in gm.lugares_iluminados):
            ningun_iluminado = True
            for indice_iluminacion in range(0, len(iluminacion)):
                if(iluminacion[indice_iluminacion] in self.inventario_nombres):
                    ningun_iluminado = False
                    break
            objeto_usado = len(iluminacion)
            if(not ningun_iluminado):
                print("Quieres usar algun objeto para ayudarte a buscar?")
                for indice_iluminacion in range(0, len(iluminacion)):
                    if(iluminacion[indice_iluminacion] in self.inventario_nombres):
                        print(f"{indice_iluminacion+1}: "
                              + "iluminacion[indice_iluminacion]")
                print(f"{len(iluminacion)+1}: Nada")
                objeto_usado = int(input())-1
            
            if(objeto_usado < len(iluminacion)):
                for nombre in range(0, len(gm.Dfnombres_objetos)):
                    if(gm.Dfnombres_objetos.iloc[nombre,0] == iluminacion[
                            objeto_usado]):
                        break
                if(gm.Dfusos_objetos.iloc[nombre,0] == 1):
                    self.peso -= gm.Dfespacios_objetos.iloc[nombre,0]
                    indice = self.inventario_nombres.index(objeto.nombre)
                    self.inventario_nombres.remove(objeto.nombre)
                    self.inventario.pop(indice)
                multiplicador = (objeto_usado+1)*2
                probabilidad+=multiplicador
        
        if(self.nombre == "Ruben" and self.arbol["A3"][0] == 1):
            probabilidad += 20
        elif(self.nombre == "Norman" and self.arbol["A1"][0] == 1):
            probabilidad += 10
        
        objeto_buscado = ""
        print("Buscando...")
        if(objeto == None):
            #---------------------------------------------------------aleatorio
            tirada = gm.dados(1, len(lugar.objetos_activos[indice_zona]))
            objeto = lugar.objetos_activos[indice_zona][tirada-1]
        else:
            encontrado = False
            for indice_objeto in range(0, len(lugar.objetos_activos[
                    indice_zona])):
                if(objeto == lugar.objetos_activos[indice_zona][
                        indice_objeto].nombre):
                    encontrado = True
                    break
            if(not encontrado):
                print("Aqui no existe shavo")
                return False                
            objeto = lugar.objetos_activos[indice_zona][indice_objeto]
            
        print(objeto.nombre)
        if(objeto.nombre == "SCP 053"):
            print("No nel no puedes jaja salu3")
        if(objeto.nombre in scp):
            #------------------------------dialogo scp, crear objeto pertinente
            print("\nDi lo tuyo...\n")
            if(objeto.nombre == "SCP 079"):
                objeto_buscado = Objeto("Tecla", "--", "--", 0, 1, 1, 0)
                gm.anadir_obj_manual(objeto_buscado, self)
                print("(texto de la compu)")
                gm.anadir_obj_manual("Nota de consejo", self)
                return True
            elif(objeto.nombre == "SCP 682"):
                objeto_buscado = Objeto("Escama", "--", "--", 0, 1, 1, 0)
                gm.anadir_obj_manual(objeto_buscado, self)
                return True
        elif(objeto.nombre in ultra_raros):
            #--------------------------------busca objeto con probabilidad baja
            if(probabilidad >= 80):
                objeto_buscado = objeto
        elif(objeto.nombre in raros):
            #-------------------------------busca objeto con probabilidad media
            if(probabilidad >= 45):
                objeto_buscado = objeto
        else:
            #--------------------------------busca objeto con probabilidad alta
            if(probabilidad >= 15):
                objeto_buscado = objeto
        
        print(probabilidad)
        print(objeto_buscado, "\n")
        if(objeto_buscado == ""):
            print("Que mala suerte shavo, no encontraste el amor de tu bida")
        elif(objeto.nombre == "Dinero"):
            self.anadir_obj(1)
        else:
            for indice_objeto in range(0, len(lugar.objetos_activos[
                    indice_zona])):
                if(objeto.nombre == lugar.objetos_activos[indice_zona][
                        indice_objeto]):
                    break
            
            print("Quedan "
                  + f"{int(lugar.cantidades_objetos[indice_zona][indice_objeto])-1}"
                  + f" {objeto.nombre}s")
            
            if(self.ubicacion != lugar):
                lugar.cantidades_objetos[indice_zona][indice_objeto] -= 1
                if(lugar.cantidades_objetos[indice_zona][indice_objeto] <= 0):
                    lugar.objetos_activos[indice_zona].pop(indice)
                gm.anadir_obj_manual(objeto.nombre, self)
                return True
            
            self.anadir_obj(objeto)
            if(self.zona == "Mercado"):
                print("Eh! Las vas a pagar con tu vida")
                # lista personajes
                personajes_presentes = []
                for personaje in gm.personajes:
                    if(personaje.zona == self.zona):
                        personajes_presentes.append(personaje)
                # mult enemigos
                multiplicador = 1
                if(objeto.precio <= 6):
                    multiplicador += objeto.precio/10
                elif(objeto.precio < 300):
                    multiplicador += 0.8
                else:
                    multiplicador*=2
                
                enemigos_presentes = []
                for enemigo in self.ubicacion.enemigos_activos[indice_zona]:
                    enemigo.salud *= multiplicador
                    enemigo.fuerza *= multiplicador
                    enemigo.resistencia *= multiplicador
                    enemigo.carisma *= multiplicador
                    enemigo.inteligencia *= multiplicador
                    enemigo.sabiduria *= multiplicador
                    enemigos_presentes.append(enemigo)
                    
                Juego.iniciar_pelea(personajes_presentes, enemigos_presentes,
                                    [], self, multiplicador)
            
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
    
    def cambiar_hp(self, hp:int):
        #DEBUG
#    print("------------------------------------------------Metodo cambiar hp")
        self.salud += round(hp)
        if(self.salud <= 0):
            print("\n"+self.nombre + " murio, F")
            return self.is_ded()
        self.actualizar_stats()
        self.exceso_peso()
        return False
    
    def comprar(self):
        if(self.zona != "Mercado"):
            print("Comprale a tu abuela")
            return False
        else:
            print("Que quieres comprar?\nNOMBRE \t PRECIO")
            for objeto in range (0, len(self.ubicacion.objetos_activos[0])):
                print(f"{objeto+1}: "
                      + f"{self.ubicacion.objetos_activos[0][objeto].nombre}: "
                      + "\t"
                      + f"{self.ubicacion.objetos_activos[0][objeto].precio}")
            objeto = int(input())
            if(self.inventario_nombres.count("Dinero") 
               >= self.ubicacion.objetos_activos[0][objeto-1].precio):
                print("Compra realizada!")
                pago = self.ubicacion.objetos_activos[0][objeto-1].precio
                self.anadir_obj(-pago)
                self.anadir_obj(self.ubicacion.objetos_activos[0][objeto-1])
            else:
                decision = input("Oh no! No alcanzan los dineros :( "
                                 + "Quieres vender algo? (S/N) \n")
                if(decision == "S"):
                    venta = self.vender(self.ubicacion.objetos_activos[0][
                        objeto-1].precio)
                    if(venta):
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
    
    def craftear(self):
        seguir_crafteando = True
        ingredientes = []
        while(seguir_crafteando):
            print("Que quieres usar?")
            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
            indice=0
            for objeto in self.cartera_obj:
                print(f"{indice+1}, \t{objeto:.<24s}: "
                      + f"{self.cartera_obj[objeto]} | "
                      + "\t\t"
                      + str(self.inventario[
                          self.inventario_nombres.index(objeto)].estadistica)
                      + "| \t"
                      + str(self.inventario[
                          self.inventario_nombres.index(objeto)].boosteo))
                indice+=1
            print(f"{indice+1}: Terminar")
            indice_objeto = int(input())-1
            if(indice_objeto == indice): # Terminando
                ingredientes.sort()
                for crafteo in gm.crafteos:
                    lista_crafteo = list(crafteo)
                    if("Amuleto" in ingredientes):
                        nuevo_asistente = Asistente(19, 15, 3, 15, 5, 9,
                                          ("Golem de " 
                                           + ingredientes[-1].nombre),
                                          {"Saludable": 1}, ["Amuleto"],
                                          "Monstruo", len(ingredientes), 1,
                                          self.zona, self, "Golem")
                        for ingrediente in ingredientes:
                            estadistica = ingrediente.estadistica
                            boosteo = ingrediente.boosteo
                            if(estadistica == "F"):
                                nuevo_asistente.fuerza += boosteo
                            elif(estadistica == "R"):
                                nuevo_asistente.resistencia += boosteo
                            elif(estadistica == "C"):
                                nuevo_asistente.carisma += boosteo
                            elif(estadistica == "I"):
                                nuevo_asistente.inteligencia += boosteo
                            elif(estadistica == "S"):
                                nuevo_asistente.sabiduria += boosteo
                        self.reclutar(nuevo_asistente)
                        return True
                    lista_crafteo.sort()
                    if(lista_crafteo == ingredientes):
                        print("Crafteo exitoso!")
                        gm.anadir_obj_manual(gm.crafteos[crafteo], self)
                        for ingrediente in ingredientes:
                            self.inventario.remove(ingrediente)
                            self.inventario_nombres.remove(ingrediente.nombre)
                    else:
                        print("Crafteo no disponible")
                        return False
                seguir_crafteando = False
            else:
                objeto = self.inventario[indice_objeto]
                ingredientes.append(objeto)
        return [True, ingredientes, gm.crafteos[crafteo]]
                
    def desequipar(self):
        print("Que objeto quieres desequiparte?")
        self.ver_equipo()
        print(f"{len(self.equipo_nombres)+1}: Salir")    
        objeto_indice = int(input())
        if(objeto_indice == len(self.equipo_nombres)+1):
            return False
        objeto = self.equipo[objeto_indice-1]
        if(objeto.estadistica == "F"):
            self.fuerza -= objeto.boosteo
        elif(objeto.estadistica == "R"):
            self.resistencia -= objeto.boosteo
        elif(objeto.estadistica == "C"):
            self.carisma -= objeto.boosteo
        elif(objeto.estadistica == "I"):
            self.inteligencia -= objeto.boosteo
        elif(objeto.estadistica == "S"):
            self.sabiduria -= objeto.boosteo
        elif(objeto.estadistica == "V"):
            if(self.zona in gm.agua):
                self.velocidad -= objeto.boosteo
        print(f"{self.nombre} se ha quitado {objeto.nombre}")
        self.quitar_equipo(objeto)
        self.equipo.pop(objeto_indice-1)
        self.equipo_nombres.pop(objeto_indice-1)
        self.actualizar_stats()
        print("--------------------------------------------------------------")
        return True
    
    def efecto(self):
        super().efecto()
        for asistente in self.asistentes:
            if("Lealtad" in asistente.condicion 
               and asistente.condicion["Lealtad"] == 0):
                self.asistentes.remove(asistente)
        self.actualizar_stats()
    
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
            self.condicion.update({"Invisible": 10})
        self.anadir_equipo(objeto, indice)
        self.ver_equipo()
        self.actualizar_stats()
        print("--------------------------------------------------------------")
    
    def exceso_peso(self):
        #DEBUG
#    print("-----------------------------------------------Metodo exceso peso")
        if(self.peso > self.carga):
            if(self.inventario != []):
                print(f"{self.nombre} estas muy gordo :(")
                self.tirar_objeto()
            else:
                self.carga = self.peso
    
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
    
    def huir(self, enemigos_presentes): #-------------------------e_presentes = turnos
        from Enemigos import Enemigo
        for enemigo in range(0, len(enemigos_presentes)):
            if(type(enemigos_presentes[enemigo]) == Enemigo):
                break
        if(self.velocidad > enemigos_presentes[enemigo].velocidad):
            return True
        else:
            probabilidad = (self.velocidad/enemigos_presentes[
                enemigo].velocidad)*100
            tirada = gm.dados(1, 100)
            if(tirada <= probabilidad):
                return True
            else:
                return False
    
    def is_ded(self):
        #DEBUG
#        print("------------------------------------------------Metodo is_ded")
        zonas = self.ubicacion.zonas
        zona = zonas.index(self.zona)
        self.condicion = {"Muerto": 1}
        gm.personajes_muertos.append(self)
        gm.personajes.remove(self)
        objeto = gm.transformar_objeto("Cadaver de "+self.nombre)
        print(objeto)
        self.ubicacion.objetos_activos[zona].append(objeto)
#        self.ubicacion.cantidades_objetos_activos[z].append(1)
        self.ubicacion.objetos[zona].append(objeto.nombre)
        self.ubicacion.cantidades_objetos[zona].append(1)
        
        if(self != gm.personaje_malo):
            for objeto_inventario in self.inventario:
                self.ubicacion.objetos_activos[zona].append(objeto_inventario)
                if(objeto_inventario.nombre not in self.ubicacion.objetos[
                        zona]):
                    self.ubicacion.objetos[zona].append(
                        objeto_inventario.nombre)
                    self.ubicacion.cantidades_objetos[zona].append(1)
                else:
                    indice = self.ubicacion.objetos[zona].index(
                        objeto_inventario.nombre)
                    self.ubicacion.cantidades_objetos[zona][indice] += 1
            self.inventario = []
            self.inventario_nombres = []
            for equipo in self.equipo:
                self.ubicacion.objetos_activos[zona].append(equipo)
                if(equipo.nombre not in self.ubicacion.objetos[zona]):
                    self.ubicacion.objetos[zona].append(equipo.nombre)
                    self.ubicacion.cantidades_objetos[zona].append(1)
                else:
                    indice = self.ubicacion.objetos[zona].index(equipo.nombre)
                    self.ubicacion.cantidades_objetos[zona][indice] += 1
            self.equipo = []
            self.equipo_nombres = []
            self.cartera_obj = {}
            self.cartera = 0
        super().is_ded()
        return True
    
    def liberar(self, asistente):
        self.asistentes.remove(asistente)
        self.espacio_asistentes += asistente.rango
        return True
    
    def moverse(self, zona = None):
        #DEBUG
#    print("---------------------------------------------------Metodo moverse")
        self.lugar_previo = self.zona

        ubicaciones = []
        if(zona == None):
            print("A donde deseas moverte?")
            for indice in range(0, len(self.mapa[self.zona])):
                print(f"{indice+1}: {self.mapa[self.zona][indice]}")
            zona = int(input())
            zona = self.mapa[self.zona][zona - 1]
        
        lugar = gm.busca_lugar(zona)
        
        values = self.mapa.values() #Ni modo, tu confia
        
        for personaje in gm.personajes:
            ubicaciones.append(personaje.ubicacion.nombre)
        
        zonas_vistas = []
        for personaje in gm.personajes:
            if(personaje == self):
                continue
            for mapa in personaje.mapa[personaje.zona]:
                zonas_vistas.append(mapa)
            zonas_vistas.append(personaje.zona)
        zonas_vistas.append(zona)
        zonas_vistas.append(self.zona)
        
#        if(ubicacion not in ubicaciones):
#            eliminar(self.ubicacion.objetos_activos)
#            self.ubicacion.objetos_activos = []
#            for i in range(0, len(self.ubicacion.zonas)):
#                self.ubicacion.objetos_activos.append([])
#            Juego.generar_objetos(lugar)
        
        for nueva_zona in gm.master.mapa[zona]:
            if(nueva_zona not in zonas_vistas):
                for indice_lugar in range(0, len(gm.objetos_lugares)):
                    zonas_lugar = gm.objetos_lugares[indice_lugar].zonas
#                    print(nueva_zona)
#                    print(zonas_lugar)
                    if(nueva_zona in zonas_lugar):
                        zona_ubicacion = gm.objetos_lugares[indice_lugar]
                        break
#                print(type(zona_ubicacion))
#                print(type(nueva_zona))
                Juego.generar_enemigos_zona(Juego, zona_ubicacion, nueva_zona)
                Juego.generar_objetos_zona(Juego, zona_ubicacion, nueva_zona)
        
        if(zona == "Entrada"):
            if("Submarino" not in [
                    x for v in values for x in v if type(v)==list] 
                    or "Submarino" not in values):
                lugar = gm.fondo_del_mar
                zona = "Submarino"
            if(self.viaje_astral != True and self == gm.personaje_malo):
                self.viaje_astral = True
                lugar = gm.viaje_astral
                zona = "camion" #----------------------------------------------
        elif(zona == "Profundidades" 
           and "Pin de bob esponja" in self.equipo_nombres):
            print("Escuchas a lo lejos una voz que dice: ""EsToY LiStO"" "
                  + "seguido de una risa infantil...")
        elif(zona == "Sala principal"):
            gm.dificultad = 2
        elif(zona == "Escalera"):
            niv_maquina = gm.dados(1, 10)
            niv_nina = gm.dados(1, 20)
            niv_monstruo = gm.dados(1, 25)
            self.condicion.update({"Escalando": [0, niv_maquina, niv_nina, 
                                                 niv_monstruo]})
        
        for zona_adyacente_futura in self.mapa[zona]:
            zonas_vistas.append(zona_adyacente_futura)
        
        for zona_adyacente in self.mapa[self.zona]:
            for indice_lugar in range(0, len(gm.objetos_lugares)):
                zonas_lugar = gm.objetos_lugares[indice_lugar].zonas
                if(zona_adyacente in zonas_lugar):
                    ubicacion_adyacente = gm.objetos_lugares[indice_lugar]
                    break
            zonas = ubicacion_adyacente.zonas
            indice_zona = zonas.index(zona_adyacente)
            if(zona_adyacente not in zonas_vistas):
                gm.eliminar(ubicacion_adyacente.enemigos_activos[indice_zona])
                gm.eliminar(ubicacion_adyacente.objetos_activos[indice_zona])
                ubicacion_adyacente.enemigos_activos[indice_zona] = []
                ubicacion_adyacente.objetos_activos[indice_zona] = []
#                print(f"enemigos y objetos eliminados de: {zona_adyacente}")
        
        if(self.zona in gm.zonas_agua 
           and "Traje de buzo mejorado" in self.equipo_nombres 
           and zona not in gm.zonas_agua):
            self.velocidad -= self.equipo[
                self.equipo_nombres.index("Traje de buzo mejorado")].boosteo
        elif(self.zona not in gm.zonas_agua 
             and "Traje de buzo mejorado" in self.equipo_nombres 
             and zona in gm.zonas_agua):
            self.velocidad += self.equipo[self.equipo_nombres.index(
                "Traje de buzo mejorado")].boosteo
        
#        print(lugar.jaulas)
        
        self.ubicacion = lugar
        self.zona = zona
        
        for asistente in self.asistentes:
            asistente.zona = zona
        
        print(f"{self.nombre} se ha movido a {zona} en {lugar.nombre}")
#        print(self.ubicacion.enemigos_activos)
#        print(self.ubicacion.objetos_activos)
        return True
    
    def quitar_equipo(self, objeto:Objeto):
        if(objeto.nombre not in self.cartera_obj.keys()):
            self.cartera_obj.update({objeto.nombre: 1})
        else:
            self.cartera_obj[objeto.nombre] += 1
        self.inventario.append(objeto)
        self.inventario_nombres.append(objeto.nombre)
        return True
    
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
                if(gm.ubicar.count(self.zona) > 1): # Si no estas solo en la zona
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
        renombrar = False
        if(type(asistente) == Enemigo):
            decision = input("Quieres ponerle un nombre?(S/N)\n")
            if(decision == "S"):
                nombre = input("Como quieres llamarlo?\n")
            else:
#                Generador de nombres 2000
                renombrar = True
        elif(issubclass(type(asistente), Enemigo)): # Si ya tiene apodo
            nombre = asistente.apodo
        print(f"Felicidades! {nombre} se ha unido a tu aventura!!")
#        agresividad_max = (((gm.oso_marino.carisma 
#                             + gm.oso_marino.fuerza)
#                             - (gm.oso_marino.inteligencia 
#                             + gm.oso_marino.resistencia))+4)
        agresividad_max = 11
        suma = (asistente.salud_max + asistente.fuerza + asistente.resistencia
        + asistente.carisma_max + asistente.inteligencia + asistente.sabiduria)
        boosteo = int((asistente.salud/asistente.salud_max
                   - asistente.agresividad/agresividad_max) * suma / 4)
        for punto in range(0, boosteo):
            tirada = gm.dados(1, 6)
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
        if(asistente in self.ubicacion.enemigos_activos[zona]):
            self.ubicacion.enemigos_activos[zona].remove(asistente)
            asistente = Asistente(asistente.salud_max, asistente.fuerza,
                              asistente.resistencia, asistente.carisma_max,
                              asistente.inteligencia, asistente.sabiduria,
                              asistente.nombre, asistente.condicion,
                              asistente.dropeo, asistente.categoria,
                              asistente.rango, asistente.cantidad,
                              asistente.zona, self, nombre)
        if(renombrar):
            asistente.bautizo()
        self.asistentes.append(asistente)
        
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
            for complemento_contador in range(0, 5):
                print("Que estadistica deseas mejorar? Tienes: "
                      + str(contador-complemento_contador) 
                      + " puntos disponibles")
                seleccion = int(input("\nFuerza(1)\nResistencia(2)"
                                      + "\nCarisma(3)\n"
                                + "Inteligencia(4)\nSabiduria(5)\n"))
                if(seleccion == 1):        
                    self.fuerza+=1
                    if("Super Sayain" in self.condicion):
                        self.condicion["Super Sayain"] += 1
                elif(seleccion == 2):
                    self.resistencia+=1
                elif(seleccion == 3):
                    self.carisma+=1
                elif(seleccion == 4):
                    self.inteligencia+=1
                elif(seleccion == 5):
                    self.sabiduria+=1
            self.salud = self.salud_max
            self.actualizar_stats()
        else:
            self.actualizar_stats()
            print("\nSUBISTE DE NIVEL!!\n")
        print(self)
    
    def subir_salud_max(self):
        #DEBUG
#    print("----------------------------------------Metodo subir salud maxima")
        self.salud_max+=15
        self.energia_max+=4
        print("Tu salud y energia han aumentado!!")
        self.actualizar_stats()
        return True
    
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
        print("Que quieres tirar?")
        print("INDICE \t NOMBRE \t CANTIDAD \t PESO")
        contador=0
        for objeto in self.cartera_obj:
            print(f"{contador+1},\t {objeto:.<24s}: "
                  + f"{self.cartera_obj[objeto]} | "
                  + str(self.inventario[
                      self.inventario_nombres.index(objeto)].peso))
            contador+=1
        objeto = int(input())-1
        if("Confundido" in self.condicion):
            objeto = gm.dados(1, len(self.cartera_obj))-1
            
        for objeto_tirado in self.cartera_obj:
            if(objeto == 0):
                break
            objeto -= 1
        
        print(f"{self.nombre} se ha desecho de {objeto_tirado}, "
              + "descanse en paz "
              + f"{objeto_tirado}, F")
        zonas = self.ubicacion.zonas
        zona = zonas.index(self.zona)
        indice = self.inventario_nombres.index(objeto_tirado)
        objeto = self.inventario[indice]
        
        self.ubicacion.objetos_activos[zona].append(objeto)
        if(objeto.nombre not in self.ubicacion.objetos[zona]):
            self.ubicacion.objetos[zona].append(objeto.nombre)
            self.ubicacion.cantidades_objetos[zona].append(1)
        else:
            indice_objeto_zona = self.ubicacion.objetos[zona].index(
                objeto.nombre)
            self.ubicacion.cantidades_objetos[zona][indice_objeto_zona] += 1
        
        self.anadir_equipo(objeto, indice)
        
        self.actualizar_stats()
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
    
    def usar_objeto(self, objetivo = None, objeto = None):
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
        elif(objetivo in gm.personajes):
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
                print("No se encontraron los objetivos")
                return False
        else:
            print("No se encontro el objetivo")
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
            pocion = pociones[gm.dados(1, len(pociones))-1]
            if("III" in objeto.nombre):
                pocion += " III"
            elif("II" in objeto.nombre):
                pocion += " II"
            else:
                pocion += " I"
            objeto = gm.transformar_objeto(pocion)
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
                    tirada = gm.dados(1, 10)
                    print("Tiraste "+str(tirada))
                    dano = self.fuerza + int(objeto.boosteo) + tirada
                    tirada = gm.dados(1, 10)
                    if(tirada >= 4):
                        dano = 0
                        print("Has fallado tu ataque!")
                    objetivo.cambiar_hp(-dano)
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
                    self.ubicacion.cantidades_objetos[zona].append(1)
                self.inventario = []
                self.inventario_nombres = []
                for equipo in self.equipo:
                    self.ubicacion.objetos_activos[zona].append(equipo)
                    self.ubicacion.objetos[zona].append(equipo.nombre)
                    self.ubicacion.cantidades_objetos[zona].append(1)
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
            tirada = gm.dados(1, 20)
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
                objetivo = objetivos[1][gm.dados(1, len(objetivos[1]))-1]
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
            tirada = gm.dados(1, 20)
            if(tirada <= 2):#------------------------------Todos los personajes
                print("Le has hechado lodo a todos tus companeros, "
                      + "maravillosa jugada! :D")
                for objetivo in objetivos[0]:
                    objetivo.condicion.update({"Cegado": 1})
            elif(tirada <= 5):#-----------------------------------------Tu solo
                print("Te has resbalado y echado lodo tu solo, que egoista...")
                self.condicion.update({"Cegado": 1})
            elif(tirada <= 10):#-------------------------------------Un enemigo
                objetivo = objetivos[1][gm.dados(1, len(objetivos[1]))-1]
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
            tirada = gm.dados(1, 20)
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
                objetivo = objetivos[1][gm.dados(1, len(objetivos[1]))-1]
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
                print(objetivo)
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
            if(Dfestadisticas_objetos == "H"):
                objetivo.salud += cantidad
                if(objetivo.salud > limite_nivel):
                    objetivo.salud = limite_nivel
            elif(Dfestadisticas_objetos =="F"):
                objetivo.fuerza += cantidad
                if("Super Sayain" in self.condicion):
                        self.condicion["Super Sayain"] += cantidad
                if(objetivo.fuerza > limite_nivel):
                    objetivo.fuerza = limite_nivel
            elif(Dfestadisticas_objetos=="R"):
                objetivo.resistencia += cantidad
                if(objetivo.resistencia > limite_nivel):
                    objetivo.resistencia = limite_nivel
            elif(Dfestadisticas_objetos=="C"):
                objetivo.carisma += cantidad
                if(objetivo.carisma > limite_nivel):
                    objetivo.carisma = limite_nivel
            elif(Dfestadisticas_objetos=="I"):
                objetivo.inteligencia += cantidad
                if(objetivo.inteligencia > limite_nivel):
                    objetivo.inteligencia = limite_nivel
            elif(Dfestadisticas_objetos=="S"):
                objetivo.sabiduria += cantidad
                if(objetivo.sabiduria > limite_nivel):
                    objetivo.sabiduria = limite_nivel
            elif(Dfestadisticas_objetos=="V"):
                objetivo.condicion.update({"Acelerado": cantidad})
            elif(Dfestadisticas_objetos=="E" and objetivo in gm.personajes):
                objetivo.energia += cantidad
                if(objetivo.energia > limite_nivel):
                    objetivo.energia = limite_nivel
        
        else:
            if(Dfestadisticas_objetos== "H"):
                if(self.nombre == "Turati" and self.arbol["B1"][0] == 1):
                    cantidad = (int(cantidad 
                                       * np.random.randint(10, 21) / 10))
                objetivo.salud += cantidad
                if(objetivo.salud > objetivo.salud_max):
                    objetivo.salud = objetivo.salud_max
            elif(Dfestadisticas_objetos=="Saludable III"):
                if ("Envenenado III" in objetivo.condicion):
                    objetivo.condicion.pop("Envenenado III")
                    objetivo.curar()
            elif(Dfestadisticas_objetos=="Saludable II"):
                if ("Envenenado II" in objetivo.condicion):
                    objetivo.condicion.pop("Envenenado II")
                    objetivo.curar()
            elif(Dfestadisticas_objetos=="Saludable I"):
                if ("Envenenado I" in objetivo.condicion):
                    objetivo.condicion.pop("Envenenado I")
                    objetivo.curar()
            elif(Dfestadisticas_objetos=="Envenenado I"):
                if (("Envenenado III" not in objetivo.condicion) 
                    and ("Envenenado II" not in objetivo.condicion)):
                    objetivo.enfermar("Envenenado I", cantidad)
            elif(Dfestadisticas_objetos=="Envenenado II"):
                if ("Envenenado III" not in objetivo.condicion):
                    objetivo.enfermar("Envenenado II", cantidad)
                    if("Envenenado I" in objetivo.condicion):
                        objetivo.condicion.pop("Envenenado I")
            elif(Dfestadisticas_objetos=="Envenenado III"):
                objetivo.enfermar("Envenenado III", cantidad)
                if("Envenenado I" in objetivo.condicion):
                    objetivo.condicion.pop("Envenenado I")
                elif("Envenenado II" in objetivo.condicion):
                    objetivo.condicion.pop("Envenenado II")
            elif(Dfestadisticas_objetos=="Confusion"):
                objetivo.enfermar("Confundido", cantidad)
            elif(Dfestadisticas_objetos=="Cuarto salud"):
                objetivo.salud += objetivo.salud_max/4
                if(objetivo.salud > objetivo.salud_max):
                    objetivo.salud = objetivo.salud_max
            elif(Dfestadisticas_objetos=="Mitad salud"):
                objetivo.salud += objetivo.salud_max/2
                if(objetivo.salud > objetivo.salud_max):
                    objetivo.salud = objetivo.salud_max
            elif(Dfestadisticas_objetos=="Tres cuartos salud"):
                objetivo.salud += objetivo.salud_max*3/4
                if(objetivo.salud > objetivo.salud_max):
                    objetivo.salud = objetivo.salud_max
            elif(Dfestadisticas_objetos=="Salud maxima"):
                objetivo.condicion = {"Saludable": 1}
                objetivo.salud = objetivo.salud_max
            elif(Dfestadisticas_objetos=="Revivir"):
                if(objetivo.salud <= 0 and objetivo in gm.personajes_muertos 
                   and (("Cadaver de "+objetivo.nombre) 
                        in self.inventario_nombres)):
                    gm.personajes_muertos.remove(objetivo)
                    gm.personajes.append(objetivo)
                    objetivo.salud = objetivo.salud_max/2
                    indice = self.inventario_nombres.index(
                        "Cadaver de "+objetivo.nombre)
                    self.inventario_nombres.remove("Cadaver de "+objetivo.nombre)
                    self.inventario.pop(indice)
                    objetivo.condicion = {"Saludable": 1}
            elif(Dfestadisticas_objetos=="Invisible"):
                objetivo.condicion.update({"Invisible": 3})
            elif(Dfestadisticas_objetos=="Habilidad"):
                if(objeto.usos == 1):
                    objetivo.puntos_habilidad += 1
                    print(objeto.boosteo)
                    objeto.usos -= 1
                    return True
                print(objeto.boosteo)
                
        if(objeto.usos == 1 and "Pistola laser" not in objeto.nombre):
            indice = self.inventario_nombres.index(objeto.nombre)
            self.anadir_equipo(objeto, indice)
        self.actualizar_stats()
        print(f"\n{self.nombre} ha usado con exito {objeto.nombre}, "
              + "es super efectivo!")
        return True
    
    def vender(self, pobre = None):
        if(self.zona != "Mercado"):
            print("Vendele a tu abuela")
            return False
        else:
            print("Que quieres vender?\nNOMBRE \t PRECIO")
            for objeto in range(0, len(self.inventario)):
                print(f"{objeto+1}: {self.inventario_nombres[objeto]} "
                      + f"{round(self.inventario[objeto].precio*.6)}")
            indice = int(input())-1
            objeto = self.inventario[indice]
            if(objeto.nombre == "Nota de consejo" or objeto.precio == 0):
                print("No compramos basura")
                return False
            pago = int(round(objeto.precio*.6))
            if(pobre != None):
                if(pobre > pago):
                    print("Con eso no te va a alcanzar vato loko")
                    return False            
            self.anadir_obj(pago)
            self.inventario.pop(indice)
            self.inventario_nombres.pop(indice)
            return True
    
    def ver_equipo(self):
        if(len(self.equipo_nombres) == 0):
            print("No tiene nada equipado de momento caballero")
        else:
            for equipo in range(0, len(self.equipo_nombres)):
                print(f"{equipo+1}: {self.equipo_nombres[equipo]} | "
                      + f"{self.equipo[equipo].estadistica}: "
                      + f"{self.equipo[equipo].boosteo}")

from Juegos import Juego
import Game_Manager as gm

# =============================================================================
mirek = Personaje(27, 14, 13, 15, 16, 18, "Mirek", {"Saludable": 1}, 20, [], gm.campamento, "Cabana", 1, gm.mapa_mirek, 0, 10, gm.arbol_mirek)
compa = Asistente(15, 14, 13, 10, 11, 15, "Aguila", "Saludable", "%Esencia velocidad II/Esencia sabiduria II", "Animal", 3, 1, "Cabana", mirek, "El compa")
#mirek.reclutar(compa)
#print(mirek)
#print(compa)
#compa.cambiar_hp(-690, mirek)
#print(compa)
compa.bautizo()
print(compa)
# =============================================================================
