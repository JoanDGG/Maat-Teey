# -*- coding: ISO-8859-1 -*-
import pandas as pd
import numpy as np
from Lugares import Lugar


Data_enemigos = pd.read_csv("D-D_Enemigos_3.csv")
Data_objetos2 = pd.read_csv("D-D_Objetos_3.csv", index_col = "Nombre")

Data_objetos  = pd.read_csv("D-D_Objetos_3.csv")
Dfnombres_objetos       = Data_objetos.loc[:,["Nombre"]]
Dfestadisticas_objetos  = Data_objetos.loc[:,["Estadistica"]]
Dfboosteos_objetos      = Data_objetos.loc[:,["Boosteo"]]
Dfmejoras_objetos       = Data_objetos.loc[:,["Mejora"]]
#------
Dfestropeos_objetos     = Data_objetos.loc[:,["Estropeo"]]
Dfespacios_objetos      = Data_objetos.loc[:,["Espacio"]]
Dfusos_objetos          = Data_objetos.loc[:,["Usos"]]
Dfcantidades_objetos    = Data_objetos.loc[:,["Cantidad"]]

Dfnombres_enemigos      = Data_enemigos.loc[:,["Nombre"]]
Dfcantidades_enemigos   = Data_enemigos.loc[:,["Cantidad"]]
Dfdificultad_enemigos   = Data_enemigos.loc[:,["Dificultad"]]
Dfcategorias_enemigos   = Data_enemigos.loc[:,["Categoria"]]
Dfintimidar_enemigos    = Data_enemigos.loc[:, ["Intimidar"]]
Dftranquilizar_enemigos = Data_enemigos.loc[:, ["Tranquilizar"]]
Dfpersuadir_enemigos    = Data_enemigos.loc[:, ["Persuadir"]]

jefes = {"Zombie policia": "Puesto de seguridad", 
         "Siren Head": "Aire libre", 
         "Chaman demente": "Casa de chaman", 
         "Wendigo Azteca": "Zona clausurada", 
         "Rat King": "Sala de investigacion", 
         "Sub Bismark": "Carguero", 
         "Shombie": "Carniceria", 
         "Doctor": "Cabana doctor", 
         "Jenauu Ja": "Submarino",
         "SCP-3000": "Profundidades",
         "Kuiy Jam": "Mar", 
         "Magnate": "Banco", 
         "Ogro": "Casa ogro",
         "Basilisco": "Entrada mistica",
         "???": "Sala principal",
         "Arana": "Cueva",
         "SCP-953": "Cuarto de contencion SCP-953",
         "SCP-1048": "Cuarto de contencion SCP-1048",
         "SCP-4715": "Cuarto de contencion SCP-4715",
         "SCP-076": "Cuarto de contencion SCP-076",
         "SCP-439": "Cuarto de contencion SCP-439",
         "Chaman poseido": "Puerta",
         "Senuelo": ["comedor", "almacen", "cabanas vecinas", 
                     "puesto de seguridad", "entrada"]
         }

jefes_no_jefes = list(jefes.keys()) + ["Policia", "Guardabosques", "Lobo feroz", 
                     "Big foot", "Maykuyak Teey", "Burgues", "Magnate boosted", 
                     "Cocinendigo", "Cocinero", "Rata de dos patas", "Goat Z", 
                     "King of the mountain", "Ae", "Sr. Smith"]

enemigos_op = list(jefes.keys()) + ["Alumno Revo", "Mentor Revo", "Lobo", 
                  "Zombie chasqueador", "Murcielagos", "Wendigos", "Cocinendigo", 
                  "King of the mountain", "Vampiro", "SCP 953", "SCP 1048", 
                  "SCP 4715", "SCP 076", "SCP 439", "Norman", "Mirek", "Ruben", 
                  "Turati", "Sebas"]

atrapables = ["Lobo", "Oso", "Murcielago", "Serpiente", 
              "Anguila electrica", "Rata", "Rata de dos patas", "Aguila", 
              "Cocodrilo", "Trol", "Oso marino", "Wendigo"]

atrapables_medianos = ["Lobo", "Murcielago", "Serpiente", 
                       "Anguila electrica", "Rata", "Rata de dos patas", "Aguila"]

atrapables_trampa_osos = ["Lobo", "Oso", "Rata de dos patas", 
                     "Cocodrilo", "Trol", "Oso marino"]

domables = ["Lobo", "Oso", "Murcielago", "Serpiente", "Anguila electrica", 
            "Rata", "Aguila", "Cocodrilo", "Trol", "Oso marino"]

# Añadir zombies, humanos, monstruos, que no son jefes 
# ni cocineros en atrapables por trampa de osos
for enemigo in range(0, len(Dfcantidades_enemigos)):
    if(Dfcantidades_enemigos.iloc[enemigo,0] == "Zombie" 
       or Dfcantidades_enemigos.iloc[enemigo,0] == "Humano" 
       or Dfcantidades_enemigos.iloc[enemigo,0] == "Monstruo"):
        if(Dfnombres_enemigos.iloc[enemigo,0] not in jefes 
           and Dfnombres_enemigos.iloc[enemigo,0] not in jefes_no_jefes 
           and Dfnombres_enemigos.iloc[enemigo,0] not in atrapables_trampa_osos):
            atrapables_trampa_osos.append(Dfnombres_enemigos.iloc[enemigo,0])

lugares = ["Campamento", "Bosque", "Pueblo", "Mina", "Edificio Abandonado", 
           "Puerto", "Normancueva", "Deshuesadero", "Montana", "Mercado", "Puerta", 
           "Fondo del mar", "Pantano", "Mejoras"]
fin = False
dificultad = 1

consejos = [
            #--------------------------------------------------------Consejos utiles
            "**************Sabias que**************\nPara la gente de la montaña, "
            + "comer carne no es de Dios",
            "OFERTA TENEDORES AL 2X1 :D",
            "Tratar de mejorar lo inmejorable no siempre es bueno...",
            "La lagrima de una niña mata mas rapido que un ataque al corazon",
            "La respuesta no siempre es la violencia <3",
            "La basura de unos es el tesoro de otros",
            "owo",
            "Queso Gromit!!!",
            "Un buen amigo nunca muere en realidad",
            "Una herramienta es tan buena como su usuario",
            "Encontramos las armas mas poderosas en los objetos que no buscamos..",
            "Un buen guerrero nunca descuida sus debilidades",
            "En las Vegas, la casa siempre gana",
            "Viajar ligero siempre viene bien para viajes largos",
            "El mejor amigo del hombre no necesariamente es un perro",
            #----------------------------------------------------------Consejos trol
            "Quien vive en una piña debajo del mar...",
            "Lavate tus dientes tres veces al dia :)",
            "Mira ambos lados antes de cruzar la calle",
            "Despues de comer, debes esperar una hora antes de entrar al agua",
            "Si no tienes nada que perder a que le tienes miedo",
            "La ley de la confianza brotheeeeeeeer",
            "Los accidentes no existen",
            "Si no sabes a donde ir, no importa que camino sigas"
            ]

# 
sabiduria_del_mas_alla = [
                            ""
                            ]

mapa_master  = {#---------------------------------------------------------Campamento
                "Cabana":  ["Comedor", "Cabanas vecinas", "Almacen"],
                "Comedor": ["Cabana", "Cabanas vecinas", "Almacen"], 
                "Almacen": ["Cabana", "Comedor", "Cabanas vecinas", 
                            "Puesto de seguridad"], 
                "Cabanas vecinas": ["Cabana", "Comedor", "Almacen"], 
                "Puesto de seguridad": ["Almacen", "Pradera"],
                #-------------------------------------------------------------Bosque
                "Aire libre": ["Entrada mina bosque", "Cabana de guardabosques", 
                               "Pradera", #-------------------------------Campamento
                               "Comunidad", #---------------------------------Pueblo
                               "Bahia",#--------------------------------------Puerto
                               "Corazon del bosque",#------------------------Montana
                               "Exterior",#----------------------------------Pantano
                               "Carretera"],
                "Cabana de guardabosques": ["Aire libre"],
                "Entrada mina bosque": ["Aire libre", "Tunel salida bosque"],
                "Pradera": ["Puesto de seguridad", "Aire libre", "Casa"],
                "Corazon del bosque": ["Subida", "Aire libre", "Templo"],
                "Carretera": ["Comunidad", "Entrada", "Aire libre"],
                #-------------------------------------------------------------Pueblo
                "Comunidad": ["Aire libre", "Ayuntamiento", "Mercado", 
                              "Casa de chaman", "Entrada mina pueblo", "Carretera"],
                "Casa de chaman": ["Comunidad"],
                "Ayuntamiento": ["Comunidad"],
                "Entrada mina pueblo": ["Comunidad", "Tunel salida pueblo"],
                #---------------------------------------------------------------Mina
                "Zona de exploracion I": ["Zona de exploracion II", 
                                          "Tunel de exploracion I"],
                "Zona de exploracion II": ["Zona de exploracion I", 
                                           "Tunel de exploracion II", 
                                           "Tunel salida deshuesadero"],
                "Tunel de exploracion I": ["Zona de exploracion I", 
                                           "Puestos de trabajo"],
                "Tunel de exploracion II": ["Zona de exploracion II", 
                                            "Puestos de trabajo"],
                "Tunel salida bosque": ["Entrada mina bosque", 
                                        "Puestos de trabajo"],
                "Tunel salida pueblo": ["Entrada mina pueblo", 
                                        "Puestos de trabajo"],
                "Tunel salida pantano": ["Entrada mina pantano", 
                                         "Puestos de trabajo"],
                "Tunel salida deshuesadero": ["Entrada mina deshuesadero", 
                                              "Zona de exploracion II"],
                "Tunel ???": ["Templo", "Zona clausurada"],
                "Tunel derrumbado": ["Zona clausurada", "Puestos de trabajo"],
                "Puestos de trabajo": ["Tunel de exploracion I", 
                                       "Tunel de exploracion II", 
                                       "Tunel salida bosque", 
                                       "Tunel salida pueblo", 
                                       "Tunel salida pantano", 
                                       "Tunel derrumbado"],
                "Zona clausurada": ["Tunel derrumbado", "Tunel ???"],
                #-----------------------------------------------------------Edificio
                "Entrada": ["Exterior", "Carretera", "Escalera", "Laboratorio", 
                            "Sala de investigacion", "Submarino"],
                "Maquina": ["Escalera"],
                "Escalera": ["Entrada", "Laboratorio", "Sala de investigacion"],
                "Laboratorio": ["Entrada", "Escalera", "Sala de investigacion"],
                "Sala de investigacion": ["Entrada", "Laboratorio", 
                                          "Escalera", "Bahia"],
                #-------------------------------------------------------------Puerto
                "Bahia": ["Sala de investigacion", "Carguero", "Aire libre", "Mar"],
                "Carguero": ["Bahia", "Mar"],
                #--------------------------------------------------------Normancueva
                "Entrada mistica": ["Mar", "Sala principal"],
                "Sala principal": ["Entrada mistica"],
                #-------------------------------------------------------Deshuesadero
                "Casa": ["Pradera", "Sotano"],
                "Sotano": ["Casa", "Carniceria", "Basurero", "Alacena"],
                "Carniceria": ["Sotano", "Alacena"],
                "Basurero": ["Sotano", "Entrada mina deshuesadero"],
                "Alacena": ["Sotano", "Carniceria"],
                "Entrada mina deshuesadero": ["Basurero", 
                                              "Tunel salida deshuesadero"],
                #------------------------------------------------------------Montana
                "Cabana doctor": ["Cima"],
                "Cima": ["Cabana doctor", "Subida"],
                "Subida": ["Cima", "Corazon del bosque"],
                #------------------------------------------------------------Pantano
                "Zona de control": ["Exterior"],
                "Exterior": ["Aire libre", "Zona de control", "Casa ogro"],
                "Casa ogro": ["Exterior", "Entrada mina pantano"],
                "Entrada mina pantano": ["Casa ogro", "Tunel salida pantano"],
                #------------------------------------------------------Fondo del mar
                "Submarino": ["Entrada", "Profundidades"],
                "Profundidades": ["Submarino", "Mar"],
                "Mar": ["Profundidades", "Bahia", "Carguero", "Entrada mistica"],
                #------------------------------------------------------------Mercado
                "Mercado": ["Banco", "Comunidad"],
                "Banco": ["Mercado"],
                #-------------------------------------------------------------Puerta
                "Templo": ["Cueva", "Corazon del bosque", "Tunel ???"],
                "Cueva": ["Templo", "Tunel misterioso", "Tunel rocoso", 
                          "Tunel terrible", "Tunel negro", "Tunel Siniestro"],
                "Tunel misterioso": ["Cueva", "Cuarto de contencion scp 953"],
                "Tunel rocoso": ["Cueva", "Cuarto de contencion scp 076"],
                "Tunel terrible": ["Cueva", "Cuarto de contencion scp 1048"],
                "Tunel negro": ["Cueva", "Cuarto de contencion scp 439"],
                "Tunel siniestro": ["Cueva", "Cuarto de contencion scp 4715"],
                "Cuarto de contencion scp 953": ["Tunel misterioso", "Puerta"], 
                "Cuarto de contencion scp 076": ["Tunel rocoso", "Puerta"], 
                "Cuarto de contencion scp 1048": ["Tunel terrible", "Puerta"], 
                "Cuarto de contencion scp 439": ["Tunel negro", "Puerta"],
                "Cuarto de contencion scp 4715": ["Tunel siniestro", "Puerta"],
                "Puerta": ["Tunel misterioso", 
                           "Cuarto de contencion scp 953", 
                           "Cuarto de contencion scp 076", 
                           "Cuarto de contencion scp 1048", 
                           "Cuarto de contencion scp 439",
                           "Cuarto de contencion scp 4715"],
                #-------------------------------------------------------Viaje astral
                "camion": ["cabana", "cabanas vecinas"],
                "cabana":  ["comedor", "cabanas vecinas", "almacen", "camion"],
                "comedor": ["cabana", "cabanas vecinas", "almacen"], 
                "almacen": ["cabana", "comedor", "cabanas vecinas", 
                            "puesto de seguridad"], 
                "cabanas vecinas": ["cabana", "comedor", "almacen", "camion"], 
                "puesto de seguridad": ["almacen", "pradera"],
                "aire libre": ["pradera", "carretera"],
                "pradera": ["puesto de seguridad", "aire libre"],
                "carretera": ["entrada", "aire libre"],
                "entrada": ["carretera", "Sala principal"]
                }

mapa_mirek   = {"Cabana":  ["Comedor", "Cabanas vecinas", "Almacen"],
                "Comedor": ["Cabana", "Cabanas vecinas", "Almacen"], 
                "Almacen": ["Cabana", "Comedor", "Cabanas vecinas"], 
                "Cabanas vecinas": ["Cabana", "Comedor", "Almacen"]}
mapa_sebas   = mapa_mirek.copy()
mapa_ruben   = mapa_mirek.copy()
mapa_bugatti = mapa_mirek.copy()
mapa_norman  = mapa_mirek.copy()

crafteos = {("Tela", "Hilo"): "Sombrero",
            ("Tela", "Tela", "Hilo"): "Capa",
            ("Polvora", "Piedra", "Lodo"): "Dinamita",
            ("Ojo de vaca", "Hongo", "Botella"): "Veneno I",
            ("Rifle", "Mira de rifle"): "Sniper",
            ("Casco", "Linterna", "Cuerda"): "Casco con linterna",
            ("Hongo", "Planta azul"): "Comida",
            ("Hongo", "Planta blanca"): "Comida",
            ("Hongo", "Planta roja"): "Comida",
            ("Hongo", "Planta verde"): "Comida",
            ("Hongo", "Planta morada"): "Comida",
            ("Hongo", "Planta amarilla"): "Comida",
            ("Hongo", "Planta naranja"): "Comida",
            ("Bate", "Clavos"): "Bate con clavos",
            ("Capa", "Sombrero", "Chaqueta de cuero"): "Disfraz",
            ("Hierro", "Hierro", "Hierro", "Hierro"): "Pechera",
            ("Hierro", "Hierro", "Hierro"): "Pantalones",
            ("Hierro", "Hierro"): "Casco",
            ("Hierro"): "Botas",
            ("Carnada", "Hierro"): "Anzuelo",
            ("Anzuelo", "Rama", "Cuerda"): "Cana",
            ("Rama", "Hierro", "Hierro", "Cuerda"): "Pico de hierro",
            ("Rama", "Hierro", "Cuerda"): "Hacha",
            ("Rama", "Rama", "Rama", "Cuerda"): "Arco",
            ("Rama", "Piedra"): "Flecha",
            ("Rama", "Piedra", "Pluma"): "Flecha mejorada",
            ("Lena", "Aceite", "Fosforo"): "Antorcha",
            ("Lena", "Aceite", "Encendedor"): "Antorcha",
            ("Lena", "Aceite", "Antorcha"): "Antorcha",
            ("Lena", "Aceite de pecao", "Fosforo"): "Antorcha",
            ("Lena", "Aceite de pecao", "Encendedor"): "Antorcha",
            ("Lena", "Aceite de pecao", "Antorcha"): "Antorcha",
            ("Lena", "Gasolina", "Fosforo"): "Antorcha",
            ("Lena", "Gasolina", "Encendedor"): "Antorcha",
            ("Lena", "Gasolina", "Antorcha"): "Antorcha",
            ("Lena", "Alcohol", "Fosforo"): "Antorcha",
            ("Lena", "Alcohol", "Encendedor"): "Antorcha",
            ("Lena", "Alcohol", "Antorcha"): "Antorcha",
            ("Rama", "Aceite", "Fosforo"): "Antorcha",
            ("Rama", "Aceite", "Encendedor"): "Antorcha",
            ("Rama", "Aceite", "Antorcha"): "Antorcha",
            ("Rama", "Aceite de pecao", "Fosforo"): "Antorcha",
            ("Rama", "Aceite de pecao", "Encendedor"): "Antorcha",
            ("Rama", "Aceite de pecao", "Antorcha"): "Antorcha",
            ("Rama", "Gasolina", "Fosforo"): "Antorcha",
            ("Rama", "Gasolina", "Encendedor"): "Antorcha",
            ("Rama", "Gasolina", "Antorcha"): "Antorcha",
            ("Rama", "Alcohol", "Fosforo"): "Antorcha",
            ("Rama", "Alcohol", "Encendedor"): "Antorcha",
            ("Rama", "Alcohol", "Antorcha"): "Antorcha",
            ("Veneno I", "Hongo"): "Antidoto I",
            ("Esencia salud I", "Planta blanca"): "Pocion salud I",
            ("Esencia fuerza I", "Planta roja"): "Pocion fuerza I",
            ("Esencia resistencia I", "Planta azul"): "Pocion resistencia I",
            ("Esencia carisma I", "Planta amarilla"): "Pocion carisma I",
            ("Esencia inteligencia I", "Planta verde"): "Pocion inteligencia I",
            ("Esencia sabiduria I", "Planta morada"): "Pocion sabiduria I",
            ("Esencia energia I", "Planta naranja"): "Pocion energia I",
            ("Esencia velocidad I", "Planta azul", "Planta blanca", 
             "Planta roja"): "Pocion velocidad I",
            ("Esencia invisibilidad I", "Planta azul", "Planta verde", 
             "Planta morada"): "Pocion invisibilidad I",
            ("Veneno II", "Hongo", "Hongo"): "Antidoto II",
            ("Esencia salud II", "Planta blanca", 
             "Planta blanca"): "Pocion salud II",
            ("Esencia fuerza II", "Planta roja", 
             "Planta roja"): "Pocion fuerza II",
            ("Esencia resistencia II", "Planta azul", 
             "Planta azul"): "Pocion resistencia II",
            ("Esencia carisma II", "Planta amarilla", 
             "Planta amarilla"): "Pocion carisma II",
            ("Esencia inteligencia II", "Planta verde", 
             "Planta verde"): "Pocion inteligencia II",
            ("Esencia sabiduria II", "Planta morada", 
             "Planta morada"): "Pocion sabiduria II",
            ("Esencia energia II", "Planta naranja", 
             "Planta naranja"): "Pocion energia II",
            ("Esencia velocidad II", "Planta azul", "Planta blanca", 
             "Planta roja"): "Pocion velocidad II",
            ("Esencia invisibilidad II", "Planta azul", "Planta verde", 
             "Planta morada"): "Pocion invisibilidad II",
            ("Veneno III", "Hongo", "Hongo", "Hongo"): "Antidoto III",
            ("Esencia salud III", "Planta blanca", "Planta blanca", 
             "Planta blanca"): "Pocion salud III",
            ("Esencia fuerza III", "Planta roja", "Planta roja", 
             "Planta roja"): "Pocion fuerza III",
            ("Esencia resistencia III", "Planta azul", "Planta azul", 
             "Planta azul"): "Pocion resistencia III",
            ("Esencia carisma III", "Planta amarilla", "Planta amarilla", 
             "Planta amarilla"): "Pocion carisma III",
            ("Esencia inteligencia III", "Planta verde", "Planta verde", 
             "Planta verde"): "Pocion inteligencia III",
            ("Esencia sabiduria III", "Planta morada", "Planta morada", 
             "Planta morada"): "Pocion sabiduria III",
            ("Esencia energia III", "Planta naranja", "Planta naranja", 
             "Planta naranja"): "Pocion energia III",
            ("Esencia velocidad III", "Planta azul", "Planta blanca", 
             "Planta roja"): "Pocion velocidad III",
            ("Esencia invisibilidad III", "Planta azul", "Planta verde", 
             "Planta morada"): "Pocion invisibilidad III"}

habilidades = {"Jugar": {"Sabiduria del mas alla": 34, "Pociones": 22, 
                         "Boosteo": 34}, 
               "Turno personaje": {"Disfraz": 10, "Carisma absoluta": 22, 
                                   "Grito de guerra": 34, "Habilidad animal": 22, 
                                   "Invocar animal": 34, "Special Curry": 10, 
                                   "Kaio Ken": 10, "Ultra instinto": 34, 
                                   "Analitico": 22, "Momazo": 10, 
                                   "Meme de enemigos": 22, "Lord meme": 34, 
                                   "Robots": 22, "Boosteo": 34, 
                                   "Llamar al viento": 22, "Mente dormida": 34},
               "Turno enemigo": {"Anticipacion": 10},
               "Buscar": {"Explorador": 0, "Vision nocturna": 0},
               "Iniciar pelea": {"Explorador": 34},
               "Actualizar stats": {"Super sayain": 0, "Bolsa magica": 0},
               "Usar obj": {"Nutrirse": 0},
               "Atacar personaje": {"Critical": 0, "Kaio Ken": 0, 
                                    "Smash ball": 34, "Cazador": 0},
               "Atacar enemigo": {"Simpatizar con animales": 0, 
                                  "Ultra instinto": 0, "Kaio Ken": 0},
               "Maquina": {"Artesano": 22, "Alquimista": 34}}

dia = True
count_turnos = 0
lugares_iluminados = ["Puesto de seguridad", "Cabana de guardabosques", "Comunidad", 
              "Ayuntamiento", "Puestos de trabajo", "Laboratorio", 
              "Sala de investigacion", "Sala principal", "Casa", "Sotano", 
              "Carniceria", "Alacena", "Cabana doctor", "Zona de control", 
              "Mercado", "Banco", "puesto de seguridad"]

# Enemigos que dropean carne
carneables = []

notaxeables = ["Zombie Base", "Zombie corredor", "Acechadores", 
               "Zombie chasqueador", "Zombie gordinflon", "Wendigos", 
               "Zombie Obrero", "Zombie pescador", "Anguilas electricas", 
               "Cocinendigo", "Shombie", "Sr. Smith"]
multiples = ["Gasolina", "Gasolina de pecao", "Aceite", "Aceite de pecao", 
             "Dinamita", "Lodo", "Fosforo", "Antorcha", "Encendedor"]
armash_shidas = ["Cushillo", "Mashete", "Eshpada", "Eshpada mejorada"]


cabeza = ["Sombrero", "Casco con linterna", "Casco", "Peluca"]
cara = ["Lector de poder", "Lector de poder mejorado", "Lentes"]
cuello = ["Pin", "Pin de bob esponja", "Simbolo comunidad"]
torso = ["Chaqueta de cuero", "Pechera", "Abrigo"]
piernas = ["Pantalones", "Shorts"]
pies = ["Botas", "Crocks"]
espalda = ["Maleta", "Capa", "Mochila", "Mochila campista", "Cubeta", 
           "Shaed", "Shaed mejorado"]
cuerpo_completo = ["Disfraz", "Traje de obrero", "Traje de buzo", 
                   "Traje de buzo mejorado"]
equipables = (cabeza + cara + cuello + torso + piernas + pies + espalda 
              + cuerpo_completo)
mochilas = ["Mochila", "Mochila campista", "Mochila mejorada", "Maleta", "Cubeta"]
         
agua = ["Profundidades", "Mar"]

def anadir_obj_manual(nombre, personaje, cantidad = None):
    from Juegos import Juego

    indice = personaje.ubicacion.zonas.index(personaje.zona)    
    if("sabia" in nombre):
        boosteo = sabiduria_del_mas_alla[dados(1, len(sabiduria_del_mas_alla))[0]-1]
        nombre = "Nota de consejo"
        objeto = Juego.tranformar_objeto(nombre, cantidad)
        objeto.boosteo = boosteo
    else:
        objeto = Juego.tranformar_objeto(nombre, cantidad)
    
    if(objeto.nombre == "Nota de consejo" and "sabia" not in objeto.nombre):
        objeto.boosteo = consejos[dados(1, len(consejos))[0]-1]
    
    personaje.ubicacion.objetos_activos[indice].append(objeto)
    personaje.ubicacion.cantidades[indice].append(1)
    personaje.ubicacion.objetos[indice].append(objeto.nombre)
    personaje.anadir_obj(objeto)
    return True

def busca_lugar(zona: str):
    # Sacar lugar a partir de zona
    for lugar_original in range(0, len(objetos_lugares)):
            if(zona in objetos_lugares[lugar_original].zonas):
                lugar = objetos_lugares[lugar_original]
                break
    return lugar

def dados(cantidad_dados: int, cantidad_caras: int):
    #DEBUG
#    print("----------------------------------------------------------Metodo dados")
    if(cantidad_dados == 0):
        return 0
    tiradas = []
    for indice in range (0, cantidad_dados):
        tiradas.append(np.random.randint(1, cantidad_caras + 1))
    return tiradas

def eliminar(lista):
    for elemento in lista:
        del(elemento)
    return True

def generar_carneables():
    categorias_si = ["Animal", "Monstruo", "Zombie"]
    nombres = Dfnombres_enemigos
    categorias = Dfcategorias_enemigos
    for indice in range(0, len(nombres)):
        if(categorias.iloc[indice,0] in categorias_si) and (nombres.iloc[indice,0] 
        not in carneables) and (nombres.iloc[indice,0] not in jefes.keys()):
            carneables.append(nombres.iloc[indice,0])

def generar_lugar(nombre, zonas):
    enemigos_activos = []
    objetos_activos = []
    for i in range(0, len(zonas)):
        enemigos_activos.append([])
        objetos_activos.append([])
    lugar = Lugar(nombre, zonas,
                  separar("enemigos", nombre, zonas, "elementos"), 
                  separar("enemigos", nombre, zonas, "cantidades"), 
                  separar("objetos", nombre, zonas, "elementos"), 
                  separar("objetos", nombre, zonas, "cantidades"), 
                  enemigos_activos, objetos_activos)
    for i in range (0, len(zonas)):
        lugar.jaulas.append({})
    return lugar

def jamon():
    print("JAMON")

def queso():
    print("Queso")

def malo():
    return personajes[dados(1, len(personajes))[0]-1]

def mezclar_listas(lista1, lista2, tipo):
    # Tipo 1 = Lista simple, tipo 2 = Lista de listas
    lista3 = []
    lista4 = []
    
    for i in range (0, len(lista1)):
        if(tipo == 1):
            lista3.append([])
            lista4.append([])
            for j in range(0, len(lista1[i])):
                lista3[i].append("")
                lista4[i].append("")
        elif(tipo == 2):
            lista3.append("")
            lista4.append("")
    
    
    if(tipo == 1):
        c=0
        while "" in lista3:
            valor = np.random.randint(0, len(lista1))
            if(lista3[valor] == ""):
                lista3[valor] = lista1[c]
                lista4[valor] = lista2[c]
                c+=1
    elif(tipo == 2):
        for h in range (0, len(lista1)):
            c=0
            while "" in lista3[h]:
                valor = np.random.randint(0, len(lista1[h]))
                if(lista3[h][valor] == ""):
                    lista3[h][valor] = lista1[h][c]
                    lista4[h][valor] = lista2[h][c]
                    c+=1

    return (lista3,lista4)

def repetido(self, lugar, zona:int, jefe:str):
    for enemigo in lugar.enemigos_activos[zona]:
        if(enemigo.nombre == jefe):
            return True
    return False

def revisar_string(nombre):
    # Revisa el texto dividido por diagonales
    salida = ""
    cantidad_diagonales = nombre.count("/")
    tirada = dados(1, cantidad_diagonales + 1)[0]
    contador = 0
    for indice in range(0, len(nombre)):
        if(nombre[indice] == "/"):
            contador += 1
        if(contador == tirada-1):
            indice += 1
            break
    if(tirada != cantidad_diagonales + 1): #-----Revisar en donde esta la n diagonal
        while(nombre[indice] != "/"):
            salida += nombre[indice]
            indice += 1
    else:
        salida = nombre[indice:]
    return salida

def separar(entidades, lugar, zonas, tipo):
    #DEBUG
#    print("------------------------------------------------Metodo separar objetos")
    is_enemigos = False
    if(entidades == "objetos"):
        nombres = Dfnombres_objetos
        cantidades = Dfcantidades_objetos
        is_enemigos = False
    else:
        nombres = Dfnombres_enemigos
        cantidades = Dfcantidades_enemigos
        is_enemigos = True

    elementos = []
    cantidad = []
    for indice in range (0, len(zonas)):
        elementos.append([])
        cantidad.append([])
        
    dentro_de_lugar = False
    indice_elemento = -1
    for indice in range (0, len(nombres)):
        if ((nombres.iloc[indice,0] in lugares and nombres.iloc[indice,0] != lugar) 
            or (nombres.iloc[indice,0] == "")):
            dentro_de_lugar = False
        if(dentro_de_lugar):
            if (nombres.iloc[indice,0] in zonas):
                indice_elemento += 1
            else:
                if(is_enemigos):
                    if(nombres.iloc[indice,0]=="Rat King G" 
                       or nombres.iloc[indice,0]=="Rat King C" 
                       or nombres.iloc[indice,0]=="Cocinero" 
                       or Dfdificultad_enemigos.iloc[indice,0] != dificultad):
                        continue
                elementos[indice_elemento].append(nombres.iloc[indice,0])
                cantidad[indice_elemento].append(cantidades.iloc[indice,0])
        if(nombres.iloc[indice,0] == lugar):
            dentro_de_lugar = True
#    print(elementos)
#    print(cantidad)
    if(tipo == "elementos"):
        return elementos
    elif(tipo == "cantidades"):
        return cantidad

def ubicar(self):
    #DEBUG
#    print("---------------------------------------------------------Metodo ubicar")
    for personaje in personajes:
        print(personaje.nombre + " esta en: " + personaje.ubicacion.nombre 
              + ", en la zona " + personaje.zona)
    print("------------------------------------------------------------------")
    ubicaciones = []
    for indice in range (0, len(personajes)):
        ubicaciones.append(personajes[indice].zona)
    return ubicaciones


campamento    = generar_lugar("Campamento", ["Cabana", "Comedor", 
                                                 "Almacen", "Cabanas vecinas", 
                                                 "Puesto de seguridad"])
bosque        = generar_lugar("Bosque", ["Aire libre", 
                                             "Cabana de guardabosques", 
                                             "Entrada mina bosque", "Pradera", 
                                             "Carretera", "Corazon del bosque"])
pueblo        = generar_lugar("Pueblo", ["Comunidad", "Casa de chaman",
                                             "Ayuntamiento", "Entrada mina pueblo"])
mina          = generar_lugar("Mina", ["Zona de exploracion I", 
                                           "Zona de exploracion II", 
                                           "Tunel salida bosque", 
                                           "Tunel salida pueblo", 
                                           "Tunel salida pantano", 
                                           "Tunel salida deshuesadero", 
                                           "Tunel ???", "Tunel derrumbado", 
                                           "Tunel de exploracion I", 
                                           "Tunel de exploracion II", 
                                           "Puestos de trabajo", "Zona clausurada"])
edificio      = generar_lugar("Edificio Abandonado", ["Entrada", 
                                                          "Maquina", "Escalera", 
                                                          "Laboratorio", 
                                                          "Sala de investigacion"])
puerto        = generar_lugar("Puerto", ["Bahia", "Carguero"])
normancueva   = generar_lugar("Normancueva", ["Sala principal", 
                                                  "Entrada mistica"])
deshuesadero  = generar_lugar("Deshuesadero", ["Casa", "Almacen", "Carniceria", 
                                                   "Basurero", "Alacena", 
                                                   "Entrada mina deshuesadero"])
montana       = generar_lugar("Montana", ["Cabana doctor", "Cima", "Subida"])
mercado       = generar_lugar("Mercado", ["Mercado", "Banco"])
puerta        = generar_lugar("Puerta", ["Templo", "Cueva", "Tunel misterioso", 
                                             "Tunel rocoso", "Tunel terrible", 
                                             "Tunel negro", "Tunel siniestro", 
                                             "Cuarto de contencion scp 953", 
                                             "Cuarto de contencion scp 1048", 
                                             "Cuarto de contencion scp 4715", 
                                             "Cuarto de contencion scp 076", 
                                             "Cuarto de contencion scp 439", 
                                             "Puerta"])
fondo_del_mar = generar_lugar("Fondo del mar", ["Submarino", "Mar", 
                                                    "Profundidades"])
pantano       = generar_lugar("Pantano", ["Zona de control", "Exterior", 
                                              "Casa ogro", "Entrada mina pantano"])
viaje_astral  = generar_lugar("campamento", ["camion", "cabana", "comedor", 
                                                 "almacen", "cabanas vecinas", 
                                                 "puesto de seguridad", 
                                                 "aire libre", "pradera", 
                                                 "carretera", "entrada"])

objetos_lugares = [campamento, bosque, pueblo, mina, edificio, 
             puerto, normancueva, deshuesadero, montana, mercado, 
             puerta, fondo_del_mar, pantano, viaje_astral]

campamento_original = generar_lugar("Campamento", ["Cabana", "Comedor", 
                                                       "Almacen", "Cabanas vecinas", 
                                                       "Puesto de seguridad"])
bosque_original = generar_lugar("Bosque", ["Aire libre", 
                                               "Cabana de guardabosques", 
                                               "Entrada mina bosque", "Pradera", 
                                               "Carretera", "Corazon del bosque"])
pueblo_original = generar_lugar("Pueblo", ["Comunidad", "Casa de chaman", 
                                               "Ayuntamiento", 
                                               "Entrada mina pueblo"])
mina_original = generar_lugar("Mina", ["Zona de exploracion I", 
                                           "Zona de exploracion II", 
                                           "Tunel salida bosque", 
                                           "Tunel salida pueblo", 
                                           "Tunel salida pantano", 
                                           "Tunel salida deshuesadero", 
                                           "Tunel ???", "Tunel derrumbado", 
                                           "Tunel de exploracion I", 
                                           "Tunel de exploracion II", 
                                           "Puestos de trabajo", "Zona clausurada"])
edificio_original = generar_lugar("Edificio Abandonado", ["Entrada", "Maquina", 
                                                              "Escalera", 
                                                              "Laboratorio", 
                                                              "Sala de "
                                                              + "investigacion"])
puerto_original        = generar_lugar("Puerto", ["Bahia", "Carguero"])
normancueva_original   = generar_lugar("Normancueva", ["Sala principal", 
                                                           "Entrada mistica"])
deshuesadero_original  = generar_lugar("Deshuesadero", ["Casa", "Almacen", 
                                                            "Carniceria", 
                                                            "Basurero", "Alacena", 
                                                            "Entrada mina "
                                                            + "deshuesadero"])
montana_original       = generar_lugar("Montana", ["Cabana doctor", "Cima", 
                                                       "Subida"])
mercado_original       = generar_lugar("Mercado", ["Mercado", "Banco"])
puerta_original        = generar_lugar("Puerta", ["Templo", "Cueva", 
                                                      "Tunel misterioso", 
                                                      "Tunel rocoso", 
                                                      "Tunel terrible", 
                                                      "Tunel negro", 
                                                      "Tunel siniestro", 
                                                      "Cuarto de contencion "
                                                      + "scp 953", 
                                                      "Cuarto de contencion "
                                                      + "scp 1048", 
                                                      "Cuarto de contencion "
                                                      + "scp 4715", 
                                                      "Cuarto de contencion "
                                                      + "scp 076", 
                                                      "Cuarto de contencion "
                                                      + "scp 439", "Puerta"])
fondo_del_mar_original = generar_lugar("Fondo del mar", ["Submarino", "Mar", 
                                                             "Profundidades"])
pantano_original       = generar_lugar("Pantano", ["Zona de control", 
                                                       "Exterior", "Casa ogro", 
                                                       "Entrada mina pantano"])
viaje_astral_original  = generar_lugar("campamento", ["camion", "cabana", 
                                                          "comedor", "almacen", 
                                                          "cabanas vecinas", 
                                                          "puesto de seguridad", 
                                                          "aire libre", "pradera", 
                                                          "carretera", "entrada"])

lugares_o_originales = [campamento_original, bosque_original, pueblo_original, 
                        mina_original, edificio_original, puerto_original, 
                        normancueva_original, deshuesadero_original, 
                        montana_original, mercado_original, puerta_original, 
                        fondo_del_mar_original, pantano_original, 
                        viaje_astral_original]

arbol_mirek   = {"A1": [0, 1, "Disfraz"],
                 "A2": [0, 2, "Carisma absoluta"],
                 "A3": [0, 3, "Grito de guerra"],
                 "B1": [0, 1, "Simpatizar con animales"],
                 "B2": [0, 2, "Habilidad animal"],
                 "B3": [0, 3, "Invocar animal"]}

arbol_bugatti = {"A1": [0, 1, "Special curry"],
                 "A2": [0, 2, "Critical"],
                 "A3": [0, 3, "Smash ball"],
                 "B1": [0, 1, "Nutrirse"],
                 "B2": [0, 2, "Artesano"],
                 "B3": [0, 3, "Alquimista"]}

arbol_sebas   = {"A1": [0, 1, "Kaio ken"],
                 "A2": [0, 2, "Super Sayain"],
                 "A3": [0, 3, "Ultra instinto"],
                 "B1": [0, 1, "Anticipacion"],
                 "B2": [0, 2, "Llamar al viento"],
                 "B3": [0, 3, "Mente dormida"]}

arbol_ruben   = {"A1": [0, 1, "Cazador"],
                 "A2": [0, 2, "Analitico"],
                 "A3": [0, 3, "Explorador"],
                 "B1": [0, 1, "Momazo"],
                 "B2": [0, 2, "Meme de enemigos"],
                 "B3": [0, 3, "Lord meme"]}

arbol_norman  = {"A1": [0, 1, "Vision nocturna"],
                 "A2": [0, 2, "Robots"],
                 "A3": [0, 3, "Sabiduria del mas alla"],
                 "B1": [0, 1, "Bolsa magica"],
                 "B2": [0, 2, "Pociones"],
                 "B3": [0, 3, "Boosteo"]}


mirek   = None
bugatti = None
ruben   = None
sebas   = None
norman  = None

master  = None
ninja   = None

personajes = [mirek, bugatti, ruben, sebas, norman]
#personajes = [master, ninja]
#personajes = [ninja]
#personajes = [mirek, bugatti, ruben, sebas, norman, master, ninja]
personajes_muertos = []

personaje_malo = malo()
