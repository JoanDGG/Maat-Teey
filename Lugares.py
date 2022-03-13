class Lugar:
    
    def __init__(self, nombre:str, zonas:list, enemigos:list, 
                 cantidades_enemigos:list, objetos:list, 
                 cantidades_objetos:list, enemigos_activos: list, 
                 objetos_activos: list):
        self.nombre = nombre
        self.zonas = zonas
        self.jaulas = []
        for i in range (0, len(self.zonas)):
            self.jaulas.append({})
        self.enemigos = enemigos
        self.enemigos_activos = enemigos_activos
        self.cantidades_objetos = cantidades_objetos
        self.cantidades_enemigos = cantidades_enemigos
        self.objetos = objetos
        self.objetos_activos = objetos_activos
    
    def enemigos_zona_setter(self, enemigos, zona):
        self.enemigos[self.indice_zona(zona)] = enemigos
    
    def objetos_zona_setter(self, objetos, zona):
        self.objetos[self.indice_zona(zona)] = objetos

    def cantidades_enemigos_zona_setter(self, cantidades, zona):
        self.cantidades_enemigos[self.indice_zona(zona)] = cantidades
    
    def cantidades_objetos_zona_setter(self, cantidades, zona):
        self.cantidades_objetos[self.indice_zona(zona)] = cantidades
        
    def indice_zona(self, zona):
        indice = self.zonas.index(zona)
        return indice
    
    def __str__(self):        
        texto = f"\n{self.nombre:.^50}"
        texto += "\n Zonas:\n"
        texto += ", ".join(self.zonas)
        texto += "\n Jaulas:\n"
        jaulas = [[self.jaulas[jaula][jaula_enemigo].nombre 
                   for jaula_enemigo in jaula] for jaula in self.jaulas]
        texto += " | ".join([", ".join(jaulas[zona]) 
                                        for zona in range(0, len(self.zonas))])
        texto += "\n Enemigos activos:\n"
        enemigos = [[enemigo.nombre 
                  for enemigo in self.enemigos_activos[self.indice_zona(zona)]]
                  for zona in self.zonas]
        texto += " | ".join([", ".join(enemigos[zona]) 
                                        for zona in range(0, len(self.zonas))])
        texto += "\n Objetos activos:\n"
        objetos = [[objeto.nombre 
                 for objeto in self.objetos_activos[self.indice_zona(zona)]]
                 for zona in self.zonas]
        texto += " | ".join([", ".join(objetos[zona]) 
                                        for zona in range(0, len(self.zonas))])
        texto += "\n"
        return texto

# =============================================================================
#lug = Lugar("A", ["zona a", "zona b"], ["ea ", "eb"], [69, 96], ["oa", "ob"], 
# [101, 1010], [[], []], [[], []])
#print(lug)
#lug.enemigos_zona_setter(["uwu", "lol"], "zona a")
#print(lug.enemigos[lug.indice_zona("zona a")])
#lug.cantidades_enemigos_zona_setter([1, 0], "zona a")
#print(lug.cantidades_enemigos[lug.indice_zona("zona a")])
#lug.objetos_zona_setter(["pito", "rabo"], "zona b")
#print(lug.objetos[lug.indice_zona("zona b")])
#lug.cantidades_objetos_zona_setter([1, 1], "zona b")
#print(lug.cantidades_objetos[lug.indice_zona("zona b")])
#print(lug.indice_zona("zona b"))
# =============================================================================
