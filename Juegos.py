# -*- coding: ISO-8859-1 -*-
import pandas as pd
import numpy as np
import Game_Manager as gm
from Lugares import Lugar
from Objetos import Objeto
from Individuos import Individuo

class Juego:
    
    def __init__(self):
        self.funcional = True
        self.domas = []
        self.oso_marino = None
    
    def jugar(self, reses = []):
        #DEBUG
#        print("------------------------------------------------------Metodo jugar")
        # Quitar los que ya no estan domando
        domar_nuevo = []
        for domar in self.domas:
            if(domar[0]):
               domar_nuevo.append(domar)
        self.domas = domar_nuevo
#        print("-----------------"+ str(self.oso_marino.carisma))
        fin = False
        per = []
#        print("Per")
#        print(reses)
        for r in reses:
            for r1 in r[1]:
                print(r1.nombre)
#                print("-.-.-.-.-.-.-.-.-.")
                per.append(r1)
#        print(per)
        turnos = personajes
        for p in range(len(personajes)-1,0,-1):
            for i in range(p):
                if personajes[i].velocidad>personajes[i+1].velocidad:
                    temp = turnos[i]
                    turnos[i] = turnos[i+1]
                    turnos[i+1] = temp
        
        turnos_aux = []
        for t in range(len(turnos)-1, 0, -1):
            turnos_aux.append(turnos[t])
        turnos_aux.append(turnos[0])
        
        turnos = turnos_aux
        
        for t in range(0, len(turnos)):
            if("Domando" in turnos[t].condicion):
                print(turnos[t].nombre + "esta domando...")
                for doma in range (0, len(self.domas)):
                    if(turnos[t] in self.domas[doma]):
                        #doma[2] = enemigo, doma[3] = jaula, doma[4] = defensas, doma[5] = cancel, doma[6] = hist
                        self.domas[doma] = self.domar(turnos[t], self.domas[doma][2], self.domas[doma][3], self.domas[doma][4], self.domas[doma][5], self.domas[doma][6])
                        break
                continue
            
            domar_posible = ""
            for enemigo in turnos[t].ubicacion.enemigos_activos()[turnos[t].ubicacion.zonas().index(turnos[t].zona)]:
                if("Atrapado" in enemigo.condicion):
                    domar_posible = "9: Domar"
                elif("Atrapado" not in enemigo.condicion):
                    domar_posible = ""
                    break
            
            is_mercado = "Buscar"
            if(turnos[t] in per):
                continue
            if(turnos[t].zona == "Mercado"):
                is_mercado = "Robar"
            turnos[t].stats()
            
            turnos[t].efecto() # efecto a personajes que no esten peleando
            print(f"{turnos[t].nombre}, ¿Que deseas hacer?")
            seleccion = int(input("1: Moverte\n2: "+is_mercado+"\n3: Usar objeto\n4: Tirar objeto\n5: Esperar\n6: Curarse\n7: Usar habilidad\n8: Guardar(Salir por ahora)\n" + domar_posible))
            if(seleccion == 1):
                turnos[t].moverse()
            elif(seleccion == 2):
                if(mercado == "Buscar"):
                    objeto = input("¿Que quieres "+is_mercado.lower()+"? (0 para nada en especifico)\n")
                    if(objeto == '0'):
                        turnos[t].buscar()
                    else:
                        turnos[t].buscar(objeto)
                else:
                    print("¿Que quieres "+is_mercado.lower()+"?\n")
                    for o in mercado.objetos_activos()[0]:
                        print(f"{o.nombre}")
                    objeto = input()
                    turnos[t].buscar(objeto)
                    
            elif(seleccion == 3):
                objetos_permitidos = []
                for i in range(0, len(turnos[t].inventario)):
                    if(turnos[t].inventario[i].nombre != "F" or "Pocion" in turnos[t].inventario_nombres[i] and turnos[t].inventario_nombres[i] != "SCP 427"):
                        objetos_permitidos.append(turnos[t].inventario[i].nombre)
                
                print(f"¿Que quieres usar?")
                print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                i=0
                for llave in turnos[t].cartera_obj:
                    if(llave in objetos_permitidos):
                        print(f"{i+1}, \t{llave:.<24s}: {turnos[t].cartera_obj[llave]} | \t\t{turnos[t].inventario[self.inventario_nombres.index(llave)].estadistica} | \t{turnos[t].inventario[turnos[t].inventario_nombres.index(llave)].boosteo}")
                        i+=1
                
                obj = int(input())-1
                for llave in turnos[t].cartera_obj:
                    if(llave in objetos_permitidos):
                        if(obj == 0):
                            break
                        obj -= 1
                objeto = turnos[t].inventario[turnos[t].inventario_nombres.index(llave)]
                
                turnos[t].usar_obj(objeto)
            elif(seleccion == 4):
                turnos[t].tirar_objeto()
            elif(seleccion == 5):
                turnos[t].energia = turnos[t].energia_max
                print("Energia restaurada!!")
                continue
            elif(seleccion == 6):
                turnos[t].energetizar()
            elif(seleccion == 7):
                turnos[t].activar_habilidad("Jugar")
            elif(seleccion == 8):
                fin = True
                return ""
            elif(seleccion == 9 and domar_posible != ""):
                print("¿Que enemigo intentaras domar?")
                contador = 0
                jaulas = []
                for jaula in t.ubicacion.jaulas:
                    for jaula_enemigo in jaula:
                        print(str(contador) + jaula + ": " + t.ubicacion.jaulas[jaula][jaula_enemigo].nombre)
                        jaulas.append(jaula_enemigo)
                        contador += 1
                jaula_select = jaulas[int(input())]
                # t = objeto personaje, t.ubicacion.jaulas[jaula_select.nombre][jaula_select] = objeto enemigo, jaula_selecct = objeto jaula, defensas, cancel, hist
                self.domas.append(self.domar(t, t.ubicacion.jaulas[jaula_select.nombre][jaula_select], jaula_select, [0, 0], [], []))
            else:
                print("Tas tonto shavo")
                t -= 2
                continue
        
        p_presentes = []
        peleas = []
        zonas = []
        
        zonas_vistas = []
        
        for p in personajes:
            p.actualizar_stats()
            for i in p.inventario_nombres:
                if(i == "Pistola laser"):
                    indio = p.inventario_nombres.index("Pistola laser")
                    p.inventario[indio].uso -= 2
                elif(i == "Pistola laser mejorada"):
                    indio = p.inventario_nombres.index("Pistola laser mejorada")
                    p.inventario[indio].uso -= 2
            
            z = p.ubicacion.zonas().index(p.zona)
            if(p.ubicacion.enemigos_activos()[z] != []):
                p_presentes.append(p)
#                print(p.nombre)
#                print(p.ubicacion.enemigos_activos())
                
            # revisar zonas vistas de todos
            for m in p.mapa[p.zona]:
                zonas_vistas.append(m)
            zonas_vistas.append(p.zona)
        
        #Listas de enemigos activos de zonas vistas
        for zona_vista in zonas_vistas:
            lugar_visto = buscaLugar(zona_vista)
            z = lugar_visto.index(zona_vista)
            #Obtener todas las jaulas de todos los tipos de jaula de la zona actual
            jaulas_activas=[]
            for jaulas in lugar_visto[z].jaulas:
                for jaula in jaulas:
                    if(Juego.dados(1, 2)[0] == 1 and jaulas[jaula] != ""):
                        jaulas_activas.append(jaula)
            
            if(jaulas_activas != []):
                for enemigo in lugar_visto.enemgios_activos()[z]:
                    for trampa in jaulas_activas:
                        if(trampa.nombre == "Trampa de osos"):
                            if(enemigo in atrapables_t_osos):
                                tirada = Juego.dados(1, 10)[0]
                                if(enemigo.sabiduria + tirada <= 20):
                                    #Enemigo atrapado
                                    enemigo.condicion.update({"Atrapado": 1})
                                    lugar_visto[z].jaulas[trampa.nombre][trampa] = enemigo.nombre
                                    lugar_visto[z].objetos_activos.remove(trampa)
                                    break
                        elif(trampa.nombre == "Jaula"):
                            if(enemigo in atrapables_medianos):
                                tirada = Juego.dados(1, 10)[0]
                                if(enemigo.sabiduria + tirada <= 20):
                                    #Enemigo atrapado
                                    enemigo.condicion.update({"Atrapado": 1})
                                    lugar_visto[z].jaulas[trampa.nombre][trampa] = enemigo.nombre
                                    lugar_visto[z].objetos_activos.remove(trampa)
                                    break
                        elif(trampa.nombre == "Jaula mas grande"):
                            if(enemigo in atrapables):
                                tirada = Juego.dados(1, 20)[0]
                                if(enemigo.sabiduria/2 + tirada <= 25):
                                    #Enemigo atrapado
                                    enemigo.condicion.update({"Atrapado": 1})
                                    lugar_visto[z].jaulas[trampa.nombre][trampa] = enemigo.nombre
                                    lugar_visto[z].objetos_activos.remove(trampa)
                                    break
        
        if(p_presentes != []):
            for p in p_presentes:
                zonas.append(p.zona)
                
            zona = ""
            c=0  # Numero de pelea
            c2=0 # Cuantos personajes ha anadido a peleas
            saltar = False

            for p in p_presentes:
                for pelea in range(0, len(peleas)):
                    if(p in peleas[pelea]):
                        saltar = True
                if(saltar):
                    saltar = False
                    continue
                if(c2 < len(p_presentes)):
                    peleas.append([])
                zona = p.zona
                for z in range(0, len(zonas)):
                    if(zona == zonas[z]):
                        peleas[c].append(p_presentes[z])
                        c2+=1
                c+=1
                
            for pelea in peleas:
                for i in pelea:
                    print(i.nombre, end = ", ")
                print()
#            print(peleas)
#            print(reses)
            for pelea in peleas:
                omitir = True
                cancel = []
                defensas = []
                turnos_pelea = []
                empezar = False
                for r in range(0,len(reses)):
                    for r1 in reses[r][1]:
                        if(r1 in pelea):
                            
                            cancel = reses[r][5].copy()
                            defensas = reses[r][3].copy()
                            turnos_pelea = reses[r][4].copy()
                            omitir = False
                            break
                    if(not omitir):
                        break
                if(omitir):
                    #Esta en pelea y no en reses (la pelea esta comenzando)
                    empezar = True
#                if(reses != []):
                if(reses != [] and not reses[r][0]):
                    reses.remove(r)
                elif(reses != [] and reses[r] == []):
                    cancel = []
                    defensas = []
                    turnos_pelea = []
                    empezar = True
                print(cancel)
                print(pelea[0].nombre, pelea[0].zona)
                z = pelea[0].ubicacion.zonas().index(pelea[0].zona)
                e_presentes = pelea[0].ubicacion.enemigos_activos()[z]
                e_presentes_aux = e_presentes.copy()
                if(empezar):
                    for e in e_presentes_aux:
                        if(e.categoria == "Humano" and e not in jefes.keys() and e.salud > 0):
                            e_presentes.remove(e)
#                print(pelea)
#                print(pelea[0].nombre)
#                print(e_presentes)
                
                if(empezar):
                    print("La pelea ha comenzado")
                    reses.append(self.iniciar_pelea(self, pelea, e_presentes, cancel))
                else:
                    print("Que siga la pelea")
                    # La r se sobre escribe de las reses   r5 esta antes por el orden en que recibe iniciar pelea
                    # r1 = p_presentes, r2 = e_presentes, r5 = cancel, r3 = defensas, r4 = turnos, per = personajes peleando
#                    print("reses")
#                    print(reses)
                    reses[r] = self.iniciar_pelea(self, pelea, e_presentes, cancel, defensas, turnos_pelea, per)
#                    print("\nr")
#                    print(reses[r])
        
        if(not fin):
            return reses
            
    def iniciar_pelea(self, p_presentes, e_presentes, cancel = [], defensas = [], turnos = [], per = [], victima = None, mult = 1):
        #DEBUG
        print("----------------------------------------------Metodo iniciar_pelea")
        if(e_presentes == []):
                print("Disfruta tu estadia")
                return [False, p_presentes]
        estemen = False
        for ie in e_presentes:
            if(ie in jefes.keys()):
                estemen = True
        e_sabiduria = 0
        p_pelea = []
        enemigos_op_activos = []        
        for e in e_presentes:
            if(e.sabiduria > e_sabiduria):
                e_sabiduria = e.sabiduria
            if(e.nombre in enemigos_op):
                enemigos_op_activos.append(e)
                
        if(victima != None): # Cuando estas robando
            p_presentes.remove(victima)
            if(victima.sabiduria < e_sabiduria):
                p_pelea.append(victima)
                print(f"{victima.nombre} has sido detectado, hora de pelear!")
                for p in p_presentes:
                    decision = input(f"¿{p.nombre}, quieres hacer la guerra? (S/N)")
                    if(decision == "S"):
                        p_pelea.append(p)
                        for a in p.asistentes:
                            p_pelea.append(a)
            else:
                print("Oof, te has salvado...")
                for e in e_presentes:
                    e.salud /= mult
                    e.fuerza /= mult
                    e.resistencia /= mult
                    e.carisma /= mult
                    e.inteligencia /= mult
                    e.sabiduria /= mult
        else:
            for p_m in personajes_muertos: # Añadir a asistentes de personajes muertos
                if(p_m.zona == p_presentes[0].zona):
                    for a in p_m.asistentes:
                        p_pelea.append(a)
            for p in p_presentes:
                sigilo = False
                if(p in per):
                    p_pelea.append(p)
                    for a in p.asistentes:
                        p_pelea.append(a)
                    continue
                if("Invisible" not in p.condicion or enemigos_op_activos != []):
                    if(p.sabiduria < e_sabiduria):
                        p_pelea.append(p)
                        for a in p.asistentes:
                            p_pelea.append(a)
                        print(f"{p.nombre} has sido detectado, hora de pelear!")
                    else:
                        sigilo = True
                else:
                    sigilo = True
                    
                if(sigilo):
                    if(p.nombre == "Ruben" and p.arbol["A3"][0] == 1):
                        decision = input("¿Ruben, quieres utilizar tu habilidad? (S/N)")
                        if(decision == "S"):
                            p.activar_habilidad("Iniciar pelea", cancel)
                    else:
                        zonas = p.ubicacion.zonas()
                        z = zonas.index(p.zona)
                        tirada = Juego.dados(1, len(p.ubicacion.enemigos_activos()[z]))[0]
                        print(f"{p.nombre}, has avistado a {tirada} enemigos...")
                        enemigos_vistos = []
                        for i in range(0, tirada):
                            print(f"... hay un {p.ubicacion.enemigos_activos()[z][i].nombre} cerca...")
                            enemigos_vistos.append(p.ubicacion.enemigos_activos()[z][i])
                        print("\n...posiblemente hayan mas enemigos en la zona...\n")
                    print(f"{p.nombre}, estas en modo sigilo sigilozo ¿que deseas hacer?")
                    decision = int(input("0: Atacar\n1: Unirse a la pelea\n2: Usar objeto\n3: Tirar objeto \n4: Moverte\n5: Esperar\n"))
                    if(decision == 0):
                        ataque = p.atacar(enemigos_vistos, 1.5)
                        ataque[0].cambiar_hp(-ataque[1], p)
                        if(p.sabiduria < e_sabiduria+Juego.dados(1, (e_sabiduria//2)+1)[0] or estemen):
                            p_pelea.append(p)
                            for a in p.asistentes:
                                p_pelea.append(a)
                            print(f"{p.nombre} has sido detectado, hora de pelear!")
                        else:
                            print("Te mantienes detras de las sombras..")
                    elif(decision == 1):
                        p_pelea.append(p)
                        for a in p.asistentes:
                            p_pelea.append(a)
                        print(f"{p.nombre}, hora de pelear!!")
                    elif(decision == 2):
                        p.usar_obj(p_presentes+enemigos_vistos)
                    elif(decision == 3):
                        p.tirar_objeto()
                    elif(decision == 4):
                        p.moverse()
                    else:
                        print(f"{p.nombre} se esconde...")
                        for i in range(tirada, tirada + Juego.dados(1, 3)[0]):
                            if(i >= len(p.ubicacion.enemigos_activos()[z])):
                                break
                            print(f"... has avistado a {p.ubicacion.enemigos_activos()[z][i].nombre} tambien...")
                if(e_presentes == []):
                    print("Victoria!")
                    if(estemen):
                        for ip in p_presentes:
                            ip.subir_nivel()
                    p_presentes = []
                    return [False, p_presentes]
        enemigos = []
        for enemigo in e_presentes:
            if("Atrapado" not in enemigo.condicion):
                enemigos.append(enemigo)
        
        if(p_pelea != []):
            return self.pelea(self, p_pelea, enemigos, defensas, turnos, cancel)
        return [False, p_pelea]

    def pelea(self, p_presentes, e_presentes, defensas = [], turnos = [], cancel = []):
        #DEBUG
#        print("------------------------------------------------------Metodo pelea")
        for j in jefes.keys():
            notaxeables.append(j)
        estemen = False
        for ie in e_presentes:
            if(ie in jefes.keys()):
                estemen = True
        for p in personaje: # Añadir a asistentes de personajes vivos que no esten en pelea
            if(p in personajes):
                for a in p.asistentes:
                    if(a not in p_presentes):
                        p_presentes.append(a)
        for p_m in personajes_muertos: # Añadir a asistentes de personajes muertos solo una vez por pelea
            if(p_m.zona == p_presentes[0].zona):
                for a in p_m.asistentes:
                    if(a not in p_presentes):
                        p_presentes.append(a)
        if(turnos == []):
            turnos = p_presentes + e_presentes
        velocidades = []
        hist = []
        for pr in turnos:
            velocidades.append(pr.velocidad)
        for numPasada in range(len(velocidades)-1,0,-1):
            for i in range(numPasada):
                if velocidades[i]>velocidades[i+1]:
                    temp = velocidades[i]
                    velocidades[i] = velocidades[i+1]
                    velocidades[i+1] = temp
                    temp1 = turnos[i]
                    turnos[i] = turnos[i+1]
                    turnos[i+1] = temp1
        
        turnos_aux = []
        for t in range(len(turnos)-1, 0, -1):
            turnos_aux.append(turnos[t])
        turnos_aux.append(turnos[0])
        turnos = []
        for t in turnos_aux:
            turnos.append(t)
        # ----------------------------------------------------------turnos asignados
        
        if(defensas == []):
            for d in turnos:
                defensas.append(0)
        for tu in turnos:
            print(tu.nombre)
            tu.efecto()
        for j in (turnos_aux):
#            print(cancel)
            if(j in cancel):
                cancel.remove(j)
                turnos.pop(turnos.index(j))
                continue
            elif(j not in turnos or "Indefenso" in j.condicion):
                continue
            print(f"Es turno de: {j.nombre}\n")
            if(j in e_presentes):# ----------------------------------------------------Turno enemigo
                p_presentes, e_presentes, defensas, turnos, cancel, hist = self.turno_enemigo(self, p_presentes, e_presentes, defensas, turnos, cancel, turnos_aux, j, hist)
            elif(j in personajes):# --------------------------------------------------------------------Turno personaje
                p_presentes, e_presentes, defensas, turnos, cancel, hist = self.turno_personaje(self, p_presentes, e_presentes, defensas, turnos, cancel, turnos_aux, j, hist)
            else:
                # turno asistente
                p_presentes, e_presentes, defensas, turnos, cancel, hist = self.turno_enemigo(self, p_presentes, e_presentes, defensas, turnos, cancel, turnos_aux, j, hist)
            if(p_presentes == []):
                return [False, p_presentes, e_presentes, defensas, turnos_aux, cancel]
            elif(e_presentes == []):
                print("Victoria!")
                if(estemen):
                    for ip in p_presentes:
                        ip.subir_nivel()
                for p in p_presentes: # Revivir a quien tenia SCP 427
                    if("Temporal" in p.condicion):
                        personajes_muertos.remove(p.dueño)
                        personajes.append(p.dueño)
                        p.dueño.asistentes.remove(p)
                        p.zona = "Vacio"
                p_presentes = []
                return [False, p_presentes, e_presentes, defensas, turnos_aux, cancel]
        turnos_aux = p_presentes + e_presentes
        return [True, p_presentes, e_presentes, defensas, turnos_aux, cancel]
    
    
    def turno_enemigo(self, p_presentes, e_presentes, defensas, turnos, cancel, turnos_aux, enemigo, hist, jaula = None):
        if(enemigo in cancel):
            cancel.remove(enemigo)
            turnos.pop(turnos.index(enemigo))
            return p_presentes, e_presentes, defensas, turnos, cancel, hist
        elif(enemigo not in turnos or "Indefenso" in enemigo.condicion):
            return p_presentes, e_presentes, defensas, turnos, cancel, hist
        indio_e = turnos.index(enemigo)
        indio_e_aux = turnos_aux.index(enemigo)
        
        if("Confundido" in enemigo.condicion):
            accion = enemigo.decidir(turnos_aux, hist, turnos_aux, defensas)
        elif(issubclass(enemigo, Enemigo)):
            accion = enemigo.decidir(e_presentes, hist, turnos_aux, defensas)
        else:
            accion = enemigo.decidir(p_presentes, hist, turnos_aux, defensas)
        
        if("Atacando normal" in enemigo.condicion or "Atacando especial" in enemigo.condicion):
            for a in accion[0]:
                print(f"{enemigo.nombre} se dispone a atacar a {a.nombre}!!")
                indio_aux = turnos_aux.index(a)
                if(a in turnos and a in personajes):
                    indio = turnos.index(a)
                    salida = True
                    while salida:
                        print(f"¿{a.nombre}, que deseas hacer?") # Respuesta personaje                        
                        if(a.nombre == "Sebas" and a.arbol["B1"][0] == 1):
                            print("0: Anticipacion")
                        
                        decision = int(input("1: Defenderte\n2: Usar objeto\n3: No hacer nada\n"))
                        
                        if(decision == 0):
                            if(not a.activar_habilidad("anticipacion")[0]):
                                continue
                            else:
                                print("Daño posible = "+ str(accion[1]))
                                decision = input("¿Vas a querer atacar?(S/N)")
                                if(decision == "S"):
                                    a.atacar(enemigo)
                                salida = False
                        elif(decision == 1):
                            defensas[indio_aux] = a.defender()
                            turnos.pop(indio)
                            break
                        elif(decision == 2):
                            #-----------------------------------------Usar objeto
                            objetos_permitidos = []
                            for i in range(0, len(a.inventario)):
                                if(a.inventario[i].estadistica != "F" or "Pocion" in a.inventario_nombres[i] or a.inventario_nombres[i] not in multiples):
                                    objetos_permitidos.append(a.inventario[i].nombre)
                            
                            print(f"¿Que quieres usar?")
                            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                            i=0
                            for llave in a.cartera_obj:
                                if(llave in objetos_permitidos):
                                    print(f"{i+1}, \t{llave:.24s}: \t\t{a.cartera_obj[llave]} | \t\t{a.inventario[a.inventario_nombres.index(llave)].estadistica} | \t{a.inventario[a.inventario_nombres.index(llave)].boosteo}")
                                    i+=1
                            
                            obj = int(input())-1
                            for llave in a.cartera_obj:
                                if(llave in objetos_permitidos):
                                    if(obj == 0):
                                        break
                                    obj -= 1
                            objeto = a.inventario[a.inventario_nombres.index(llave)]
                            #----------------------------------------Objeto seleccionado
                            print("¿Con quien usaras el objeto?")
                            if(objeto.estadistica == "Revivir"):
                                print(f"0: Regresar")
                                for inv in range (0, len(a.inventario_nombres)):
                                    if("Cadaver" in a.inventario_nombres[inv]):
                                        print(f"{inv+1}: {a.inventario_nombres[inv]}")
                                q = int(input())-1
                                if(q == -1):
                                    continue
                                else:
                                    uso = a.usar_obj(a.inventario_nombres[q], objeto)
                                    salida = not uso
                            else:
                                for p in range(0, len(turnos_aux)):
                                    print(f"{p+1}: {turnos_aux[p].nombre}")
                                print(f"{len(turnos_aux)+1}: Regresar")
                                q = int(input())-1
                                if(q == len(turnos_aux)):
                                    continue
                                elif(a.nombre == turnos_aux[q].nombre):
                                    uso = a.usar_obj(a, objeto)
                                    if(type(uso) == bool):
                                        salida = not uso
                                    elif(list(uso.keys())[0] == "Escudo"):
                                        defensas[q] = list(uso.values())[0]
                                        break
                                else:
                                    uso = a.usar_obj(turnos_aux[q], objeto)
                                    if(type(uso) != bool):
                                        if(list(uso.keys())[0] == "Escudo"):
                                            defensas[q] += list(uso.values())[0]
                                        else:
                                            if(type(accion)!=int):
                                                accion[1] = 0
                                            defensas[indio_e_aux] = uso
                                            print(turnos[indio_e].nombre+" ha sido confundido!")
                                            turnos.pop(indio)
                                        break
                                    else:
                                        salida = not uso
                            if(not salida):
                                turnos.pop(indio)
                        elif(decision == 3):
                            break
                daño = defensas[indio_aux] - accion[1]
                if(enemigo.salud <= 0):
                    daño = 0
                if(daño < 0):
                    print(f"{a.nombre} recibio {abs(daño)} de daño!\n")
                    defensas[indio_aux] = 0
                    ded = a.cambiar_hp(daño, enemigo)
                    if(ded):
                        if(a in turnos):
                            turnos.pop(indio)
                        if(a in personajes_muertos):
                            p_presentes.remove(a)
#                                    print(f"{a.nombre} ha muerto...")
#                                    print(p_presentes)
#                                    print("\n\n")
#                            defensas.pop(indio_aux)
#                            turnos_aux.pop(indio_aux)
                else:
                    defensas[indio_aux] = daño
                    print(f"{a.nombre} bloqueo el ataque")
        elif("Defendiendose" in enemigo.condicion):
            print(f"{enemigo.nombre} se defiende... {accion}")
            defensas[indio_e_aux] = accion
        elif("Huyendo" in enemigo.condicion):
            e_presentes.remove(enemigo)
        elif("Atacando con carisma" in enemigo.condicion):
                                # objetivo, defensa del objetivo
            self.pelea_carisma(accion[0], defensas[turnos_aux.index(accion[0])], daño_enemigo = accion[1], enemigo = enemigo)
        turnos.pop(indio_e)
        return p_presentes, e_presentes, defensas, turnos, cancel, hist
    
    
    def turno_personaje(self, p_presentes, e_presentes, defensas, turnos, cancel, turnos_aux, personaje, hist, jaula = None):
        if(personaje in cancel):
            cancel.remove(personaje)
            turnos.pop(turnos.index(personaje))
            return p_presentes, e_presentes, defensas, turnos, cancel, hist
        elif(personaje not in turnos or "Indefenso" in personaje.condicion):
            return p_presentes, e_presentes, defensas, turnos, cancel, hist
        
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
        indio=turnos_aux.index(personaje)
        while salida:
            print(f"¿{personaje.nombre}, que deseas hacer?")
            decision = int(input("0: Atacar\n1: Influenciar\n2: Defenderte\n3: Usar objeto\n4: Tirar objeto \n5: Huir\n6: Curarse\n" + captura + habilidad))
            if(decision == 0):
#                        print(e_presentes)
                res = personaje.atacar(e_presentes)
#                        print(e_presentes)
                indio_e_aux=turnos_aux.index(res[0])
                eleccion = input(f"¿Deseas atacar a {res[0].nombre}? (S/N)\n")
                if(eleccion == 'S'):
                    if("Confundido" in personaje.condicion):
                        res[0] = turnos_aux[Juego.dados(1, len(turnos_aux))[0]-1]
                    print(f"{personaje.nombre} ataca a {res[0].nombre} con {res[2].nombre} con una increible fuerza de {res[1]}")
                    salida = False
                elif(eleccion == 'N'):
                    continue
                else:
                    print("Tas tonto shavo")
                    continue
                hist.append([personaje, res[0]])
                daño = defensas[indio_e_aux] - res[1]
#                        print(defensas)
                if(daño < 0):
                    defensas[indio_e_aux] = 0
                    ded = res[0].cambiar_hp(daño, personaje)
                    print(f"{res[0].nombre} recibio {daño} de daño!")
#                            print(e_presentes)
                    if(ded):
                        if(res[2] in armash_shidas):
                            if(res[0].categoria == "Humano"):
                                anadir_obj_manual("Carne humana", personaje)
                        if(res[0] in turnos):
                            indio_e=turnos.index(res[0])
                            turnos.pop(indio_e)
#                                print(e_presentes)
#                                print(res[0])
#                                e_presentes.remove(res[0])
#                                defensas.pop(indio_e_aux)
#                                turnos_aux.pop(indio_e_aux)
                    elif(res[2].nombre == "Taxer" and res[0].nombre not in notaxeables):
                        print(res[0].nombre +" ha sido paralizado!")
                        if(res[0] not in turnos):
                            cancel.append(res[0])
                            print(cancel)
                else:
                    defensas[indio_e_aux] = daño
                    print(f"{res[0].nombre} bloqueo el ataque")
            elif(decision == 1):
                self.pelea_carisma(personaje, defensas[turnos_aux.index(personaje)], e_presentes = e_presentes)
            elif(decision == 2):
                defensas[indio] = personaje.defender()
                salida = False
            elif(decision == 3):
                #-----------------------------------------Usar objeto
                objetos_permitidos = []
                for i in range(0, len(personaje.inventario)):
                    if(personaje.inventario[i].estadistica != "F" or "Pocion" in personaje.inventario_nombres[i]):
                        objetos_permitidos.append(personaje.inventario[i].nombre)
                
                print(f"¿Que quieres usar?")
                print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                i=0
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        print(f"{i+1}, \t{llave:.24s}: \t\t{personaje.cartera_obj[llave]} | \t\t{personaje.inventario[personaje.inventario_nombres.index(llave)].estadistica} | \t{personaje.inventario[personaje.inventario_nombres.index(llave)].boosteo}")
                        i+=1
                
                obj = int(input())-1
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        if(obj == 0):
                            break
                        obj -= 1
                objeto = personaje.inventario[personaje.inventario_nombres.index(llave)]
                if("Confundido" in personaje.condicion):
                    objeto = personaje.inventario[Juego.dados(1, len(personaje.inventario))[0]-1]
                #----------------------------------------Objeto seleccionado
                muerto = True
                if(objeto.nombre in multiples):
                    q = -1
                else:
                    print("¿Con quien usaras el objeto?")
                    if(objeto.estadistica == "Revivir"):
                        print(f"0: Regresar")
                        
                        #personaje estaba en accion[0]
                        for inv in range (0, len(personaje.inventario_nombres)):
                            if("Cadaver" in personaje.inventario_nombres[inv]):
                                print(f"{inv+1}: {personaje.inventario_nombres[inv]}")
                        q = int(input())-1
                        if(q == -1):
                            continue
                        else:
                            uso = personaje.usar_obj(personaje.inventario_nombres[q], objeto)
                            salida = not uso
                            muerto = False
                    else:
                        for p in range(0, len(turnos_aux)):
                            if(turnos_aux[p].salud > 0):
                                print(f"{p+1}: {turnos_aux[p].nombre}")
                        print(f"{len(turnos_aux)+1}: Regresar")
                        q = int(input())-1
                    
                if(muerto): # Uso normal de objeto, callate
                    if("Confundido" in personaje.condicion):
                        q = turnos_aux[Juego.dados(1, len(turnos_aux))[0]-1]
                    if(q == len(turnos_aux)): # Regresar
                        continue
                    elif(q == -1): # Objetivo multiple
                        personaje.usar_obj(turnos_aux, objeto)
                    elif(personaje.nombre == turnos_aux[q].nombre):
                        uso = personaje.usar_obj(personaje, objeto)
                        if(type(uso) == bool):
                            salida = not uso
                        elif(list(uso.keys())[0] == "Escudo"):
                            defensas[q] = list(uso.values())[0]
                            break
                    else:
                        uso = personaje.usar_obj(turnos_aux[q], objeto)
                        if(type(uso) != bool):
                            if(list(uso.keys())[0] == "Escudo"):
                                defensas[q] += list(uso.values())[0]
                            else:
                                defensas[q] = uso[objeto.nombre]
                                salida = False
                                print(turnos_aux[q].nombre+" ha sido confundido!")
                                if(turnos_aux[q] not in turnos):
                                    cancel.append(turnos_aux[q])
#                                            print(cancel)
                                else:
                                    salto = turnos.index(turnos_aux[q])
                                    turnos.pop(salto)
                        else:
                            salida = not uso
                            
            elif(decision == 4):
                salida = not personaje.tirar_objeto()
            elif(decision == 5):
                h = personaje.huir(e_presentes)
                print(f"{personaje.nombre} esta intentando escapar...", end = " ")
                if("Confundido" in personaje.condicion):
                    print(f"...{personaje.nombre} esta tan confundido que se tropezo con una rama...")
                    h = False
                if(h): # va a escapar
                    if("Domando" in personaje.condicion):
                        if(enemigo.velocidad > personaje.velocidad and enemigo.carisma > personaje.carisma):
                            z = personaje.ubicacion.zonas().index(personaje.zona)
                            personaje.ubicacion[z].jaulas[jaula.nombre].pop(jaula) #salirse de jaula
                            agresividad_max = ((self.oso_marino.carisma + self.oso_marino.fuerza)-(self.oso_marino.inteligencia + self.oso_marino.resistencia))+4
                            pelear = (enemigo.salud/enemigo.salud_max) * (enemigo.agresividad/agresividad_max) * 100
                            if(enemigo.nombre in domables and Juego.dados(1, 100)[0] <= pelear):
                                if(personaje in turnos):
                                    indio = turnos.index(personaje)
                                    turnos.pop(indio)
                                return p_presentes, e_presentes, defensas, turnos, cancel, hist
                            else:
                                enemigo.huir([enemigo]) #[enemigo] = para que siempre escape
                                e_presentes.remove(enemigo)
                                turnos.pop(turnos.index(enemigo))
                    print("y lo ha logrado!!")
#                            defensas.pop(indio)
                    p_presentes.remove(personaje)
                    turnos.pop(turnos.index(personaje))
                    if(personaje.inteligencia >= (13 + 5 *(personaje.nivel))* 3/4):
                        personaje.moverse()
                    elif(personaje.inteligencia >= (13 + 5 *(personaje.nivel))* 1/2):
                        personaje.moverse(personaje.hogar)
                    else:
                        lugar = personaje.mapa[personaje.zona][Juego.dados(1, len(personaje.mapa[personaje.zona]))[0]-1]
                        personaje.moverse(lugar)
                else:
                    print("...y fracaso!! Como siempre")
                salida = False
            elif(decision == 6):
                salida = not personaje.energetizar()
            elif(decision == 7 and "Domando" in personaje.condicion):
                agresividad_max = ((self.oso_marino.carisma + self.oso_marino.fuerza)-(self.oso_marino.inteligencia + self.oso_marino.resistencia))+4
                capturar = (enemigo.salud/enemigo.salud_max) * (enemigo.agresividad/agresividad_max) * 100
                if(enemigo.nombre in domables and Juego.dados(1, 100)[0] <= capturar):
                    personaje.reclutar(enemigo)
            elif(decision == 7 and habilidad[0] == "7" or decision == 8 and habilidad[0] == "8"):
                resultado = self.activar_habilidad("Turno personaje", cancel)
                if(not resultado[1]):
                    salida = False
                else:
                    hist.append([personaje, resultado[1][0]])
                    daño = defensas[indio_e_aux] - resultado[1][1]
                    if(daño < 0):
                        defensas[indio_e_aux] = 0
                        ded = resultado[1][0].cambiar_hp(daño, personaje)
                        print(f"{resultado[1][0].nombre} recibio {daño} de daño!")
                        if(ded):
                            if(resultado[1][2] in armash_shidas):
                                if(resultado[1][0].categoria == "Humano"):
                                    anadir_obj_manual("Carne humana", personaje)
                            if(resultado[1][0] in turnos):
                                indio_e=turnos.index(resultado[1][0])
                                turnos.pop(indio_e)
                        elif(resultado[1][2].nombre == "Taxer" and resultado[1][0].nombre not in notaxeables):
                            print(resultado[1][0].nombre +" ha sido paralizado!")
                            if(resultado[1][0] not in turnos):
                                cancel.append(resultado[1][0])
                                print(cancel)
                    else:
                        defensas[indio_e_aux] = daño
                        print(f"{resultado[1][0].nombre} bloqueo el ataque")
            if(personaje in turnos):
                indio = turnos.index(personaje)
                turnos.pop(indio)
        return p_presentes, e_presentes, defensas, turnos, cancel, hist
    
    
    def pelea_carisma(self, personaje, defensa, e_presentes = None, daño_enemigo = None, enemigo = None):
        if(enemigo == None):
            print(f"\n¿{personaje.nombre}, quién será tu victima?")
            print("INDICE \t NOMBRE \t SALUD")
            for i in range (0, len(e_presentes)):
                print(f"{i+1}: {e_presentes[i].nombre}\t{e_presentes[i].salud}")
            enemigo = e_presentes[int(input())-1]
            daño_enemigo = enemigo.ataque_carisma(objetivo = personaje)[1]
        daño_personaje = personaje.atacar_carisma(enemigo)[1]
        if("Indefenso" not in personaje.condicion):
            if(daño_personaje < daño_enemigo):
                print(f"{personaje.nombre} ha perdido el duelo de carisma")
                personaje.carisma -= daño_enemigo-daño_personaje
                if(personaje.carisma <= 0):
                    personaje.condicion.update({"Indefenso":2})
            elif(daño_personaje > daño_enemigo):
                print(f"{enemigo.nombre} ha perdido el duelo de carisma")
                enemigo.carisma -= daño_personaje-daño_enemigo
                if(enemigo.carisma <= 0):
                    enemigo.condicion.update({"Indefenso":2})
            else:
                print("El duelo fue un empate!!")
        else:
            print(f"{personaje.nombre} esta indefenso, {enemigo.nombre} ataca!!")
            daño = defensa - daño_enemigo
            if(daño < 0):
                print(f"{personaje.nombre} recibe {daño_enemigo} de daño")
                personaje.cambiar_hp(-daño_enemigo)
            else:
                print(f"El ataque de {enemigo.nombre} ha sido bloqueado!")
        return True
    
    
    def domar(self, personaje, enemigo, jaula, defensas, cancel, hist):
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
            personaje, enemigo, defensas, turnos, cancel, hist = self.turno_personaje([personaje], [enemigo], defensas, turnos, cancel, turnos, personaje, hist, jaula = jaula)
            #Turno enemigo
            personaje, enemigo, defensas, turnos, cancel, hist = self.turno_enemigo(personaje, enemigo, defensas, turnos, cancel, turnos, enemigo[0], hist, jaula = jaula)
        else:
            #Turno enemigo
            personaje, enemigo, defensas, turnos, cancel, hist = self.turno_enemigo([personaje], [enemigo], defensas, turnos, cancel, turnos, enemigo, hist, jaula = jaula)
            #Turno personaje
            personaje, enemigo, defensas, turnos, cancel, hist = self.turno_personaje(personaje, enemigo, defensas, turnos, cancel, turnos, personaje[0], hist, jaula = jaula)
            
        return [True, personaje[0], enemigo[0], jaula, defensas, cancel, hist]
    
    def casino(self, personaje, premio = 0):
        print(f"----------------------- {personaje.nombre}, bienvenido al casino!! ---------------- Premio actual: {premio}")
        print("¿Que quieres hacer?")
        inp = int(input("1: Jugar una ronda\n2: Ver premios\n3:Salir\n"))
        if(premio <= -500):
            inp = 3
        if(inp == 1):
            apuesta = int(input(f"\n----------------------- A jugar! ---------------------------- Premio actual: {premio}"+
                                "\n¿Cuánto deseas apostar?\n"))
            
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
            print(f"\n----------------------- Premios ----------------------------- Premio actual: {premio}"+
                  "\n 481 - 625 puntos: apuesta x 10 (PREMIO MAXIMO!!!!!!!)"+
                  "\n 336 - 480 puntos: apuesta x 8"+
                  "\n 191 - 335 puntos: apuesta x 6"+
                  "\n 46 - 190  puntos: apuesta x 4"+
                  "\n 22 - 45   puntos: apuesta x 2"+
                  "\n 1 - 21    puntos: apuesta x 1"+
                  "\n 0         puntos: 0\n")
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
                            if personaje.inventario[i].precio > personaje.inventario[i+1].precio:
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
                        print(f"Me las vas a pagar con tu vida shavo!\n...{personaje.nombre} ha recibido una paliza... -{personaje.salud/4}")
                        personaje.cambiar_hp(-(personaje.salud/4))
                else:
                    personaje.anadir_obj(-premio)
            return True
        self.casino(personaje, premio)
    
    def escalera(self, p, nivel = 0, niv_maquina = 0, niv_nina = 0, niv_monstruo = 0):
        #DEBUG
#    print("-------------------------------------------------------Metodo escalera")
        print(f"{p.nombre}, estas en el nivel {nivel}")
        if(nivel == 0):
            niv_maquina = Juego.dados(1, 10)[0]
            niv_nina = Juego.dados(1, 20)[0]
            niv_monstruo = Juego.dados(1, 25)[0]
        sel = input(f"{p.nombre}, ¿quieres bajar? (S/N)\n")
        if(sel == 'S'):
            nivel += 1
        elif(sel == 'N'):
            print("Has vuelto al inicio de las escaleras")
            nivel = 0
        else:
            print("Tas tonto shavo")
        if(nivel == niv_monstruo):
            print("Has encontrado al monstruo!! :O")
            prob = (nivel*100)/25
            pr = Juego.dados(1, 100)[0]
            if(pr <= prob):
                p.cambiar_hp(-2000)
            else:
                print("Lograste escapar con éxito! Has vuelto al inicio de las escaleras")
                nivel = 0
        if(nivel == niv_nina):
            s = input("Has encontrado una sala misteriosa... ¿Quieres entrar? (S/N)\n")
            if(s == 'S'):
                print("Dialogo intenso...")
                obj = Objeto("Pelo", "--", "--", 0, 1, 10000, 0)
                zonas = p.ubicacion.zonas()
                i = zonas.index(p.zona)
                p.ubicacion.objetos()[i].append(obj.nombre)
                p.ubicacion.objetos_activos()[i].append(obj)
                p.ubicacion.cantidades()[i].append(10000)
                p.anadir_obj(obj)
        if(nivel == niv_maquina):
            s = input("Has encontrado la sala de la maquina!! ¿Quieres entrar? (S/N)\n")
            if(s == 'S'):
                p.moverse(edificio, "Maquina")
                p.usar_maquina()
        return [p, nivel, niv_maquina, niv_nina, niv_monstruo]
    
    
    def generar_jefes(self, lugar, zona:str):
        print("-------------------------------------------------------Metodo jefes")
        z = lugar.zonas().index(zona)
        jeff = []
        lugar_original = lugares_o_originales[lugares_o.index(lugar)]
        from Enemigos import Enemigo
        
        print(lugar.enemigos()[z])
        
        for e in lugar.enemigos()[z]:
            if(e in jefes_no_jefes):
                jeff.append(e)
        contador = -1
#        print(jefes_no_jefes)
#        print(jeff)
        for h in range (0, len(Dfnombres_e)):
            if(abs(contador) > len(jeff)):
                break
            if (Dfnombres_e.iloc[h,0] in jeff) and (lugar_original.cantidades()[z][contador] > 0) and (not self.repetido(lugar, z, Dfnombres_e.iloc[h,0])):
                nombre = Dfnombres_e.iloc[h,0]
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
                
                e = Enemigo(salud, fuerza, resistencia, hostilidad, inteligencia, sabiduria, nombre, {"Saludable": 1}, dropeos, categoria, rango, cantidad, zona)
                lugar.enemigos_activos()[z].append(e)
                contador -= 1
                e.stats()
        
    def generar_enemigos_zona(self, lugar:Lugar, zona:str):
        #DEBUG
        
        self.generar_jefes(lugar, zona)
        indio = lugar.zonas().index(zona)
        enemigos,cantidades = shuffleproplusultra(lugar.enemigos()[indio],lugar.cantidades_enemigos()[indio])
        lugar.enemigos_zona_s(enemigos, zona)
        lugar.cantidades_enemigos_zona_s(cantidades, zona)
        from Enemigos import Enemigo
        
        enemigos_aux = []
        cantidades_aux = []
        contador3 = 0
        for e in range(0, len(enemigos)):
            if(enemigos[e] not in jefes.keys()):
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
        contador = minimo + Juego.dados(1, maximo)[0]
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
            enemigos_a.append(enemigos[Juego.dados(1, len(enemigos))[0]-1])
#                print("contador: " + str(contador))
#                print("contador 2: " + str(contador2))
        
        for en in enemigos_a:
            if(en not in jefes_no_jefes):
                enemigos_a_aux.append(en)
            else:
                contador -= 1
        enemigos_a = enemigos_a_aux
        print(enemigos_a)
        print(contador)
        while(contador > 0):
            for j in range(0, len(enemigos_a)):
    #            j+=contador2
                for h in range (0, len(Dfnombres_e)):
                    if(contador<=0):
                        break
                    if(Dfnombres_e.iloc[h,0] == enemigos_a[j])  and (cantidades[j] > 0.0) and (Dfnombres_e.iloc[h,0] not in jefes.keys()):
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
                        
                        e = Enemigo(salud, fuerza, resistencia, hostilidad, inteligencia, sabiduria, enemigos_a[j], {"Saludable": 1}, dropeos, categoria, rango, cantidad, zona)
                        lugar.enemigos_activos()[indio].append(e)
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
#        print("------------------------------------------------Metodo generar objetos")
        fragmento = Objeto("Fragmento de libro de secretos", 0, 'Habilidad', 0, 1, 1, 300)
        if(lugar == pueblo) and (pueblo_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == bosque) and (bosque_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == normancueva) and (normancueva_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == fondo_del_mar) and (fondo_del_mar_original.cantidades()[0][0] > 0):
            lugar.objetos_activos()[0].append(fragmento)
            
        indio = lugar.zonas().index(zona)
        objetos,cantidades = shuffleproplusultra(lugar.objetos()[indio],lugar.cantidades()[indio])
        lugar.objetos_zona_s(objetos, zona)
        lugar.cantidades_objetos_zona_s(cantidades, zona)
        
#        print(lugar.objetos())
#        print(objetos)
        if(len(objetos) == 0):
            contador = 0
        elif(len(objetos) == 1):
            contador = 1
        else:
            contador = Juego.dados(1, len(objetos))[0]//2
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
                if(gm.Dfnombres_o.iloc[h,0] == objetos[j])  and (cantidades[j] > 0.0) and (gm.Dfnombres_o.iloc[h,0] != 'Fragmento de Libro de Secretos'):
                    nombre = objetos[j]
                    o = self.tranformar_objeto(nombre, cantidades[j])
                    lugar.objetos_activos()[indio].append(o)
#                    o.stats()
                    contador -= 1
#                    contador2 += 1
                    break
        return ""
    
    def generar_objetos(self, lugar):
        #DEBUG
        print("------------------------------------------------Metodo generar objetos")
        fragmento = Objeto("Fragmento de libro de secretos", 0, 'Habilidad', 0, 1, 1, 300)
        if(lugar == pueblo) and (pueblo_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == bosque) and (bosque_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == normancueva) and (normancueva_original.cantidades()[1][0] > 0):
            lugar.objetos_activos()[1].append(fragmento)
        elif(lugar == fondo_del_mar) and (fondo_del_mar_original.cantidades()[0][0] > 0):
            lugar.objetos_activos()[0].append(fragmento)
        objetos,cantidades = shufflepro(lugar.objetos(),lugar.cantidades())
        lugar.objetos_s(objetos)
        lugar.cantidades_s(cantidades)
#        print(lugar.objetos())
#        print(objetos)
        for i in range (0, len(lugar.zonas())):
            contador = len(lugar.objetos()[i])//2
#            contador2 = 0
            if(contador<1):
                contador+=1
            print("--------------------------------------------------------------")
            print("\t\t"+lugar.zonas()[i])
            print("--------------------------------------------------------------")
            for j in range(0, len(lugar.objetos()[i])):
#                j+=contador2
                for h in range (0, len(gm.Dfnombres_o)):
                        if(contador<=0):
                            break
                        if (gm.Dfnombres_o.iloc[h,0] == lugar.objetos()[i][j]) and (lugar.cantidades()[i][j] > 0.0) and (lugar.objetos()[i][j] != 'Fragmento de Libro de Secretos'):
                                nombre = lugar.objetos()[i][j]
                                o = self.tranformar_objeto(nombre, lugar.cantidades()[i][j])
                                lugar.objetos_activos()[i].append(o)
                                o.stats()
                                contador -= 1
#                                contador2 += 1
                                break
        return ""

    def tranformar_objeto(self, nombre: str, cantidad_manual = None):
        #DEBUG
#        print("-----------------------------------------Metodo transformar objeto")
        for h in range (0, len(gm.Dfnombres_o)):
            if (gm.Dfnombres_o.iloc[h,0] == nombre):
                basura = False
                boosteo = (gm.Data_o2.loc[nombre, "Boosteo"])
                if(type(boosteo) == pd.core.series.Series):
                    basura = True
                    boosteo = int(boosteo.iloc[0])
                estadistica = (gm.Data_o2.loc[nombre, "Estadistica"])
                peso = (gm.Data_o2.loc[nombre, "Espacio"])
                usos = (gm.Data_o2.loc[nombre, "Usos"])
                cantidad = (gm.Data_o2.loc[nombre, "Cantidad"])
                precio = (gm.Data_o2.loc[nombre, "Precio"])
                if(basura):
                    estadistica = estadistica.iloc[0]
                    peso = float(peso.iloc[0])
                    usos = int(usos.iloc[0])   
                    cantidad = int(cantidad.iloc[0])
                    precio = int(precio.iloc[0])
                if(cantidad_manual != None):
                    cantidad = cantidad_manual
                if(nombre == "Nota de consejo"):
                    boosteo = consejos[Juego.dados(1, len(consejos))[0]-1]
                objeto = Objeto(nombre, boosteo, estadistica, peso, usos, cantidad, precio)
#                objeto.stats()
                break
#        print("------------------------------------------------------------------")
        return objeto

    def maquina(self, nombre: str, usuario, mult = 1):
        #DEBUG
        print("--------------------------------------------------------Metodo maquina")
        if(not self.funcional):
            return False
        
        indio = usuario.inventario_nombres.index(nombre)
        usuario.peso -= usuario.inventario[indio].peso
        zonas = usuario.ubicacion.zonas()
        i = zonas.index(usuario.zona)
        usuario.inventario_nombres.pop(indio)
        usuario.inventario.pop(indio)
        
        tirada = Juego.dados(1, 4)[0]
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
            nombre = revisar_string(nombre)
        
        if("Cadaver " in nombre):
            nombre = "Cadaver de " + usuario.nombre
            
        if(nombre[0].isdigit() and nombre[2:] != "Dinero"):
            for i in range(0, int(nombre[0])):
                anadir_obj_manual(nombre[2:], usuario)
            return True
        
        if(nombre == "3 Dinero"):
            usuario.anadir_obj(3)
            return True
        
#        o = self.tranformar_objeto(nombre, 9999)
#        edificio.objetos_activos()[1].append(o)
#        edificio.objetos()[1].append(o.nombre)
#        edificio.cantidades()[1].append(o.cantidad)
        anadir_obj_manual(nombre, usuario, 9999)
#        print("------------------------------------------------------------------")
        
    