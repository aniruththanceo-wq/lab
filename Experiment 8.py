from itertools import permutations

INF = float("inf")


def reduce_matrix(matrix):
    reduced = [row[:] for row in matrix]
    n = len(reduced)
    reduction_cost = 0

    for i in range(n):
        values = [x for x in reduced[i] if x != INF]
        if values:
            minimum = min(values)
            if minimum > 0:
                reduction_cost += minimum
                for j in range(n):
                    if reduced[i][j] != INF:
                        reduced[i][j] -= minimum

    for j in range(n):
        values = [reduced[i][j] for i in range(n) if reduced[i][j] != INF]
        if values:
            minimum = min(values)
            if minimum > 0:
                reduction_cost += minimum
                for i in range(n):
                    if reduced[i][j] != INF:
                        reduced[i][j] -= minimum

    return reduced, reduction_cost


def tsp_branch_and_bound(cost_matrix):
    n = len(cost_matrix)
    cities = list(range(1, n))

    reduce_matrix(cost_matrix)

    best_cost = INF
    best_path = []

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]

        total_cost = 0
        valid = True

        for i in range(n):
            edge = cost_matrix[path[i]][path[i + 1]]
            if edge == INF:
                valid = False
                break
            total_cost += edge

        if valid and total_cost < best_cost:
            best_cost = total_cost
            best_path = path

    return best_path, best_cost


cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

cities = ["A", "B", "C", "D", "E"]

optimal_path, minimum_cost = tsp_branch_and_bound(cost)

print("5-City TSP - Cost Matrix:")
print(f'{"":>4}', " ".join(f"{city:>5}" for city in cities))

for i, row in enumerate(cost):
    values = ["INF" if x == INF else str(x) for x in row]
    print(f"{cities[i]:>4}", " ".join(f"{value:>5}" for value in values))

print("\nOptimal Tour:", " -> ".join(cities[i] for i in optimal_path))
print("Minimum Cost:", minimum_cost)

print("\nPath verification:")

for i in range(len(optimal_path) - 1):
    u = optimal_path[i]
    v = optimal_path[i + 1]
    print(f"{cities[u]} -> {cities[v]}: cost = {cost[u][v]}")