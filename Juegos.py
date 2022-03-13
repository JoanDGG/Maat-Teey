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
    
    def casino(self, personaje, premio = 0):
        print(f"-------- {personaje.nombre}, bienvenido al casino!! -------- "
              + f"Premio actual: {premio}")
        print("¿Que quieres hacer?")
        seleccion =int(input("1: Jugar una ronda\n2: Ver premios\n3: Salir\n"))
        if(premio <= -500):
            seleccion = 3
        if(seleccion == 1):
            apuesta = int(input("\n----- A jugar! ----- "
                                + f"Premio actual: {premio}"
                                + "\n¿Cuánto deseas apostar?"))
            print(f" Saldo: {personaje.cartera}\n")
            premio -= apuesta    
            
            lista1 = [1, 2, 3, 4, 5]
            lista2 = [1, 2, 3, 4, 5]
            lista3 = [1, 2, 3, 4, 5]
            lista4 = [1, 2, 3, 4, 5]
            lista5 = [1, 2, 3, 4, 5]
            listas = [lista1, lista2, lista3, lista4, lista5]
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            columna = 1
            for indice in range(0, 3):
                print("\t", end = "")
                for fila in range(0, 5):
                    print(listas[fila][columna], end="\t")
                    if(columna >= 4):
                        break
                columna += 1
                print()
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            print("\nA jugar!\n")
            
            lista_final = []
            for lista in listas:
                np.random.shuffle(lista)
                lista_final.append(lista[2])
            
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            columna = 1
            for indice in range(0, 3):
                print("\t", end = "")
                for fila in range(0, 5):
                    print(listas[fila][columna], end="\t")
                    if(columna >= 4):
                        break
                columna += 1
                print()
            print(" \t_____\t_____\t_____\t_____\t_____\n")
            
            premio_base = sum(lista_final)
            mult = []
            for indice in range(1, 6):
                mult.append(lista_final.count(indice))
            mult_final = 0
            if(max(mult) >= 3):
                mult_final = mult.index(max(mult))+1
            premio_actual = premio_base * mult_final * max(mult)
            print(f"Ganaste {premio_actual} puntos!!")
            
            # calculo automatico de dineros
            rangos = [0, 1, 22, 46, 190, 335, 480]
            multi = [0, 1, 2, 4, 6, 8, 10]
            bonificacion = 0
            for indice in range(0, len(rangos)):
                if(premio_actual > rangos[indice]):
                    bonificacion = multi[indice]
                else:
                    break
            print(f"Obtuviste {bonificacion * apuesta} dineros!!\n")
            if(bonificacion != 0):
                premio += bonificacion * apuesta + apuesta
            else:
                premio += bonificacion * apuesta
        elif(seleccion == 2):
            print(f"\n----- Premios ----- Premio actual: {premio}"
                  + "\n 481 - 625 puntos: apuesta x 10 (PREMIO MAXIMO!!!!!!!)"
                  + "\n 336 - 480 puntos: apuesta x 8"
                  + "\n 191 - 335 puntos: apuesta x 6"
                  + "\n 46 - 190  puntos: apuesta x 4"
                  + "\n 22 - 45   puntos: apuesta x 2"
                  + "\n 1 - 21    puntos: apuesta x 1"
                  + "\n 0         puntos: 0\n")
        elif(seleccion == 3):
            personaje.condicion.pop("Apostando")
            presupuesto = personaje.cartera
            if(premio >= 0):
                personaje.anadir_obj(premio)
            else:
                deuda = presupuesto + premio
                if(deuda < 0):
                    personaje.anadir_obj(-presupuesto)
                    for inventario in range(len(personaje.inventario)-1, 0,-1):
                        for indice in range(inventario):
                            if (personaje.inventario[indice].precio 
                                > personaje.inventario[indice + 1].precio):
                                temp = personaje.inventario[indice]
                                personaje.inventario[
                                indice] = personaje.inventario[indice + 1]
                                personaje.inventario[indice + 1] = temp
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

        personaje.condicion.update({"Apostando": premio})
        
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
        empieza_personaje = (personaje.velocidad >= enemigo.velocidad)
        turnos = [personaje, enemigo]
        for individuo in turnos:
            individuo.efecto()
        if(empieza_personaje):     
            #Turno personaje
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_personaje(
                                      [personaje], [enemigo], defensas, turnos, 
                                      omitidos, turnos, personaje, historial, 
                                      jaula = jaula)
            #Turno enemigo
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_enemigo(
                                       personaje, enemigo, defensas, turnos, 
                                       omitidos, turnos, enemigo[0], historial, 
                                       jaula = jaula)
        else:
            #Turno enemigo
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_enemigo(
                                      [personaje], [enemigo], defensas, turnos, 
                                      omitidos, turnos, enemigo, historial, 
                                      jaula = jaula)
            #Turno personaje
            (personaje, enemigo, 
             defensas, turnos, omitidos, historial) = self.turno_personaje(
                                     personaje, enemigo, defensas, turnos, 
                                     omitidos, turnos, personaje[0], historial, 
                                     jaula = jaula)
            
        return[True, personaje[0], enemigo[0], jaula, 
               defensas, omitidos, historial]
        

    def escalera(self, personaje, nivel = 0, niv_maquina = 0, niv_nina = 0, 
                                                             niv_monstruo = 0):
        #DEBUG
#        print("----------------------------------------------Metodo escalera")
        print(f"{personaje.nombre}, estas en el nivel {nivel}")
        if(nivel == 0):
            niv_maquina = gm.dados(1, 10)
            niv_nina = gm.dados(1, 20)
            niv_monstruo = gm.dados(1, 25)
        seleccion = input(f"{personaje.nombre}, ¿quieres bajar? (S/N)\n")
        if(seleccion == "S"):
            nivel += 1
            print(f"Bajaste al nivel {nivel}...\n")
        elif(seleccion == "N"):
            if(nivel == 0):
                personaje.moverse(personaje.lugar_previo)
                personaje.condicion.pop("Escalando")
                return False
            else:
                print("Has vuelto al inicio de las escaleras")
                nivel = 0
        else:
            print("Tas tonto shavo")
        if(nivel == niv_monstruo):
            print("Has encontrado al monstruo!! :O")
            probabilidad = (nivel*100)/25
            tirada = gm.dados(1, 100)
            if(tirada <= probabilidad):
                print("Empiezas a oir un llanto en la distancia...")
                personaje.cambiar_hp(-2000)
            else:
                print("Lograste escapar con éxito! "
                      + "Has vuelto al inicio de las escaleras")
                nivel = 0
        if(nivel == niv_nina):
            seleccion = input("Has encontrado una sala misteriosa... "
                      + "¿Quieres entrar? (S/N)\n")
            if(seleccion == "S"):
                print("Dialogo intenso...")
                objeto = Objeto("Pelo", "--", "--", 0, 1, 10000, 0)
                zonas = personaje.ubicacion.zonas
                zona = zonas.index(personaje.zona)
                personaje.ubicacion.objetos[zona].append(objeto.nombre)
                personaje.ubicacion.objetos_activos[zona].append(objeto)
                personaje.ubicacion.cantidades_objetos[zona].append(10000)
                personaje.anadir_obj(objeto)
        if(nivel == niv_maquina):
            seleccion = input("Has encontrado la sala de la maquina!! "
                      + "¿Quieres entrar? (S/N)\n")
            if(seleccion == "S"):
                personaje.moverse("Maquina")
                personaje.usar_maquina()
        
        personaje.condicion.update({"Escalando": [nivel, niv_maquina, 
                                                  niv_nina, niv_monstruo]})

    def generar_enemigos_zona(self, lugar:Lugar, zona:str):
        #DEBUG
#        print("---------------------------------Metodo generar enemigos zona")
        self.generar_jefes(self, lugar, zona)
        indice = lugar.zonas.index(zona)
        enemigos, cantidades = gm.mezclar_listas(lugar.enemigos[indice],
                                          lugar.cantidades_enemigos[indice], 1)
        lugar.enemigos_zona_setter(enemigos, zona)
        lugar.cantidades_enemigos_zona_setter(cantidades, zona)
#        from Enemigos import Enemigo
        
        enemigos_aux = []
        cantidades_aux = []
        contador = 0
        for enemigo in range(0, len(enemigos)):
            if(enemigos[enemigo] not in gm.jefes.keys()):
                enemigos_aux.append(enemigos[enemigo])
                cantidades_aux.append(cantidades[enemigo])
            else:
                contador += 1
                
        enemigos, cantidades = enemigos_aux, cantidades_aux
        minimo_enemigos = 2
        if(zona == "Mercado"):
            minimo_enemigos *= 2
            
        maximo_enemigos = len(enemigos)//4
        if(maximo_enemigos == 0):
            maximo_enemigos = 1
        contador = minimo_enemigos + gm.dados(1, maximo_enemigos)
        if(sum(cantidades) < contador):
            contador = sum(cantidades) + contador
        contador -= contador
        
#        print("----------------------------------------------------------")
#        print("\t\t"+zona)
#        print("----------------------------------------------------------")
        enemigos_activos = []
        enemigos_activos_aux = []
        for indice_enemigo in range(0, len(enemigos)):
            enemigos_activos.append(enemigos[gm.dados(1, len(enemigos))-1])
#                print("contador: " + str(contador))
        
        for enemigo in enemigos_activos:
            if(enemigo not in gm.jefes_no_jefes):
                enemigos_activos_aux.append(enemigo)
            else:
                contador -= 1
        enemigos_activos = enemigos_activos_aux
#        print(enemigos_activos)
#        print(contador)
        while(contador > 0):
            for indice in range(0, len(enemigos_activos)):
                for indice_nombre in range (0, len(gm.Dfnombres_enemigos)):
                    if(contador<=0):
                        break
                    if((gm.Dfnombres_enemigos.iloc[
                            indice_nombre,0] == enemigos_activos[indice])  
                        and (cantidades[indice] > 0.0) 
                        and (gm.Dfnombres_enemigos.iloc[indice_nombre,0] 
                        not in gm.jefes.keys())):
                        multiples = False
                        salud = gm.Data_enemigos.iloc[indice_nombre,1]
                        if(type(salud) == pd.core.series.Series):
                                multiples = True
                                salud = salud.iloc[0]
                        fuerza = gm.Data_enemigos.iloc[indice_nombre,2]
                        resistencia = gm.Data_enemigos.iloc[indice_nombre,3]
                        hostilidad = gm.Data_enemigos.iloc[indice_nombre,4]
                        inteligencia = gm.Data_enemigos.iloc[indice_nombre,5]
                        sabiduria = gm.Data_enemigos.iloc[indice_nombre,6]
                        categoria = gm.Data_enemigos.iloc[indice_nombre,7]
                        rango = gm.Data_enemigos.iloc[indice_nombre,8]
                        dropeos = gm.Data_enemigos.iloc[indice_nombre,9]
                        cantidad = gm.Data_enemigos.iloc[indice_nombre,10]
                        if(multiples):
                                fuerza = fuerza.iloc[0]
                                resistencia = resistencia.iloc[0]
                                hostilidad = hostilidad.iloc[0]
                                inteligencia = inteligencia.iloc[0]
                                sabiduria = sabiduria.iloc[0]
                                categoria = categoria.iloc[0]
                                rango = rango.iloc[0]
                                dropeos = dropeos.iloc[0]
                                cantidad = cantidad.iloc[0]
                        
                        enemigo = Enemigo(salud, fuerza, resistencia, 
                                  hostilidad, inteligencia, sabiduria, 
                                  enemigos_activos[indice], {"Saludable": 1}, 
                                  dropeos, categoria, rango, cantidad, zona)
                        lugar.enemigos_activos[indice].append(enemigo)
                        if(enemigo.nombre == "Oso marino"):
                            gm.oso_marino = enemigo
#                            print("AAAAAAAAAAAAA")
#                        e.stats()
                        contador -= 1
                        break
    
    def generar_jefes(self, lugar, zona:str):
        #DEBUG
#        print("-----------------------------------------Metodo generar jefes")
        indice_zona = lugar.zonas.index(zona)
        jefes = []
        lugar_original = gm.lugares_o_originales[
                gm.objetos_lugares.index(lugar)]
#        from Enemigos import Enemigo
        
#        print(lugar.enemigos[indice_zona])
        
        for enemigo in lugar.enemigos[indice_zona]:
            if(enemigo in gm.jefes_no_jefes):
                jefes.append(enemigo)
        contador = -1
#        print(gm.jefes_no_jefes)
#        print(jefes)
        for indice_nombre in range (0, len(gm.Dfnombres_enemigos)):
            if(abs(contador) > len(jefes)):
                break
            if ((gm.Dfnombres_enemigos.iloc[indice_nombre,0] in jefes) 
                and (lugar_original.cantidades_objetos[indice_zona][contador] > 0) 
                and (not gm.repetido(lugar, indice_zona, 
                                gm.Dfnombres_enemigos.iloc[indice_nombre,0]))):
                nombre = gm.Dfnombres_enemigos.iloc[indice_nombre,0]
                multiples = False
                salud = gm.Data_enemigos.iloc[indice_nombre,1]
                if(type(salud) == pd.core.series.Series):
                        multiples = True
                        salud = salud.iloc[0]
                fuerza = gm.Data_enemigos.iloc[indice_nombre,2]
                resistencia = gm.Data_enemigos.iloc[indice_nombre,3]
                hostilidad = gm.Data_enemigos.iloc[indice_nombre,4]
                inteligencia = gm.Data_enemigos.iloc[indice_nombre,5]
                sabiduria = gm.Data_enemigos.iloc[indice_nombre,6]
                categoria = gm.Data_enemigos.iloc[indice_nombre,7]
                rango = gm.Data_enemigos.iloc[indice_nombre,8]
                dropeos = gm.Data_enemigos.iloc[indice_nombre,9]
                cantidad = gm.Data_enemigos.iloc[indice_nombre,10]
                if(multiples):
                        fuerza = fuerza.iloc[0]
                        resistencia = resistencia.iloc[0]
                        hostilidad = hostilidad.iloc[0]
                        inteligencia = inteligencia.iloc[0]
                        sabiduria = sabiduria.iloc[0]
                        categoria = categoria.iloc[0]
                        rango = rango.iloc[0]
                        dropeos = dropeos.iloc[0]
                        cantidad = cantidad.iloc[0]
                
                enemigo = Enemigo(salud, fuerza, resistencia, hostilidad, 
                                  inteligencia, sabiduria, nombre, 
                                  {"Saludable": 1}, dropeos, categoria, rango, 
                                  cantidad, zona)
                lugar.enemigos_activos[indice_zona].append(enemigo)
                contador -= 1
                enemigo.stats()
    
    def generar_objetos_zona(self, lugar, zona:str):
        #DEBUG
#        print("---------------------------------------Metodo generar objetos")
        fragmento = Objeto("Fragmento de libro de secretos", 
                           0, "Habilidad", 0, 1, 1, 300)
        if(lugar == gm.pueblo) and (gm.pueblo_original.cantidades_objetos[
                                                                    1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif(lugar == gm.bosque) and (gm.bosque_original.cantidades_objetos[
                                                                    1][0] > 0):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.normancueva) 
            and (gm.normancueva_original.cantidades_objetos[1][0] > 0)):
            lugar.objetos_activos[1].append(fragmento)
        elif((lugar == gm.fondo_del_mar) 
            and (gm.fondo_del_mar_original.cantidades_objetos[0][0] > 0)):
            lugar.objetos_activos[0].append(fragmento)
            
#        print("-------------------------------------------------------------")
#        print(f"{zona:^50s}")
#        print("-------------------------------------------------------------")
#        print(lugar.objetos)

        indice = lugar.zonas.index(zona)
        objetos, cantidades = gm.mezclar_listas(lugar.objetos[indice],
                                           lugar.cantidades_objetos[indice], 1)
        lugar.objetos_zona_setter(objetos, zona)
        lugar.cantidades_objetos_zona_setter(cantidades, zona)
        
#        print(len(objetos))
#        print(len(lugar.objetos_activos))
        
#        if(contador<1):
#            contador+=1
#       print("contador: " + str(contador))
        
        if(len(objetos) == 0):
            contador = 0
        elif(len(objetos) == 1):
            contador = 1
        else:
            contador = gm.dados(1, len(objetos))//2

        for indice_nombre in range (0, len(gm.Dfnombres_objetos)):
            if(contador<=0):
                break
            if((gm.Dfnombres_objetos.iloc[indice_nombre,0] == objetos[
            indice]) and (cantidades[indice] > 0.0) 
            and (gm.Dfnombres_objetos.iloc[indice_nombre,0] 
            != "Fragmento de Libro de Secretos")):
                nombre = objetos[indice]
                objeto = gm.transformar_objeto(nombre, cantidades[indice])
#                    print(indice)
#                    print(lugar.objetos_activos)
                lugar.objetos_activos[indice].append(objeto)
#                    print(lugar.objetos_activos)
#                print(objeto)
#                print(f" Cantidad: {int(cantidades[indice])}")
                contador -= 1
                break
#        for objeto in lugar.objetos_activos[indice]:
#            print(objeto)

    def iniciar_pelea(self, p_presentes, e_presentes, omitidos=[], defensas=[], 
                   turnos=[], personajes_peleando=[], victima = None, mult =1):
        #DEBUG
        print("-----------------------------------------Metodo iniciar_pelea")
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
                    decision = input(f"¿{personaje.nombre}, " 
                                     + "quieres hacer la guerra?+ (S/N)")
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
                            personaje.activar_habilidad("Iniciar pelea", 
                                                        omitidos)
                    else:
                        zonas = personaje.ubicacion.zonas
                        zona = zonas.index(personaje.zona)
                        tirada = gm.dados(1, 
                               len(personaje.ubicacion.enemigos_activos[zona]))
                        print(f"{personaje.nombre}, " 
                              + f"has avistado a {tirada} enemigos...")
                        enemigos_vistos = []
                        for i in range(0, tirada):
                            print("... hay un " 
                     +f"{personaje.ubicacion.enemigos_activos[zona][i].nombre}"
                     +" cerca...")
                            enemigos_vistos.append(
                                 personaje.ubicacion.enemigos_activos[zona][i])
                        print("\n..posiblemente hayan mas " 
                              + "enemigos en la zona..\n")
                    print(f"{personaje.nombre}"
                         +", estas en modo sigilo sigilozo ¿que deseas hacer?")
                    decision = int(input("0: Atacar\n1: Unirse a la pelea"
                                         + "\n2: Usar objeto\n3: Tirar objeto "
                                         + "\n4: Moverte\n5: Esperar\n"))
                    if(decision == 0):
                        ataque = personaje.atacar(enemigos_vistos, 1.5)
                        ataque[0].cambiar_hp(-ataque[1])
                        if(personaje.sabiduria < e_sabiduria+gm.dados(1, 
                                       (e_sabiduria//2)+1) or jefes_presentes):
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
                        personaje.usar_objeto(p_presentes+enemigos_vistos)
                    elif(decision == 3):
                        personaje.tirar_objeto()
                    elif(decision == 4):
                        personaje.moverse()
                    else:
                        print(f"{personaje.nombre} se esconde...")
                        for i in range(tirada, tirada + gm.dados(1, 3)):
                            if(i>=len(personaje.ubicacion.enemigos_activos[
                                                                    zona])):
                                break
                            print("... has avistado a " 
                     +f"{personaje.ubicacion.enemigos_activos[zona][i].nombre}"
                     +" tambien...")
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
            return self.pelea(self, p_pelea, enemigos, 
                              defensas, turnos, omitidos)
        return [False, p_pelea]


    def jugar(self, resultados = []):
        #DEBUG
#        print("-------------------------------------------------Metodo jugar")
        # Quitar los que ya no estan domando
        domar_nuevo = []
        for domar in self.peleas_doma:
            if(domar[0]):
               domar_nuevo.append(domar)
               self.peleas_doma = domar_nuevo
        fin = False
        personajes_peleando = []
#        print("Resultados de peleas actuales")
#        print(resultados)
        
        # Añadir a personajes que esten dentro de peleas
        for resultado in resultados:
            for personaje in resultado[1]:
                print(personaje.nombre + " esta peleando")
#                print("-.-.-.-.-.-.-.-.-.")
                personajes_peleando.append(personaje)
                
        # Ordenar personajes por su velocidad para turnos
        turnos = gm.personajes
        for personaje in range(len(gm.personajes)-1,0,-1):
            for indice in range(personaje):
                if (gm.personajes[indice].velocidad > 
                    gm.personajes[indice + 1].velocidad):
                    temp = turnos[indice]
                    turnos[indice] = turnos[indice + 1]
                    turnos[indice + 1] = temp
        
        # Se crea turnos aux para voltear el orden de turnos originales
        turnos_aux = []
        for turno in range(len(turnos)-1, 0, -1):
            turnos_aux.append(turnos[turno])
        turnos_aux.append(turnos[0])
        turnos = turnos_aux
        
        for turno in range(0, len(turnos)):
            personaje = turnos[turno]
            
            print(personaje.ubicacion)

            # Añadir personajes que esten domando en lista
            if("Domando" in personaje.condicion):
                print(personaje.nombre + "esta domando...")
                for doma in range (0, len(self.peleas_doma)):
                    if(personaje in self.peleas_doma[doma]):
                        #doma[2] = enemigo, doma[3] = jaula, doma[4] =defensas, 
                        #doma[5] = omitidos, doma[6] = historial
                        self.peleas_doma[doma] = self.domar(personaje, 
                                  self.peleas_doma[doma][2], 
                                  self.peleas_doma[doma][3], 
                                  self.peleas_doma[doma][4], 
                                  self.peleas_doma[doma][5], 
                                  self.peleas_doma[doma][6])
                        break
                continue
            elif("Apostando" in personaje.condicion):
                self.casino(personaje, personaje.condicion["Apostando"])
                continue
            elif("Escalando" in personaje.condicion):
                (nivel, niv_maquina, 
                 niv_nina, niv_monstruo) = personaje.condicion["Escalando"]
                
                self.escalera(personaje, nivel, niv_maquina, 
                               niv_nina, niv_monstruo)
                continue
            
            # Realizar efectos y menu para turno de personaje
            personaje.stats()
            personaje.efecto() # efecto a personajes que no esten peleando
            print(f"Turno actual: {personaje.nombre:~^18s}")
            accion = self.menu(personaje)
            if(accion == "Salir"):
                return True
            
        p_presentes = []
        zonas_vistas = []
        
        for personaje in gm.personajes:
            personaje.actualizar_stats()
            
            # Actualizar efectos de armas de carga
            for objeto in personaje.inventario_nombres:
                if(objeto == "Pistola laser"):
                    indice = personaje.inventario_nombres.index("Pistola "
                                                                +"laser")
                    personaje.inventario[indice].uso -= 2
                elif(objeto == "Pistola laser mejorada"):
                    indice = personaje.inventario_nombres.index(
                            "Pistola laser mejorada")
                    personaje.inventario[indice].uso -= 2
            
            # Añadir personajes en p_presentes de su zona actual
            zona = personaje.ubicacion.zonas.index(personaje.zona)
            if(personaje.ubicacion.enemigos_activos[zona] != []):
                p_presentes.append(personaje)
#                print(personaje.nombre)
#                print(personaje.ubicacion.enemigos_activos)
                
            # Revisar zonas vistas de todos
            for zona in personaje.mapa[personaje.zona]:
                zonas_vistas.append(zona)
            zonas_vistas.append(personaje.zona)
        
        # Listas de enemigos activos de zonas vistas
        for zona_vista in zonas_vistas:
            lugar_visto = gm.busca_lugar(zona_vista)
            zona = lugar_visto.zonas.index(zona_vista)
            #Obtener las jaulas de todos los tipos de jaula de la zona actual
            jaulas_activas = []
            for jaulas in lugar_visto.jaulas:
                for jaula in jaulas:
                    if(gm.dados(1, 2) == 1 and jaulas[jaula] != ""):
                        jaulas_activas.append(jaula)
            
            # Calcular si algun enemigo cae en trampa
            if(jaulas_activas != []):
                for enemigo in lugar_visto.enemgios_activos()[zona]:
                    for trampa in jaulas_activas:
                        if((trampa.nombre == "Trampa de osos") 
                        and (enemigo in gm.atrapables_trampa_osos)):
                                tirada = gm.dados(1, 10)
                        elif((trampa.nombre == "Jaula")
                        and (enemigo in gm.atrapables_medianos)):
                                tirada = gm.dados(1, 10)
                        elif((trampa.nombre == "Jaula mas grande")
                        and (enemigo in gm.atrapables)):
                                tirada = gm.dados(1, 20)
                        if(enemigo.sabiduria + tirada <= 20):
                            #Enemigo atrapado
                            enemigo.condicion.update({"Atrapado": 1})
                            lugar_visto.jaulas[
                                    trampa.nombre][trampa] = enemigo.nombre
                            lugar_visto.objetos_activos.remove(trampa)
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
                    #Esta en pelea y no en resultados (comenzando)
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

    def maquina(self, nombre: str, usuario, mult = 1):
        #DEBUG
#        print("-----------------------------------------------Metodo maquina")
        if(not self.funcional):
            return False
        
        indice = usuario.inventario_nombres.index(nombre)
        usuario.peso -= usuario.inventario[indice].peso
        usuario.inventario_nombres.pop(indice)
        usuario.inventario.pop(indice)
        
        tirada = gm.dados(1, 4)
        for indice_nombre in range(0, len(gm.Dfnombres_objetos)):
            if(gm.Dfnombres_objetos.iloc[indice_nombre,0] == nombre):
                break
        if(tirada < 4 * mult):
            objetos = gm.Dfmejoras_objetos
        else:
            objetos = gm.Dfestropeos_objetos
        objeto = objetos.iloc[indice_nombre,0]
        for indice_nombre in range(0, len(gm.Dfnombres_objetos)):
            if(gm.Dfnombres_objetos.iloc[indice_nombre,0] == objeto):
                break
        nombre = objeto
        
        if(nombre[0] == "XXX"):
            self.funcional = False
        
        if(nombre[0] == "%"):
            nombre = gm.revisar_string(nombre)
        
        if("Cadaver " in nombre):
            nombre = "Cadaver de " + usuario.nombre
            
        if(nombre[0].isdigit() and nombre[2:] != "Dinero"):
            for indice in range(0, int(nombre[0])):
                gm.anadir_obj_manual(nombre[2:], usuario)
            return True
        
        if(nombre == "3 Dinero"):
            usuario.anadir_obj(3)
            return True
        
#        o = gm.transformar_objeto(nombre, 9999)
#        edificio.objetos_activos[1].append(o)
#        edificio.objetos[1].append(o.nombre)
#        edificio.cantidades_objetos[1].append(o.cantidad)
        gm.anadir_obj_manual(nombre, usuario, 9999)
#        print("-------------------------------------------------------------")

    def menu(self, personaje):
        lista_titulos = ["Acciones", "Interactuar", "Inventario", "Evento", 
                         "Opciones"]
        lista_menu = [["Administrar habilidades", "Curarse", "Esperar", 
                       "Moverse", "Usar habilidad", "Ver status"], 
                     ["Buscar", "Explorar"], 
                     ["Craftear", "Ver equipo", "Ver asistentes", "Ver in memoriams", "Desequipar", "Tirar objeto", 
                      "Usar objeto"],
                     [],
                     ["Guardar", "Guardar y salir", "Salir"]]
        
        if(personaje.zona == "Ayuntamiento"):
            lista_menu[3].append("Apostar")
        elif(personaje.zona == "Mercado"):
            lista_menu[3].append("Comprar")
            lista_menu[3].append("Vender")
        zona_personaje = personaje.ubicacion.zonas.index(personaje.zona)
        for enemigo in personaje.ubicacion.enemigos_activos[
                zona_personaje]:
            if("Atrapado" in enemigo.condicion):
                lista_menu[3].append("Domar")
        
        decision = "D"
        indice_titulo = -1
        while(decision == "I" or decision == "D" or decision == "Quedarse aqui"):
            if(decision == "D"):
                indice_titulo += 1
                if(indice_titulo >= len(lista_titulos)):
                    indice_titulo = 0
            elif(decision == "I"):
                indice_titulo -= 1
                if(indice_titulo < 0):
                    indice_titulo = len(lista_titulos) - 1
            
            print(f"{lista_titulos[indice_titulo]:-^24s}")
            for indice in range(0, len(lista_menu[indice_titulo])):
                print(f"{indice + 1}. {lista_menu[indice_titulo][indice]}")
            if(len(lista_menu[indice_titulo]) == 0):
                print("No hay ninguna opcion disponible de momento")
            print("<-- I | D -->")
            
            decision = input().upper()
            if(decision.isnumeric()):
                if(int(decision) < 1 or int(decision) > len(
                                                   lista_menu[indice_titulo])):
                    print("tas tonto shavo")
                    decision = "Quedarse aqui"
                else:
                    decision = lista_menu[indice_titulo][int(decision) - 1]
            elif(decision != "I" and decision != "D" and decision != "Quedarse aqui"):
                print("tas tonto shavo")
                decision = "Quedarse aqui"
        
        print(decision + " seleccionado")
        if(decision == "Administrar habilidades"):
            print(personaje)
            personaje.arbol_habilidades()
        elif(decision == "Curarse"):
            personaje.energetizar()
        elif(decision == "Esperar"):
            personaje.energia = personaje.energia_max
            print(f"Energia restaurada!!\nEnergia actual: {personaje.energia}")
        elif(decision == "Moverse"):
            personaje.moverse()
        elif(decision == "Usar habilidad"):
            personaje.activar_habilidad("Jugar")
        elif(decision == "Ver status"):
            print(personaje)
        elif(decision == "Buscar"):
            objeto = input("¿Que quieres buscar? (0 para nada en especifico)\n")
            if(objeto == "0"):
                personaje.buscar()
            else:
                personaje.buscar(objeto)
        elif(decision == "Explorar"):
            personaje.explorar()
        elif(decision == "Craftear"):
            personaje.craftear()
        elif(decision == "Ver equipo"):
            personaje.ver_equipo()
        elif(decision == "Ver asistentes"):
            for asistente in personaje.asistentes:
                print(asistente)
        elif(decision == "Ver in memoriams"):
            for muerto in personaje.in_memoriam:
                print(f" {muerto}: '{personaje.in_memoriam[muerto]}' ")
        elif(decision == "Desequipar"):
            personaje.desequipar()
        elif(decision == "Tirar objeto"):
            personaje.tirar_objeto()
        elif(decision == "Usar objeto"):
            objetos_permitidos = []
            # Imprimir objetos utilizables solo en jugar 
            # (excluyendo los que se usan en pelea)
            for indice in range(0, len(personaje.inventario)):
                if(personaje.inventario[indice].estadistica != "F" or "Pocion" 
                   in personaje.inventario_nombres[indice]
                   and personaje.inventario_nombres[indice] != "SCP 427"):
                    objetos_permitidos.append(personaje.
                                              inventario[indice].nombre)
            if(len(objetos_permitidos) == 0):
                print("No hay ningun objeto disponible")
            else:
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
                
                personaje.usar_objeto(objeto)
        elif(decision == "Apostar"):
            self.casino(personaje)
        elif(decision == "Comprar"):
            personaje.comprar()
        elif(decision == "Domar"):
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
            self.peleas_doma.append(self.domar(personaje, 
            personaje.ubicacion.jaulas[jaula_select.nombre][jaula_select], 
            jaula_select, [0, 0], [], []))
        elif(decision == "Vender"):
            personaje.vender()
        elif(decision == "Guardar"):
            # Añadir funcionalidad de guardar
            pass
        elif(decision == "Guardar y salir"):
            # Añadir funcionalidad de guardar
            return "Salir"
        elif(decision == "Salir"):
            return "Salir"
        else:
            print("Tas tonto shavo")
            return False
        return True

    def pelea(self, p_presentes, e_presentes, defensas = [], 
              turnos = [], omitidos = []):
        #DEBUG
#        print("-------------------------------------------------Metodo pelea")
        for jefe in gm.jefes.keys():
            gm.notaxeables.append(jefe)
        jefes_presentes = False
        for enemigo in e_presentes:
            if(enemigo in gm.jefes.keys()):
                jefes_presentes = True
        # Anadir asistentes de personajes vivos no peleando
        for personaje in gm.personajes: 
            if(personaje in gm.personajes):
                for asistente in personaje.asistentes:
                    if(asistente not in p_presentes):
                        p_presentes.append(asistente)
        # Anadir asistentes de personajes muertos
        for personaje_muerto in gm.personajes_muertos: 
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
        # -----------------------------------------------------turnos asignados
        
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
            elif(personaje not in turnos 
                 or "Indefenso" in personaje.condicion):
                continue
            print(f"Es turno de: {personaje.nombre}\n")
            if(personaje in e_presentes):# -----------------------Turno enemigo
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_enemigo(
                                              self, p_presentes, e_presentes, 
                                              defensas, turnos, omitidos, 
                                              turnos_aux, personaje, historial)
            elif(personaje in gm.personajes):# -----------------Turno personaje
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_personaje(
                                              self, p_presentes, e_presentes, 
                                              defensas, turnos, omitidos, 
                                              turnos_aux, personaje, historial)
            else:
                # turno asistente
                (p_presentes, e_presentes, 
                 defensas, turnos, omitidos, historial) = self.turno_enemigo(
                                              self, p_presentes, e_presentes, 
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

    def pelea_carisma(self, personaje, defensa, e_presentes = None, 
                      dano_enemigo = None, enemigo = None):
        if(enemigo == None):
            print(f"\n¿{personaje.nombre}, quién será tu victima?")
            print("INDICE \t NOMBRE \t SALUD")
            for indice in range (0, len(e_presentes)):
                print(f"{indice + 1}: {e_presentes[indice].nombre}\t" 
                      + f"{e_presentes[indice].salud}")
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
            print(f"{personaje.nombre} esta indefenso, " 
                  +f"{enemigo.nombre} ataca!!")
            dano = defensa - dano_enemigo
            if(dano < 0):
                print(f"{personaje.nombre} recibe {dano_enemigo} de dano")
                personaje.cambiar_hp(-dano_enemigo)
            else:
                print(f"El ataque de {enemigo.nombre} ha sido bloqueado!")
    
    def turno_enemigo(self, p_presentes, e_presentes, defensas, turnos, 
                      omitidos, turnos_aux, enemigo, historial, jaula = None):
        if(enemigo in omitidos):
            omitidos.remove(enemigo)
            turnos.pop(turnos.index(enemigo))
            return (p_presentes, e_presentes, defensas, 
                    turnos, omitidos, historial)
        elif(enemigo not in turnos or "Indefenso" in enemigo.condicion):
            return (p_presentes, e_presentes, defensas, 
                    turnos, omitidos, historial)
        indice_enemigo = turnos.index(enemigo)
        indice_enemigo_aux = turnos_aux.index(enemigo)
        
        if("Confundido" in enemigo.condicion):
            accion = enemigo.decidir(turnos_aux, historial, 
                                     turnos_aux, defensas)
        elif(issubclass(enemigo, Enemigo)):
            accion = enemigo.decidir(e_presentes, historial, 
                                     turnos_aux, defensas)
        else:
            accion = enemigo.decidir(p_presentes, historial, 
                                     turnos_aux, defensas)
        
        if("Atacando normal" in enemigo.condicion 
           or "Atacando especial" in enemigo.condicion):
            for personaje in accion[0]:
                print(f"{enemigo.nombre} se dispone " 
                      +f"a atacar a {personaje.nombre}!")
                indice_aux = turnos_aux.index(personaje)
                if(personaje in turnos and personaje in gm.personajes):
                    indice = turnos.index(personaje)
                    salida = True
                    while salida:
                        #-----------------------------------Respuesta personaje
                        print(f"¿{personaje.nombre}, que deseas hacer?")
                        if(personaje.nombre == "Sebas" 
                           and personaje.arbol["B1"][0] == 1):
                            print("0: Anticipacion")
                        
                        decision = int(input("1: Defenderte\n2: Usar objeto"
                                             + "\n3: No hacer nada\n"))
                        
                        if(decision == 0):
                            if(not personaje.activar_habilidad(
                                    "anticipacion")[0]):
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
                            #---------------------------------------Usar objeto
                            objetos_permitidos = []
                            for indice in range(0, len(personaje.inventario)):
                                if(personaje.inventario[
                                   indice].estadistica != "F" or "Pocion" 
                                   in personaje.inventario_nombres[indice] 
                                   or personaje.inventario_nombres[indice] 
                                   not in gm.multiples):
                                    objetos_permitidos.append(
                                           personaje.inventario[indice].nombre)
                            
                            print("¿Que quieres usar?")
                            print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA"
                                  +" \t BOOSTEO")      
                            contador = 0
                            for llave in personaje.cartera_obj:
                                if(llave in objetos_permitidos):
                                    print(f"{contador + 1}, \t{llave:.24s}: " 
                                          + "\t\t"+personaje.cartera_obj[llave] 
                                          + " | \t\t" + personaje.inventario[
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
                            #-------------------------------Objeto seleccionado
                            print("¿Con quien usaras el objeto?")
                            if(objeto.estadistica == "Revivir"):
                                print("0: Regresar")
                                for objeto in range (0, len(
                                        personaje.inventario_nombres)):
                                    if("Cadaver" 
                                      in personaje.inventario_nombres[objeto]):
                                        print(f"{objeto + 1}: "
                                    +f"{personaje.inventario_nombres[objeto]}")
                                seleccion = int(input())-1
                                if(seleccion == -1):
                                    continue
                                else:
                                    uso = personaje.usar_objeto(
                                            personaje.
                                            inventario_nombres[seleccion], 
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
                                    uso = personaje.usar_objeto(personaje, 
                                                                objeto)
                                    if(type(uso) == bool):
                                        salida = not uso
                                    elif(list(uso.keys())[0] == "Escudo"):
                                        defensas[seleccion] = list(
                                                               uso.values())[0]
                                        break
                                else:
                                    uso = personaje.usar_objeto(turnos_aux[
                                                        seleccion], objeto)
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
                    muerto = personaje.cambiar_hp(dano)
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
            self.pelea_carisma(accion[0],defensas[turnos_aux.index(accion[0])], 
                               dano_enemigo = accion[1], enemigo = enemigo)
        turnos.pop(indice_enemigo)
        return (p_presentes, e_presentes, defensas, 
                turnos, omitidos, historial)
    
    
    def turno_personaje(self, p_presentes, e_presentes, defensas, turnos, 
                     omitidos, turnos_aux, personaje, historial, jaula = None):
        if(personaje in omitidos):
            omitidos.remove(personaje)
            turnos.pop(turnos.index(personaje))
            return (p_presentes, e_presentes, defensas, 
                    turnos, omitidos, historial)
        elif(personaje not in turnos or "Indefenso" in personaje.condicion):
            return (p_presentes, e_presentes, defensas, 
                    turnos, omitidos, historial)
        
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
                                 + "\n3: Usar objeto\n4: Tirar objeto "
                                 + "\n5: Huir\n6: Curarse\n" + captura + 
                                 habilidad))
            if(decision == 0):
#                        print(e_presentes)
                resultado = personaje.atacar(e_presentes)
#                        print(e_presentes)
                indice_enemigo_aux = turnos_aux.index(resultado[0])
                eleccion = input(f"¿Deseas atacar a {resultado[0].nombre}? "
                                                     +"(S/N)\n")
                if(eleccion == "S"):
                    if("Confundido" in personaje.condicion):
                        resultado[0] = turnos_aux[
                                gm.dados(1, len(turnos_aux))-1]
                    print(f"{personaje.nombre} ataca a"
                          + " {resultado[0].nombre} con "
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
                    muerto = resultado[0].cambiar_hp(dano)
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
                self.pelea_carisma(personaje, defensas[
                                                  turnos_aux.index(personaje)], 
                                                  e_presentes = e_presentes)
            elif(decision == 2):
                defensas[indice] = personaje.defender()
                salida = False
            elif(decision == 3):
                #-----------------------------------------Usar objeto
                objetos_permitidos = []
                for indice in range(0, len(personaje.inventario)):
                    if(personaje.inventario[indice].estadistica != "F" 
                       or "Pocion" in personaje.inventario_nombres[indice]):
                        objetos_permitidos.append(
                                personaje.inventario[indice].nombre)
                
                print("¿Que quieres usar?")
                print("INDICE \t NOMBRE \t CANTIDAD \t ESTADISTICA \t BOOSTEO")      
                contador = 0
                for llave in personaje.cartera_obj:
                    if(llave in objetos_permitidos):
                        print(f"{contador + 1}, \t{llave:.24s}: \t\t"
                              + personaje.cartera_obj[llave]+" | \t\t"
                              + personaje.inventario[
                                      personaje.inventario_nombres.index(
                                              llave)].estadistica + " | \t"
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
                if("Confundido" in personaje.condicion):
                    objeto = personaje.inventario[gm.dados(1, 
                                                  len(personaje.inventario))-1]
                #----------------------------------------Objeto seleccionado
                revivir = False
                if(objeto.nombre in gm.multiples):
                    seleccion = -1
                else:
                    print("¿Con quien usaras el objeto?")
                    if(objeto.estadistica == "Revivir"):
                        print("0: Regresar")
                        
                        #personaje estaba en accion[0]
                        for objeto in range (0, len(
                                personaje.inventario_nombres)):
                            if("Cadaver" in personaje.inventario_nombres[
                                                                      objeto]):
                                print(f"{objeto+1}: "
                                    +f"{personaje.inventario_nombres[objeto]}")
                        seleccion = int(input())-1
                        if(seleccion == -1):
                            continue
                        else:
                            uso = personaje.usar_objeto(
                               personaje.inventario_nombres[seleccion], objeto)
                            salida = not uso
                            revivir = True
                    else:
                        for personaje in range(0, len(turnos_aux)):
                            if(turnos_aux[personaje].salud > 0):
                                print(f"{personaje + 1}: " 
                                      + f"{turnos_aux[personaje].nombre}")
                        print(f"{len(turnos_aux) + 1}: Regresar")
                        seleccion = int(input())-1
                    
                if(not revivir): # Uso normal de objeto, callate
                    if("Confundido" in personaje.condicion):
                        seleccion = turnos_aux[gm.dados(1, len(turnos_aux))-1]
                    if(seleccion == len(turnos_aux)): # Regresar
                        continue
                    elif(seleccion == -1): # Objetivo multiple
                        personaje.usar_objeto(turnos_aux, objeto)
                    elif(personaje.nombre == turnos_aux[seleccion].nombre):
                        uso = personaje.usar_objeto(personaje, objeto)
                        if(type(uso) == bool):
                            salida = not uso
                        elif(list(uso.keys())[0] == "Escudo"):
                            defensas[seleccion] = list(uso.values())[0]
                            break
                    else:
                        uso = personaje.usar_objeto(turnos_aux[seleccion], 
                                                    objeto)
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
                huyendo = personaje.huir(e_presentes)
                print(f"{personaje.nombre} esta intentando escapar...", 
                      end = " ")
                if("Confundido" in personaje.condicion):
                    print(f"...{personaje.nombre} "
                         +"esta tan confundido que se tropezo con una rama...")
                    huyendo = False
                if(huyendo): # va a escapar
                    if("Domando" in personaje.condicion):
                        if(enemigo.velocidad > personaje.velocidad 
                           and enemigo.carisma > personaje.carisma):
                            zona = personaje.ubicacion.zonas.index(
                                    personaje.zona)
                            personaje.ubicacion[zona].jaulas[
                                                jaula.nombre].pop(jaula) 
                            #salirse de jaula
                            agresividad_max = (((self.oso_marino.carisma 
                                             + self.oso_marino.fuerza)
                                             - (self.oso_marino.inteligencia 
                                             + self.oso_marino.resistencia))+4)
                            pelear = ((enemigo.salud/enemigo.salud_max) 
                                 * (enemigo.agresividad/agresividad_max) * 100)
                            if(enemigo.nombre in gm.domables 
                               and gm.dados(1, 100) <= pelear):
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
                    p_presentes.remove(personaje)
                    turnos.pop(turnos.index(personaje))
                    if(personaje.inteligencia >=(13 +5*(personaje.nivel))*3/4):
                        personaje.moverse()
                    elif(personaje.inteligencia 
                         >= (13 + 5 *(personaje.nivel))* 1/2):
                        personaje.moverse(personaje.hogar)
                    else:
                        lugar = personaje.mapa[personaje.zona][
                           gm.dados(1, len(personaje.mapa[
                                   personaje.zona]))-1]
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
                   and gm.dados(1, 100) <= capturar):
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
                        muerto = resultado[1][0].cambiar_hp(dano)
                        print(f"{resultado[1][0].nombre} recibio {dano} "
                                 +"puntos de dano!")
                        if(muerto):
                            if(resultado[1][2] in gm.armash_shidas):
                                if(resultado[1][0].categoria == "Humano"):
                                    gm.anadir_obj_manual("Carne humana", 
                                                         personaje)
                            if(resultado[1][0] in turnos):
                                indice_enemigo=turnos.index(resultado[1][0])
                                turnos.pop(indice_enemigo)
                        elif(resultado[1][2].nombre == "Taxer" 
                             and resultado[1][0].nombre not in gm.notaxeables):
                            print(resultado[1][0].nombre 
                                  +" ha sido paralizado!")
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

#lugar = Lugar("A", [], [3], [], [], [], [], [])
#print(lugar.enemigos)
juego = Juego()
#juego.jugar()