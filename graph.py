import networkx as nx
import matplotlib.pyplot as plt

# Створення графа
G = nx.Graph()

# Додавання вершин (міста України)
ukrainian_cities = ["Київ", "Харків", "Львів", "Одеса", "Дніпро"]
G.add_nodes_from(ukrainian_cities)

# Додавання ребер (зв'язків між містами) з вагами
connections_with_weights = [
    ("Київ", "Харків", 500),
    ("Київ", "Львів", 550),
    ("Київ", "Одеса", 480),
    ("Харків", "Дніпро", 220),
    ("Львів", "Одеса", 800),
    ("Львів", "Дніпро", 950),
    ("Одеса", "Дніпро", 600),
    ("Дніпро", "Київ", 450)
]

for edge in connections_with_weights:
    G.add_edge(edge[0], edge[1], weight=edge[2])


# Аналіз основних характеристик графа
print("Кількість вершин:", G.number_of_nodes())
print("Кількість ребер:", G.number_of_edges())
print("Ступінь вершин:", dict(G.degree()))

# Реалізація алгоритмів DFS і BFS
def dfs_paths(graph, start, end, path=None):
    if path is None:
        path = [start]
    if start == end:
        yield path
    for neighbor in set(graph.neighbors(start)) - set(path):
        yield from dfs_paths(graph, neighbor, end, path + [neighbor])

def bfs_paths(graph, start, end):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for neighbor in set(graph.neighbors(vertex)) - set(path):
            if neighbor == end:
                yield path + [neighbor]
            else:
                queue.append((neighbor, path + [neighbor]))

# Знаходження шляхів використовуючи DFS і BFS
start_city = "Київ"
end_city = "Одеса"

dfs_result = list(dfs_paths(G, start_city, end_city))
bfs_result = list(bfs_paths(G, start_city, end_city))

# Виведення результатів
print("\nDFS шляхи з", start_city, "до", end_city, ":", dfs_result)
print("\nBFS шляхи з", start_city, "до", end_city, ":", bfs_result)

# Застосування алгоритму Дейкстри для знаходження найкоротших шляхів
all_shortest_paths = dict(nx.all_pairs_dijkstra_path(G, weight='weight'))

# Виведення результатів
for source in all_shortest_paths:
    print(f"\nНайкоротші шляхи для міста {source}:")
    for target, path in all_shortest_paths[source].items():
        if source != target:
            weight = nx.dijkstra_path_length(G, source=source, target=target, weight='weight')
            print(f"Від {source} до {target}: {path}, Довжина: {weight}")


# Візуалізація графа
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=10, edge_color='gray')

# Відображення ваг ребер на графі
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображення графа
plt.show()
