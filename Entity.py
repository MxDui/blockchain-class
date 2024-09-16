import random as r
from Point import Point

class Entity:
    '''Class that models an entity like Alice or Bob.'''

    def __init__(self, name, curve, generator_point, table):
        '''Constructs a new entity with keys and mappings.

        Args:
            name: Name of the entity
            curve: An elliptic curve
            generator_point: A generator point on the curve
            table: A mapping from characters to points on the curve
        '''
        self.name = name
        self.curve = curve
        self.generator_point = generator_point
        self.order = curve.order(generator_point)
        # Private attributes
        self.private_key = r.randint(1, self.order - 1)
        self.private_point = r.choice([p for p in self.curve.points if p is not None])
        # Public attributes
        self.public_key_1 = None
        self.public_key_2 = None
        self.public_key_3 = None
        self.another_entity_public_key_1 = None
        self.another_entity_public_key_2 = None
        self.another_entity_public_key_3 = None
        # Validate the table
        self.table = table
        self.reverse_table = {v: k for k, v in table.items()}
        required_characters = set(table.keys())
        if len(self.table) < len(required_characters):
            raise ValueError("The mapping table does not cover all required characters.")
        # Ensure all characters are mapped
        unmapped_chars = [c for c in required_characters if c not in self.table]
        if unmapped_chars:
            raise ValueError(f"The following characters are not mapped: {unmapped_chars}")

    def __str__(self):
        '''String representation of the entity'''
        return f'''{self.name}:
EC: {self.curve}
G: {self.generator_point}
Private Key: {self.private_key}
Private Point: {self.private_point}
'''

    def descifrar(self, mensaje_encriptado):
        '''Descifra pares de caracteres de vuelta al mensaje original.'''
        texto = []
        for char_e1, char_e2 in mensaje_encriptado:
            # Mapear caracteres de vuelta a puntos
            e1 = self.table.get(char_e1)
            e2 = self.table.get(char_e2)
            if e1 is None or e2 is None:
                print(f"Advertencia: Carácter {char_e1} o {char_e2} no encontrado en la tabla. Se reemplazará por un espacio.")
                e1 = e1 if e1 is not None else self.table[' ']
                e2 = e2 if e2 is not None else self.table[' ']
            # Asegurarse de que e1 y e2 son objetos Point
            if not isinstance(e1, Point) or not isinstance(e2, Point):
                raise ValueError(f"Descifrado fallido: e1 ({e1}) o e2 ({e2}) no son objetos Point.")
            # Calcular m = e2 - d * e1
            d_e1 = self.curve.mult(self.private_key, e1)
            m = self.curve.sum(e2, self.curve.inv(d_e1))
            # Mapear el punto m de vuelta a carácter
            c = self.reverse_table.get(m)
            if c is None:
                print(f"Advertencia: Punto {m} no encontrado en la tabla inversa. Se reemplazará por un carácter aleatorio.")
                c = r.choice(list(self.table.keys()))
            texto.append(c)
        return "".join(texto)
    def cifrar(self, mensaje):
        '''Encripta el mensaje a pares de caracteres que representan puntos en la curva.'''
        if not mensaje:
            return []
        cifrado = []
        alphabet = list(self.table.keys())
        for c in mensaje:
            # Mapear carácter a punto
            m = self.table.get(c)
            if m is None:
                print(f"Advertencia: Carácter '{c}' no está en la tabla de mapeo. Se reemplazará por un espacio.")
                c = ' '
                m = self.table[' ']
            # Elegir k aleatorio
            k = r.randint(1, self.order - 1)
            # Calcular e1 = k * G
            e1 = self.curve.mult(k, self.generator_point)
            # Calcular e2 = m + k * Y (Y es another_entity_public_key_1)
            kY = self.curve.mult(k, self.another_entity_public_key_1)
            e2 = self.curve.sum(m, kY)
            # Mapear e1 y e2 de vuelta a caracteres
            char_e1 = self.reverse_table.get(e1)
            char_e2 = self.reverse_table.get(e2)
            if char_e1 is None or char_e2 is None:
                # Si no se encuentra en la tabla inversa, elegir un carácter aleatorio del alfabeto
                char_e1 = char_e1 if char_e1 is not None else r.choice(alphabet)
                char_e2 = char_e2 if char_e2 is not None else r.choice(alphabet)
            # Añadir caracteres al cifrado
            cifrado.append((char_e1, char_e2))
        return cifrado

    def genera_llaves_publicas(self):
        '''Generates the first round of public keys of this entity PK1 and PK2.'''
        self.public_key_1 = self.curve.mult(self.private_key, self.generator_point)
        self.public_key_2 = self.curve.mult(self.private_key, self.private_point)
        return [self.public_key_1, self.public_key_2]

    def recibe_llaves_publicas(self, public_keys):
        '''Receives the public keys from another entity and stores them.'''
        if len(public_keys) == 3:
            self.another_entity_public_key_3 = public_keys[2]
        else:
            self.another_entity_public_key_1 = public_keys[0]
            self.another_entity_public_key_2 = public_keys[1]

    def final_keys(self):
        '''Generates the final public key in combination with another entity's public key.
        Returns the 3 public keys of this entity.'''
        self.public_key_3 = self.curve.mult(self.private_key, self.another_entity_public_key_1)
        return [self.public_key_1, self.public_key_2, self.public_key_3]
