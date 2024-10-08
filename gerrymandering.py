


from enum import Enum
import ast
import cv2



class Color(Enum):
    PURPLE = 1
    ORANGE = 0


eff_gap = None
eff_gap_max = 0.1
winner_wanted = Color.PURPLE

"""
map = 'map.png'
map_info = 'mapinfobig.txt'
"""

map = 'small_map.png'
map_info = 'mapinfosmall.txt'

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

    def check_conditions(self, affiliation_sums):

        #purple = 1
        #orange = 0
        if 1:
            ##returns true if orange won
            districts_won = 0
            global eff_gap

            wasted1 = 0
            wasted2 = 0

            for sum in affiliation_sums:
                if((num_per_district-sum) > (int(num_per_district/2))):
                    districts_won+=1
                    #orange wins
                    wasted2 += sum
                    wasted1 += (num_per_district-sum)%(int(num_per_district/2)+1)
                else:
                    wasted2 += sum%(int(num_per_district/2)+1)
                    wasted1 += num_per_district-sum
            eff_gap = round(abs(wasted1-wasted2)/num,3)
            #eff_gap check
            if(eff_gap > eff_gap_max):
                return(False)

            #win check
            if(districts_won > int(districts/2)):

                if(winner_wanted == Color.ORANGE):
                    return(True)
                return(False)
            if(winner_wanted == Color.PURPLE):
                return(True)
            return(False)

    def get_all_paths(self, start_node):
        visited = set()
        path = []

        def dfs_helper(node):

            visited.add(node)
            path.append(node)

            if len(visited) == len(self.node_colors):
                affiliation_sums = []
                for i in range(0, len(path), num_per_district):
                    if i + num_per_district-1 < len(path): 
                        subset_sum = sum(self.node_colors[path[j]].value for j in range(i, i + num_per_district))
                        affiliation_sums.append(subset_sum)
                if(self.check_conditions(affiliation_sums) == True):
                    returnlist = [path, affiliation_sums]
                    return(returnlist)

            for neighbor in self.adjacency_list.get(node):
                if neighbor not in visited:
                    result = dfs_helper(neighbor)
                    if result:
                        return result;

            visited.remove(node)
            path.pop()
            

        return(dfs_helper(start_node))

graph = Graph()


#read data in from mapinfo.txt

f=open(map_info)
lines=f.readlines()
edges = ast.literal_eval(lines[0])
colors = ast.literal_eval(lines[1])
points = ast.literal_eval(lines[2])

f.close()

#input into graph


for edge in edges:
    graph.add_edge(edge[0], edge[1])


for color in colors:
    graph.set_color(color[0], Color[color[1]])


num = 15
districts = 5

num_per_district = int(num/districts)


paths = graph.get_all_paths(0)

img = cv2.imread(map) 

i = 0
for node in paths[0]:
    #from node id -> get x,y

    for point in points:
        if(point[3] == node):



            cv2.putText(img, 'g: ' + str(int(i/num_per_district)+1), (int(point[0]), int(point[1])), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2) 
            continue
    i+=1


cv2.putText(img, "winner: "+ str(winner_wanted.name), (100, 100), 
cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2) 

cv2.putText(img, "eff_gap: "+ str(eff_gap), (100, 200), 
cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2) 

cv2.imshow('path', img) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 
