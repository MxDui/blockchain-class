# Default alphabet
alphabet = [chr(i) for i in range(256)]

def isPrime(n):
    '''Nos dice si un número n es primo'''
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def inv_add(a, mod):
    '''Nos da el inverso aditivo tal que a + i == 0 modulo n'''
    return (-a) % mod

def inv_mult(a, mod):
    '''Nos da el inverso multiplicativo modulo n'''
    for i in range(1, mod):
        if (a * i) % mod == 1:
            return i
    return None  # If no inverse exists

def table(elliptic_curve, alphabet=alphabet):
    '''Regesa una tabla de un abecedario mapeado a puntos de la curva elíptica e'''
    pts = getattr(elliptic_curve, 'points', None)
    if pts is None:
        raise AttributeError("EllipticCurve object has no attribute 'points'")
    
    if len(pts) < len(alphabet):
        l = alphabet[:len(pts)]
    else:
        l = alphabet
        while len(pts) > len(l):
            l = l + l
    
    table = {}
    i = 0
    while i != len(pts):
        table[l[i]] = pts[i]
        i += 1
    return table