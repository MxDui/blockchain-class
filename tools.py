# Default alphabet
alphabet = [chr(i) for i in range(256)]

def isPrime(n):
    '''Nos dice si un número n es primo'''
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def inv_add(a, mod):
    '''Nos da el inverso aditivo tal que a + i == 0 modulo mod'''
    return (-a) % mod

def inv_mult(a, mod):
    '''Nos da el inverso multiplicativo modulo mod usando el algoritmo extendido de Euclides'''
    def gcd_extended(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = gcd_extended(a, mod)
    if gcd != 1:
        raise ValueError(f"{a} no tiene inverso multiplicativo módulo {mod}")
    return x % mod

def table(curve, alphabet=None):
    points = [p for p in curve.points if p is not None]
    if alphabet is None:
        # Incluir espacio, letras minúsculas, letras mayúsculas y algunos caracteres especiales
        alphabet = [' '] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + list('.,;:!?')
    
    if len(points) > len(alphabet):
        print(f"Advertencia: El número de puntos en la curva ({len(points)}) es mayor que el alfabeto ({len(alphabet)} caracteres). Se generarán caracteres adicionales.")
        additional_chars = [chr(i) for i in range(256) if chr(i) not in alphabet]
        alphabet.extend(additional_chars)
    
    if len(points) > len(alphabet):
        print(f"Error: No hay suficientes caracteres únicos para mapear todos los puntos de la curva. Se truncarán los puntos.")
        points = points[:len(alphabet)]
    
    t = {}
    for i, p in enumerate(points):
        t[alphabet[i]] = p
    return t