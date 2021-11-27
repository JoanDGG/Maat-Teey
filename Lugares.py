class Lugar:
    
    def __init__(self, nombre:str, zonas:list, enemigos:list, 
                 cantidades_enemigos:list, objetos:list, cantidades:list, 
                 enemigos_activos: list, objetos_activos: list):
        self.nombre = nombre
        self.zonas = zonas
        self.jaulas = []
        self.enemigos = enemigos
        self.enemigos_activos = enemigos_activos
        self.cantidades = cantidades
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
        self.cantidades[self.indice_zona(zona)] = cantidades
        
    def indice_zona(self, zona):
        indice = self.zonas.index(zona)
        return indice

#lug = Lugar("A", [], [], [], [], [], [], [])