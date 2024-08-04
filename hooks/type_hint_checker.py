import ast
import sys

class TypeHintChecker(ast.NodeVisitor):
    
    def __init__(self):
        self.errors = []

    def visit_ClassDef(self, node):
        if any(self.is_base_model(base) for base in node.bases):
            for field in node.body:
               if isinstance(field, (ast.AnnAssign, ast.Assign)) and (not hasattr(field, 'annotation') or field.annotation is None):
                # Field name for ast.Assign can be more complex to extract
                field_name = field.targets[0].id if hasattr(field.targets[0], 'id') else 'unknown'
                self.errors.append((field.lineno, f"Field '{field_name}' in class '{node.name}' lacks a type hint"))
        self.generic_visit(node)

    def is_base_model(self, base):
        try:
            while isinstance(base, ast.Attribute):
                base = base.value
            return isinstance(base, ast.Name) and base.id in {'BaseModel', 'BM'}
        except AttributeError:
          return False

    def check_file(self, filename): #dosyayı oku AST olusturur
        with open(filename, 'r', encoding='utf-8') as file:
            node = ast.parse(file.read(), filename=filename)
            self.visit(node)
        print(filename)
        if self.errors:
            for error in self.errors:
                print(f"{filename}:{error[0]}: {error[1]}")
            sys.exit(1)

def run_check(filenames):
    all_errors = []

    for filename in filenames:
        checker = TypeHintChecker()
        checker.check_file(filename)
    if all_errors:
        sys.exit(1)

if __name__ == "__main__":
    run_check(sys.argv[1:])
