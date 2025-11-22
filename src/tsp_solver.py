import pulp
from subtour_detection import find_subtours, add_subtour_constraints


def solve_tsp_constraint_generation(n, d):
    model = pulp.LpProblem("TSP", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(n) if i != j],
                              lowBound=0, upBound=1, cat="Continuous")  # relaxed TSP

    model += pulp.lpSum(d[i, j] * x[i, j] for i, j in x)

    for i in range(n):
        # Outgoing edges from node i
        model += pulp.lpSum(x[i, j] for j in range(n) if i != j) == 1
        # Incoming edges to node i
        model += pulp.lpSum(x[j, i] for j in range(n) if j != i) == 1

    iteration = 0
    while True:
        iteration += 1 # Counts iterations
        status = model.solve(pulp.PULP_CBC_CMD(msg=False))
        if status != 1:
            raise RuntimeError("Solver failed")

        sol = [(i, j) for (i, j) in x if pulp.value(x[i, j]) > 0]
        subtours = find_subtours(sol, n)
        print(f"Iteration {iteration}: {len(subtours)} subtours found")

        if len(subtours) == 1:
            break

        add_subtour_constraints(model, x, subtours, n)

    # Reconstruct ordered tour
    tour_edges = {(i, j) for (i, j) in sol}
    tour = [0]
    while len(tour) < n:
        i = tour[-1]
        for j in range(n):
            if (i, j) in tour_edges:
                tour.append(j)
                break

    total_cost = pulp.value(model.objective)
    return tour, total_cost
