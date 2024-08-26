import random as r

class Entity:
    '''Clase que modela una entidad como Alice o Bob.'''

    def __init__(self, name, curve, generator_point, table):
        '''Construye un nuevo personaje con un mensaje para compartir
        Una entidad tiene:
        1. name: Nombre de la entidad
        2. curve: Una curva elíptica a compartir
        3. generator_point: Un punto generador a compartir
        4. table: Una codificacion de caracteres a puntos de la curva.

        Además, debe inicializar sus llaves, públicas y privadas:
        5. private_key: Un entero aleatorio entre 1 y el orden del punto generador-1
        6. private_point: Un punto aleatorio de la curva que no sea el punto al infinito
        ## 3 llaves públicas de esta entidad
        7. public_key_1, public_key_2, public_key_3 = None
        ## 3 llaves públicas de la otra entidad
        8. another_entity_public_key_1, another_entity_public_key_2, another_entity_public_key_3 = None'''
        self.name = name
        self.curve = curve
        self.generator_point = generator_point
        self.order = curve.order(generator_point)
        ## Cosas privadas
        self.private_key = r.randint(1, self.order - 1)
        self.private_point = r.choice([p for p in getattr(self.curve, 'points', []) if p is not None])

        # Cosas publicas
        self.public_key_1 = None #Public key using private point
        self.public_key_2 = None #Public key using only private key
        self.public_key_3 = None

        self.another_entity_public_key_1 = None #Public keys from another entity
        self.another_entity_public_key_2 = None
        self.another_entity_public_key_3 = None

        self.table = table

    def __str__(self):
        '''Representacion en cadena de la entidad'''
        return f"{self.name}:\nEC: {self.curve}\nG: {self.generator_point}\nPrivate Key: {self.private_key}\nPrivate Point: {self.private_point}"

    def descifrar(self, encripted_msg):
        '''Descifra un conjunto de parejas de puntos (e1, e2) de una curva elíptica a un texto
        plano legible humanamente'''
        text = []

        values = list(self.table.values())
        keys = list(self.table.keys())

        for p in encripted_msg:
            e1 = self.table[p[0]]
            e2 = self.table[p[1]]

            m = self.curve.sum(e2, self.curve.inv(self.curve.mult(self.private_key, e1)))

            # (e1, e2) -> m
            idx = values.index(m)
            chr = keys[idx]
            text.append(chr)
        s = "".join(text)
        return s

    def cifrar(self, message):
        '''Cifra el mensaje (self.message) a puntos de la curva elíptica. Cada caracter es 
        mapeado a una pareja de puntos (e1, e2) con e1, e2 en EC.'''
        if not message:
            return []
        values = list(self.table.values())
        keys = list(self.table.keys())
        self.cipher = []
        for c in message:
            l = r.randint(1, self.order - 1)
            p = self.table[c]

            e1 = self.curve.mult(l, self.generator_point)
            e2 = self.curve.sum(p, self.curve.mult(l, self.another_entity_public_key_2))

            idx1 = values.index(e1)
            idx2 = values.index(e2)
            chr1 = keys[idx1]
            chr2 = keys[idx2]
            self.cipher.append((chr1, chr2))
        return self.cipher

    def genera_llaves_publicas(self):
        '''Hace las operaciones correspondientes para generar la primera ronda de llaves
        públicas de esta entidad PK1 y PK2.'''
        self.public_key_1 = self.private_point
        self.public_key_2 = self.curve.mult(self.private_key, self.generator_point)
        return [self.public_key_1, self.public_key_2]

    def recibe_llaves_publicas(self, public_keys):
        '''Recibe la llave publica de otra entidad y las guarda. (primera ronda solo guarda 2)
        o si ya es la segunda ronda, guarda la última llave (pk1, pk2 y pk3 != None)'''
        if len(public_keys) == 3:
            self.another_entity_public_key_3 = public_keys[2]
            return
        else:
            self.another_entity_public_key_1 = public_keys[0]
            self.another_entity_public_key_2 = public_keys[1]

    def final_keys(self):
        '''Genera la última llave pública, en combinación con otra llave pública de otra entidad
        Regresa las 3 llaves públicas de esta entidad.'''
        public_keys = [self.public_key_1, self.public_key_2]
        self.public_key_3 = self.curve.mult(self.private_key, self.another_entity_public_key_1)
        public_keys.append(self.public_key_3)
        return public_keys

