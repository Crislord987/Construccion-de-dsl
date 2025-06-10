# DSL Deep Learning Interpreter

Un intérprete completo para un lenguaje específico de dominio (DSL) orientado al aprendizaje automático y análisis de datos.

## Características

- **Operaciones matemáticas**: Aritmética básica, funciones trigonométricas, logaritmos
- **Matrices**: Transposición, multiplicación, suma, resta, inversión
- **Machine Learning**: Regresión lineal, clasificadores MLP, K-means clustering
- **Visualización**: Gráficos de líneas, dispersión, histogramas
- **Control de flujo**: Condicionales (if-else), bucles (while)
- **Archivos**: Lectura y escritura de archivos CSV y texto
- **Interfaz interactiva**: REPL con comandos especiales

## Requisitos

- Python 3.6+
- ANTLR4 para Python
- Archivos generados por ANTLR4:
  - `DeepLearningDSLLexer.py`
  - `DeepLearningDSLParser.py`
  - `DeepLearningDSLVisitor.py`

## Instalación

1. **Instala ANTLR4 para Python:**
   ```bash
   pip install antlr4-python3-runtime
   ```

2. **Genera los archivos ANTLR4 (si no los tienes):**
   ```bash
   antlr4 -Dlanguage=Python3 -visitor DeepLearningDSL.g4
   ```

3. **Coloca todos los archivos en el mismo directorio:**
   - `main.py` (intérprete principal)
   - `DSLInterpreterVisitor.py` (visitor personalizado)
   - Archivos generados por ANTLR4
   - `ejemplo.dsl` (ejemplos de código)

## Uso

### Modo Interactivo

```bash
python main.py
```

Esto iniciará el REPL interactivo donde puedes escribir comandos DSL:

```
DSL Deep Learning - Intérprete Interactivo
Escribe '.help' para ver ayuda o '.exit' para salir
------------------------------------------------------------
>>> x = 5;
x = 5
Ejecutado correctamente
>>> y = x * 2 + 3;
y = 13
Ejecutado correctamente
>>> .vars
Variables definidas:
--------------------------------------------------
x = 5
y = 13
--------------------------------------------------
```

### Ejecutar Archivo

```bash
python main.py ejemplo.dsl
```

### Comandos Especiales del REPL

- `.help` - Muestra ayuda completa
- `.vars` - Lista todas las variables definidas
- `.history` - Muestra historial de comandos
- `.clear` - Limpia variables e historial
- `.exit` - Sale del intérprete

## Sintaxis del Lenguaje

### Variables y Asignaciones

```javascript
x = 5;
nombre = "Juan";
lista = [1, 2, 3, 4, 5];
```

### Operaciones Matemáticas

```javascript
resultado = x + 5 * 2;
seno = sin(3.14159);
raiz = sqrt(25);
potencia = x ^ 2;
```

### Matrices

```javascript
matriz = [[1, 2], [3, 4]];
transpuesta = transpose(matriz);
inversa = inverse(matriz);
producto = matmul(matriz, matriz);
suma_mat = matsum(matriz, matriz);
```

### Estructuras de Control

```javascript
if x > 0 then
    resultado = "Positivo";
else
    resultado
