from pytest import raises
from tests.test_fgir import *
from pype.optimize import *
import copy



def test_AssignmentEllision():
    test_fg = copy.deepcopy(FG)
    test_AE = AssignmentEllision()
    test_AE.visit(test_fg)
    # print(test_fg.nodes.keys())
    assert set(test_fg.nodes.keys()) == set(['@N6', '@N0', '@N1', '@N7', '@N2', '@N4'])
    # print(test_fg.dotfile())
  #   assert test_fg.dotfile()=='digraph TEST_1 {\n \
  # "@N2" -> "@N4"\n\
  # "@N0" -> "@N2"\n\
  # "@N1" -> "@N2"\n\
  # "@N6" -> "@N7"\n\
  # "@N4" [ color = "red" ]\n\
  # }\n'

def test_DeadCodeElimination():
    test_fg = copy.deepcopy(FG)
    testDeadCodeElimination = DeadCodeElimination()
    testDeadCodeElimination.visit(test_fg)
    assert set(test_fg.nodes.keys()) == set(['@N4', '@N3', '@N0', '@N2', '@N1'])
  #   assert FG.dotfile()== 'digraph TEST_1 {\
  # "@N2" -> "@N3"\
  # "@N3" -> "@N4"\
  # "@N0" -> "@N2"\
  # "@N1" -> "@N2"\
  # "@N4" [ color = "red" ]\
  # }'
