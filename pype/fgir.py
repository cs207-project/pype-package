import enum

FGNodeType = enum.Enum('FGNodeType','component libraryfunction librarymethod input output assignment literal unknown')

class FGNode(object):
  def __init__(self, nodeid, nodetype, ref=None, inputs=[]):
    self.nodeid = nodeid
    self.type = nodetype
    self.ref = ref
    self.inputs = inputs
  def __repr__(self):
    return '<'+str(self.type)+' '+str(self.nodeid)+'<='+','.join(map(str,self.inputs))+' : '+str(self.ref)+'>'

class Flowgraph(object):
  def __init__(self, name='?'):
    self.name = name
    self.variables = {} # { str -> nodeid }
    self.nodes = {} # { nodeid -> Node }
    self.inputs = [] # [ nodeid, ... ]
    self.outputs = [] # [ nodeid, ... ]
    self._id_counter = 0

  def new_node(self,nodetype,ref=None):
    nid = '@N'+str(self._id_counter)
    self._id_counter += 1
    node = FGNode(nid, nodetype, ref, [])
    self.nodes[nid] = node
    return node

  def get_var(self, name):
    return self.variables.get(name, None)

  def set_var(self, name, nodeid):
    self.variables[name] = nodeid

  def add_input(self, nodeid):
    self.inputs.append(nodeid)

  def add_output(self, nodeid):
    self.outputs.append(nodeid)

  def dotfile(self):
    s = ''
    s+= 'digraph '+self.name+' {\n'
    for (src,node) in self.nodes.items():
      for dst in node.inputs:
        s+= '  "'+str(dst)+'" -> "'+str(src)+'"\n'
    for (var,nid) in self.variables.items():
      s+= '  "'+str(nid)+'" [ label = "'+str(var)+'" ]\n'
    for nid in self.inputs:
      s+= '  "'+str(nid)+'" [ color = "green" ]\n'
    for nid in self.outputs:
      s+= '  "'+str(nid)+'" [ color = "red" ]\n'
    s+= '}\n'
    return s
    

  def pre(self, nodeid):
    return self.nodes[nodeid].inputs

  def post(self, nodeid):
    return [i for (i,n) in self.nodes.items() if nodeid in self.nodes[i].inputs]

  ''' 
  Kahn algorithm, try both
  def topological_sort(self):
    # TODO : implement a topological sort
    graph_sorted = []
    for i in self.nodes.items():
      print(i,'selfnodes\n')
    graph_unsorted = list(self.nodes.keys())
    print(graph_unsorted,'graph_unsorted\n')

    while graph_unsorted:
      acyclic = False
      for node in graph_unsorted:
        for edge in self.nodes[node].inputs:
          if edge in graph_unsorted:
            break
        else:
          acyclic = True
          graph_unsorted.remove(node)
          graph_sorted.append(node)
      if not acyclic:
        raise RuntimeError('A cyclic dependency occur')
    print(graph_sorted,'graph_sorted')
    return graph_sorted # should return a list of node ids in sorted order
  '''

  def recursive_visit(self, node, graph_sorted, graph_unsorted_keys):
    if node in graph_sorted:
      #print("Hit the bottom")
      return
    else:
      for n in self.nodes[node].inputs:
        self.recursive_visit(n, graph_sorted, graph_unsorted_keys)
      graph_sorted.append(node)
      graph_unsorted_keys.remove(node)
      return 


  def topological_sort(self, debug = False):
    graph_sorted = []
    graph_unsorted_keys = list(self.nodes.keys())
    graph_unsorted_kv = list(self.nodes.items())
    length = len(graph_unsorted_keys)
    while graph_unsorted_keys:
      node = graph_unsorted_keys[0]
      self.recursive_visit(node, graph_sorted, graph_unsorted_keys)
    #assert (len(graph_sorted)==length),'The length is wrong'
    if debug:
      print('Sorted Graph has order {}'.format(graph_sorted))
    return graph_sorted



class FGIR(object):
  def __init__(self):
    self.graphs = {} # { component_name:str => Flowgraph }

  def __getitem__(self, component):
    return self.graphs[component]

  def __setitem__(self, component, flowgraph):
    self.graphs[component] = flowgraph

  def __iter__(self):
    for component in self.graphs:
      yield component

  def flowgraph_pass(self, flowgraph_optimizer):
    for component in self.graphs:
     # print(self.graphs[component])
      fg = flowgraph_optimizer.visit(self.graphs[component])
      if fg is not None:
        self.graphs[component] = fg

  def node_pass(self, node_optimizer, *args, topological=False):
    for component in self.graphs:
      fg = self.graphs[component]
      if topological:
        node_order = fg.topological_sort()
      else:
        node_order = fg.nodes.keys()
      for node in node_order:
        n = node_optimizer.visit(fg.nodes[node])
        if n is not None:
          fg.nodes[node] = n

  def topological_node_pass(self, topo_optimizer):
    self.node_pass(topo_optimizer, topological = True)

# for testing the sort (test case from Pype Part 3 explanation)
# just refer to Pype 3 part 3 graph
FG = Flowgraph('TEST_1')

A = FG.new_node(FGNodeType.unknown, 'x')
B = FG.new_node(FGNodeType.unknown, 'y')
C = FG.new_node(FGNodeType.unknown, 'n2')
D = FG.new_node(FGNodeType.unknown, 'z')
E = FG.new_node(FGNodeType.unknown, 'n4')
F = FG.new_node(FGNodeType.assignment, 'n5') #this is dead code for test
H = FG.new_node(FGNodeType.unknown, 'n6')
I = FG.new_node(FGNodeType.unknown, 'n7')

A.inputs = []
B.inputs = []
C.inputs = ['@N0','@N1']
D.inputs = ['@N2']
E.inputs = ['@N3']
F.inputs = ['@N6']
I.inputs = ['@N5']
FG.topological_sort(True)
FG.outputs = ['@N4']
# print(FG.inputs)

x = FGIR()
x.graphs['test'] = FG
print(x.graphs['test'].dotfile(), 'original graph')
##??? x.flowgraph_pass(AssignmentEllision)
