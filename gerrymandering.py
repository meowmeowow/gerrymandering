


from enum import Enum
import ast

class Color(Enum):
    PURPLE = 1
    ORANGE = 0


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.node_colors = {}

    def add_edge(self, u, v):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

    def set_color(self, node, color):
        self.node_colors[node] = color

    def get_all_paths(self, start_node):
        visited = set()
        all_paths = []
        path = []

        def dfs_helper(node):
            visited.add(node)
            path.append(node)

            if len(visited) == len(self.adjacency_list):
                affiliation_sums = []
                for i in range(0, len(path), num_per_district):
                    if i + num_per_district-1 < len(path): 
                        subset_sum = sum(self.node_colors[path[j]].value for j in range(i, i + num_per_district))
                        affiliation_sums.append(subset_sum)
                all_paths.append((list(path), affiliation_sums))

            for neighbor in self.adjacency_list.get(node):
                if neighbor not in visited:
                    dfs_helper(neighbor)

            visited.remove(node)
            path.pop()

        dfs_helper(start_node)
        return all_paths

graph = Graph()


#read data in from mapinfo.txt

f=open('mapinfo.txt')
lines=f.readlines()
edges = ast.literal_eval(lines[0])
colors = ast.literal_eval(lines[1])
f.close()

#input into graph


for edge in edges:
    graph.add_edge(edge[0], edge[1])


for color in colors:
    graph.set_color(color[0], Color[color[1]])


num = 135
districts = 9

num_per_district = int(num/districts)


all_paths = graph.get_all_paths(0)



d = open("allpaths.txt", "a")
d.write(str(all_paths))
d.close()
