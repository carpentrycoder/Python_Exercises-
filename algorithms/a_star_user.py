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

# Function to input graph data
def input_graph():
    graph = {}
    n = int(input("Enter number of nodes in the graph: "))
    
    for _ in range(n):
        node = input(f"Enter node name (e.g., 'S'): ")
        graph[node] = {}
        num_neighbors = int(input(f"Enter number of neighbors for {node}: "))
        
        for _ in range(num_neighbors):
            neighbor, weight = input(f"Enter neighbor and weight for {node} (e.g., 'A 4'): ").split()
            graph[node][neighbor] = int(weight)
    
    # If the goal node has no neighbors, we must still initialize it
    goal_node = input("Enter the goal node (e.g., 'G'): ")
    if goal_node not in graph:
        graph[goal_node] = {}
    
    return graph


# Function to input heuristic values
def input_heuristics():
    heuristics = {}
    n = int(input("Enter number of nodes for heuristic values: "))
    
    for _ in range(n):
        node, h_val = input(f"Enter node and heuristic value (e.g., 'S 7'): ").split()
        heuristics[node] = int(h_val)
    
    return heuristics

# Main function to execute A* algorithm
def main():
    print("Input Graph:")
    graph = input_graph()
    
    print("\nInput Heuristic Values:")
    heuristics = input_heuristics()
    
    start_node = input("\nEnter start node: ")
    goal_node = input("Enter goal node: ")
    
    path = a_star_algorithm(graph, heuristics, start_node, goal_node)
    
    if path:
        print("Shortest path from", start_node, "to", goal_node, ":", path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
