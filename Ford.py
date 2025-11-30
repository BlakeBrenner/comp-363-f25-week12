# Test graph
G = [  #  A   B   C   D   E
    [0, 20, 0, 0, 0],  # A
    [0, 0, 5, 6, 0],  # B
    [0, 0, 0, 3, 7],  # C
    [0, 0, 0, 0, 8],  # D
    [0, 0, 0, 0, 0],  # E
]

#creates residual graph for graph
def create_residual(graph: list[list[int]]) -> list[list[int]]:
    residual = [[] for _ in range(len(graph))]
    for i in range(len(graph)):
        for j in graph[i]:
            residual[i].append(j)
    return residual

def find_path(graph: list[list[int]], source: int, target: int):
    """Return a path -- any path -- from source to target in the graph"""

    # Initialize return item
    path: list[int] = None

    # Make sure inputs are ok
    if graph is not None:
        n: int = len(graph)
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            # Initialize DFS tools
            no_edge: int = graph[0][0]  # absence of edge
            marked: list[int] = [source]  # vertices already processed
            found: bool = False  # Flags detection of path

            # What vertex to explore next and what is the path
            # to it. The information is stored as a tuple in
            # the form:
            #  (vertex, path_to_this_vertex)
            # with path_to_this_vertex being a list of the
            # vertices alonγ the path.
            stack: list[(int, list[int])] = [(source, [source])]

            while len(stack) > 0 and not found:
                # Explore the next vertex from the stack
                (u, path_from_source_to_u) = stack.pop()
                found = (u == target)
                if found:
                    # u is the end of the path, so we got what we are
                    # looking for
                    path = path_from_source_to_u
                else:
                    # Explore the neighbors of u, hopefully one of them
                    # will get us a stop closer to the target vertex.
                    v: int = n - 1
                    while v >= 0:
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1
    return path

#finds bottleneck of a graph
def get_bottleneck(graph: list[list[int]], path: list[int]) -> int:
    bottleneck: int = float('inf')
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        capacity = graph[u][v]

        if capacity < bottleneck:
            bottleneck = int(capacity)
    return bottleneck

def update_residual(residual: list[list[int]], path: list[int], bottleneck):
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        #update capacity of forward edge
        residual[u][v] = residual[u][v] - bottleneck
        #update capacity of backward edge
        residual[v][u] = residual[v][u] + bottleneck


#finds max flow and updates residual graph
def get_maxflow(graph: list[list[int]], source: int, target: int):
    residual = create_residual(graph)
    path = find_path(residual, source, target)
    max_flow = 0

    while path is not None:
        m = get_bottleneck(residual, path)
        max_flow += m
        update_residual(residual, path, m)
        path = find_path(residual, source, target)

    return max_flow, residual

def get_mincut(graph: list[list[int]], residual: list[list[int]], source: int):

    n = len(graph)

    #Mark all vertices reachable from the source in the residual graph
    visited = [False] * n
    visited[source] = True

    #Use a simple list as a queue (no imports)
    queue = [source]

    while queue:
        # pop from front
        u = queue.pop(0)
        for v in range(n):
            if residual[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)

    #Build S (reachable) and T (not reachable)
    S = []
    T = []
    for i in range(n):
        if visited[i]:
            S.append(i)
        else:
            T.append(i)

    #Identify cut edges from ORIGINAL graph: edges u->v where u in S, v in T
    cut_edges = []
    cut_capacity = 0

    for u in S:
        for v in T:
            if graph[u][v] > 0:     # original capacity, not residual
                cut_edges.append((u, v))
                cut_capacity += graph[u][v]

    return S, T, cut_edges, cut_capacity

def ford_fulkerson(graph: list[list[int]], source: int, target: int):
    # 1. Compute max flow and final residual graph
    max_flow, residual = get_maxflow(graph, source, target)

    # 2. Compute min cut based on the final residual graph
    S, T, cut_edges, cut_capacity = get_mincut(graph, residual, source)

    # 3. Return whatever you care about; here we return everything
    return {
        "max_flow": max_flow,
        "mincut_S": S,
        "mincut_T": T,
        "mincut_edges": cut_edges,
        "mincut_capacity": cut_capacity,
    }

#main method
if __name__ == "__main__":
    result = ford_fulkerson(G, 0, 4)
    print("Max flow:", result["max_flow"])
    print("Min cut capacity:", result["mincut_capacity"])
    print("Cut edges:", result["mincut_edges"])
