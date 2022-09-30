import random
import math
import os

class Node(object):

    def __init__(self, name):
        ''' Se considera el nombre como un string '''
        self.name = name

    def get_name(self):
        return self.name

class Edge(object):

    def __init__(self, src, dest):
        '''src = source node, dest = destination node '''
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest



class Graph(object):
    # node is a list of the nodes in the graph
    # edges is a dict mapping each node to a list of its children
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_node(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate Node')
        else:
            self.nodes.append(node)
            self.edges[node] = []

    def get_nodes(self):
      return self.nodes

    def get_edges(self):
      return self.edges

    def add_edge(self, edge):
        src = edge.get_source()
        dest = edge.get_destination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        if dest not in self.edges[src]:
          self.edges[src].append(dest)

    def children_of(self, node):
        return self.edges[node]

    def has_node(self, node):
        return node in self.nodes

    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.get_name() + \
                    '--' + dest.get_name() + '\n'
        return result[:-1] # remove last newline

    def resultado(self):
        result = {}
        for src in self.nodes:
          result[src.get_name()]=[]
          for dest in self.edges[src]:
            result[src.get_name()].append(dest.get_name())
        return result

    def save_graph(self, grafo, nombreGrafo, nombre):
        file = open(f'{os.path.abspath(os.getcwd())}/{nombre}.dot', "w")
        file.write(f"graph {nombreGrafo}" + " {" + os.linesep)
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.get_name() + \
                    '--' + dest.get_name() + '\n'
        file.write(result)
        file.write('}')
        file.close()


    def grafoMalla(self, grafo, m, n):
        k = {}
        for i in range(m):
          for j in range(n):
            k[f'n_{i}_{j}'] = Node(f'n_{i}_{j}')
            grafo.add_node(k[f'n_{i}_{j}'])
        for i in range(m):
          for j in range(n):
            if i >= 1:
              grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i-1}_{j}']))
            if j >= 1:
              grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i}_{j-1}']))
            if i == (m-1):
              if j == (n-1):
                continue
              grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i}_{j+1}']))
            elif j == (n-1):
                grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i+1}_{j}']))
            else:
              grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i+1}_{j}']))
              grafo.add_edge(Edge(k[f'n_{i}_{j}'],k[f'n_{i}_{j+1}']))
        return grafo.resultado()

    def grafoErdosRenyi(self, grafo, n, m):
      k = {}
      for i in range(n):
        k[f'n_{i}'] = Node(f'n_{i}')
        grafo.add_node(k[f'n_{i}'])
      j = 0
      while j < m:
        position = [x for x in range(n)]
        p1 = random.choice(position)
        first_node = k[f'n_{p1}']
        position.remove(p1)
        p2 = random.choice(position)
        second_node = k[f'n_{p2}']
        grafo.add_edge(Edge(first_node,second_node))
        grafo.add_edge(Edge(second_node,first_node))
        j += 1
      return grafo.resultado()

    def grafoGilbert(self, grafo, n, p):
      k = {}
      for i in range(n):
        k[f'n_{i}'] = Node(f'n_{i}')
        grafo.add_node(k[f'n_{i}'])
      for i in range(n):
        for j in range(i):
          p_random = random.uniform(0,1)
          if p_random <= p:
            if i == j:
              continue
            else:
              grafo.add_edge(Edge(k[f'n_{i}'], k[f'n_{j}']))
              grafo.add_edge(Edge(k[f'n_{j}'], k[f'n_{i}']))
      return grafo.resultado()

    def grafoGeografico(self, grafo, n, r):
      k = {}
      for i in range(n):
        x = random.random()
        y = random.random()
        k[f'n_{i}'] = [Node(f'n_{i}'), x, y]
        grafo.add_node(k[f'n_{i}'][0])
      for i in range(n):
          for j in range(i):
            dist = math.sqrt((k[f'n_{j}'][1]-k[f'n_{i}'][1])**2 + (k[f'n_{j}'][2]-k[f'n_{i}'][1])**2)
            if dist <= r:
              if i == j:
                continue
              else:
                grafo.add_edge(Edge(k[f'n_{i}'][0], k[f'n_{j}'][0]))
                grafo.add_edge(Edge(k[f'n_{j}'][0], k[f'n_{i}'][0]))
      return grafo.resultado()    

    def grafoBarabasiAlbert(self, grafo, n, d):
      k = {}
      for i in range(n):
        k[f'n_{i}'] = Node(f'n_{i}')
        grafo.add_node(k[f'n_{i}'])
        for j in range(len(k)):
          if i == j:
            continue
          p = 1 - (len(grafo.children_of(grafo.get_nodes()[j])))/d
          p_random = random.uniform(0,1)
          if p_random <= p:
              grafo.add_edge(Edge(k[f'n_{i}'], k[f'n_{j}']))
              grafo.add_edge(Edge(k[f'n_{j}'], k[f'n_{i}']))
      return grafo.resultado()

    def grafoDorogovtsevMendes(self, grafo, n):
      while n < 3:
        n = int(input('n debe ser mayor o igual que 3: '))
      k={}
      for i in range(3):
        k[f'n_{i}'] = Node(f'n_{i}')
        grafo.add_node(k[f'n_{i}'])
      lista = [x for x in range(3)]
      for j in range(3):
        grafo.add_edge(Edge(k[f'n_{lista[j]}'], k[f'n_{lista[j-1]}']))
        grafo.add_edge(Edge(k[f'n_{lista[j-1]}'], k[f'n_{lista[j]}']))
      if n > 3:
        for i in range(3,n):
          l = len(k)
          k[f'n_{i}'] = Node(f'n_{i}')
          grafo.add_node(k[f'n_{i}'])
          node_random = grafo.get_nodes()[random.randint(0, l-1)]
          children = random.choice(grafo.children_of(node_random))
          grafo.add_edge(Edge(k[f'n_{i}'], node_random))
          grafo.add_edge(Edge(node_random, k[f'n_{i}']))
          grafo.add_edge(Edge(k[f'n_{i}'], children))
          grafo.add_edge(Edge(children, k[f'n_{i}']))
      return grafo.resultado() 
