from pype.lexer import lexer
from pype.parser import parser
#from ast import *
from pype.semantic_analysis import CheckSingleAssignment
from pype.translate import SymbolTableVisitor

class Pipeline(object):
  def __init__(self, source):
    with open(source) as f:
      self.compile(f)

  def compile(self, file):
    input = file.read()
    # Lexing, parsing, AST construction
    ast = parser.parse(input, lexer=lexer)
    # Semantic analysis
    ast.walk( CheckSingleAssignment() )
    # Translation
    syms = ast.walk( SymbolTableVisitor())
    syms.pprint()
    return syms

t=Pipeline('./samples/example1.ppl')
