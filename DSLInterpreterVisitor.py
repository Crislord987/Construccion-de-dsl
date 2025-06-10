import math
import random
import os
from DeepLearningDSLParser import DeepLearningDSLParser
from DeepLearningDSLVisitor import DeepLearningDSLVisitor

class DSLInterpreterVisitor(DeepLearningDSLVisitor):
    """Visitor que implementa la lógica de interpretación del DSL"""
    
    def __init__(self):
        self.variables = {}
        self.plot_data = []
    
    # === PROGRAMA PRINCIPAL ===
    def visitProgram(self, ctx):
        """Visita el programa principal"""
        result = None
        for statement in ctx.statement():
            if statement:
                result = self.visit(statement)
        return result
    
    # === STATEMENTS ===
    def visitStatement(self, ctx):
        """Visita un statement genérico"""
        if ctx.assignment():
            return self.visit(ctx.assignment())
        elif ctx.expressionStatement():
            return self.visit(ctx.expressionStatement())
        elif ctx.controlStructure():
            return self.visit(ctx.controlStructure())
        elif ctx.plotStatement():
            return self.visit(ctx.plotStatement())
        elif ctx.fileOperation():
            return self.visit(ctx.fileOperation())
        return None
    
    def visitAssignment(self, ctx):
        """Maneja asignaciones de variables"""
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expression())
        self.variables[var_name] = value
        print(f"📝 {var_name} = {self._format_value(value)}")
        return value
    
    def visitExpressionStatement(self, ctx):
        """Maneja statements de expresión"""
        result = self.visit(ctx.expression())
        if result is not None:
            print(f"📊 Resultado: {self._format_value(result)}")
        return result
    
    # === ESTRUCTURAS DE CONTROL ===
    def visitControlStructure(self, ctx):
        """Visita estructuras de control"""
        if ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        return None
    
    def visitIfStatement(self, ctx):
        """Implementa la lógica del if"""
        condition = self.visit(ctx.booleanExpression())
        
        if self._to_boolean(condition):
            # Ejecutar bloque then
            result = None
            for statement in ctx.statement():
                if statement:
                    result = self.visit(statement)
            return result
        else:
            # Ejecutar bloque else si existe
            if len(ctx.statement()) > 1:  # Hay bloque else
                result = None
                # Los statements del else empiezan después del then
                else_statements = ctx.statement()[1:]
                for statement in else_statements:
                    if statement:
                        result = self.visit(statement)
                return result
        return None
    
    def visitWhileStatement(self, ctx):
        """Implementa la lógica del while"""
        result = None
        iterations = 0
        max_iterations = 10000  # Prevenir bucles infinitos
        
        while self._to_boolean(self.visit(ctx.booleanExpression())):
            if iterations >= max_iterations:
                raise RuntimeError("Bucle while excedió el límite de iteraciones")
            
            for statement in ctx.statement():
                if statement:
                    result = self.visit(statement)
            iterations += 1
        
        return result
    
    # === EXPRESIONES ===
    def visitExpression(self, ctx):
        """Maneja todas las expresiones"""
        # Operaciones binarias
        if ctx.op:
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            op = ctx.op.text
            
            if op == '+':
                return self._add(left, right)
            elif op == '-':
                return self._subtract(left, right)
            elif op == '*':
                return self._multiply(left, right)
            elif op == '/':
                return self._divide(left, right)
            elif op == '^':
                return self._power(left, right)
            elif op == '==':
                return self._equals(left, right)
            elif op == '!=':
                return not self._equals(left, right)
            elif op == '<':
                return self._to_number(left) < self._to_number(right)
            elif op == '<=':
                return self._to_number(left) <= self._to_number(right)
            elif op == '>':
                return self._to_number(left) > self._to_number(right)
            elif op == '>=':
                return self._to_number(left) >= self._to_number(right)
        
        # Expresión entre paréntesis
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expression(0))
        
        # Literales
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]  # Remover comillas
        if ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise RuntimeError(f"Variable no definida: {var_name}")
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False
        # Otros tipos de expresiones
        if ctx.matrixLiteral():
            return self.visit(ctx.matrixLiteral())
        if ctx.listLiteral():
            return self.visit(ctx.listLiteral())
        if ctx.matrixOperation():
            return self.visit(ctx.matrixOperation())
        if ctx.trigFunction():
            return self.visit(ctx.trigFunction())
        if ctx.mlOperation():
            return self.visit(ctx.mlOperation())
        
        return None
    
    def visitBooleanExpression(self, ctx):
        """Maneja expresiones booleanas"""
        if ctx.comparator():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            op = ctx.comparator().getText()
            
            if op == '==':
                return self._equals(left, right)
            elif op == '!=':
                return not self._equals(left, right)
            elif op == '<':
                return self._to_number(left) < self._to_number(right)
            elif op == '<=':
                return self._to_number(left) <= self._to_number(right)
            elif op == '>':
                return self._to_number(left) > self._to_number(right)
            elif op == '>=':
                return self._to_number(left) >= self._to_number(right)
        
        # Operadores lógicos
        if ctx.getChild(0).getText() == 'not':
            return not self._to_boolean(self.visit(ctx.booleanExpression(0)))
        
        if ctx.getChildCount() == 3:
            left = self._to_boolean(self.visit(ctx.booleanExpression(0)))
            op = ctx.getChild(1).getText()
            right = self._to_boolean(self.visit(ctx.booleanExpression(1)))
            
            if op == 'and':
                return left and right
            elif op == 'or':
                return left or right
        
        # Expresión simple
        return self._to_boolean(self.visit(ctx.expression(0)))
    
    # === OPERACIONES DE MATRICES ===
    def visitMatrixOperation(self, ctx):
        """Maneja operaciones de matrices"""
        op = ctx.getChild(0).getText()
        
        if op == 'transpose':
            matrix = self.visit(ctx.expression(0))
            return self._transpose(matrix)
        elif op == 'inverse':
            matrix = self.visit(ctx.expression(0))
            return self._inverse(matrix)
        elif op == 'matmul':
            m1 = self.visit(ctx.expression(0))
            m2 = self.visit(ctx.expression(1))
            return self._matrix_multiply(m1, m2)
        elif op == 'matsum':
            m1 = self.visit(ctx.expression(0))
            m2 = self.visit(ctx.expression(1))
            return self._matrix_add(m1, m2)
        elif op == 'matsub':
            m1 = self.visit(ctx.expression(0))
            m2 = self.visit(ctx.expression(1))
            return self._matrix_subtract(m1, m2)
        
        return None
    
    # === OPERACIONES DE MACHINE LEARNING ===
    def visitMlOperation(self, ctx):
        """Maneja operaciones de machine learning"""
        op = ctx.getChild(0).getText()
        
        if op == 'linearRegression':
            X = self.visit(ctx.expression(0))
            y = self.visit(ctx.expression(1))
            return self._linear_regression(X, y)
        elif op == 'mlpClassifier':
            X = self.visit(ctx.expression(0))
            y = self.visit(ctx.expression(1))
            layers = self.visit(ctx.expression(2))
            return self._mlp_classifier(X, y, layers)
        elif op == 'kmeans':
            data = self.visit(ctx.expression(0))
            k = self.visit(ctx.expression(1))
            return self._kmeans(data, k)
        
        return None
    
    # === FUNCIONES TRIGONOMÉTRICAS ===
    def visitTrigFunction(self, ctx):
        """Maneja funciones trigonométricas y matemáticas"""
        func = ctx.getChild(0).getText()
        value = self._to_number(self.visit(ctx.expression()))
        
        if func == 'sin':
            return math.sin(value)
        elif func == 'cos':
            return math.cos(value)
        elif func == 'tan':
            return math.tan(value)
        elif func == 'sqrt':
            if value < 0:
                raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
            return math.sqrt(value)
        elif func == 'log':
            if value <= 0:
                raise ValueError("El logaritmo requiere un valor positivo")
            return math.log(value)
        elif func == 'exp':
            return math.exp(value)
        
        return None
    
    # === VISUALIZACIÓN ===
    def visitPlotStatement(self, ctx):
        """Dibuja gráficas ASCII (plot, scatter, hist)"""
        plot_type = ctx.getChild(0).getText()
        try:
            x_data = self.visit(ctx.expression(0))
            y_data = self.visit(ctx.expression(1)) if ctx.expression(1) else None
        except Exception as e:
            print(f"❌ Error al procesar expresiones: {str(e)}")
            return

        # Convertir cualquier cosa iterable a lista
        if isinstance(x_data, (str, tuple)):
            x_data = list(x_data)
        if isinstance(y_data, (str, tuple)):
            y_data = list(y_data)

        if plot_type in ("plot", "scatter"):
            if not isinstance(x_data, list) or not isinstance(y_data, list):
                print("❌ Los datos deben ser listas para plot/scatter")
                return
            
            # Manejar caso especial: matriz vs vector
            if (isinstance(x_data[0], list) if x_data else False) and not (isinstance(y_data[0], list) if y_data else False):
                print("⚠️  Detectada matriz vs vector - usando primera columna de la matriz")
                x_plot = [row[0] for row in x_data]  # Usar primera columna
                y_plot = y_data
            elif not (isinstance(x_data[0], list) if x_data else False) and (isinstance(y_data[0], list) if y_data else False):
                print("⚠️  Detectado vector vs matriz - usando primera columna de la matriz")
                x_plot = x_data
                y_plot = [row[0] for row in y_data]  # Usar primera columna
            else:
                x_plot = x_data
                y_plot = y_data
            
            if len(x_plot) != len(y_plot):
                print("❌ Las listas x e y deben tener la misma longitud")
                return
            self._ascii_plot_exact(x_plot, y_plot, show_trend=(plot_type == "scatter"))
        elif plot_type == "hist":
            if not isinstance(x_data, list):
                print("❌ El argumento para hist debe ser una lista")
                return
            self._ascii_histogram_vertical(x_data)

    def _ascii_plot_exact(self, x_data, y_data, show_trend=False):
        """Gráfico ASCII con ejes X y Y numéricos claramente alineados"""
        
        # Manejar el caso donde x_data es una matriz (lista de listas)
        if isinstance(x_data, list) and x_data and isinstance(x_data[0], list):
            # Si x_data es una matriz, aplanar todos los valores para encontrar el rango
            x_flat = [val for row in x_data for val in row]
            max_x = int(max(x_flat))
            min_x = int(min(x_flat))
            # Para visualización, usar solo la primera columna o un índice
            x_plot = [row[0] if isinstance(row, list) else row for row in x_data]
        else:
            # x_data es una lista simple
            x_plot = x_data
            max_x = int(max(x_data))
            min_x = int(min(x_data))
        
        # Similar para y_data
        if isinstance(y_data, list) and y_data and isinstance(y_data[0], list):
            y_flat = [val for row in y_data for val in row]
            max_y = int(max(y_flat))
            min_y = int(min(y_flat))
            y_plot = [row[0] if isinstance(row, list) else row for row in y_data]
        else:
            y_plot = y_data
            max_y = int(max(y_data))
            min_y = int(min(y_data))
        
        # Ajustar para que el rango comience desde 0 o el mínimo
        width = max(max_x - min_x + 1, len(x_plot))
        height = max(max_y - min_y + 1, len(y_plot))
        
        # Crear lienzo
        canvas = [[' ' for _ in range(width)] for _ in range(height)]

        # Dibujar puntos reales
        for x, y in zip(x_plot, y_plot):
            xi, yi = int(x) - min_x, int(y) - min_y
            if 0 <= xi < width and 0 <= yi < height:
                canvas[height - yi - 1][xi] = '*'

        # Línea de tendencia
        if show_trend and len(x_plot) >= 2:
            n = len(x_plot)
            sum_x = sum(x_plot)
            sum_y = sum(y_plot)
            sum_xx = sum(x ** 2 for x in x_plot)
            sum_xy = sum(x * y for x, y in zip(x_plot, y_plot))
            denominator = n * sum_xx - sum_x ** 2
            if denominator != 0:
                a = (n * sum_xy - sum_x * sum_y) / denominator
                b = (sum_y - a * sum_x) / n
                for x in range(width):
                    y = int(round(a * (x + min_x) + b)) - min_y
                    if 0 <= y < height and canvas[height - y - 1][x] == ' ':
                        canvas[height - y - 1][x] = '+'

        # Imprimir gráfico con etiquetas Y
        for row_idx, row in enumerate(canvas):
            y_label = f"{max_y - row_idx:>2}"  # etiqueta Y alineada
            print(f"{y_label} | " + '  '.join(row))

        # Eje X
        print("   +" + "---" * width)

        # Etiquetas X: espacio alineado con el contenido
        x_labels = "    " + '  '.join(f"{x + min_x}" for x in range(width))
        print(x_labels)

        print(f"x: [{min(x_plot)} … {max(x_plot)}]  y: [{min(y_plot)} … {max(y_plot)}]")
        if show_trend:
            print("'*' puntos   '+' línea de tendencia")
        # === OPERACIONES DE ARCHIVOS ===
        def visitFileOperation(self, ctx):
            """Maneja operaciones de archivos"""
            op = ctx.getChild(0).getText()
            
            if op == 'readFile':
                filename = self.visit(ctx.expression(0))
                return self._read_file(filename)
            elif op == 'writeFile':
                filename = self.visit(ctx.expression(0))
                data = self.visit(ctx.expression(1))
                self._write_file(filename, data)
            
            return None
    
    # === LITERALES ===
    def visitMatrixLiteral(self, ctx):
        """Maneja literales de matriz"""
        matrix = []
        for list_literal in ctx.listLiteral():
            row = self.visit(list_literal)
            matrix.append(row)
        return matrix
    
    def visitListLiteral(self, ctx):
        """Maneja literales de lista"""
        if not ctx.expression():
            return []
        
        result = []
        for expr in ctx.expression():
            result.append(self.visit(expr))
        return result
    
    # === MÉTODOS AUXILIARES ===
    def _format_value(self, value):
        """Formatea un valor para mostrar"""
        if isinstance(value, list):
            if len(value) > 10:
                return f"[Lista con {len(value)} elementos]"
            elif all(isinstance(row, list) for row in value):
                return f"[Matriz {len(value)}x{len(value[0]) if value else 0}]"
            else:
                return str(value)
        elif isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            else:
                return f"{value:.6g}"
        return str(value)
    
    def _to_number(self, value):
        """Convierte un valor a número"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                raise TypeError(f"No se puede convertir '{value}' a número")
        else:
            raise TypeError(f"Tipo no válido para operación numérica: {type(value)}")
    
    def _to_boolean(self, value):
        """Convierte un valor a booleano"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return value != ""
        elif isinstance(value, list):
            return len(value) > 0
        else:
            return bool(value)
    
    def _equals(self, left, right):
        """Compara dos valores por igualdad"""
        return left == right
    
    def _add(self, left, right):
        """Suma dos valores"""
        if isinstance(left, list) and isinstance(right, list):
            return left + right
        elif isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        else:
            return self._to_number(left) + self._to_number(right)
    
    def _subtract(self, left, right):
        """Resta dos valores"""
        return self._to_number(left) - self._to_number(right)
    
    def _multiply(self, left, right):
        """Multiplica dos valores"""
        if isinstance(left, list) and isinstance(right, (int, float)):
            return left * int(right)
        elif isinstance(left, str) and isinstance(right, (int, float)):
            return left * int(right)
        else:
            return self._to_number(left) * self._to_number(right)
    
    def _divide(self, left, right):
        """Divide dos valores"""
        right_num = self._to_number(right)
        if right_num == 0:
            raise ZeroDivisionError("División por cero")
        return self._to_number(left) / right_num
    
    def _power(self, left, right):
        """Eleva un valor a una potencia"""
        return self._to_number(left) ** self._to_number(right)
    
    # === OPERACIONES DE MATRICES ===
    def _transpose(self, matrix):
        """Transpone una matriz"""
        if not isinstance(matrix, list) or not matrix:
            raise ValueError("Se requiere una matriz no vacía")
        
        if not isinstance(matrix[0], list):
            # Vector columna a vector fila
            return [[item] for item in matrix]
        
        # Matriz 2D
        rows = len(matrix)
        cols = len(matrix[0])
        result = [[0] * rows for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                result[j][i] = matrix[i][j]
        
        return result
    
    def _inverse(self, matrix):
        """Calcula la inversa de una matriz 2x2 (simplificado)"""
        if not isinstance(matrix, list) or len(matrix) != 2:
            raise ValueError("Solo se soporta inversa para matrices 2x2")
        
        if len(matrix[0]) != 2 or len(matrix[1]) != 2:
            raise ValueError("Solo se soporta inversa para matrices 2x2")
        
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]
        
        det = a * d - b * c
        if det == 0:
            raise ValueError("La matriz no es invertible (determinante = 0)")
        
        return [[d/det, -b/det], [-c/det, a/det]]
    
    def _matrix_multiply(self, m1, m2):
        """Multiplica dos matrices"""
        if not isinstance(m1, list) or not isinstance(m2, list):
            raise ValueError("Se requieren dos matrices")
        
        # Convertir vectores a matrices si es necesario
        if not isinstance(m1[0], list):
            m1 = [m1]
        if not isinstance(m2[0], list):
            m2 = [[row] for row in m2]
        
        rows1, cols1 = len(m1), len(m1[0])
        rows2, cols2 = len(m2), len(m2[0])
        
        if cols1 != rows2:
            raise ValueError(f"Dimensiones incompatibles: {rows1}x{cols1} y {rows2}x{cols2}")
        
        result = [[0] * cols2 for _ in range(rows1)]
        
        for i in range(rows1):
            for j in range(cols2):
                for k in range(cols1):
                    result[i][j] += m1[i][k] * m2[k][j]
        
        return result
    
    def _matrix_add(self, m1, m2):
        """Suma dos matrices"""
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        
        result = []
        for i in range(len(m1)):
            row = []
            for j in range(len(m1[0])):
                row.append(m1[i][j] + m2[i][j])
            result.append(row)
        
        return result
    
    def _matrix_subtract(self, m1, m2):
        """Resta dos matrices"""
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        
        result = []
        for i in range(len(m1)):
            row = []
            for j in range(len(m1[0])):
                row.append(m1[i][j] - m2[i][j])
            result.append(row)
        
        return result
    
    # === MACHINE LEARNING===
    def _linear_regression(self, X, y):
        """Implementación simplificada de regresión lineal"""
        if not isinstance(X, list) or not isinstance(y, list):
            raise ValueError("X e y deben ser listas")
        
        if len(X) != len(y):
            raise ValueError("X e y deben tener la misma longitud")
        
        n = len(X)
        if n == 0:
            raise ValueError("Los datos no pueden estar vacíos")
        
        # Calcular medias
        mean_x = sum(X) / n
        mean_y = sum(y) / n
        
        # Calcular pendiente y intercepto
        numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((X[i] - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = mean_y - slope * mean_x
        
        model = {
            'type': 'LinearRegression',
            'slope': slope,
            'intercept': intercept,
            'r_squared': self._calculate_r_squared(X, y, slope, intercept)
        }
        
        print(f"🤖 Modelo de regresión lineal entrenado:")
        print(f"   Pendiente: {slope:.6f}")
        print(f"   Intercepto: {intercept:.6f}")
        print(f"   R²: {model['r_squared']:.6f}")
        
        return model
    
    def _calculate_r_squared(self, X, y, slope, intercept):
        """Calcula el coeficiente de determinación R²"""
        n = len(y)
        mean_y = sum(y) / n
        
        ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
        ss_res = sum((y[i] - (slope * X[i] + intercept)) ** 2 for i in range(n))
        
        if ss_tot == 0:
            return 1.0
        
        return 1 - (ss_res / ss_tot)
    
    def _mlp_classifier(self, X, y, layers):
        """Simulación de un clasificador MLP"""
        if not isinstance(X, list) or not isinstance(y, list):
            raise ValueError("X e y deben ser listas")
        
        if len(X) != len(y):
            raise ValueError("X e y deben tener la misma longitud")
        
        # Simular entrenamiento
        unique_classes = list(set(y))
        n_features = len(X[0]) if isinstance(X[0], list) else 1
        
        model = {
            'type': 'MLPClassifier',
            'layers': layers,
            'n_features': n_features,
            'classes': unique_classes,
            'accuracy': random.uniform(0.7, 0.95)  # Accuracy simulada
        }
        
        print(f"🧠 Clasificador MLP entrenado:")
        print(f"   Capas: {layers}")
        print(f"   Características: {n_features}")
        print(f"   Clases: {unique_classes}")
        print(f"   Accuracy estimada: {model['accuracy']:.3f}")
        
        return model
    
    def _kmeans(self, data, k):
        """Implementación simplificada de K-means"""
        if not isinstance(data, list) or not data:
            raise ValueError("Los datos deben ser una lista no vacía")
        
        k = int(self._to_number(k))
        if k <= 0 or k > len(data):
            raise ValueError("K debe ser un número positivo menor o igual al número de puntos")
        
        # Simulación simple de clustering
        n_points = len(data)
        clusters = [i % k for i in range(n_points)]
        
        # Calcular centroides simulados
        centroids = []
        for cluster_id in range(k):
            cluster_points = [data[i] for i in range(n_points) if clusters[i] == cluster_id]
            if cluster_points:
                if isinstance(cluster_points[0], list):
                    # Puntos multidimensionales
                    centroid = [sum(point[dim] for point in cluster_points) / len(cluster_points) 
                               for dim in range(len(cluster_points[0]))]
                else:
                    # Puntos unidimensionales
                    centroid = sum(cluster_points) / len(cluster_points)
                centroids.append(centroid)
        
        model = {
            'type': 'KMeans',
            'k': k,
            'centroids': centroids,
            'labels': clusters,
            'inertia': random.uniform(10, 100)  # Inercia simulada
        }
        
        print(f"🎯 Modelo K-means entrenado:")
        print(f"   K (clusters): {k}")
        print(f"   Centroides: {len(centroids)}")
        print(f"   Inercia: {model['inertia']:.2f}")
        
        return model
    
    # === VISUALIZACIÓN ===
    def _ascii_histogram_vertical(self, data):
        """Histograma vertical ASCII"""
        # Contar frecuencias manualmente
        freqs = {}
        for value in data:
            if value in freqs:
                freqs[value] += 1
            else:
                freqs[value] = 1

        keys = sorted(freqs.keys())
        values = [freqs[k] for k in keys]
        max_count = max(values)
        height = max_count

        print("\n📊 Histograma (ASCII vertical)")

        # Construir gráfico de arriba hacia abajo
        for level in range(height, 0, -1):
            row = f"{level:>2} |"
            for count in values:
                row += ' # ' if count >= level else '   '
            print(row)

        # Eje X
        print("   +" + "---" * len(keys))
        label_line = "    " + ''.join(f"{str(k):^3}" for k in keys)
        print(label_line)
        print(f"Valores: {keys}")

    # === OPERACIONES DE ARCHIVOS ===
    def _read_file(self, filename):
        """Lee un archivo"""
        try:
            if not isinstance(filename, str):
                raise ValueError("El nombre del archivo debe ser una cadena")
            
            if not os.path.exists(filename):
                raise FileNotFoundError(f"El archivo '{filename}' no existe")
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Intentar parsear como CSV si es posible
            if filename.endswith('.csv'):
                lines = content.split('\n')
                data = []
                for line in lines:
                    if line.strip():
                        row = [self._try_parse_number(cell.strip()) for cell in line.split(',')]
                        data.append(row)
                
                print(f"📂 Archivo CSV leído: {filename}")
                print(f"   Filas: {len(data)}")
                print(f"   Columnas: {len(data[0]) if data else 0}")
                
                return data
            else:
                # Archivo de texto plano
                lines = content.split('\n')
                
                print(f"📂 Archivo de texto leído: {filename}")
                print(f"   Líneas: {len(lines)}")
                
                return lines
                
        except Exception as e:
            raise RuntimeError(f"Error al leer archivo '{filename}': {str(e)}")
    
    def _write_file(self, filename, data):
        """Escribe datos a un archivo"""
        try:
            if not isinstance(filename, str):
                raise ValueError("El nombre del archivo debe ser una cadena")
            
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, list):
                    if data and isinstance(data[0], list):
                        # Matriz - escribir como CSV
                        for row in data:
                            f.write(','.join(str(cell) for cell in row) + '\n')
                    else:
                        # Lista - una línea por elemento
                        for item in data:
                            f.write(str(item) + '\n')
                else:
                    # Dato simple
                    f.write(str(data))
            
            print(f"💾 Datos escritos al archivo: {filename}")
            
        except Exception as e:
            raise RuntimeError(f"Error al escribir archivo '{filename}': {str(e)}")
    
    def _try_parse_number(self, value):
        """Intenta parsear un valor como número, si no es posible lo deja como string"""
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value
