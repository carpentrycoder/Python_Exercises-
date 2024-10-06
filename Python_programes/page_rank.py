import networkx as nx

def compute_pagerank(graph, alpha=0.85, max_iter=100, tol=1e-6):
    # Initialize PageRank values
    pagerank = {node: 1 / len(graph) for node in graph}

    for _ in range(max_iter):
        new_pagerank = {}

        for node in graph:
            # Calculate the sum of PageRank values from incoming edges
            incoming_pr = sum(pagerank[neighbor] / len(graph[neighbor]) for neighbor in graph.predecessors(node))
            new_pagerank[node] = (1 - alpha) / len(graph) + alpha * incoming_pr

        # Check for convergence
        if all(abs(new_pagerank[node] - pagerank[node]) < tol for node in graph):
            break

        pagerank = new_pagerank

    return pagerank

# Create a directed graph
G = nx.DiGraph()
G.add_edges_from([
    (1, 2),
    (2, 3),
    (3, 1),
    (3, 4),
    (4, 2)
])

# Compute PageRank
pagerank_values = compute_pagerank(G)
print("PageRank values:", pagerank_values)
