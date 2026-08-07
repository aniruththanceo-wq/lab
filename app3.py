import streamlit as st
import heapq
import time

st.set_page_config(page_title="Experiment 3", page_icon="🌳")

st.title("Experiment 3 - Minimum Spanning Tree")


class UnionFind:

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


def kruskal(n, edges):

    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    cost = 0

    for w, u, v in edges:

        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


def prim(n, adj, start=0):

    key = [float("inf")] * n
    parent = [-1] * n
    visited = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:

        weight, u = heapq.heappop(pq)

        if visited[u]:
            continue

        visited[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, weight))
            cost += weight

        for v, wt in adj.get(u, []):

            if not visited[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6)
]

adj = {}

for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

st.write("### Sample Graph")

st.table([
    {"Source": u, "Destination": v, "Weight": w}
    for w, u, v in edges
])

if st.button("Find Minimum Spanning Tree"):

    kruskal_mst, kruskal_cost = kruskal(n, edges[:])
    prim_mst, prim_cost = prim(n, adj)

    st.write("### Kruskal's Algorithm")

    st.table([
        {
            "Edge": f"{u} - {v}",
            "Weight": w
        }
        for u, v, w in kruskal_mst
    ])

    st.success(f"Total MST Cost : {kruskal_cost}")

    st.write("### Prim's Algorithm")

    st.table([
        {
            "Edge": f"{u} - {v}",
            "Weight": w
        }
        for u, v, w in prim_mst
    ])

    st.success(f"Total MST Cost : {prim_cost}")

st.write("---")

if st.button("Run Performance Analysis"):

    st.write("### Performance Analysis")

    sizes = [50, 100, 200, 500]

    results = []

    for size in sizes:

        graph_edges = []

        for i in range(size - 1):
            graph_edges.append((i + 1, i, i + 1))

        for i in range(size):
            for j in range(i + 2, min(size, i + 5)):
                graph_edges.append((i + j + 2, i, j))

        adjacency = {}

        for w, u, v in graph_edges:
            adjacency.setdefault(u, []).append((v, w))
            adjacency.setdefault(v, []).append((u, w))

        start = time.perf_counter()

        for _ in range(20):
            kruskal(size, graph_edges[:])

        kruskal_time = (time.perf_counter() - start) / 20 * 1000

        start = time.perf_counter()

        for _ in range(20):
            prim(size, adjacency)

        prim_time = (time.perf_counter() - start) / 20 * 1000

        results.append({
            "Vertices": size,
            "Edges": len(graph_edges),
            "Kruskal Time (ms)": round(kruskal_time, 5),
            "Prim Time (ms)": round(prim_time, 5)
        })

    st.table(results)