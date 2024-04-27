import networkx as nx
import matplotlib.pyplot as plt

class Intersection:
    def __init__(self, intersection_id):
        self.id = intersection_id
        self.connected_roads = []

    def add_road(self, road_id):
        self.connected_roads.append(road_id)

class Road:
    def __init__(self, road_id, road_name, length):
        self.id = road_id
        self.road_name = road_name
        self.length = length

class RoadNetworkGraph:
    def __init__(self):
        self.intersections = {}
        self.roads = {}
        self.next_road_id = 1

    def add_intersection(self, intersection_id):
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = Intersection(intersection_id)

    def add_road(self, road_id, road_name, length):
        self.roads[road_id] = Road(road_id, road_name, length)
        return road_id

    def connect_intersection_to_road(self, intersection_id, road_id):
        if intersection_id in self.intersections and road_id in self.roads:
            intersection = self.intersections[intersection_id]
            intersection.add_road(road_id)

    def visualize_graph(self):
        G = nx.DiGraph()

        for intersection_id in self.intersections:
            G.add_node(intersection_id)

        for road_id, road in self.roads.items():
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    G.add_edge(intersection_id, road_id, road_name=f"{road.road_name} (ID: {road.id})", length=road.length)

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, scale=5)
        nx.draw(G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{G.edges[u, v]['road_name']} ({G.edges[u, v]['length']} KM)" for u, v in G.edges()}, font_size=10, font_color='red')
        plt.title("Road Network Graph")
        plt.show()

    def ensure_vertex_connectivity(self):
        for intersection_id in self.intersections:
            if not self.intersections[intersection_id].connected_roads:
                print("Intersection", intersection_id, "is not connected to any road.")
                break

    def find_shortest_path(self, start_intersection_id, end_intersection_id):
        G = nx.Graph()
        for road_id, road in self.roads.items():
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    G.add_edge(intersection_id, road_id, weight=road.length)

        if nx.has_path(G, start_intersection_id, end_intersection_id):
            shortest_path = nx.shortest_path(G, source=start_intersection_id, target=end_intersection_id, weight='weight')
            return shortest_path
        else:
            return None

    def routing_suggestions(self, start_intersection_id, end_intersection_id):
        shortest_path = self.find_shortest_path(start_intersection_id, end_intersection_id)
        if shortest_path:
            suggestions = []
            for i in range(len(shortest_path) - 1):
                intersection_id = shortest_path[i]
                road_id = shortest_path[i + 1]
                for connected_road_id in self.intersections[intersection_id].connected_roads:
                    if connected_road_id == road_id:
                        road = self.roads[road_id]
                        suggestions.append(road.road_name)
                        break
            return suggestions
        else:
            return None

    def plot_shortest_path(self, start_intersection_id, end_intersection_id):
        shortest_path = self.find_shortest_path(start_intersection_id, end_intersection_id)
        if shortest_path:
            G = nx.DiGraph()
            for intersection_id in self.intersections:
                G.add_node(intersection_id)

            for road_id, road in self.roads.items():
                for intersection_id in self.intersections:
                    if road_id in self.intersections[intersection_id].connected_roads:
                        G.add_edge(intersection_id, road_id, road_name=f"{road.road_name} (ID: {road.id})", length=road.length)

            edge_colors = ['black' if (u, v) not in shortest_path else 'red' for u, v in G.edges()]
            edge_labels = {(u, v): f"{G.edges[u, v]['road_name']} ({G.edges[u, v]['length']} KM)" for u, v in G.edges()}

            plt.figure(figsize=(10, 10))
            pos = nx.spring_layout(G, scale=5)
            nx.draw(G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold', edge_color=edge_colors)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red')
            plt.title("Shortest Path")
            plt.show()
        else:
            print("No path between the intersections.")

    def plot_routing_suggestions(self, start_intersection_id, end_intersection_id):
        suggestions = self.routing_suggestions(start_intersection_id, end_intersection_id)
        if suggestions:
            G = nx.DiGraph()
            for intersection_id in self.intersections:
                G.add_node(intersection_id)

            for road_id, road in self.roads.items():
                for intersection_id in self.intersections:
                    if road_id in self.intersections[intersection_id].connected_roads:
                        G.add_edge(intersection_id, road_id, road_name=f"{road.road_name} (ID: {road.id})", length=road.length)

            suggested_edges = [(u, v) for u, v in G.edges() if G.edges[u, v]['road_name'] in suggestions]

            plt.figure(figsize=(10, 10))
            pos = nx.spring_layout(G, scale=5)
            nx.draw(G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold')
            nx.draw_networkx_edges(G, pos, edgelist=suggested_edges, edge_color='red', width=2)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G.edges[u, v]['road_name'] for u, v in suggested_edges}, font_size=10, font_color='red')
            plt.title("Routing Suggestions")
            plt.show()
        else:
            print("No routing suggestions available.")


# Create a road network graph
road_network = RoadNetworkGraph()

# Add intersections
for i in range(1, 6):
    road_network.add_intersection(i)

# Add roads and connect them to intersections
road_network.add_road(1, "Anwar st", 10)
road_network.add_road(2, "AlQudarat st", 15)
road_network.add_road(3, "Sheikh Zayed st", 8)
road_network.add_road(4, "Khaleej AlArab st", 12)
road_network.add_road(5, "Qarm st", 7)

# Connect intersections to roads
road_network.connect_intersection_to_road(1, 4)
road_network.connect_intersection_to_road(1, 2)
road_network.connect_intersection_to_road(2, 3)
road_network.connect_intersection_to_road(3, 4)
road_network.connect_intersection_to_road(4, 5)

# Visualize the road network graph
road_network.visualize_graph()

# Ensure vertex connectivity
road_network.ensure_vertex_connectivity()

# Plot the shortest path between two intersections
start_intersection_id = 3
end_intersection_id = 5
road_network.plot_shortest_path(start_intersection_id, end_intersection_id)

# Plot routing suggestions between two intersections
road_network.plot_routing_suggestions(start_intersection_id, end_intersection_id)
