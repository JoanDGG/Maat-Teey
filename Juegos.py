# -*- coding: ISO-8859-1 -*-
import pandas as pd
import numpy as np
import Game_Manager as gm
from Lugares import Lugar
from Objetos import Objeto
from Enemigos import Enemigo

class Juego:
    
    def __init__(self):
        self.funcional = True
        self.peleas_doma = []
        self.oso_marino = None
    
    def jugar(self, resultados = []):
        #DEBUG
#        print("------------------------------------------------------Metodo jugar")
        # Quitar los que ya no estan domando
        domar_nuevo = []
        for domar in self.peleas_doma:
            if(domar[0]):
               domar_nuevo.append(domar)
        self.peleas_doma = domar_nuevo
#        print("-----------------"+ str(self.oso_marino.carisma))
        fin = False
        personajes_peleando = []
#        print("Per")
#        print(resultados)
        for resultado in resultados:
            for personaje in resultado[1]:
                print(personaje.nombre)
#                print("-.-.-.-.-.-.-.-.-.")
                personajes_peleando.append(personaje)
#        print(per)
        turnos = gm.personajes
        for personaje in range(len(gm.personajes)-1,0,-1):
            for indice in range(personaje):
                if (gm.personajes[indice].velocidad > 
                    gm.personajes[indice + 1].velocidad):
                    temp = turnos[indice]
                    turnos[indice] = turnos[indice + 1]
                    turnos[indice + 1] = temp
        
        turnos_aux = []
        for turno in range(len(turnos)-1, 0, -1):
            turnos_aux.append(turnos[turno])
        turnos_aux.append(turnos[0])
        
        turnos = turnos_aux
        
        for turno in range(0, len(turnos)):
            personaje = turnos[turno]
            if("Domando" in personaje.condicion):
                print(personaje.nombre + "esta domando...")
                for doma in range (0, len(self.peleas_doma)):
                    if(personaje in self.peleas_doma[doma]):
                        #doma[2] = enemigo, doma[3] = jaula, doma[4] = defensas, 
                        #doma[5] = omitidos, doma[6] = historial
                        self.peleas_doma[doma] = self.domar(personaje, 
                                  self.peleas_doma[doma][2], 
                                  self.peleas_doma[doma][3], 
                                  self.peleas_doma[doma][4], 
                                  self.peleas_doma[doma][5], 
                                  self.peleas_doma[doma][6])
                        break
                continue
            
            domar_posible = ""
            zona_personaje = personaje.ubicacion.zonas.index(personaje.zona)
            for enemigo in personaje.ubicacion.enemigos_activos[zona_personaje]:
                if("Atrapado" in enemigo.condicion):
                    domar_posible = "9: Domar"
                elif("Atrapado" not in enemigo.condicion):
                    domar_posible = ""
                    break
            
            es_mercado = "Buscar"
            if(personaje in personajes_peleando):
                continue
            if(personaje.zona == "Mercado"):
                es_mercado = "Robar"
            personaje.stats()
            
            personaje.efecto() # efecto a personajes que no esten peleando
            print(f"{personaje.nombre}, ¿Que deseas hacer?")
            seleccion = int(input("1: Moverte\n2: " + es_mercado 
                                  + "\n3: Usar objeto\n4: Tirar objeto\n5: Esperar"
                                  + "\n6: Curarse\n7: Usar habilidad "
                                  + "\n8: Guardar(Salir por ahora)\n" 
                                  + domar_posible))
            if(seleccion == 1):
                personaje.moverse()
            elif(seleccion == 2):
                if(gm.mercado == "Buscar"):
                    objeto = input("¿Que quieres " + es_mercado.lower() 
                                   + "? (0 para nada en especifico)\n")
                    if(objeto == "0"):
                        personaje.buscar()
                    else:
                        personaje.buscar(objeto)
                else:
                    print("¿Que quieres "+es_mercado.lower()+"?\n")
                    for objeto in gm.mercado.objetos_activos[0]:
                        print(f"{objeto.nombre}")
                    objeto_seleccionado = input()
                    personaje.buscar(objeto_seleccionado)
                    
            elif(seleccion == 3):
                objetos_permitidos = []
                for indice in range(0, len(personaje.inventario)):
                    if(personaje.inventario[indice].nombre != "F" or "Pocion" 
                       in personaje.inventario_nombres[indice] 
                       and personaje.inventario_nombres[indice] != "SCP 427"):
                        objetos_permitidos.append(personaje.
                                                  inventario[indice].nombre)
                
                print("¿Que quieres usar?")
                print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                contador = 0
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        print(str(contador + 1) + f", \t{llave:.<24s}: " 
                              + str(personaje.cartera_obj[llave]) + " | \t\t" 
                              + personaje.inventario[
                                self.inventario_nombres.index(
                                llave)].estadistica + " | \t" 
                              + personaje.inventario[
                                personaje.inventario_nombres.index(llave)].boosteo)
                        contador += 1
                
                indice_objeto = int(input())-1
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        if(indice_objeto == 0):
                            break
                        indice_objeto -= 1
                objeto = personaje.inventario[
                        personaje.inventario_nombres.index(llave)]
                
                personaje.usar_obj(objeto)
            elif(seleccion == 4):
                personaje.tirar_objeto()
            elif(seleccion == 5):
                personaje.energia = personaje.energia_max
                print("Energia restaurada!!")
                continue
            elif(seleccion == 6):
                personaje.energetizar()
            elif(seleccion == 7):
                personaje.activar_habilidad("Jugar")
            elif(seleccion == 8):
                fin = True
                return ""
            elif(seleccion == 9 and domar_posible != ""):
                print("¿Que enemigo intentaras domar?")
                contador = 0
                jaulas = []
                for jaula in personaje.ubicacion.jaulas:
                    for jaula_enemigo in jaula:
                        print(str(contador) + jaula + ": " 
                              + personaje.ubicacion.jaulas[
                                      jaula][jaula_enemigo].nombre)
                        jaulas.append(jaula_enemigo)
                        contador += 1
                jaula_select = jaulas[int(input())]
#               personaje = objeto personaje, 
#               personaje.ubicacion.jaulas[jaula_select.nombre][jaula_select] = 
#               objeto enemigo, jaula_select = objeto jaula, defensas, omitidos, historial
                self.peleas_doma.append(self.domar(personaje, 
                personaje.ubicacion.jaulas[jaula_select.nombre][jaula_select], 
                jaula_select, [0, 0], [], []))
            else:
                print("Tas tonto shavo")
                turno -= 2
                continue
        
        p_presentes = []
        zonas_vistas = []
        
        for personaje in gm.personajes:
            personaje.actualizar_stats()
            for objeto in personaje.inventario_nombres:
                if(objeto == "Pistola laser"):
                    indice = personaje.inventario_nombres.index("Pistola laser")
                    personaje.inventario[indice].uso -= 2
                elif(objeto == "Pistola laser mejorada"):
                    indice = personaje.inventario_nombres.index(
                            "Pistola laser mejorada")
                    personaje.inventario[indice].uso -= 2
            
            zona = personaje.ubicacion.zonas.index(personaje.zona)
            if(personaje.ubicacion.enemigos_activos[zona] != []):
                p_presentes.append(personaje)
#                print(personaje.nombre)
#                print(personaje.ubicacion.enemigos_activos)
                
            # revisar zonas vistas de todos
            for zona in personaje.mapa[personaje.zona]:
                zonas_vistas.append(zona)
            zonas_vistas.append(personaje.zona)
        
        #Listas de enemigos activos de zonas vistas
        for zona_vista in zonas_vistas:
            lugar_visto = gm.buscaLugar(zona_vista)
            zona = lugar_visto.index(zona_vista)
            #Obtener todas las jaulas de todos los tipos de jaula de la zona actual
            jaulas_activas=[]
            for jaulas in lugar_visto[zona].jaulas:
                for jaula in jaulas:
                    if(gm.dados(1, 2)[0] == 1 and jaulas[jaula] != ""):
                        jaulas_activas.append(jaula)
            
            if(jaulas_activas != []):
                for enemigo in lugar_visto.enemgios_activos()[zona]:
                    for trampa in jaulas_activas:
                        if((trampa.nombre == "Trampa de osos") 
                        and (enemigo in gm.atrapables_t_osos)):
                                tirada = gm.dados(1, 10)[0]
                        elif((trampa.nombre == "Jaula")
                        and (enemigo in gm.atrapables_medianos)):
                                tirada = gm.dados(1, 10)[0]
                        elif((trampa.nombre == "Jaula mas grande")
                        and (enemigo in gm.atrapables)):
                                tirada = gm.dados(1, 20)[0]
                        if(enemigo.sabiduria + tirada <= 20):
                            #Enemigo atrapado
                            enemigo.condicion.update({"Atrapado": 1})
                            lugar_visto[zona].jaulas[
                                    trampa.nombre][trampa] = enemigo.nombre
                            lugar_visto[zona].objetos_activos.remove(trampa)
                            break
        
        peleas = []
        zonas = []
        
        if(p_presentes != []):
            for personaje in p_presentes:
                zonas.append(personaje.zona)
                
            zona_personaje = ""
            cantidad_peleas = 0  # Numero de pelea
            personajes_peleando = 0 # Cuantos personajes ha anadido a peleas
            saltar = False

            for personaje in p_presentes:
                for pelea in range(0, len(peleas)):
                    if(personaje in peleas[pelea]):
                        saltar = True
                if(saltar):
                    saltar = False
                    continue
                if(personajes_peleando < len(p_presentes)):
                    peleas.append([])
                zona_personaje = personaje.zona
                for zona in range(0, len(zonas)):
                    if(zona_personaje == zonas[zona]):
                        peleas[cantidad_peleas].append(p_presentes[zona])
                        personajes_peleando += 1
                cantidad_peleas += 1
                
            for pelea in peleas:
                for personaje in pelea:
                    print(personaje.nombre, end = ", ")
                print()
#            print(peleas)
#            print(resultados)
            for pelea in peleas:
                omitir = True
                omitidos = []
                defensas = []
                turnos_pelea = []
                empezar = False
                for resultado in range(0,len(resultados)):
                    for personaje in resultados[resultado][1]:
                        if(personaje in pelea):
                            omitidos = resultados[resultado][5].copy()
                            defensas = resultados[resultado][3].copy()
                            turnos_pelea = resultados[resultado][4].copy()
                            omitir = False
                            break
                    if(not omitir):
                        break
                if(omitir):
                    #Esta en pelea y no en resultados (la pelea esta comenzando)
                    empezar = True
#                if(resultados != []):
                if(resultados != [] and not resultados[resultado][0]):
                    resultados.remove(resultado)
                elif(resultados != [] and resultados[resultado] == []):
                    omitidos = []
                    defensas = []
                    turnos_pelea = []
                    empezar = True
                print(omitidos)
                print(pelea[0].nombre, pelea[0].zona)
                zona = pelea[0].ubicacion.zonas.index(pelea[0].zona)
                e_presentes = pelea[0].ubicacion.enemigos_activos[zona]
                e_presentes_aux = e_presentes.copy()
                if(empezar):
                    for enemigo in e_presentes_aux:
                        if(enemigo.categoria == "Humano" 
                           and enemigo not in gm.jefes.keys() 
                           and enemigo.salud > 0):
                            e_presentes.remove(enemigo)
#                print(pelea)
#                print(pelea[0].nombre)
#                print(e_presentes)
                
                if(empezar):
                    print("La pelea ha comenzado")
                    resultados.append(self.iniciar_pelea(self, pelea, 
                                                    e_presentes, omitidos))
                else:
                    print("Que siga la pelea")
                    # La r se sobreescribe de las resultados, 
                    # r5 esta antes por el orden en que recibe iniciar pelea
                    # r1 = p_presentes, r2 = e_presentes, r5 = omitidos, 
                    # r3 = defensas, r4 = turnos, per = personajes peleando
#                    print("resultados")
#                    print(resultados)
                    resultados[resultado] = self.iniciar_pelea(self, pelea, 
                                                  e_presentes, omitidos, defensas, 
                                                  turnos_pelea, personajes_peleando)
#                    print("\n")
#                    print(resultados[r])
        
        if(not fin):
            return resultados
            
    def iniciar_pelea(self, p_presentes, e_presentes, omitidos = [], defensas = [], 
                   turnos = [], personajes_peleando = [], victima = None, mult = 1):
        #DEBUG
        print("----------------------------------------------Metodo iniciar_pelea")
        if(e_presentes == []):
                print("Disfruta tu estadia")
                return [False, p_presentes]
        jefes_presentes = False
        for enemigo in e_presentes:
            if(enemigo in gm.jefes.keys()):
                jefes_presentes = True
        e_sabiduria = 0
        p_pelea = []
        enemigos_op_activos = []        
        for enemigo in e_presentes:
            if(enemigo.sabiduria > e_sabiduria):
                e_sabiduria = enemigo.sabiduria
            if(enemigo.nombre in gm.enemigos_op):
                enemigos_op_activos.append(enemigo)
                
        if(victima != None): # Cuando estas robando
            p_presentes.remove(victima)
            if(victima.sabiduria < e_sabiduria):
                p_pelea.append(victima)
                print(f"{victima.nombre} has sido detectado, hora de pelear!")
                for personaje in p_presentes:
                    decision = input(f"¿{personaje.nombre}, quieres hacer la guerra? (S/N)")
                    if(decision == "S"):
                        p_pelea.append(personaje)
                        for asistente in personaje.asistentes:
                            p_pelea.append(asistente)
            else:
                print("Oof, te has salvado...")
                for enemigo in e_presentes:
                    enemigo.salud /= mult
                    enemigo.fuerza /= mult
                    enemigo.resistencia /= mult
                    enemigo.carisma /= mult
                    enemigo.inteligencia /= mult
                    enemigo.sabiduria /= mult
        else:
            # Anadir asistentes de personajes muertos
            for personaje_muerto in gm.personajes_muertos: 
                if(personaje_muerto.zona == p_presentes[0].zona):
                    for asistente in personaje_muerto.asistentes:
                        p_pelea.append(asistente)
            for personaje in p_presentes:
                sigilo = False
                if(personaje in personajes_peleando):
                    p_pelea.append(personaje)
                    for asistente in personaje.asistentes:
                        p_pelea.append(asistente)
                    continue
                if("Invisible" not in personaje.condicion 
                   or enemigos_op_activos != []):
                    if(personaje.sabiduria < e_sabiduria):
                        p_pelea.append(personaje)
                        for asistente in personaje.asistentes:
                            p_pelea.append(asistente)
                        print(f"{personaje.nombre} has sido detectado, " 
                              + "hora de pelear!")
                    else:
                        sigilo = True
                else:
                    sigilo = True
                    
                if(sigilo):
                    if(personaje.nombre == "Ruben" 
                       and personaje.arbol["A3"][0] == 1):
                        decision = input("¿Ruben, "
                                         + "quieres utilizar tu habilidad? (S/N)")
                        if(decision == "S"):
                            personaje.activar_habilidad("Iniciar pelea", omitidos)
                    else:
                        zonas = personaje.ubicacion.zonas
                        zona = zonas.index(personaje.zona)
                        tirada = gm.dados(1, 
                                 len(personaje.ubicacion.enemigos_activos[zona]))[0]
                        print(f"{personaje.nombre}, " 
                              + f"has avistado a {tirada} enemigos...")
                        enemigos_vistos = []
                        for i in range(0, tirada):
                            print("... hay un " 
                        + f"{personaje.ubicacion.enemigos_activos[zona][i].nombre} "
                        + "cerca...")
                            enemigos_vistos.append(
                                     personaje.ubicacion.enemigos_activos[zona][i])
                        print("\n..posiblemente hayan mas enemigos en la zona..\n")
                    print(f"{personaje.nombre}"
                          + ", estas en modo sigilo sigilozo ¿que deseas hacer?")
                    decision = int(input("0: Atacar\n1: Unirse a la pelea"
                                         + "\n2: Usar objeto\n3: Tirar objeto "
                                         + "\n4: Moverte\n5: Esperar\n"))
                    if(decision == 0):
                        ataque = personaje.atacar(enemigos_vistos, 1.5)
                        ataque[0].cambiar_hp(-ataque[1], personaje)
                        if(personaje.sabiduria < e_sabiduria+gm.dados(1, 
                                        (e_sabiduria//2)+1)[0] or jefes_presentes):
                            p_pelea.append(personaje)
                            for asistente in personaje.asistentes:
                                p_pelea.append(asistente)
                            print(f"{personaje.nombre} has sido detectado, " 
                                  + "hora de pelear!")
                        else:
                            print("Te mantienes detras de las sombras..")
                    elif(decision == 1):
                        p_pelea.append(personaje)
                        for asistente in personaje.asistentes:
                            p_pelea.append(asistente)
                        print(f"{personaje.nombre}, hora de pelear!!")
                    elif(decision == 2):
                        personaje.usar_obj(p_presentes+enemigos_vistos)
                    elif(decision == 3):
                        personaje.tirar_objeto()
                    elif(decision == 4):
                        personaje.moverse()
                    else:
                        print(f"{personaje.nombre} se esconde...")
                        for i in range(tirada, tirada + gm.dados(1, 3)[0]):
                            if(i>= len(personaje.ubicacion.enemigos_activos[zona])):
                                break
                            print("... has avistado a " 
                        + f"{personaje.ubicacion.enemigos_activos[zona][i].nombre} "
                        + "tambien...")
                if(e_presentes == []):
                    print("Victoria!")
                    if(jefes_presentes):
                        for personaje in p_presentes:
                            personaje.subir_nivel()
                    p_presentes = []
                    return [False, p_presentes]
        enemigos = []
        for enemigo in e_presentes:
            if("Atrapado" not in enemigo.condicion):
                enemigos.append(enemigo)
        
        if(p_pelea != []):
            return self.pelea(self, p_pelea, enemigos, defensas, turnos, omitidos)
        return [False, p_pelea]

    def pelea(self, p_presentes, e_presentes, defensas = [], 
              turnos = [], omitidos = []):
        #DEBUG
#        print("------------------------------------------------------Metodo pelea")
        for jefe in gm.jefes.keys():
            gm.notaxeables.append(jefe)
        jefes_presentes = False
        for enemigo in e_presentes:
            if(enemigo in gm.jefes.keys()):
                jefes_presentes = True
        for personaje in gm.personajes: # Anadir asistentes de personajes vivos no peleando
            if(personaje in gm.personajes):
                for asistente in personaje.asistentes:
                    if(asistente not in p_presentes):
                        p_presentes.append(asistente)
        for personaje_muerto in gm.personajes_muertos: # Anadir asistentes de personajes muertos
            if(personaje_muerto.zona == p_presentes[0].zona):
                for asistente in personaje_muerto.asistentes:
                    if(asistente not in p_presentes):
                        p_presentes.append(asistente)
        if(turnos == []):
            turnos = p_presentes + e_presentes
        velocidades = []
        historial = []
        for personaje in turnos:
            velocidades.append(personaje.velocidad)
        for velocidad in range(len(velocidades)-1, 0, -1):
            for indice in range(velocidad):
                if velocidades[indice]>velocidades[indice + 1]:
                    temp = velocidades[indice]
                    velocidades[indice] = velocidades[indice + 1]
                    velocidades[indice + 1] = temp
                    temp1 = turnos[indice]
                    turnos[indice] = turnos[indice + 1]
                    turnos[indice + 1] = temp1
        
        turnos_aux = []
        for turno in range(len(turnos)-1, 0, -1):
            turnos_aux.append(turnos[turno])
        turnos_aux.append(turnos[0])
        turnos = []
        for turno in turnos_aux:
            turnos.append(turno)
        # ----------------------------------------------------------turnos asignados
        
        if(defensas == []):
            for defensa in turnos:
                defensas.append(0)
        for turno in turnos:
            print(turno.nombre)
            turno.efecto()
        for personaje in (turnos_aux):
#            print(omitidos)
            if(personaje in omitidos):
                omitidos.remove(personaje)
                turnos.pop(turnos.index(personaje))
                continue
            elif(personaje not in turnos or "Indefenso" in personaje.condicion):
                continue
            print(f"Es turno de: {personaje.nombre}\n")
            if(personaje in e_presentes):# ----------------------------Turno enemigo
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_enemigo(self, 
                                                   p_presentes, e_presentes, 
                                                   defensas, turnos, omitidos, 
                                                   turnos_aux, personaje, historial)
            elif(personaje in gm.personajes):# ----------------------Turno personaje
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_personaje(self, 
                                                   p_presentes, e_presentes, 
                                                   defensas, turnos, omitidos, 
                                                   turnos_aux, personaje, historial)
            else:
                # turno asistente
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_enemigo(self, 
                                                   p_presentes, e_presentes, 
                                                   defensas, turnos, omitidos, 
                                                   turnos_aux, personaje, historial)
            if(p_presentes == []):
                return [False, p_presentes, e_presentes, 
                        defensas, turnos_aux, omitidos]
            elif(e_presentes == []):
                print("Victoria!")
                if(jefes_presentes):
                    for personaje in p_presentes:
                        personaje.subir_nivel()
                for personaje in p_presentes: # Revivir a quien tenia SCP 427
                    if("Temporal" in personaje.condicion):
                        gm.personajes_muertos.remove(personaje.dueno)
                        gm.personajes.append(personaje.dueno)
                        personaje.dueno.asistentes.remove(personaje)
                        personaje.zona = "Vacio"
                p_presentes = []
                return [False, p_presentes, e_presentes, 
                        defensas, turnos_aux, omitidos]
        turnos_aux = p_presentes + e_presentes
        return [True, p_presentes, e_presentes, defensas, turnos_aux, omitidos]
    
    
    def turno_enemigo(self, p_presentes, e_presentes, defensas, turnos, omitidos, 
                      turnos_aux, enemigo, historial, jaula = None):
        if(enemigo in omitidos):
            omitidos.remove(enemigo)
            turnos.pop(turnos.index(enemigo))
            return p_presentes, e_presentes, defensas, turnos, omitidos, historial
        elif(enemigo not in turnos or "Indefenso" in enemigo.condicion):
            return p_presentes, e_presentes, defensas, turnos, omitidos, historial
        indice_enemigo = turnos.index(enemigo)
        indice_enemigo_aux = turnos_aux.index(enemigo)
        
        if("Confundido" in enemigo.condicion):
            accion = enemigo.decidir(turnos_aux, historial, turnos_aux, defensas)
        elif(issubclass(enemigo, Enemigo)):
            accion = enemigo.decidir(e_presentes, historial, turnos_aux, defensas)
        else:
            accion = enemigo.decidir(p_presentes, historial, turnos_aux, defensas)
        
        if("Atacando normal" in enemigo.condicion 
           or "Atacando especial" in enemigo.condicion):
            for personaje in accion[0]:
                print(f"{enemigo.nombre} se dispone a atacar a {personaje.nombre}!")
                indice_aux = turnos_aux.index(personaje)
                if(personaje in turnos and personaje in gm.personajes):
                    indice = turnos.index(personaje)
                    salida = True
                    while salida:
                        #----------------------------------------Respuesta personaje
                        print(f"¿{personaje.nombre}, que deseas hacer?")
                        if(personaje.nombre == "Sebas" 
                           and personaje.arbol["B1"][0] == 1):
                            print("0: Anticipacion")
                        
                        decision = int(input("1: Defenderte\n2: Usar objeto"
                                             + "\n3: No hacer nada\n"))
                        
                        if(decision == 0):
                            if(not personaje.activar_habilidad("anticipacion")[0]):
                                continue
                            else:
                                print("Dano posible = "+ str(accion[1]))
                                decision = input("¿Vas a querer atacar?(S/N)")
                                if(decision == "S"):
                                    personaje.atacar(enemigo)
                                salida = False
                        elif(decision == 1):
                            defensas[indice_aux] = personaje.defender()
                            turnos.pop(indice)
                            break
                        elif(decision == 2):
                            #-----------------------------------------Usar objeto
                            objetos_permitidos = []
                            for indice in range(0, len(personaje.inventario)):
                                if(personaje.inventario[indice].estadistica != "F" 
                                   or "Pocion" 
                                   in personaje.inventario_nombres[indice] 
                                   or personaje.inventario_nombres[indice] 
                                   not in gm.multiples):
                                    objetos_permitidos.append(
                                            personaje.inventario[indice].nombre)
                            
                            print("¿Que quieres usar?")
                            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA "
                                  + "\t BOOSTEO")      
                            contador = 0
                            for llave in personaje.cartera_obj:
                                if(llave in objetos_permitidos):
                                    print(f"{contador + 1}, \t{llave:.24s}: \t\t" 
                                          + personaje.cartera_obj[llave] + " | \t\t" 
                                          + personaje.inventario[
                                            personaje.inventario_nombres.index(
                                                            llave)].estadistica
                                          + " | \t" 
                                          + personaje.inventario[
                                            personaje.inventario_nombres.index(
                                                                llave)].boosteo)
                                    contador += 1
                            
                            indice_objeto = int(input())-1
                            for llave in personaje.cartera_obj:
                                if(llave in objetos_permitidos):
                                    if(indice_objeto == 0):
                                        break
                                    indice_objeto -= 1
                            objeto = personaje.inventario[
                                    personaje.inventario_nombres.index(llave)]
                            #------------------------------------Objeto seleccionado
                            print("¿Con quien usaras el objeto?")
                            if(objeto.estadistica == "Revivir"):
                                print("0: Regresar")
                                for objeto in range (0, len(
                                        personaje.inventario_nombres)):
                                    if("Cadaver" in personaje.inventario_nombres[
                                                                        objeto]):
                                        print(f"{objeto + 1}: "
                                        + f"{personaje.inventario_nombres[objeto]}")
                                seleccion = int(input())-1
                                if(seleccion == -1):
                                    continue
                                else:
                                    uso = personaje.usar_obj(
                                            personaje.inventario_nombres[seleccion], 
                                            objeto)
                                    salida = not uso
                            else:
                                for personaje in range(0, len(turnos_aux)):
                                    print(f"{personaje + 1}: " 
                                          + f"{turnos_aux[personaje].nombre}")
                                print(f"{len(turnos_aux) + 1}: Regresar")
                                seleccion = int(input())-1
                                if(seleccion == len(turnos_aux)):
                                    continue
                                elif(personaje.nombre == 
                                     turnos_aux[seleccion].nombre):
                                    uso = personaje.usar_obj(personaje, objeto)
                                    if(type(uso) == bool):
                                        salida = not uso
                                    elif(list(uso.keys())[0] == "Escudo"):
                                        defensas[seleccion] = list(uso.values())[0]
                                        break
                                else:
                                    uso = personaje.usar_obj(turnos_aux[seleccion], 
                                                             objeto)
                                    if(type(uso) != bool):
                                        if(list(uso.keys())[0] == "Escudo"):
                                            defensas[seleccion] += list(
                                                        uso.values())[0]
                                        else:
                                            if(type(accion)!=int):
                                                accion[1] = 0
                                            defensas[indice_enemigo_aux] = uso
                                            print(turnos[indice_enemigo].nombre 
                                                  + " ha sido confundido!")
                                            turnos.pop(indice)
                                        break
                                    else:
                                        salida = not uso
                            if(not salida):
                                turnos.pop(indice)
                        elif(decision == 3):
                            break
                dano = defensas[indice_aux] - accion[1]
                if(enemigo.salud <= 0):
                    dano = 0
                if(dano < 0):
                    print(f"{personaje.nombre} recibio {abs(dano)} de dano!\n")
                    defensas[indice_aux] = 0
                    muerto = personaje.cambiar_hp(dano, enemigo)
                    if(muerto):
                        if(personaje in turnos):
                            turnos.pop(indice)
                        if(personaje in gm.personajes_muertos):
                            p_presentes.remove(personaje)
#                            print(f"{a.nombre} ha muerto...")
#                            print(p_presentes)
#                            print("\n\n")
#                            defensas.pop(indice_aux)
#                            turnos_aux.pop(indice_aux)
                else:
                    defensas[indice_aux] = dano
                    print(f"{personaje.nombre} bloqueo el ataque")
        elif("Defendiendose" in enemigo.condicion):
            print(f"{enemigo.nombre} se defiende... {accion}")
            defensas[indice_enemigo_aux] = accion
        elif("Huyendo" in enemigo.condicion):
            e_presentes.remove(enemigo)
        elif("Atacando con carisma" in enemigo.condicion):
                                # objetivo, defensa del objetivo
            self.pelea_carisma(accion[0], defensas[turnos_aux.index(accion[0])], 
                               dano_enemigo = accion[1], enemigo = enemigo)
        turnos.pop(indice_enemigo)
        return p_presentes, e_presentes, defensas, turnos, omitidos, historial
    
    
    def turno_personaje(self, p_presentes, e_presentes, defensas, turnos, omitidos, 
                        turnos_aux, personaje, historial, jaula = None):
        if(personaje in omitidos):
            omitidos.remove(personaje)
            turnos.pop(turnos.index(personaje))
            return p_presentes, e_presentes, defensas, turnos, omitidos, historial
        elif(personaje not in turnos or "Indefenso" in personaje.condicion):
            return p_presentes, e_presentes, defensas, turnos, omitidos, historial
        
        captura = ""
        habilidad = ""
        if("Domando" in personaje.condicion):
            captura = "7: Capturar\n"
            enemigo = e_presentes[0]
        if(self.arbol["A1"][0] == 1 or self.arbol["B1"][0] == 1):
            if("Domando" in personaje.condicion):
                habilidad = "8: Usar habilidad\n"
            else:
                habilidad = "7: Usar habilidad\n"
        
        salida = True
        indice = turnos_aux.index(personaje)
        while salida:
            print(f"¿{personaje.nombre}, que deseas hacer?")
            decision = int(input("0: Atacar\n1: Influenciar\n2: Defenderte"
                                 + "\n3: Usar objeto\n4: Tirar objeto \n5: Huir"
                                 + "\n6: Curarse\n" + captura + habilidad))
            if(decision == 0):
#                        print(e_presentes)
                resultado = personaje.atacar(e_presentes)
#                        print(e_presentes)
                indice_enemigo_aux = turnos_aux.index(resultado[0])
                eleccion = input(f"¿Deseas atacar a {resultado[0].nombre}? (S/N)\n")
                if(eleccion == "S"):
                    if("Confundido" in personaje.condicion):
                        resultado[0] = turnos_aux[gm.dados(1, len(turnos_aux))[0]-1]
                    print(f"{personaje.nombre} ataca a {resultado[0].nombre} con "
                          + f"{resultado[2].nombre} con una increible fuerza " 
                          + f"de {resultado[1]}")
                    salida = False
                elif(eleccion == "N"):
                    continue
                else:
                    print("Tas tonto shavo")
                    continue
                historial.append([personaje, resultado[0]])
                dano = defensas[indice_enemigo_aux] - resultado[1]
#                print(defensas)
                if(dano < 0):
                    defensas[indice_enemigo_aux] = 0
                    muerto = resultado[0].cambiar_hp(dano, personaje)
                    print(f"{resultado[0].nombre} recibio {dano} de dano!")
#                    print(e_presentes)
                    if(muerto):
                        if(resultado[2] in gm.armash_shidas):
                            if(resultado[0].categoria == "Humano"):
                                gm.anadir_obj_manual("Carne humana", personaje)
                        if(resultado[0] in turnos):
                            indice_enemigo=turnos.index(resultado[0])
                            turnos.pop(indice_enemigo)
#                            print(e_presentes)
#                            print(res[0])
#                            e_presentes.remove(res[0])
#                            defensas.pop(indice_enemigo_aux)
#                            turnos_aux.pop(indice_enemigo_aux)
                    elif(resultado[2].nombre == "Taxer" 
                         and resultado[0].nombre not in gm.notaxeables):
                        print(resultado[0].nombre +" ha sido paralizado!")
                        if(resultado[0] not in turnos):
                            omitidos.append(resultado[0])
                            print(omitidos)
                else:
                    defensas[indice_enemigo_aux] = dano
                    print(f"{resultado[0].nombre} bloqueo el ataque")
            elif(decision == 1):
                self.pelea_carisma(personaje, defensas[turnos_aux.index(personaje)], 
                                                       e_presentes = e_presentes)
            elif(decision == 2):
                defensas[indice] = personaje.defender()
                salida = False
            elif(decision == 3):
                #-----------------------------------------Usar objeto
                objetos_permitidos = []
                for i in range(0, len(personaje.inventario)):
                    if(personaje.inventario[i].estadistica != "F" 
                       or "Pocion" in personaje.inventario_nombres[i]):
                        objetos_permitidos.append(personaje.inventario[i].nombre)
                
                print("¿Que quieres usar?")
                print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                i=0
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        print(f"{i+1}, \t{llave:.24s}: \t\t"
                              + personaje.cartera_obj[llave]+" | \t\t"
                              + personaje.inventario[
                                      personaje.inventario_nombres.index(
                                              llave)].estadistica + " | \t"
                              + personaje.inventario[
                                      personaje.inventario_nombres.index(
                                              llave)].boosteo)
                        i+=1
                
                obj = int(input())-1
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        if(obj == 0):
                            break
                        obj -= 1
                objeto = personaje.inventario[
                        personaje.inventario_nombres.index(llave)]
                if("Confundido" in personaje.condicion):
                    objeto = personaje.inventario[gm.dados(1, 
                                                  len(personaje.inventario))[0]-1]
                #----------------------------------------Objeto seleccionado
                muerto = True
                if(objeto.nombre in gm.multiples):
                    seleccion = -1
                else:
                    print("¿Con quien usaras el objeto?")
                    if(objeto.estadistica == "Revivir"):
                        print("0: Regresar")
                        
                        #personaje estaba en accion[0]
                        for inv in range (0, len(personaje.inventario_nombres)):
                            if("Cadaver" in personaje.inventario_nombres[inv]):
                                print(f"{inv+1}: "
                                      +f"{personaje.inventario_nombres[inv]}")
                        seleccion = int(input())-1
                        if(seleccion == -1):
                            continue
                        else:
                            uso = personaje.usar_obj(
                                    personaje.inventario_nombres[seleccion], objeto)
                            salida = not uso
                            muerto = False
                    else:
                        for p in range(0, len(turnos_aux)):
                            if(turnos_aux[p].salud > 0):
                                print(f"{p+1}: {turnos_aux[p].nombre}")
                        print(f"{len(turnos_aux)+1}: Regresar")
                        seleccion = int(input())-1
                    
                if(muerto): # Uso normal de objeto, callate
                    if("Confundido" in personaje.condicion):
                        seleccion = turnos_aux[gm.dados(1, len(turnos_aux))[0]-1]
                    if(seleccion == len(turnos_aux)): # Regresar
                        continue
                    elif(seleccion == -1): # Objetivo multiple
                        personaje.usar_obj(turnos_aux, objeto)
                    elif(personaje.nombre == turnos_aux[seleccion].nombre):
                        uso = personaje.usar_obj(personaje, objeto)
                        if(type(uso) == bool):
                            salida = not uso
                        elif(list(uso.keys())[0] == "Escudo"):
                            defensas[seleccion] = list(uso.values())[0]
                            break
                    else:
                        uso = personaje.usar_obj(turnos_aux[seleccion], objeto)
                        if(type(uso) != bool):
                            if(list(uso.keys())[0] == "Escudo"):
                                defensas[seleccion] += list(uso.values())[0]
                            else:
                                defensas[seleccion] = uso[objeto.nombre]
                                salida = False
                                print(turnos_aux[seleccion].nombre 
                                      + " ha sido confundido!")
                                if(turnos_aux[seleccion] not in turnos):
                                    omitidos.append(turnos_aux[seleccion])
#                                   print(omitidos)
                                else:
                                    salto = turnos.index(turnos_aux[seleccion])
                                    turnos.pop(salto)
                        else:
                            salida = not uso
                            
            elif(decision == 4):
                salida = not personaje.tirar_objeto()
            elif(decision == 5):
                h = personaje.huir(e_presentes)
                print(f"{personaje.nombre} esta intentando escapar...", end = " ")
                if("Confundido" in personaje.condicion):
                    print(f"...{personaje.nombre}"
                          + " esta tan confundido que se tropezo con una rama...")
                    h = False
                if(h): # va a escapar
                    if("Domando" in personaje.condicion):
                        if(enemigo.velocidad > personaje.velocidad 
                           and enemigo.carisma > personaje.carisma):
                            z = personaje.ubicacion.zonas.index(personaje.zona)
                            personaje.ubicacion[z].jaulas[jaula.nombre].pop(jaula) 
                            #salirse de jaula
                            agresividad_max = (((self.oso_marino.carisma 
                                                + self.oso_marino.fuerza)
                                                - (self.oso_marino.inteligencia 
                                                  + self.oso_marino.resistencia))+4)
                            pelear = ((enemigo.salud/enemigo.salud_max) 
                                      * (enemigo.agresividad/agresividad_max) * 100)
                            if(enemigo.nombre in gm.domables 
                               and gm.dados(1, 100)[0] <= pelear):
                                if(personaje in turnos):
                                    indice = turnos.index(personaje)
                                    turnos.pop(indice)
                                return (p_presentes, e_presentes, defensas, 
                                        turnos, omitidos, historial)
                            else:
                                #[enemigo] = para que siempre escape
                                enemigo.huir([enemigo]) 
                                e_presentes.remove(enemigo)
                                turnos.pop(turnos.index(enemigo))
                    print("y lo ha logrado!!")
#                            defensas.pop(indice)
                    p_presentes.remove(personaje)
                    turnos.pop(turnos.index(personaje))
                    if(personaje.inteligencia >= (13 + 5 *(personaje.nivel))* 3/4):
                        personaje.moverse()
                    elif(personaje.inteligencia 
                         >= (13 + 5 *(personaje.nivel))* 1/2):
                        personaje.moverse(personaje.hogar)
                    else:
                        lugar = personaje.mapa[personaje.zona][
                           gm.dados(1, len(personaje.mapa[personaje.zona]))[0]-1]
                        personaje.moverse(lugar)
                else:
                    print("...y fracaso!! Como siempre")
                salida = False
            elif(decision == 6):
                salida = not personaje.energetizar()
            elif(decision == 7 and "Domando" in personaje.condicion):
                agresividad_max = (((self.oso_marino.carisma 
                                     + self.oso_marino.fuerza)
                                     - (self.oso_marino.inteligencia 
                                        + self.oso_marino.resistencia))+4)
                capturar = ((enemigo.salud/enemigo.salud_max) 
                            * (enemigo.agresividad/agresividad_max) * 100)
                if(enemigo.nombre in gm.domables 
                   and gm.dados(1, 100)[0] <= capturar):
                    personaje.reclutar(enemigo)
            elif(decision == 7 and habilidad[0] == "7" 
                 or decision == 8 and habilidad[0] == "8"):
                resultado = self.activar_habilidad("Turno personaje", omitidos)
                if(not resultado[1]):
                    salida = False
                else:
                    historial.append([personaje, resultado[1][0]])
                    dano = defensas[indice_enemigo_aux] - resultado[1][1]
                    if(dano < 0):
                        defensas[indice_enemigo_aux] = 0
                        muerto = resultado[1][0].cambiar_hp(dano, personaje)
                        print(f"{resultado[1][0].nombre} recibio {dano} de dano!")
                        if(muerto):
                            if(resultado[1][2] in gm.armash_shidas):
                                if(resultado[1][0].categoria == "Humano"):
                                    gm.anadir_obj_manual("Carne humana", personaje)
                            if(resultado[1][0] in turnos):
                                indice_enemigo=turnos.index(resultado[1][0])
                                turnos.pop(indice_enemigo)
                        elif(resultado[1][2].nombre == "Taxer" 
                             and resultado[1][0].nombre not in gm.notaxeables):
                            print(resultado[1][0].nombre +" ha sido paralizado!")
                            if(resultado[1][0] not in turnos):
                                omitidos.append(resultado[1][0])
                                print(omitidos)
                    else:
                        defensas[indice_enemigo_aux] = dano
                        print(f"{resultado[1][0].nombre} bloqueo el ataque")
            if(personaje in turnos):
                indice = turnos.index(personaje)
                turnos.pop(indice)
        return p_presentes, e_presentes, defensas, turnos, omitidos, historial
    
    
    def pelea_carisma(self, personaje, defensa, e_presentes = None, 
                      dano_enemigo = None, enemigo = None):
        if(enemigo == None):
            print(f"\n¿{personaje.nombre}, quién será tu victima?")
            print("INDICE \t NOMBRE \t SALUD")
            for i in range (0, len(e_presentes)):
                print(f"{i+1}: {e_presentes[i].nombre}\t{e_presentes[i].salud}")
            enemigo = e_presentes[int(input())-1]
            dano_enemigo = enemigo.ataque_carisma(objetivo = personaje)[1]
        dano_personaje = personaje.atacar_carisma(enemigo)[1]
        if("Indefenso" not in personaje.condicion):
            if(dano_personaje < dano_enemigo):
                print(f"{personaje.nombre} ha perdido el duelo de carisma")
                personaje.carisma -= dano_enemigo-dano_personaje
                if(personaje.carisma <= 0):
                    personaje.condicion.update({"Indefenso":2})
            elif(dano_personaje > dano_enemigo):
                print(f"{enemigo.nombre} ha perdido el duelo de carisma")
                enemigo.carisma -= dano_personaje-dano_enemigo
                if(enemigo.carisma <= 0):
                    enemigo.condicion.update({"Indefenso":2})
            else:
                print("El duelo fue un empate!!")
        else:
            print(f"{personaje.nombre} esta indefenso, {enemigo.nombre} ataca!!")
            dano = defensa - dano_enemigo
            if(dano < 0):
                print(f"{personaje.nombre} recibe {dano_enemigo} de dano")
                personaje.cambiar_hp(-dano_enemigo)
            else:
                print(f"El ataque de {enemigo.nombre} ha sido bloqueado!")
        return True
    
    
    def domar(self, personaje, enemigo, jaula, defensas, omitidos, historial):
        personaje.condicion.update({"Domando": 1})
        enemigo.condicion.update({"Domando": 1})
        if(jaula.nombre == "Trampa de osos"):
            enemigo.cambiar_hp(-5)
            enemigo.carisma += 1
            enemigo.fuerza += 1
        elif(jaula.nombre == "Jaula mas grande"):
            enemigo.fuerza -= int(enemigo.fuerza*.1)
        enemigo.actualizar_stats()
        p_primero = (personaje.velocidad >= enemigo.velocidad)
        turnos = [personaje, enemigo]
        for t in turnos:
            t.efecto()
        if(p_primero):     
            #Turno personaje
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_personaje([personaje], 
                                           [enemigo], defensas, turnos, omitidos, 
                                           turnos, personaje, historial, jaula = jaula)
            #Turno enemigo
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_enemigo(personaje, 
                                           enemigo, defensas, turnos, omitidos, 
                                           turnos, enemigo[0], historial, jaula = jaula)
        else:
            #Turno enemigo
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_enemigo([personaje], 
                                           [enemigo], defensas, turnos, omitidos, 
                                           turnos, enemigo, historial, jaula = jaula)
            #Turno personaje
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_personaje(personaje, 
                                           enemigo, defensas, turnos, omitidos, 
                                           turnos, personaje[0], historial, jaula=jaula)
            
        return [True, personaje[0], enemigo[0], jaula, defensas, omitidos, historial]
    
    def casino(self, personaje, premio = 0):
        print(f"---------- {personaje.nombre}, bienvenido al casino!! ---------- "
              + f"Premio actual: {premio}")
        print("¿Que quieres hacer?")
        inp = int(input("1: Jugar una ronda\n2: Ver premios\n3:Salir\n"))
        if(premio <= -500):
            inp = 3
        if(inp == 1):
            apuesta = int(input(f"\n----- A jugar! ----- "
                                + f"Premio actual: {premio}"
                                + "\n¿Cuánto deseas apostar?\n"))
            
            premio -= apuesta    
            
            lista1 = [1, 2, 3, 4, 5]
            lista2 = [1, 2, 3, 4, 5]
            lista3 = [1, 2, 3, 4, 5]
            lista4 = [1, 2, 3, 4, 5]
            lista5 = [1, 2, 3, 4, 5]
            listas = [lista1, lista2, lista3, lista4, lista5]
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            c=1
            for i in range(0, 3):
                print("\t", end = "")
                for j in range(0, 5):
                    print(listas[j][c], end="\t")
                    if(c>=4):
                        break
                c+=1
                print()
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            print("\nA jugar!\n")
            
            lista_final = []
            for i in listas:
                np.random.shuffle(i)
                lista_final.append(i[2])
            
            
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            c=1
            for i in range(0, 3):
                print("\t", end = "")
                for j in range(0, 5):
                    print(listas[j][c], end="\t")
                    if(c>=4):
                        break
                c+=1
                print()
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            
            premio_base = sum(lista_final)
            mult = []
            for i in range(1, 6):
                mult.append(lista_final.count(i))
            mult_final = 0
            if(max(mult) >= 3):
                mult_final = mult.index(max(mult))+1
            premio_actual = premio_base * mult_final * max(mult)
            print(f"Ganaste {premio_actual} puntos!!")
            
            # calculo automatico de dineros
            rangos = [0, 1, 22, 46, 190, 335, 480]
            multi = [0, 1, 2, 4, 6, 8, 10]
            m = 0
            for i in range(0, len(rangos)):
                if(premio_actual > rangos[i]):
                    m = multi[i]
                else:
                    break
            print(f"Obtuviste {m*apuesta} dineros!!\n")
            if(m != 0):
                premio += m*apuesta + apuesta
            else:
                premio += m*apuesta
        elif(inp == 2):
            print(f"\n----- Premios ----- Premio actual: {premio}"
                  + "\n 481 - 625 puntos: apuesta x 10 (PREMIO MAXIMO!!!!!!!)"
                  + "\n 336 - 480 puntos: apuesta x 8"
                  + "\n 191 - 335 puntos: apuesta x 6"
                  + "\n 46 - 190  puntos: apuesta x 4"
                  + "\n 22 - 45   puntos: apuesta x 2"
                  + "\n 1 - 21    puntos: apuesta x 1"
                  + "\n 0         puntos: 0\n")
        elif(inp == 3):
            presupuesto = personaje.cartera
            if(premio >= 0):
                personaje.anadir_obj(premio)
            else:
                deuda = presupuesto + premio
                if(deuda < 0):
                    personaje.anadir_obj(-presupuesto)
                    for numPasada in range(len(personaje.inventario)-1,0,-1):
                        for i in range(numPasada):
                            if (personaje.inventario[i].precio 
                                > personaje.inventario[i+1].precio):
                                temp = personaje.inventario[i]
                                personaje.inventario[i] = personaje.inventario[i+1]
                                personaje.inventario[i+1] = temp
                    deuda = abs(deuda)
                    while(deuda > 0):
                        if(personaje.inventario == []):
                            break
                        deuda -= personaje.inventario[0].precio
                        personaje.inventario.pop(0)
                        personaje.inventario_nombres.pop(0)
                    if(deuda > 0):
                        print("Me las vas a pagar con tu vida shavo!\n..."
                              + f"{personaje.nombre}" 
                              + " ha recibido una paliza... "
                              + f"-{personaje.salud/4}")
                        personaje.cambiar_hp(-(personaje.salud/4))
                else:
                    personaje.anadir_obj(-premio)
            return True
        self.casino(personaje, premio)
    
    def escalera(self, p, nivel = 0, niv_maquina = 0, niv_nina = 0, niv_monstruo=0):
        #DEBUG
#    print("-------------------------------------------------------Metodo escalera")
        print(f"{p.nombre}, estas en el nivel {nivel}")
        if(nivel == 0):
            niv_maquina = gm.dados(1, 10)[0]
            niv_nina = gm.dados(1, 20)[0]
            niv_monstruo = gm.dados(1, 25)[0]
        sel = input(f"{p.nombre}, ¿quieres bajar? (S/N)\n")
        if(sel == "S"):
            nivel += 1
        elif(sel == "N"):
            print("Has vuelto al inicio de las escaleras")
            nivel = 0
        else:
            print("Tas tonto shavo")
        if(nivel == niv_monstruo):
            print("Has encontrado al monstruo!! :O")
            prob = (nivel*100)/25
            pr = gm.dados(1, 100)[0]
            if(pr <= prob):
                p.cambiar_hp(-2000)
            else:
                print("Lograste escapar con éxito! "
                      + "Has vuelto al inicio de las escaleras")
                nivel = 0
        if(nivel == niv_nina):
            s = input("Has encontrado una sala misteriosa... "
                      + "¿Quieres entrar? (S/N)\n")
            if(s == "S"):
                print("Dialogo intenso...")
                obj = Objeto("Pelo", "--", "--", 0, 1, 10000, 0)
                zonas = p.ubicacion.zonas
                i = zonas.index(p.zona)
                p.ubicacion.objetos[i].append(obj.nombre)
                p.ubicacion.objetos_activos[i].append(obj)
                p.ubicacion.cantidades[i].append(10000)
                p.anadir_obj(obj)
        if(nivel == niv_maquina):
            s = input("Has encontrado la sala de la maquina!! "
                      + "¿Quieres entrar? (S/N)\n")
            if(s == "S"):
                p.moverse(gm.edificio, "Maquina")
                p.usar_maquina()
        return [p, nivel, niv_maquina, niv_nina, niv_monstruo]
    
    def generar_jefes(self, lugar, zona:str):
        print("-------------------------------------------------------Metodo jefes")
        z = lugar.zonas.index(zona)
        jeff = []
        lugar_original = gm.lugares_o_originales[gm.lugares_o.index(lugar)]
        from Enemigos import Enemigo
        
        print(lugar.enemigos[z])
        
        for e in lugar.enemigos[z]:
            if(e in gm.jefes_no_jefes):
                jeff.append(e)
        contador = -1
#        print(jefes_no_jefes)
#        print(jeff)
        for h in range (0, len(gm.Dfnombres_e)):
            if(abs(contador) > len(jeff)):
                break
            if ((gm.Dfnombres_e.iloc[h,0] in gm.jeff) 
                and (lugar_original.cantidades()[z][contador] > 0) 
                and (not self.repetido(lugar, z, gm.Dfnombres_e.iloc[h,0]))):
                nombre = gm.Dfnombres_e.iloc[h,0]
                basura = False
                salud = gm.Data_e.iloc[h,1]
                if(type(salud) == pd.core.series.Series):
                        basura = True
                        salud = salud.iloc[0]
                fuerza = gm.Data_e.iloc[h,2]
                resistencia = gm.Data_e.iloc[h,3]
                hostilidad = gm.Data_e.iloc[h,4]
                inteligencia = gm.Data_e.iloc[h,5]
                sabiduria = gm.Data_e.iloc[h,6]
                categoria = gm.Data_e.iloc[h,7]
                rango = gm.Data_e.iloc[h,8]
                dropeos = gm.Data_e.iloc[h,9]
                cantidad = gm.Data_e.iloc[h,10]
                if(basura):
                        fuerza = fuerza.iloc[0]
                        resistencia = resistencia.iloc[0]
                        hostilidad = hostilidad.iloc[0]
                        inteligencia = inteligencia.iloc[0]
                        sabiduria = sabiduria.iloc[0]
                        categoria = categoria.iloc[0]
                        rango = rango.iloc[0]
                        dropeos = dropeos.iloc[0]
                        cantidad = cantidad.iloc[0]
                
                e = Enemigo(salud, fuerza, resistencia, hostilidad, inteligencia, 
                            sabiduria, nombre, {"Saludable": 1}, dropeos, categoria, 
                            rango, cantidad, zona)
                lugar.enemigos_activos[z].append(e)
                contador -= 1
                e.stats()
        
    def generar_enemigos_zona(self, lugar:Lugar, zona:str):
        #DEBUG
        
        self.generar_jefes(lugar, zona)
        indice = lugar.zonas.index(zona)
        enemigos,cantidades = gm.mezclar_listas(lugar.enemigos[indice],
                                                lugar.cantidades_enemigos[indice], 1)
        lugar.enemigos_zona_s(enemigos, zona)
        lugar.cantidades_enemigos_zona_s(cantidades, zona)
        from Enemigos import Enemigo
        
        enemigos_aux = []
        cantidades_aux = []
        contador3 = 0
        for e in range(0, len(enemigos)):
            if(enemigos[e] not in gm.jefes.keys()):
                enemigos_aux.append(enemigos[e])
                cantidades_aux.append(cantidades[e])
            else:
                contador3 += 1
                
        enemigos, cantidades = enemigos_aux, cantidades_aux
#        contador = len(enemigos)//2
        minimo = 2
        if(zona == "Mercado"):
            minimo *= 2
            
        maximo = len(enemigos)//4
        if(maximo == 0):
            maximo = 1
        contador = minimo + gm.dados(1, maximo)[0]
        if(sum(cantidades) < contador):
            contador = sum(cantidades) + contador3
        contador -= contador3
#        contador2 = 0
        
#        print("----------------------------------------------------------")
#        print("\t\t"+zona)
#        print("----------------------------------------------------------")
        enemigos_a = []
        enemigos_a_aux = []
        for i in range(0, len(enemigos)):
            enemigos_a.append(enemigos[gm.dados(1, len(enemigos))[0]-1])
#                print("contador: " + str(contador))
#                print("contador 2: " + str(contador2))
        
        for en in enemigos_a:
            if(en not in gm.jefes_no_jefes):
                enemigos_a_aux.append(en)
            else:
                contador -= 1
        enemigos_a = enemigos_a_aux
        print(enemigos_a)
        print(contador)
        while(contador > 0):
            for j in range(0, len(enemigos_a)):
    #            j+=contador2
                for h in range (0, len(gm.Dfnombres_e)):
                    if(contador<=0):
                        break
                    if((gm.Dfnombres_e.iloc[h,0] == enemigos_a[j])  
                        and (cantidades[j] > 0.0) 
                        and (gm.Dfnombres_e.iloc[h,0] not in gm.jefes.keys())):
                        basura = False
                        salud = gm.Data_e.iloc[h,1]
                        if(type(salud) == pd.core.series.Series):
                                basura = True
                                salud = salud.iloc[0]
                        fuerza = gm.Data_e.iloc[h,2]
                        resistencia = gm.Data_e.iloc[h,3]
                        hostilidad = gm.Data_e.iloc[h,4]
                        inteligencia = gm.Data_e.iloc[h,5]
                        sabiduria = gm.Data_e.iloc[h,6]
                        categoria = gm.Data_e.iloc[h,7]
                        rango = gm.Data_e.iloc[h,8]
                        dropeos = gm.Data_e.iloc[h,9]
                        cantidad = gm.Data_e.iloc[h,10]
                        if(basura):
                                fuerza = fuerza.iloc[0]
                                resistencia = resistencia.iloc[0]
                                hostilidad = hostilidad.iloc[0]
                                inteligencia = inteligencia.iloc[0]
                                sabiduria = sabiduria.iloc[0]
                                categoria = categoria.iloc[0]
                                rango = rango.iloc[0]
                                dropeos = dropeos.iloc[0]
                                cantidad = cantidad.iloc[0]
                        
                        e = Enemigo(salud, fuerza, resistencia, hostilidad, 
                                    inteligencia, sabiduria, enemigos_a[j], 
                                    {"Saludable": 1}, dropeos, categoria, 
                                    rango, cantidad, zona)
                        lugar.enemigos_activos[indice].append(e)
                        if(e.nombre == "Oso marino"):
                            self.oso_marino = e
                            print("AAAAAAAAAAAAA")
#                        e.stats()
                        contador -= 1
    #                    contador2 += 1
                        break
        return ""
    
    def generar_objetos_zona(self, lugar, zona:str):
        #DEBUG
#        print("--------------------------------------------Metodo generar objetos")
        fragmento = Objeto("Fragmento de libro de secretos", 
                           0, "Habilidad", 0, 1, 1, 300)
        if(lugar == gm.pueblo) and (gm.pueblo_original.cantidades()[1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif(lugar == gm.bosque) and (gm.bosque_original.cantidades()[1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.normancueva) 
            and (gm.normancueva_original.cantidades()[1][0] > 0)):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.fondo_del_mar) 
            and (gm.fondo_del_mar_original.cantidades()[0][0] > 0)):
            lugar.objetos_activos[0].append(fragmento)
            
        indice = lugar.zonas.index(zona)
        objetos,cantidades = gm.mezclar_listas(lugar.objetos[indice],
                                               lugar.cantidades()[indice], 1)
        lugar.objetos_zona_s(objetos, zona)
        lugar.cantidades_objetos_zona_s(cantidades, zona)
        
#        print(lugar.objetos)
#        print(objetos)
        if(len(objetos) == 0):
            contador = 0
        elif(len(objetos) == 1):
            contador = 1
        else:
            contador = gm.dados(1, len(objetos))[0]//2
#        contador2 = 0
#        if(contador<1):
#            contador+=1
#        print("----------------------------------------------------------")
#        print("\t\t"+zona)
#        print("----------------------------------------------------------")
#                print("contador: " + str(contador))
#                print("contador 2: " + str(contador2))
        for j in range(0, len(objetos)):
#            j+=contador2
            for h in range (0, len(gm.Dfnombres_o)):
                if(contador<=0):
                    break
                if((gm.Dfnombres_o.iloc[h,0] == objetos[j]) 
                and (cantidades[j] > 0.0) 
                and (gm.Dfnombres_o.iloc[h,0] != "Fragmento de Libro de Secretos")):
                    nombre = objetos[j]
                    o = self.tranformar_objeto(nombre, cantidades[j])
                    lugar.objetos_activos[indice].append(o)
#                    o.stats()
                    contador -= 1
#                    contador2 += 1
                    break
        return ""
    
    def generar_objetos(self, lugar):
        #DEBUG
        print("---------------------------------------------Metodo generar objetos")
        fragmento = Objeto("Fragmento de libro de secretos", 0, 
                           "Habilidad", 0, 1, 1, 300)
        if(lugar == gm.pueblo) and (gm.pueblo_original.cantidades()[1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif(lugar == gm.bosque) and (gm.bosque_original.cantidades()[1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.normancueva) 
            and (gm.normancueva_original.cantidades()[1][0] > 0)):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.fondo_del_mar) 
            and (gm.fondo_del_mar_original.cantidades()[0][0] > 0)):
            lugar.objetos_activos[0].append(fragmento)
        objetos,cantidades = gm.mezclar_listas(lugar.objetos, lugar.cantidades(), 2)
        lugar.objetos = objetos
        lugar.cantidades = cantidades
#        print(lugar.objetos)
#        print(objetos)
        for i in range (0, len(lugar.zonas)):
            contador = len(lugar.objetos[i])//2
#            contador2 = 0
            if(contador<1):
                contador+=1
            print("--------------------------------------------------------------")
            print("\t\t"+lugar.zonas[i])
            print("--------------------------------------------------------------")
            for j in range(0, len(lugar.objetos[i])):
#                j+=contador2
                for h in range (0, len(gm.Dfnombres_o)):
                        if(contador<=0):
                            break
                        if ((gm.Dfnombres_o.iloc[h,0] == lugar.objetos[i][j]) 
                        and (lugar.cantidades()[i][j] > 0.0) 
                        and (lugar.objetos[
                                i][j] != "Fragmento de Libro de Secretos")):
                                nombre = lugar.objetos[i][j]
                                o = self.tranformar_objeto(nombre, 
                                                           lugar.cantidades()[i][j])
                                lugar.objetos_activos[i].append(o)
                                o.stats()
                                contador -= 1
#                                contador2 += 1
                                break
        return ""

    def tranformar_objeto(self, nombre: str, cantidad_manual = None):
        #DEBUG
#        print("-----------------------------------------Metodo transformar objeto")
        for h in range (0, len(gm.Dfnombres_o)):
            if (gm.Dfnombres_objetos.iloc[h,0] == nombre):
                basura = False
                boosteo = (gm.Data_objetos2.loc[nombre, "Boosteo"])
                if(type(boosteo) == pd.core.series.Series):
                    basura = True
                    boosteo = int(boosteo.iloc[0])
                estadistica = (gm.Data_objetos2.loc[nombre, "Estadistica"])
                peso = (gm.Data_objetos2.loc[nombre, "Espacio"])
                usos = (gm.Data_objetos2.loc[nombre, "Usos"])
                cantidad = (gm.Data_objetos2.loc[nombre, "Cantidad"])
                precio = (gm.Data_objetos2.loc[nombre, "Precio"])
                if(basura):
                    estadistica = estadistica.iloc[0]
                    peso = float(peso.iloc[0])
                    usos = int(usos.iloc[0])   
                    cantidad = int(cantidad.iloc[0])
                    precio = int(precio.iloc[0])
                if(cantidad_manual != None):
                    cantidad = cantidad_manual
                if(nombre == "Nota de consejo"):
                    boosteo = gm.consejos[gm.dados(1, len(gm.consejos))[0]-1]
                objeto = Objeto(nombre, boosteo, estadistica, peso, usos, 
                                cantidad, precio)
#                objeto.stats()
                break
#        print("------------------------------------------------------------------")
        return objeto

    def maquina(self, nombre: str, usuario, mult = 1):
        #DEBUG
        print("-----------------------------------------------------Metodo maquina")
        if(not self.funcional):
            return False
        
        indice = usuario.inventario_nombres.index(nombre)
        usuario.peso -= usuario.inventario[indice].peso
        zonas = usuario.ubicacion.zonas
        i = zonas.index(usuario.zona)
        usuario.inventario_nombres.pop(indice)
        usuario.inventario.pop(indice)
        
        tirada = gm.dados(1, 4)[0]
        i, j = 0, 0
        for i in range(0, len(gm.Dfnombres_o)):
            if(gm.Dfnombres_o.iloc[i,0] == nombre):
                break
        if(tirada < 4 * mult):
            b = gm.Dfmejoras_o
        else:
            b = gm.Dfestropeos_o
        b = b.iloc[i,0]
        for j in range(0, len(gm.Dfnombres_o)):
            if(gm.Dfnombres_o.iloc[j,0] == b):
                break
        nombre = b
        
        if(nombre[0] == "XXX"):
            self.funcional = False
        
        if(nombre[0] == "%"):
            nombre = gm.revisar_string(nombre)
        
        if("Cadaver " in nombre):
            nombre = "Cadaver de " + usuario.nombre
            
        if(nombre[0].isdigit() and nombre[2:] != "Dinero"):
            for i in range(0, int(nombre[0])):
                gm.anadir_obj_manual(nombre[2:], usuario)
            return True
        
        if(nombre == "3 Dinero"):
            usuario.anadir_obj(3)
            return True
        
#        o = self.tranformar_objeto(nombre, 9999)
#        edificio.objetos_activos[1].append(o)
#        edificio.objetos[1].append(o.nombre)
#        edificio.cantidades()[1].append(o.cantidad)
        gm.anadir_obj_manual(nombre, usuario, 9999)
#        print("------------------------------------------------------------------")

lug = Lugar("A", [], [3], [], [], [], [], [])
print(lug.enemigos)