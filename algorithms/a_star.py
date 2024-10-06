import heapq

# A* algorithm function
def a_star_algorithm(graph, heuristics, start_node, goal_node):
    open_list = []
    heapq.heappush(open_list, (0, start_node))
    
    g_costs = {node: float('inf') for node in graph}
    g_costs[start_node] = 0
    
    came_from = {node: None for node in graph}
    
    while open_list:
        current_f_cost, current_node = heapq.heappop(open_list)
        
        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node)
                current_node = came_from[current_node]
            return path[::-1]
        
        for neighbor, weight in graph[current_node].items():
            tentative_g_cost = g_costs[current_node] + weight
            
            if tentative_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristics[neighbor]
                heapq.heappush(open_list, (f_cost, neighbor))
                came_from[neighbor] = current_node
    
    return None  # No path found

# Main function to execute A* algorithm
def main():
    # Input Graph: adjacency list with edge weights
    graph = {
        'S': {'A': 4, 'B': 10, 'C': 11},
        'A': {'B': 8, 'D': 5},
        'B': {'D': 15},
        'C': {'D': 8, 'E': 2},
        'D': {'E': 20, 'F': 1},
        'E': {'G': 19},
        'F': {'G': 13},
        'G': {},
        'H': {'D': 16, 'I': 1},
        'I': {'G': 5, 'J': 5, 'K': 13},
        'J': {'K': 7},
        'K': {'G': 16},
    }

    # Heuristic values (estimated cost to reach the goal 'G')
    heuristics = {
        'S': 7, 'A': 8, 'B': 6, 'C': 5, 'D': 5, 'E': 3, 
        'F': 3, 'G': 0, 'H': 7, 'I': 4, 'J': 5, 'K': 3
    }

    # Run A* algorithm
    start_node = 'S'
    goal_node = 'G'
    path = a_star_algorithm(graph, heuristics, start_node, goal_node)

    print("Shortest path from", start_node, "to", goal_node, ":", path)

if __name__ == "__main__":
    main()
