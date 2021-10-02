class Lugar:
    
    def __init__(self, nombre:str, zonas:list, enemigos:list, cantidades_enemigos:list, objetos:list, cantidades:list, objetos_activos: list, enemigos_activos: list):
        self.nombre = nombre
        self._enemigos = enemigos
        self._enemigos_activos = enemigos_activos
        self._cantidades_enemigos = cantidades_enemigos
        self._zonas = zonas
        self._objetos = objetos
        self._cantidades = cantidades
        self._objetos_activos = objetos_activos
        self.jaulas = []
#        self._cantidades_objetos_activos = self._objetos_activos 
        
    def nombre(self):
        return self._nombre
    
    def enemigos(self):
        return self._enemigos
  
    def enemigos_s(self, enemigos):
        self._enemigos = enemigos
      
    def enemigos_zona_s(self, enemigos, zona):
        indio = self.zonas().index(zona)
        self._enemigos[indio] = enemigos
    
    def objetos_zona_s(self, objetos, zona):
        indio = self.zonas().index(zona)
        self._objetos[indio] = objetos

    def enemigos_activos(self):
        return self._enemigos_activos
  
    def enemigos_activos_s(self, enemigos_activos):
        self._enemigos_activos = enemigos_activos
  
    def cantidades_enemigos(self):
        return self._cantidades_enemigos
    
    def cantidades_enemigos_s(self, cantidades_enemigos):
        self._cantidades_enemigos = cantidades_enemigos
    
        
    def cantidades_enemigos_zona_s(self, cantidades, zona):
        indio = self.zonas().index(zona)
        self._cantidades_enemigos[indio] = cantidades
    
    def cantidades_objetos_zona_s(self, cantidades, zona):
        indio = self.zonas().index(zona)
        self._cantidades[indio] = cantidades
    
    def objetos(self):
        return self._objetos
  
    def objetos_s(self, objetos):
        self._objetos = objetos

    def objetos_activos(self):
        return self._objetos_activos

    def objetos_activos_s(self, objetos_activos):
        self._objetos_activos = objetos_activos

#    def cantidades_objetos_activos(self):
#        return self._cantidades_objetos_activos
#    
#    def cantidades_objetos_activos_s(self, cantidades_objetos_activos):
#        self._cantidades_objetos_activos = cantidades_objetos_activos

    def cantidades(self):
      return self._cantidades
  
    def cantidades_s(self, cantidades):
      self._cantidades = cantidades
  
    def zonas(self):
      return self._zonas