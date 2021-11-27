import Game_Manager as gm
#from Juegos import Juego

gm.generar_carneables()

def main():

    
#    dic = {"hola":[{ruben:sebas},1]}

#    for n in dic["hola"][0]:
#        print(dic["hola"][0][n].nombre)

    # Jaula 
    
    # Terminar domar
    
        # Metodo turno enemigo/turno personaje (tanto en domar como en pelea) COMPLETADO
        # En metodo domar agregar opcion de capturar COMPLETADO
        # Enemigo huya cuando tu huyas COMPLETADO

    # Puedes liberarlo de la trampa, bajar agresividad, es más facil que huya a que se quede, y si se queda, revisa con agresividad si te ataca o no agregarle estado de "liberado"

    # (Dentro de reclutar) Porcentaje de salud con original hace variar la bonificacion (salud maxima y agresividad es 0 o casi 0, 3 + 2 * rango del enemigo)

    # Asistente

    # revisar si le queda espacio al dueño en reclutar COMPLETADO

    # Atributos de enemigo, dueño, espacio, nombre, cambiar de dueño() COMPLETADO
    # Decision igual a enemigo COMPLETADO
    # Límite de asistentes por "espacio" por personaje, si se excede, liberar asistente() COMPLETADO
    # Si se muere, meter a in memoriam COMPLETADO
    
    # liberar asistente() COMPLETADO
    
        # Seleccionar cual liberar COMPLETADO
        # Mensaje emotivo COMPLETADO
        # Lo sacas de tu lista de asistentes, lo metes a in memoriam COMPLETADO
    
    # SCP 427, solo utilizable en pelea, te conviertes en super asistente y al final se destruye
        # usar_obj() en jugar quitar scp 427 COMPLETADO
        # lista de objetos para usar en turno personaje añadir scp 427 COMPLETADO
        # (dentro de usar objeto) pasar a self a personajes_muertos COMPLETADO
        # crear un asistente con los stats boosteados del muerto COMPLETADO
        # añadir un efecto al asistente de {"Temporal": 1} COMPLETADO
        
        # quitar el efecto cuando acabe la pelea COMPLETADO
        # destruir 427 COMPLETADO
        # matar al super asistente COMPLETADO
        # revivir al vato muerto COMPLETADO
    
    # Notas de consejo (lista consejo y anadir mas notas en el juego) COMPLETADO
    
    # CRAFTEOS
        
        # orden en lista de llaves debe dar igual COMPLETADO
    
        # Diccionario (llaves listas de ingredientes y valores el resultado) COMPLETADO
        # Metodo personaje.crafteo(self) preguntar que objetos mezclar (repetir x cantidad de veces incluyendo opcion de detenerse) COMPLETADO
        # si la combinacion que ponen ya existe en la llave de crafteos, le damos ese valor y le quitamos los ingredientes COMPLETADO
        # Amuleto crafteo
            # Si el resultado es un asistente, lo creas y reclutas en vez de anadir_obj() COMPLETADO
    
        ## Meter combinaciones de crafteos en el libro de los secretos
    
    # Habilidades-------------------------------------------------------------------
        # Agregar las habilidades (en orden)
        # Costo de energia de cada habilidad
        
#        Jugar: 0
    #        Sabiduria del mas alla
        #        anadir_obj_manual(norman, "Nota de consejo sabia")
        #        Dentro de anadir manual, if(o == nota y sabia in nombre):
        #            boosteo = mensaje y nombre = "Nota de consejo" antes de transformar el objeto. Y despues, o.boosteo = boosteo

    #        Pociones
        #        for i in crafteos:
        #            for o in inventario:
        #                if o in i:
        #                    lista.append(i)
        #        for o in lista
        #            print(o + ": " + crafteos[o])
        
    #        Boosteo
        #        recorrer personajes y preguntarle a cual
        #        recorrer estadisticas y preguntarle cual
        #        preguntarle cuanto quiere boostearle (cantidad = energia que tiene y decirle el maximo que puede dar (9))
        #        if estadistica == salud: objetivo.cambiar_hp(boosteo), else: objetivo.condicion.update("Fuerza5": 3) 5=boosteo, 3= turnos, objetivo.fuerza += 5. Efecto de objetivo: if(estadistica in condicion): self.estadistica -= int(estadistica[-1])
    
#        Turno personaje:
    #        Disfraz
        #        Recorrer e_presentes y elegir a cual, y darle confundir
        
    #        Carisma absoluta
        #        Recorrer e_presentes y elegir a cual, enemigo.huir() a fuerzas
        
    #        Grito de guerra
        #        recorrer e_presentes, meterlos a cancel y darles confundir
    
    #        Habilidad animal
        #        recorrer e_presentes (filtrar por animal) y elegir a cual, recorrer estadisticas y elegir uno, if(enemigo.estadistica > self.estadistica): self.condicion.update(estadistica+"enemigo.estadistica - self.estadistica") y self.estadistica = enemimgo.estadistica, else: self.condicion.update(estadistica+"enemigo.estadistica") y self.estadistica += enemimgo.estadistica
        
    #        Invocar animal
        #        Crear asistente oso y meterlo a p_presentes y desaparecerlo al final de la pelea
    
    #        Special Curry
        #        a todos los e_presentes darles condicion quemado 2 turnos
        
    #        Kaio Ken (activacion)
        #        sebas.condicion.update({"Kaio Ken": 3})
        
    #        Ultra instinto (activacion)
        #        sebas.condicion.update({"Ultra instinto": 3})
    
    #        Analitico
        #        reccorrer e_presentes, elegir a cual e imprimir stats
        
    #        Momazo
        #        recorrer e_presentes, elegir a cual y meter a cancel
    
    #        Meme de enemigos
        #        recorrer e_presentes, elegir a cual y enemigo.carisma -= Juego.dados(1 a mitad de e.carisma)
    
    #        Lord meme
        #        recorrer e_presentes, meterlos a cancel y reducir carisma (lo de arriba)
    
    #        Robots
        #        Crear asistente robot y meterlo a p_presentes y desaparecerlo al final de la pelea
    
    #        Boosteo
        #        recorrer personajes y preguntarle a cual
        #        recorrer estadisticas y preguntarle cual
        #        preguntarle cuanto quiere boostearle (cantidad = energia que tiene y decirle el maximo que puede dar (9))
        #        if estadistica == salud: objetivo.cambiar_hp(boosteo), else: objetivo.condicion.update("Fuerza5": 3) 5=boosteo, 3= turnos, objetivo.fuerza += 5. Efecto de objetivo: if(estadistica in condicion): self.estadistica -= int(estadistica[-1])

    #        Llamar al viento
        #        recorrer p_presentes y e_presentes y atacar(mult=2)

    #        Mente dormida
        #        escoger entre todos o uno, si todos, recorrer e_presentes y atacar(mult=1.5), else atacar(enemigo,mult=3)
    
#        Turno enemigo:
    #        Anticipacion
        #        En respuesta de personaje, si es sebas, añadir opcion de usar anticipacion, imprimir accion[1] y preguntar si quiere atacar (atacar le quita el turno al personaje). Cuando enemigo vaya a atacar, preguntar si esta vivo, y si no, cancela ataque
    
#        Buscar:
    #        Explorador
        #        si es ruben y tiene desbloqueada la habilidad, iluminar += boosteo
        
    #        Vision nocturna
        #        si es norman y tiene desbloqueada la habilidad, iluminar += boosteo
    
#        Iniciar pelea:
    #        Explorador
        #        si es ruben y tiene desbloqueada la habilidad, imprimir todos los enemigos presentes
    
#        Actualizar stats:
    #        Super Sayan
        #        si es sebas y tiene "Super sayan" en condicion, self.fuerza = valor de turnos de condicion "super sayan" * 1.5, en subir nivel, si se modifica la fuerza, aumentar uno en el valor de la candicion de super sayan si es que la tiene activa
        
    #        Bolsa magica
        #        self.carga += cantidad
    
#        Usar obj:
    #        Nutrirse
        #        if self es turati, o es algun tipo de comida y tiene habilidad de nutrirse, boosteo *= Juego.dados(10, 20)/10
    
#        Atacar personaje:
    #        Critical
        #        si es turati, y tiene la habilidad desbloqueada, tirada = Juego.dados(1, 10), si tirada == 10, daño *= 2
    
    #        Kaio Ken
        #        si es sebas y tiene la condicion kaio ken, mult = 2
    
    #        Smash ball
        #        si es turati, y tiene la habilidad desbloqueada, tirada = Juego.dados(1, 2), si tirada == 1: daño *= 5, else: self.cambiar_hp(daño * -3) y daño *= 0

    #        Cazador
        #        si es ruben y enemigo es animal y tiene habilidad desbloqueada, mult = 2
    
#        Atacar enemigo:
    #        Simpatizar con animales
        #        si objetivo es mirek, si eres un animal y tiene habilidad desbloqueada, si len(p_presentes)>1 cambia de objetivo, sino, daño = 0
    
    #        Ultra instinto (ya activado)
        #        si el objetivo es sebas y tiene la condicion "ultra instinto", daño = 0
    
    #        Kaio Ken
        #        si el objetivo es sebas y tiene la condicion "kaio ken", daño *= 2
        
#        Maquina: (ambos tambien en jugar)
    #        Artesano
        #        Si el objeto es una lista, objeto = crafteos(lista) y dar objeto nuevo
    
    #        Alquimista
        #        si es buggati, si tiene la habilidad desbloqueada, y no esta en el lugar de la maquina, dejar que se haga el metodo maquina con peor probabilidad

# PENDIENTES:
# Costo de energia de cada habilidad (quitar energia en returns) COMPLETADO
# Recuperan 20% y 30% energia COMPLETADO


    # Separar codigo por documentos COMPLETADO
    # Anadir funciones
    # Reducir funciones
    # Comentar TODO
    
    # Personajes.arbol_habilidades es recursivo y no se llama en Juegos.jugar()
    # Personajes.comprar no se usa en Juegos.jugar()
    # Personajes.craftear no se usa en Juegos.jugar()
    # Personajes.desequipar no se usa
    # Personajes.equipar es recursivo
    # Personajes.explorar no se usa en Juegos.jugar()
    
    # Menu automatico:
    # Funcion que va llenando un diccionario/lista con opciones de menu
    # Decoradores en funciones que queremos que se añandan a esa lista/diccionario
    # String de menu se llena con las acciones posibles en el momento (ifs de Juego.jugar) y eso
    
    
    # str Lugares
    # Generador de nombres 2000

    # Cambiar nombre variables Juegos COMPLETADO
    # Llamar a casino COMPLETADO
    # gm.dias ? 
        #Cada jugador tiene cuenta de turnos, asi como el servidor
        #El servidor tiene la menor cuenta de turnos. El servidor aumenta de
        #turno cuando sea menor que el turno de todos (+1)
    # Dialogo intenso sala misteriosa
    # Descripcion perra de wendigo
    # Sabiduria del mas alla

    # Arreglar docs
    
    # Metodo guardar y cargar
    # ------------------------------------------------------------------------------
    # Modo admin y funciones para todo(?)
    # A prueba de bobos
    
    # Mapa
    # Tarjeta de enemigos/objetos
    # Logica del juego en fisico
    
    # Simulacion
        # Checar estadisticas enemigos/boosteo de objetos/cantidad de objetos
    
    print("------------------------------------------------------------------JUEGO")
#    print(revisar_string("%3 Hierro/4 Carbon/2 Oro"))
    
#    Juego.generar_enemigos_zona(bosque, "Pradera")
#    Juego.generar_enemigos_zona(bosque, "Aire libre")
#    Juego.generar_enemigos_zona(bosque, "Corazon del bosque")
    
#    Juego.generar_enemigos_zona(puerto, "Bahia")
#    Juego.generar_enemigos_zona(puerto, "Carguero")
    
#    for e in range(0, len(campamento.enemigos_activos())):
#        for e1 in range(0, len(campamento.enemigos_activos()[e])):
#            print(campamento.enemigos_activos()[e][e1].nombre)
#            
#    Juego.generar_objetos(campamento)
#    for e in range(0, len(campamento.objetos_activos())):
#        for e1 in range(0, len(campamento.objetos_activos()[e])):
#            print(campamento.objetos_activos()[e][e1].nombre)
#            
    
#    master.stats()
#    anadir_obj_manual("Carnada", mirek)
#    anadir_obj_manual("Pechera", master)
#    anadir_obj_manual("Pantalones", master)
#    anadir_obj_manual("Botas", master)
#    anadir_obj_manual("Lentes", master)
#    anadir_obj_manual("Traje de buzo mejorado", master)
#    master.usar_obj()
#    master.tirar_objeto()
#    master.stats()
    
#    master.usar_obj()
#    master.usar_obj()
#    master.usar_obj()
#    master.usar_obj()
#    master.usar_obj()
#    master.stats()
#    master.usar_obj()
#    print(master.equipo)
#    master.stats()
#    master.moverse()
#    master.stats()
#    master.moverse()
#    master.stats()
#    
#    sebas.stats()
#    anadir_obj_manual("Fragmento de libro de secretos", master)
#    master.usar_obj()
#    anadir_obj_manual("Escudo", ninja)
#    master.stats()
#    anadir_obj_manual("Jaula", ninja)
#    anadir_obj_manual("Carne humana", master)
#    anadir_obj_manual("Comida", master)
#    master.stats()
#    master.cambiar_hp(-20)
#    master.usar_obj()
#    master.arbol_habilidades()
#    master.stats()
#    master.activar_habilidad()
    
#    anadir_obj_manual("Control universal", master)
#    anadir_obj_manual("Pila", master)
#    anadir_obj_manual("Control universal", ninja)
#    anadir_obj_manual("Pila", ninja)
    
#    anadir_obj_manual("Cartucho de magnum", ruben)
#    anadir_obj_manual("Cartucho de magnum", ruben)
#    ruben.stats()
#    ruben.tirar_objeto()
#    ruben.stats()
#    anadir_obj_manual("Cartucho de sniper", norman)
    
#    partida = Juego()
#    partida.generar_enemigos_zona(lugar = campamento, zona = "Cabana")
#    partida.generar_enemigos_zona(lugar = campamento, zona = "Cabanas vecinas")
#    partida.generar_enemigos_zona(lugar = campamento, zona = "Almacen")
#    partida.generar_enemigos_zona(lugar = campamento, zona = "Comedor")
#    partida.generar_enemigos_zona(lugar = campamento, zona = "Puesto de seguridad")
#    
#    fin = False
#    res = []
#    while(not fin):
#        res = partida.jugar(res)
#        if(type(res) != list):
#            fin = True
    
#    Juego.generar_objetos_zona(viaje_astral, "cabana")
    
    print("----------------------------------------------------------------PRUEBAS")
    print("---------------------------------------------------------------Enemigos")
    
    #----------------------- Generar enemigos --------------------------------------
#    Juego.generar_enemigos_zona(campamento, "Cabana")
#    Juego.generar_enemigos_zona(bosque, "Aire libre")
#    Juego.generar_enemigos_zona(mercado, "Mercado")
#    Juego.generar_enemigos_zona(montana, "Cabana doctor")
#    Juego.generar_enemigos_zona(edificio, "Entrada")

#    print(separar_enemigos("Campamento", ["Cabana", "Comedor", "Almacen", "Cabanas vecinas", "Puesto de seguridad"], 1))
#    print(separar_enemigos("Campamento", ["Cabana", "Comedor", "Almacen", "Cabanas vecinas", "Puesto de seguridad"], 2))
#    print(separar_enemigos("Edificio Abandonado", ["Entrada", "Maquina", "Escalera", "Laboratorio", "Sala de investigacion"], 1))

    #----------------------- Lista e_presentes -------------------------------------
#    e_presentes = []
#    enemigo = Enemigo(15, 11, 7, 15, 8, 10, "Zombie base", "Saludable", "%hola/adios", "Zombie", 1, 10)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(100, 19, 17, 19, 20, 15, "Siren Head", "Saludable", "HDMI", "SCP", 9, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(15, 14, 13, 10, 11, 15, "Aguila", "Saludable", "%Esencia velocidad II/Esencia sabiduria II", "Animal", 3, 30)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(120, 25, 12, 25, 25, 25, "Chaman poseido", "Saludable", "Dialogo", "DIOS OSCURO", 15, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(95, 17, 18, 18, 12, 10, "Wendigo Azteca", "Saludable", "Fragmento de libro de secretos", "Monstruo", 7, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(75, 15, 16, 17, 8, 11, "Rat King G", "Saludable", "Fragmento de libro de secretos", "SCP", 5, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(20, 13, 13, 17, 14, 11, "Rat King C", "Saludable", "Veneno III", "SCP", 5, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(200, 20, 20, 2, 6, 3, "Trol", "Saludable", "Esencia salud III", "Monstruo", 6, 20)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    enemigo = Enemigo(150, 19, 13, 16, 20, 11, "SCP 3000", "Saludable", "Y909", "SCP", 8, 1)
#    enemigo.stats()
#    e_presentes.append(enemigo)
#    print(e_presentes)
    
    #----------------------- Lista p_presentes -------------------------------------
#    p_presentes = [mirek, ruben, sebas]
#    print(p_presentes)
#    Juego.pelea(p_presentes, e_presentes)
#    qwerty = Juego.iniciar_pelea(p_presentes, e_presentes)
#    for i in qwerty:
#        print(i.nombre)

    print("----------------------------------------------------------------Objetos")

    #----------------------- Generar objetos ---------------------------------------
#    Juego.generar_objetos(campamento)
#    Juego.generar_objetos(mercado)
#    print(pueblo.objetos_activos())
#    Juego.generar_objetos(montana)
#    Juego.generar_objetos(edificio)

#    print(separar_objetos("Campamento", ["Cabana", "Comedor", "Almacen", "Cabanas vecinas", "Puesto de seguridad"], 1))
#    print(separar_objetos("Bosque", ["Aire libre", "Cabana de guardabosques", "Entrada Mina"]))
#    print(separar_objetos("Pueblo", ["Comunidad", "Casa de chaman", "Ayuntamiento"]))
#    print(separar_objetos("Montana", ["Cabana doctor", "Cima", "Subida"]))
#    print(separar_objetos("Edificio Abandonado", ["Entrada", "Maquina", "Escalera", "Laboratorio", "Sala de investigacion"], 1))

    #----------------------- Generar objeto manual ---------------------------------
#    o = Objeto("Disfraz", 1, 'I', 10, 0, 1, 1)
#    o = Objeto("Fragmento de libro de secretos", 0, 'Habilidad', 0, 1, 1, 300)
#    o = Juego.tranformar_objeto("Comida")

#    pueblo.objetos_activos()[1].append(o)
#    campamento.objetos_activos()[0].append(o)

#    campamento.objetos_activos()[1].append(o)
#    campamento.objetos()[1].append(o.nombre)
#    campamento.cantidades()[1].append(1)
#    o.stats()

    print("----------------------------------------------------------------Pruebas")
    #----------------------- Stats personajes --------------------------------------
#    mirek.stats()
#    ruben.stats()
#    sebas.stats()
#    bugatti.stats()
#    norman.stats()
#    master.stats()
    
#    
#    master.moverse()
#    master.moverse()
#    master.moverse()
#    master.moverse()
#    master.moverse()
    
    #----------------------- Prueba pelear -------------------------------------
#    enemigo = Enemigo(120, 17, 17, 17, 13, 17, "Sub Bismark", "Saludable", "Fragmento de libro de secretos", "SCP", 9, 1, "zona")
#    e_presentes.append(enemigo)
#    campamento.enemigos_activos()[0].append(enemigo)
#    campamento.cantidades_enemigos()[0].append(1)
#    o= Juego.tranformar_objeto("Control universal")
#    campamento.objetos_activos()[0].append(o)
#    campamento.cantidades()[0].append(1)
#    campamento.objetos()[0].append(o.nombre)
#    sebas.anadir_obj(o)
#    o= Juego.tranformar_objeto("Pila")
#    campamento.objetos_activos()[0].append(o)
#    campamento.cantidades()[0].append(1)
#    campamento.objetos()[0].append(o.nombre)
#    sebas.anadir_obj(o)
#    sebas.stats()
#    enemigo.stats()
#    Juego.pelea([sebas],e_presentes)
#    asistente = Asistente(120, 17, 17, 17, 13, 17, "Sub Bismark", "Saludable", "Fragmento de libro de secretos", "SCP", 9, 1, "Cabana", ruben, "Queso")
#    print(type(asistente) == Asistente)
    #----------------------- Usar objeto especial ----------------------------------
#    e_presentes = []
#    enemigo = Enemigo(120, 17, 17, 17, 13, 17, "Sub Bismark", "Saludable", "Fragmento de libro de secretos", "SCP", 9, 1)
#    e_presentes.append(enemigo)
#    pueblo.enemigos_activos()[2].append(enemigo)
#    pueblo.cantidades_enemigos()[2].append(1)
#    enemigo = Enemigo(120, 17, 17, 17, 13, 17, "Alumno Pasio", "Saludable", "Fragmento de libro de secretos", "SCP", 9, 1)
#    e_presentes.append(enemigo)
#    pueblo.enemigos_activos()[2].append(enemigo)
#    pueblo.cantidades_enemigos()[2].append(1)
#    master.moverse()
#    anadir_obj_manual("Alcohol", master)
#    enemigo.stats()
#    Juego.pelea([master],e_presentes)
    
    #----------------------- Usar binoculares --------------------------------------
#    master.moverse()
#    anadir_obj_manual("Binoculares", master)
#    master.usar_obj()
    
    #----------------------- Metodo casino -----------------------------------------
#    for i in range(0,5):
#        o = Juego.tranformar_objeto("Comida")
#        master.ubicacion.objetos_activos()[2].append(o)
#        master.anadir_obj(o)
#    master.stats()
#    Juego.casino(master)
#    master.stats()
    
    #----------------------- Metodo monopoly ---------------------------------------
#    o = Juego.tranformar_objeto("Fragmento de libro de secretos")
#    mercado.objetos_activos()[0].append(o)
#    master.anadir_obj(o)
#    master.comprar()
#    master.stats()
    
    #----------------------- Metodo escalera ---------------------------------------
#    esc = [mirek, 0, 0, 0, 0]
#    for i in range(0, 25):
#        print(esc)
#        esc = Juego.escalera(esc[0], esc[1], esc[2], esc[3], esc[4])

    #----------------------- Minar -------------------------------------------------
#    mirek.moverse(mina, "Tuneles")
#    mirek.buscar("Oro")
#    mirek.stats()

    #----------------------- Moverse -----------------------------------------------
#    mirek.moverse()
#    mirek.stats()
#    mirek.moverse()
    
#    ninja.moverse()
#    ninja.stats()
#    ninja.moverse()
#    ninja.stats()
#    ninja.moverse()

    #----------------------- Buscar ------------------------------------------------
#    mirek.buscar("Disfraz")
#    mirek.buscar()
#    mirek.stats()
#    print(buscaLugar("Cabana").nombre)
    
    #----------------------- Condiciones de batalla --------------------------------
#    mirek.condicion.pop('Saludable')
#    mirek.condicion.update({"Envenenado III": 3})
#    for i in range(0,4):
#        mirek.efecto(3-i)
#        print("Recibiendo daño...")
#        mirek.stats()
#    mirek.cambiar_hp(-26)
#    mirek.stats()
    
    #----------------------- Subir de nivel ----------------------------------------
#    norman.subir_nivel()

    #----------------------- Obtener objeto ----------------------------------------
#    mirek.moverse(pueblo, "Ayuntamiento")
#    mirek.stats()
#    mirek.cambiar_hp(-16)
#    mirek.anadir_obj(o)
#    mirek.usar_obj(o)
#    mirek.stats()
#    print("----------------------------------------------------------------------")
#    ruben.moverse(pueblo, "Ayuntamiento")
#    mirek.stats()
#    ruben.stats()
#    ruben.cambiar_hp(-5)
#    mirek.anadir_obj(o)
#    mirek.stats()
#    mirek.usar_obj(o, "Ruben")
#    ruben.stats()
#    print("----------------------------------------------------------------------")
#    ruben.moverse(pueblo, "Comunidad")
#    mirek.stats()
#    ruben.stats()
#    ruben.cambiar_hp(-5)
#    mirek.anadir_obj(o)
#    mirek.usar_obj(o, "Ruben")
#    ruben.stats()
#    print("----------------------------------------------------------------------")
    
    #----------------------- Cadaver de usuario ------------------------------------
#    mirek.cambiar_hp(-100)
#    o = Juego.tranformar_objeto("Cadaver de Mirek")
#    sebas.anadir_obj(o)
#    sebas.stats()
    
    #----------------------- Metodo maquina ----------------------------------------
#    anadir_obj_manual("Fragmento de libro de secretos", master)
#    Juego.maquina("Fragmento de libro de secretos", master)
    
#    master.arbol_habilidades()
    
    #----------------------- Metodo atacar -----------------------------------------
#    mirek.atacar(e_presentes)
#    bugatti.moverse(campamento, "Comedor")
#    mirek.moverse(campamento, "Comedor")
#    bugatti.anadir_obj(o)

    #----------------------- Metodo shuffleproplus ---------------------------------
#    shuffleproplus([bugatti])
#    mirek.stats()
#    bugatti.stats()
    
    #----------------------- Metodo explorar ---------------------------------------
#    print(mirek.mapa)
#    print(mirek.explorar())
#    mirek.moverse(campamento, "Almacen")
#    print(mirek.mapa)
#    print(mirek.explorar())
#    mirek.moverse(campamento, "Puesto de seguridad")
#    print(mirek.explorar())
#    print(mirek.explorar())
    
main()