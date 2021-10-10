# -*- coding: ISO-8859-1 -*-
import pandas as pd
import numpy as np
from Lugares import Lugar


Data_e=pd.read_csv('D-D_Enemigos_3.csv')
Data_o2=pd.read_csv('D-D_Objetos_3.csv', index_col = "Nombre")

Data_o=pd.read_csv('D-D_Objetos_3.csv')
Dfnombres_o = Data_o.loc[:,['Nombre']]
Dfstats_o = Data_o.loc[:,['Estadistica']]
Dfboosts_o = Data_o.loc[:,['Boosteo']]
Dfmejoras_o = Data_o.loc[:,['Mejora']]
#------
Dfestropeos_o = Data_o.loc[:,['Estropeo']]
Dfespacios_o = Data_o.loc[:,['Espacio']]
Dfusos_o = Data_o.loc[:,['Usos']]
Dfcant_o = Data_o.loc[:,['Cantidad']]
Dfprecio_t = Data_o.loc[:,['Precio']]

Dfnombres_e = Data_e.loc[:,['Nombre']]
Dfcant_e = Data_e.loc[:,['Cantidad']]
Dfdifi_e = Data_e.loc[:,['Dificultad']]
Dfcategorias_e = Data_e.loc[:,['Categoria']]
Dfintimidar_e = Data_e.loc[:, ['Intimidar']]
Dftranquilizar_e = Data_e.loc[:, ['Tranquilizar']]
Dfpersuadir_e = Data_e.loc[:, ['Persuadir']]

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

atrapables_t_osos = ["Lobo", "Oso", "Rata de dos patas", 
                     "Cocodrilo", "Trol", "Oso marino"]

domables = ["Lobo", "Oso", "Murcielago", "Serpiente", "Anguila electrica", 
            "Rata", "Aguila", "Cocodrilo", "Trol", "Oso marino"]

# Añadir zombies, humanos, monstruos, que no son jefes 
# ni cocineros en atrapables por trampa de osos
for e in range(0, len(Dfcategorias_e)):
    if(Dfcategorias_e.iloc[e,0] == "Zombie" or Dfcategorias_e.iloc[e,0] == "Humano" 
    or Dfcategorias_e.iloc[e,0] == "Monstruo"):
        if(Dfnombres_e.iloc[e,0] not in jefes and Dfnombres_e.iloc[e,0] 
        not in jefes_no_jefes and Dfnombres_e.iloc[e,0] not in atrapables_t_osos):
            atrapables_t_osos.append(Dfnombres_e.iloc[e,0])

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
iluminados = ["Puesto de seguridad", "Cabana de guardabosques", "Comunidad", 
              "Ayuntamiento", "Puestos de trabajo", "Laboratorio", 
              "Sala de investigacion", "Sala principal", "Casa", "Sotano", 
              "Carniceria", "Alacena", "Cabana doctor", "Zona de control", 
              "Mercado", "Banco", "puesto de seguridad"]

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


def eliminar(lista):
    for l in lista:
        del(l)
    return True

def buscaLugar(zona: str):
    for l in range(0, len(lugares_o)):   # Sacar lugar a partir de zona
            lug = lugares_o[l].zonas
            if(zona in lug):
                lugar = lugares_o[l]
                break
    return lugar

def revisar_string(nombre):
    s=""
    cantidad = nombre.count("/")
    tirada = dados(1,cantidad+1)[0]
    i=0
    for l in range(0, len(nombre)):
        if(nombre[l] == "/"):
            i+=1
        if(i == tirada-1):
            l+=1
            break
    if(tirada != cantidad+1): #-------Revisar en donde esta la n diagonal
        while(nombre[l] != "/"):
            s+=nombre[l]
            l+=1
    else:
        s = nombre[l:]
    return s

def anadir_obj_manual(nombre, personaje, cant = None):
    from Juegos import Juego

    indio = personaje.ubicacion.zonas.index(personaje.zona)    
    if("sabia" in nombre):
        boosteo = sabiduria_del_mas_alla[dados(1, len(sabiduria_del_mas_alla))[0]-1]
        nombre = "Nota de consejo"
        o= Juego.tranformar_objeto(nombre, cant)
        o.boosteo = boosteo
    else:
        o= Juego.tranformar_objeto(nombre, cant)
    
    if(o.nombre == "Nota de consejo" and "sabia" not in o.nombre):
        o.boosteo = consejos[dados(1, len(consejos))[0]-1]
    
    personaje.ubicacion.objetos_activos[indio].append(o)
    personaje.ubicacion.cantidades[indio].append(1)
    personaje.ubicacion.objetos[indio].append(o.nombre)
    personaje.anadir_obj(o)

def separar(df, lugar, zonas, tipo):
    #DEBUG
#    print("------------------------------------------------Metodo separar objetos")
    enemigos = False
    if(df == "o"):
        a = Dfnombres_o
        b = Dfcant_o
        enemigos = False
    else:
        a = Dfnombres_e
        b = Dfcant_e
        enemigos = True
    elementos = []
    cantidad = []
    for i in range (0, len(zonas)):
        elementos.append([])
        cantidad.append([])
    como_quieras = False
    j=-1
    for i in range (0, len(a)):
        if (a.iloc[i,0] in lugares and a.iloc[i,0] != lugar) or (a.iloc[i,0] == ""):
            como_quieras = False
        if(como_quieras): #-----------------------------------------Dentro del lugar
            if (a.iloc[i,0] in zonas):
                j+=1
            else:
                if(enemigos):
                    if(a.iloc[i,0]=="Rat King G" or a.iloc[i,0]=="Rat King C" 
                       or a.iloc[i,0]=="Cocinero" 
                       or Dfdifi_e.iloc[i,0] != dificultad):
                        continue
                elementos[j].append(a.iloc[i,0])
                cantidad[j].append(b.iloc[i,0])
        if(a.iloc[i,0] == lugar):
            como_quieras = True
#    print(elementos)
#    print(cantidad)
    if(tipo == 1):
        return elementos
    elif(tipo == 2):
        return cantidad

def generar_lugar_arg(nombre, zonas):
    activos = []
    activos1 = []
    for i in range(0, len(zonas)):
        activos.append([])
        activos1.append([])
    lugar = Lugar(nombre, zonas,
                  separar("e", nombre, zonas, 1), 
                  separar("e", nombre, zonas, 2), 
                  separar("o", nombre, zonas, 1), 
                  separar("o", nombre, zonas, 2), 
                  activos, activos1)
    for i in range (0, len(zonas)):
        lugar.jaulas.append({})
    return lugar

def generar_carneables():
    categorias_si = ["Animal", "Monstruo", "Zombie"]
    nombres = Dfnombres_e
    categorias = Dfcategorias_e
    for n in range(0, len(nombres)):
        if(categorias.iloc[n,0] in categorias_si) and (nombres.iloc[n,0] 
        not in carneables) and (nombres.iloc[n,0] not in jefes.keys()):
            carneables.append(nombres.iloc[n,0])

def malo():
    return personajes[dados(1, len(personajes))[0]-1]

def queso():
    print('Queso')
    
def jamon():
    print('JAMON')

def shufflepro(lista1, lista2):
    #DEBUG
#    print("-----------------------------------------------------Metodo shufflepro")
    lista3 = []
    lista4 = []
    
    for i in range (0, len(lista1)):
        lista3.append([])
        lista4.append([])
        for j in range(0, len(lista1[i])):
            lista3[i].append("")
            lista4[i].append("")
    
    for h in range (0, len(lista1)):
        c=0
        while "" in lista3[h]:
            valor = np.random.randint(0, len(lista1[h]))
            if(lista3[h][valor] == ""):
                lista3[h][valor] = lista1[h][c]
                lista4[h][valor] = lista2[h][c]
                c+=1

    return (lista3,lista4)

def shuffleproplus(lista_personajes):
    #DEBUG
#    print("-------------------------------------------------Metodo shuffleproplus")
    lista1 = []
    lista2 = []
    for p in lista_personajes:
        if("Cadaver de " + malo.nombre in p.inventario_nombres):
            indio = p.inventario_nombres.index("Cadaver de " + malo.nombre)
            p.inventario_nombres.remove("Cadaver de Norman" + malo.nombre)
            p.inventario.pop(indio)
        for i in range(0, len(p.inventario)):
            lista1.append(p.inventario[i])
            lista2.append(p.inventario_nombres[i])
        p.inventario = []
        p.inventario_nombres = []
    
    lista1, lista2 = shufflepro([lista1], [lista2])
    lista1 = lista1[0]
    lista2 = lista2[0]
    c = 0
    for per in lista_personajes:
        total = 0
        while (total < per.carga) and (c < len(lista1)):
            per.inventario.append(lista1[c])
            per.inventario_nombres.append(lista2[c])
            total += lista1[c].peso
            c+=1

def shuffleproplusultra(lista1, lista2):
    #DEBUG
#    print("-----------------------------------------------------Metodo shufflepro")
    lista3 = []
    lista4 = []
    
    for i in range (0, len(lista1)):
        lista3.append("")
        lista4.append("")
    
    c=0
    while "" in lista3:
        valor = np.random.randint(0, len(lista1))
        if(lista3[valor] == ""):
            lista3[valor] = lista1[c]
            lista4[valor] = lista2[c]
            c+=1

    return (lista3,lista4)

def ubicar(self):
    #DEBUG
#    print("---------------------------------------------------------Metodo ubicar")
    for i in personajes:
        print(i.nombre + " esta en: " + i.ubicacion.nombre + ", " + i.zona)
    print("------------------------------------------------------------------")
    ubicaciones = []
    for i in range (0, len(personajes)):
        ubicaciones.append(personajes[i].zona)
    return ubicaciones

def dados(n: int, l: int):
    #DEBUG
#    print("----------------------------------------------------------Metodo dados")
    if(l == 0):
        return 0
    a=[]
    for i in range (0, n):
        a.append(np.random.randint(1, l+1))
    return a

def repetido(self, lugar, zona:int, jefe:str):
    for e in lugar.enemigos_activos[zona]:
        if(e.nombre == jefe):
            return True
    return False

campamento    = generar_lugar_arg("Campamento", ["Cabana", "Comedor", 
                                                 "Almacen", "Cabanas vecinas", 
                                                 "Puesto de seguridad"])
bosque        = generar_lugar_arg("Bosque", ["Aire libre", 
                                             "Cabana de guardabosques", 
                                             "Entrada mina bosque", "Pradera", 
                                             "Carretera", "Corazon del bosque"])
pueblo        = generar_lugar_arg("Pueblo", ["Comunidad", "Casa de chaman",
                                             "Ayuntamiento", "Entrada mina pueblo"])
mina          = generar_lugar_arg("Mina", ["Zona de exploracion I", 
                                           "Zona de exploracion II", 
                                           "Tunel salida bosque", 
                                           "Tunel salida pueblo", 
                                           "Tunel salida pantano", 
                                           "Tunel salida deshuesadero", 
                                           "Tunel ???", "Tunel derrumbado", 
                                           "Tunel de exploracion I", 
                                           "Tunel de exploracion II", 
                                           "Puestos de trabajo", "Zona clausurada"])
edificio      = generar_lugar_arg("Edificio Abandonado", ["Entrada", 
                                                          "Maquina", "Escalera", 
                                                          "Laboratorio", 
                                                          "Sala de investigacion"])
puerto        = generar_lugar_arg("Puerto", ["Bahia", "Carguero"])
normancueva   = generar_lugar_arg("Normancueva", ["Sala principal", 
                                                  "Entrada mistica"])
deshuesadero  = generar_lugar_arg("Deshuesadero", ["Casa", "Almacen", "Carniceria", 
                                                   "Basurero", "Alacena", 
                                                   "Entrada mina deshuesadero"])
montana       = generar_lugar_arg("Montana", ["Cabana doctor", "Cima", "Subida"])
mercado       = generar_lugar_arg("Mercado", ["Mercado", "Banco"])
puerta        = generar_lugar_arg("Puerta", ["Templo", "Cueva", "Tunel misterioso", 
                                             "Tunel rocoso", "Tunel terrible", 
                                             "Tunel negro", "Tunel siniestro", 
                                             "Cuarto de contencion scp 953", 
                                             "Cuarto de contencion scp 1048", 
                                             "Cuarto de contencion scp 4715", 
                                             "Cuarto de contencion scp 076", 
                                             "Cuarto de contencion scp 439", 
                                             "Puerta"])
fondo_del_mar = generar_lugar_arg("Fondo del mar", ["Submarino", "Mar", 
                                                    "Profundidades"])
pantano       = generar_lugar_arg("Pantano", ["Zona de control", "Exterior", 
                                              "Casa ogro", "Entrada mina pantano"])
viaje_astral  = generar_lugar_arg("campamento", ["camion", "cabana", "comedor", 
                                                 "almacen", "cabanas vecinas", 
                                                 "puesto de seguridad", 
                                                 "aire libre", "pradera", 
                                                 "carretera", "entrada"])

lugares_o = [campamento, bosque, pueblo, mina, edificio, 
             puerto, normancueva, deshuesadero, montana, mercado, 
             puerta, fondo_del_mar, pantano, viaje_astral]

campamento_original = generar_lugar_arg("Campamento", ["Cabana", "Comedor", 
                                                       "Almacen", "Cabanas vecinas", 
                                                       "Puesto de seguridad"])
bosque_original = generar_lugar_arg("Bosque", ["Aire libre", 
                                               "Cabana de guardabosques", 
                                               "Entrada mina bosque", "Pradera", 
                                               "Carretera", "Corazon del bosque"])
pueblo_original = generar_lugar_arg("Pueblo", ["Comunidad", "Casa de chaman", 
                                               "Ayuntamiento", 
                                               "Entrada mina pueblo"])
mina_original = generar_lugar_arg("Mina", ["Zona de exploracion I", 
                                           "Zona de exploracion II", 
                                           "Tunel salida bosque", 
                                           "Tunel salida pueblo", 
                                           "Tunel salida pantano", 
                                           "Tunel salida deshuesadero", 
                                           "Tunel ???", "Tunel derrumbado", 
                                           "Tunel de exploracion I", 
                                           "Tunel de exploracion II", 
                                           "Puestos de trabajo", "Zona clausurada"])
edificio_original = generar_lugar_arg("Edificio Abandonado", ["Entrada", "Maquina", 
                                                              "Escalera", 
                                                              "Laboratorio", 
                                                              "Sala de "
                                                              + "investigacion"])
puerto_original        = generar_lugar_arg("Puerto", ["Bahia", "Carguero"])
normancueva_original   = generar_lugar_arg("Normancueva", ["Sala principal", 
                                                           "Entrada mistica"])
deshuesadero_original  = generar_lugar_arg("Deshuesadero", ["Casa", "Almacen", 
                                                            "Carniceria", 
                                                            "Basurero", "Alacena", 
                                                            "Entrada mina "
                                                            + "deshuesadero"])
montana_original       = generar_lugar_arg("Montana", ["Cabana doctor", "Cima", 
                                                       "Subida"])
mercado_original       = generar_lugar_arg("Mercado", ["Mercado", "Banco"])
puerta_original        = generar_lugar_arg("Puerta", ["Templo", "Cueva", 
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
fondo_del_mar_original = generar_lugar_arg("Fondo del mar", ["Submarino", "Mar", 
                                                             "Profundidades"])
pantano_original       = generar_lugar_arg("Pantano", ["Zona de control", 
                                                       "Exterior", "Casa ogro", 
                                                       "Entrada mina pantano"])
viaje_astral_original  = generar_lugar_arg("campamento", ["camion", "cabana", 
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
