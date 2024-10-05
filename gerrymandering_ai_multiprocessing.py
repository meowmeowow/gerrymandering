from enum import Enum
import ast
import concurrent.futures


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


def dfs(graph, start_node, num_per_district):
    visited = set()
    all_paths = []
    path = []

    def dfs_helper(node):
        visited.add(node)
        path.append(node)

        if len(visited) == len(graph.adjacency_list):
            affiliation_sums = []
            for i in range(0, len(path), num_per_district):
                if i + num_per_district - 1 < len(path):
                    subset_sum = sum(graph.node_colors[path[j]].value for j in range(i, i + num_per_district))
                    affiliation_sums.append(subset_sum)
            all_paths.append((list(path), affiliation_sums))

        for neighbor in graph.adjacency_list.get(node, []):
            if neighbor not in visited:
                dfs_helper(neighbor)

        visited.remove(node)
        path.pop()

    dfs_helper(start_node)
    return all_paths


def get_all_paths_parallel(graph, start_nodes, num_per_district):
    # Use a process pool for parallelism
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Run DFS on each start_node in parallel
        results = list(executor.map(dfs, [graph] * len(start_nodes), start_nodes, [num_per_district] * len(start_nodes)))

    # Combine all paths from the processes
    all_paths = []
    for result in results:
        all_paths.extend(result)
    return all_paths


if __name__ == "__main__":
    # Initialize the graph
    graph = Graph()

    # Read data in from mapinfo.txt
    with open('mapinfo.txt') as f:
        lines = f.readlines()
        edges = ast.literal_eval(lines[0])
        colors = ast.literal_eval(lines[1])

    # Input into the graph
    for edge in edges:
        graph.add_edge(edge[0], edge[1])

    for color in colors:
        graph.set_color(color[0], Color[color[1]])

    # Number of nodes and districts
    num = 135
    districts = 9
    num_per_district = int(num / districts)

    # Run DFS in parallel starting from multiple nodes
    start_nodes = list(graph.adjacency_list.keys())
    all_paths = get_all_paths_parallel(graph, start_nodes, num_per_district)

    # Write results to allpaths.txt
    with open("allpaths.txt", "a") as d:
        d.write(str(all_paths))
