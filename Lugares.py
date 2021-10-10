class Lugar:
    
    def __init__(self, nombre:str, zonas:list, enemigos:list, 
                 cantidades_enemigos:list, objetos:list, cantidades:list, 
                 objetos_activos: list, enemigos_activos: list):
        self.nombre = nombre
        self.zonas = zonas
        self.jaulas = []
        self.enemigos = enemigos
        self.enemigos_activos = enemigos_activos
        self.cantidades = cantidades
        self.cantidades_enemigos = cantidades_enemigos
        self.objetos = objetos
        self.objetos_activos = objetos_activos
    
    def enemigos_zona_s(self, enemigos, zona):
        indice_zona = self.zonas.index(zona)
        self.enemigos[indice_zona] = enemigos
    
    def objetos_zona_s(self, objetos, zona):
        indice_zona = self.zonas.index(zona)
        self.objetos[indice_zona] = objetos

    def cantidades_enemigos_zona_s(self, cantidades, zona):
        indice_zona = self.zonas.index(zona)
        self.cantidades_enemigos[indice_zona] = cantidades
    
    def cantidades_objetos_zona_s(self, cantidades, zona):
        indice_zona = self.zonas.index(zona)
        self.cantidades[indice_zona] = cantidades

#lug = Lugar("A", [], [], [], [], [], [], [])