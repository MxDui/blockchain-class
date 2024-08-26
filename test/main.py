from EllipticCurve import EllipticCurve
from Entity import Entity
from tools import table
from Point import Point
import sys

# p = int(sys.argv[1])
# a = int(sys.argv[2])
# b = int(sys.argv[3])

# Curva que soporta 256 caracteres
eli = EllipticCurve(233, -2, 8)
g = eli.points[-1]
# print(g)
# print(len(eli.points))
# print(eli.order(g))
# print(eli.cofactor(g))

code = table(eli)

print("CREACIÓN DE ENTIDADES CON CURVAS\n\n")
a = Entity("Allice", eli, g, code)
msg_a = "Las ideas siempre son borrosas al inicio, pero se van aclarando mientras trabajas en ellas. -El zucaritas"
b = Entity("Bob", eli, g, code)
msg_b = "The fears we don't face, become our limits."

print(a)
print(b)

print("INTERCAMBIO DE LLAVES TIPO DIFFIE-HELLMAN")
pub_k_a = a.genera_llaves_publicas()
pub_k_b = b.genera_llaves_publicas()

print('Ronda 1: ')
print(f'{a.name} PKs: {pub_k_a}')
print(f'{b.name} PKs: {pub_k_b}')

a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

pub_k_a = a.final_keys()
pub_k_b = b.final_keys()
print('\nRonda2:')
print(f'{a.name} PKs: {pub_k_a}')
print(f'{b.name} PKs: {pub_k_b}')

a.recibe_llaves_publicas(pub_k_b)
b.recibe_llaves_publicas(pub_k_a)

print()
print("CIFRADO DE MENSAJE")
enc = b.cifrar(msg_b)
print("Mensaje cifrado:", enc)
denc = a.descifrar(enc)
print("Mensaje descifrado:", denc)

