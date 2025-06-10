import sys
import traceback
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from DeepLearningDSLLexer import DeepLearningDSLLexer
from DeepLearningDSLParser import DeepLearningDSLParser
from DSLInterpreterVisitor import DSLInterpreterVisitor

class DSLErrorListener(ErrorListener):
    """Maneja errores de parsing personalizado"""
    
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = f"Error de sintaxis en línea {line}, columna {column}: {msg}"
        self.errors.append(error_msg)
        print(f"❌ {error_msg}")

class DSLInterpreter:
    """Clase principal del intérprete"""
    
    def __init__(self):
        self.visitor = DSLInterpreterVisitor()
        self.history = []
    
    def execute_code(self, code):
        """Ejecuta código DSL y retorna el resultado"""
        try:
            # Crear lexer y parser
            input_stream = InputStream(code)
            lexer = DeepLearningDSLLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = DeepLearningDSLParser(stream)
            
            # Configurar manejo de errores
            error_listener = DSLErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)
            
            # Parsear el código
            tree = parser.program()
            
            # Si hay errores de parsing, no continuar
            if error_listener.errors:
                return False
            
            # Visitar el árbol y ejecutar
            result = self.visitor.visit(tree)
            
            # Guardar en historial
            self.history.append(code.strip())
            
            return True
            
        except Exception as e:
            print(f"❌ Error de ejecución: {str(e)}")
            if "--debug" in sys.argv:
                traceback.print_exc()
            return False
    
    def show_variables(self):
        """Muestra todas las variables definidas"""
        if not self.visitor.variables:
            print("📝 No hay variables definidas")
            return
        
        print("\n📝 Variables definidas:")
        print("-" * 50)
        for name, value in self.visitor.variables.items():
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:97] + "..."
            print(f"  {name} = {value_str}")
        print("-" * 50)
    
    def show_help(self):
        """Muestra ayuda del intérprete"""
        help_text = """
🚀 DSL Deep Learning - Intérprete Interactivo

COMANDOS ESPECIALES:
  .help         - Muestra esta ayuda
  .vars         - Muestra variables definidas
  .history      - Muestra historial de comandos
  .clear        - Limpia variables y historial
  .exit         - Sale del intérprete

SINTAXIS DEL LENGUAJE:

VARIABLES Y ASIGNACIONES:
  x = 5;
  nombre = "Juan";
  datos = [1, 2, 3, 4, 5];

MATRICES:
  matriz = [[1, 2], [3, 4]];
  transpuesta = transpose(matriz);
  inversa = inverse(matriz);
  producto = matmul(matriz, matriz);

OPERACIONES MATEMÁTICAS:
  resultado = x + 5 * 2;
  seno = sin(3.14159);
  raiz = sqrt(25);
  logaritmo = log(10);

ESTRUCTURAS DE CONTROL:
  if x > 0 then
    print("Positivo");
  else
    print("No positivo");
  fi

  while x < 10 do
    x = x + 1;
  done

MACHINE LEARNING:
  modelo = linearRegression(X, y);
  clasificador = mlpClassifier(X, y, [10, 5]);
  clusters = kmeans(datos, 3);

VISUALIZACIÓN:
  plot(x_values, y_values);
  scatter(x_data, y_data);
  hist(data);

ARCHIVOS:
  datos = readFile("archivo.csv");
  writeFile("salida.txt", datos);

EJEMPLOS:
  >>> x = [1, 2, 3, 4, 5];
  >>> y = [2, 4, 6, 8, 10];
  >>> modelo = linearRegression(x, y);
  >>> plot(x, y);
"""
        print(help_text)
    
    def show_history(self):
        """Muestra historial de comandos"""
        if not self.history:
            print("📜 No hay historial de comandos")
            return
        
        print("\n📜 Historial de comandos:")
        print("-" * 50)
        for i, cmd in enumerate(self.history, 1):
            print(f"  {i:2d}. {cmd}")
        print("-" * 50)
    
    def clear_session(self):
        """Limpia variables y historial"""
        self.visitor.variables.clear()
        self.history.clear()
        print("🧹 Sesión limpiada - variables e historial eliminados")
    
    def run_interactive(self):
        """Ejecuta el intérprete en modo interactivo"""
        print("🚀 DSL Deep Learning - Intérprete Interactivo")
        print("Escribe '.help' para ver ayuda o '.exit' para salir")
        print("-" * 60)
        
        while True:
            try:
                # Obtener entrada del usuario
                line = input(">>> ").strip()
                
                # Comandos especiales
                if line == ".exit":
                    print("👋 ¡Hasta luego!")
                    break
                elif line == ".help":
                    self.show_help()
                    continue
                elif line == ".vars":
                    self.show_variables()
                    continue
                elif line == ".history":
                    self.show_history()
                    continue
                elif line == ".clear":
                    self.clear_session()
                    continue
                elif line == "" or line.startswith("#"):
                    continue
                
                # Ejecutar código DSL
                if line and not line.endswith(';'):
                    # Si no termina en ;, agregar para expresiones simples
                    if any(op in line for op in ['=', 'if', 'while', 'plot', 'scatter', 'hist', 'readFile', 'writeFile']):
                        if not line.endswith(';'):
                            line += ';'
                    else:
                        # Para expresiones simples, agregar ; automáticamente
                        line += ';'
                
                success = self.execute_code(line)
                if success:
                    print("✅ Ejecutado correctamente")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
                break
            except EOFError:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {str(e)}")
                if "--debug" in sys.argv:
                    traceback.print_exc()

def main():
    """Función principal"""
    print("🔧 Inicializando intérprete DSL Deep Learning...")
    
    interpreter = DSLInterpreter()
    
    # Si hay argumentos, ejecutar archivo
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"📂 Ejecutando archivo: {filename}")
            print("-" * 60)
            
            success = interpreter.execute_code(code)
            
            if success:
                print("✅ Archivo ejecutado correctamente")
            else:
                print("❌ Error al ejecutar archivo")
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{filename}'")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error al leer archivo: {str(e)}")
            sys.exit(1)
    else:
        # Modo interactivo
        interpreter.run_interactive()

if __name__ == "__main__":
    main()
