import heapq

# Define possible movements (up, down, left, right)
movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def astar(matrix, start, goal):
    def heuristic(node):
        # Manhattan distance heuristic
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_set = []
    closed_set = set()
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}

    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]

        closed_set.add(current)

        for dx, dy in movements:
            neighbor = (current[0] + dx, current[1] + dy)

            if not (0 <= neighbor[0] < len(matrix) and 0 <= neighbor[1] < len(matrix[0])):
                continue

            if matrix[neighbor[0]][neighbor[1]] == 'solid' or neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in [n[1] for n in open_set] or tentative_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

# Example usage
matrix = [
    ['passthrough', 'solid', 'passthrough', 'passthrough', 'passthrough'],
    ['passthrough', 'solid', 'solid', 'passthrough', 'solid'],
    ['passthrough', 'passthrough', 'passthrough', 'passthrough', 'passthrough'],
    ['solid', 'solid', 'passthrough', 'solid', 'solid'],
    ['passthrough', 'passthrough', 'passthrough', 'passthrough', 'passthrough']
]

start = (0, 0)
goal = (4, 4)

path = astar(matrix, start, goal)
if path:
    print("Path found:", path)
else:
    print("No path found")
