import streamlit as st
import heapq
import time
import random

st.set_page_config(page_title="Experiment 4", page_icon="🛣️")

st.title("Experiment 4 - Dijkstra's Shortest Path Algorithm")


def dijkstra(graph, source):

    n = len(graph)

    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]
    visited = set()

    while pq:

        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):

    path = []

    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

st.write("### Sample Graph")

graph_table = []

for u in graph:
    for v, w in graph[u]:
        graph_table.append({
            "Source": u,
            "Destination": v,
            "Weight": w
        })

st.table(graph_table)

source = st.number_input(
    "Enter Source Vertex",
    min_value=0,
    max_value=len(graph) - 1,
    value=0,
    step=1
)

if st.button("Find Shortest Paths"):

    dist, prev = dijkstra(graph, source)

    results = []

    for v in range(len(graph)):

        path = reconstruct_path(prev, source, v)

        results.append({
            "Vertex": v,
            "Distance": dist[v] if dist[v] != float("inf") else "INF",
            "Path": " -> ".join(map(str, path)) if path else "No Path"
        })

    st.write("### Shortest Paths")

    st.table(results)

st.write("---")

if st.button("Run Performance Analysis"):

    st.write("### Performance Analysis")

    sizes = [100, 500, 1000, 2000]

    table = []

    for size in sizes:

        random_graph = {}

        for i in range(size):

            neighbors = []

            for _ in range(3):
                v = random.randint(0, size - 1)

                if v != i:
                    neighbors.append((v, random.randint(1, 20)))

            random_graph[i] = neighbors

        start = time.perf_counter()

        for _ in range(20):
            dijkstra(random_graph, 0)

        elapsed = (time.perf_counter() - start) / 20 * 1000

        table.append({
            "Vertices": size,
            "Execution Time (ms)": round(elapsed, 5)
        })

    st.table(table)