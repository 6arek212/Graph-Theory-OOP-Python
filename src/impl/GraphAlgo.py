import heapq

from src.api.GraphAlgoInterface import GraphAlgoInterface
from src.api.GraphInterface import GraphInterface
from src.impl.DiGraph import DiGraph
from typing import List
import json
import sys
import matplotlib.pyplot as plt
from numpy import inf


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        json_graph = DiGraph()
        try:
            with open(file_name) as json_file:
                #dic of json
                json_data = json.load(json_file)
            for n in json_data["Nodes"]:
                    key = n["id"]
                    if "pos" not in n:
                        json_graph.add_node(key)
                    else:
                      x, y,z = map(float, str(n["pos"]).split(","))
                      pos = (x,y,z)
                      json_graph.add_node(key, pos)
            for edge in json_data["Edges"]:
                json_graph.add_edge(edge["src"], edge["dest"], edge["w"])
            self.graph = json_graph
            return True
        except Exception as e:
            print("loading from json FAILED!! " + str(e))
            return False

    def save_to_json(self, file_name: str) -> bool:

      to_json = {"Edges": [] , "Nodes" : []}

      with open(file_name , 'w') as json_file:
        try:
           for n in  self.graph.get_all_v().values():
              if n.pos is None:
                  to_json["Nodes"].append({"id:" , n.key})
              else:
                to_json["Nodes"].append({"pos": f"{n.pos[0]},{n.pos[1]},{n.pos[2]}", "id": n.key})

           for n in self.graph.get_all_v().keys():
             out_edges = self.graph.all_out_edges_of_node(n)
             for key_out_node  in out_edges:
                 to_json["Edges"].append({"src": n, "w": out_edges[key_out_node] , "dest": key_out_node})

           json.dump(to_json , json_file , indent=2)
           return True
        except Exception as e:
            print("saving to json FAILED!! " + str(e))
            return False


    def shortest_path(self, id1: int, id2: int) -> (float, list):

        if self.graph is None or self.graph.Nodes.get(id1) is None or  self.graph.Nodes.get(id2) is None:
            return float("inf"), []

        dist = {}
        for i in self.graph.Nodes.keys():
            dist[i] = inf
        previous = {id1 : -1}
        dist [id1] = 0
        queue = []
        #priority queue taking the min
        heapq.heappush(queue , (0 ,id1))

        while queue:
            #taking the second element in tuple
            curr_min_node = heapq.heappop(queue)[1]

            if curr_min_node == id2:
                break

            for neighbour , w in self.graph.all_out_edges_of_node(curr_min_node).items():

                currWight = dist[curr_min_node] + w

                if currWight < dist[neighbour]:
                    dist[neighbour] = currWight
                    previous[neighbour] = curr_min_node
                    heapq.heappush(queue , (dist[neighbour] , neighbour))


        shortestPath  = []
        curr = id2
        if dist[id2] == inf:
            return  inf , []

        while curr !=-1:
            shortestPath.insert(0 , curr)
            curr = previous[curr]


        return dist[id2] , shortestPath



    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass

    def centerPoint(self) -> (int, float):
        pass

    def plot_graph(self) -> None:
        pass