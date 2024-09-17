Aquí tienes las preguntas y respuestas en español:

**Preguntas:**

1. **Cuando sumamos un punto \( P \) con \( -P \), que nos da como resultado el punto al infinito... ¿Qué quiere decir que un punto sea infinito?**

   - En criptografía de curvas elípticas, el "punto en el infinito" actúa como el elemento identidad en el grupo de puntos de la curva. Es análogo al número cero en la suma de números enteros: para cualquier punto \( P \), la suma de \( P \) y su inverso \( -P \) resulta en el punto en el infinito. Este punto no tiene coordenadas finitas y sirve como un punto de referencia para definir operaciones de suma en la curva.

2. **Cuando sumamos un punto \( P \) consigo mismo, ¿qué característica tiene la recta que conecta estos dos puntos?**

   - Al sumar un punto \( P \) consigo mismo, proceso conocido como "doblamiento", se utiliza la línea tangente a la curva en el punto \( P \) para identificar el tercer punto de intersección con la curva. Este tercer punto se refleja then se considera el resultado de la suma. Por lo tanto, la recta que conecta \( P \) consigo mismo es precisamente la tangente a la curva en \( P \).

3. **¿En qué otro cifrado se utiliza el protocolo Diffie-Hellman?**

   - Además de la criptografía de curvas elípticas (ECDH – Diffie-Hellman de Curva Elíptica), el protocolo Diffie-Hellman se emplea en el esquema original de Diffie-Hellman para el intercambio seguro de claves en infraestructuras de clave pública. También es fundamental en varios protocolos de seguridad como TLS (Transport Layer Security), donde facilita el establecimiento de claves compartidas de manera segura entre partes que se comunican.

4. **¿Cuántos bits de una llave de una curva necesitamos para poder igualar la seguridad en una llave de RSA?**

   - En criptografía de curvas elípticas, una llave de 256 bits proporciona un nivel de seguridad comparable al de una llave RSA de 3072 bits. Las curvas elípticas logran la misma robustez criptográfica con tamaños de claves mucho más pequeños, lo que resulta en ventajas significativas en términos de eficiencia y rendimiento.

5. **En el ejemplo, en *attack* tenemos que la letra 't' es cifrada a 2 puntos diferentes de la curva, y sigue siendo recuperable. ¿Qué valor hace esto posible?**

   - Esto se debe a la existencia de múltiples puntos en la curva que pueden representar el mismo carácter, una propiedad aprovechada por esquemas de cifrado como ECIES (Esquema de Cifrado Integrado con Curva Elíptica). La redundancia inherente o técnicas de corrección de errores permiten que, incluso si un carácter se representa por múltiples puntos, sea posible recuperar el mensaje original de manera fiable.

6. **Cifra el mensaje: "Perro salchicha, gordo bachicha" usando la curva elíptica \( EC_{233}(-2,8) \) usando los 256 caracteres del código ASCII. Pega la ejecución la salida del *main*.**

   - [('\x0e', 'a'), ('À', '2'), ('Q', 'v'), ('\x80', 'Ð'), ('\x9c', 'Ö'), ('ª', '\x8d'), ("'", 'Å'), ('£', 'P'), ('Ï', '\x13'), ('\x8b', '{'), ('\x01', 'Õ'), ('h', '·'), ('\x0c', '\x12'), ('H', 'Õ'), ('Ì', 'a'), ('\x18', '7'), ('¨', 'Á'), ('\x88', '¨'), ('\x1d', '¶'), ('¿', ' '), ('¼', 'O'), ('\t', '\x84'), ('\x87', 'n'), ('X', ';'), ('s', 'P'), ('I', '\x1e'), ('4', '¡'), ('^', '\x84'), ('O', '7'), ('µ', '\x05'), ('Ã', '\x00')]

Si necesitas un desarrollo más detallado para implementar el cifrado o ejemplos específicos, no dudes en pedírmelo.