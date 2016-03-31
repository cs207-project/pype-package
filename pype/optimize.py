from fgir import *
from error import *

# Optimization pass interfaces

class Optimization(object):
  def visit(self, obj): pass

class FlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR.
  May modify the flowgraph by adding or removing nodes (return a new Flowgraph).
  If you modify nodes, make sure inputs, outputs, and variables are all updated.
  May NOT add or remove flowgraphs.'''
  pass

class NodeOptimization(Optimization):
  '''Called on each node in a FGIR.
  May modify the node (return a new Node object, and it will be assigned).
  May NOT remove or add nodes (use a component pass).'''
  pass

class TopologicalNodeOptimization(NodeOptimization): pass

# Optimization pass implementations

class PrintIR(TopologicalNodeOptimization):
  'A simple "optimization" pass which can be used to debug topological sorting'
  def visit(self, node):
    print(str(node))

class AssignmentEllision(FlowgraphOptimization):
  '''Eliminates all assignment nodes.
  Assignment nodes are useful for the programmer to reuse the output of an
  expression multiple times, and the lowering transformation generates explicit
  flowgraph nodes for these expressions. However, they are not necessary for
  execution, as they simply forward their value. This removes them and connects
  their pre- and post-dependencies.'''

  def visit(self, flowgraph):
    # TODO: implement this
    #print(flowgraph.variables.items())
    #print(flowgraph)

    # reversed k, v in origin dict
    var_v_k = dict(map(reversed, flowgraph.variables.items()))
    n_keys = var_v_k.keys()
    n_values = var_v_k.values()

    # storage of deleting nodes
    delNodes = [] # store the deleting nodes
    for nodes in flowgraph.variables.items():

      # find assignment nodes
      if nodes[1].type == FGNodeType.assignment:

        # get its pre-denpendencies
        delNodes.append(nodes[0])
        pred = (nodes[1].inputs)[-1]
        del (nodes[1].inputs)[-1]

      # change name and connect pre-post dependencies edges
        if nodes[0] in n_keys:
          flowgraph.variables[var_v_k[nodes[0]]] = pred

        for n_nodes in flowgraph.nodes.items():

        # reconnect all the nodes
          if nodes[0] in n_nodes[1].inputs:

          # delect those edges that connected with the assignment nodes
            n_nodes[1].inputs = [a for a in n_nodes[1] if a != nodes[0]]
            n_nodes[1].inputs.append(pred)
    for n in delNodes:
      del flowgraph.nodes[n]

    return flowgraph


class DeadCodeElimination(FlowgraphOptimization):
  '''Eliminates unreachable expression statements.
  Statements which never affect any output are effectively useless, and we call
  these "dead code" blocks. This optimization removes any expressions which can
  be shown not to affect the output.
  NOTE: input statements *cannot* safely be removed, since doing so would change
  the call signature of the component. For example, it might seem that the input
  x could be removed:
    { component1 (input x y) (output y) }
  but imagine this component1 was in a file alongside this one:
    { component2 (input a b) (:= c (component a b)) (output c) }
  By removing x from component1, it could no longer accept two arguments. So in
  this instance, component1 will end up unmodified after DCE.'''

  def visit(self, flowgraph):
    # TODO: implement this
    return flowgraph
x = FGIR()
x.graphs['test'] = FG
print(x.flowgraph_pass(AssignmentEllision())),'===================='