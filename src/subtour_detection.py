import itertools

def find_subtours(solution, n):
    edges = {i: [] for i in range(n)}
    for i, j in solution:
        edges[i].append(j)

    visited = set()
    subtours = []

    for start in range(n):
        if start in visited:
            continue
        tour = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                tour.append(node)
                stack.extend(edges[node])
        subtours.append(tour)

    return subtours

constraint_counter = itertools.count()

def add_subtour_constraints(model, x, subtours, n):
    for S in subtours:
        if len(S) >= n:
            continue  # full tour
        cname = f"cut_{next(constraint_counter)}"
        model += (
            sum(x[i, j] for i in S for j in range(n)
                if j not in S and i != j) >= 1,
            cname
        )