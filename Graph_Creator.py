import networkx as nx
import matplotlib.pyplot as plt
import json

# Create a graph
def createGraph():
    G = nx.Graph()
    with open("Acquaintances.json", "r") as file:
        links_data = json.load(file)
    for link_data in links_data:
        name = link_data.get("name")
        acquaintances = link_data.get("acquaintances")
        G.add_node(name)
        for i in range(len(acquaintances)):
            G.add_edge(name, acquaintances[i])
    
    pos = nx.spring_layout(G, k = 0.7, seed= 1911)
    node_sizes = [10 * G.degree[node] for node in G.nodes]
    plt.figure(figsize=(19.20, 10.80))
    plt.get_current_fig_manager().window.wm_geometry(f"{1920}x{1080}+0+0")
    nx.draw_networkx_nodes(G, pos, node_color="#A0A0FF", node_size=node_sizes)
    nx.draw_networkx_edges(G, pos, edge_color="#202020", alpha=0.2)
    nx.draw_networkx_labels(G, pos, font_size= 7)
    return G
        
def degreeDistribution(G):
    degrees = dict(G.degree())
    plt.figure(figsize=(19.20, 10.80))
    plt.get_current_fig_manager().window.wm_geometry(f"{1920}x{1080}+0+0")
    plt.hist(degrees.values(), bins=range(min(degrees.values()), max(degrees.values()) + 2, 1), align='left', histtype= "barstacked", edgecolor='black')
    plt.xlabel('Node Degree')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.grid(axis='y', linestyle='--', alpha=0.7, which='both')
    plt.show()

def graphAttributes(G):
    mostPopulars = sorted(G.degree, key=lambda x: x[1], reverse=True)[:5] 
    betweenness_centrality = nx.betweenness_centrality(G)
    max_betweenness_centrality_node = max(betweenness_centrality, key=betweenness_centrality.get)
    average_clustering_coefficient = nx.average_clustering(G)

    print("Most Popular 5 people and their degrees: "+ ", ".join(map(str, mostPopulars)))
    print("Number of edges: " + str(G.number_of_edges()))
    print("Number of nodes: " + str(G.number_of_nodes()))
    print("Maximum Betweenness Centrality: " + str(max_betweenness_centrality_node))
    print("Average clustering coefficient: " + str(average_clustering_coefficient))

def jaccard_similarity(graph, node1, node2):
    neighbors_node1 = set(graph.neighbors(node1))
    neighbors_node2 = set(graph.neighbors(node2))

    intersection_size = len(neighbors_node1.intersection(neighbors_node2))
    union_size = len(neighbors_node1.union(neighbors_node2))

    if union_size == 0:
        print("There is no similarity between the two nodes")
    else:
        print("The Jaccard between " + str(node1) + " and " + str(node2) + str(intersection_size / union_size))
    
def small_world_coefficient(graph):
    if not nx.is_connected(graph):
        print("Graph is not connected. Calculating for the largest connected component.")
        largest_component = max(nx.connected_components(graph), key=len)
        graph = graph.subgraph(largest_component)

    clustering_coefficient = nx.average_clustering(graph)
    average_shortest_path = nx.average_shortest_path_length(graph)

    random_graph = nx.random_reference(graph, niter=3, connectivity=True)
    random_clustering_coefficient = nx.average_clustering(random_graph)
    random_average_shortest_path = nx.average_shortest_path_length(random_graph)

    omega = (random_clustering_coefficient / clustering_coefficient) / (random_average_shortest_path / average_shortest_path)
    print("Average Shortest Path: " + str(average_shortest_path))
    print(f"Small-world coefficient: {omega}")

G = createGraph()
degreeDistribution(G)
graphAttributes(G)
jaccard_similarity(G, "Jarl Balgruuf the Greater", "Jarl Igmund")
#small_world_coefficient(G)

plt.show()
