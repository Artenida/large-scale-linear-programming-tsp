import numpy as np
from sklearn.manifold import MDS

# Load graph from file (example_input.txt)
def load_graph_from_file(path):
    with open(path, "r") as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    d = np.array([list(map(float, line.split())) for line in lines[1:]])

    if d.shape != (n, n):
        raise ValueError(f"Distance matrix shape {d.shape} does not match n={n}")

    # Ensure diagonal is 0
    np.fill_diagonal(d, 0)

    # Optionally: check symmetry
    if not np.allclose(d, d.T):
        print("Warning: Distance matrix is not symmetric. For TSP, distances should be symmetric.")

    return n, d, None  # coords=None because not available from file


# Random graph generator
def generate_random_graph(n):
    coords = np.random.rand(n, 2) * 1000
    d = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(coords[i] - coords[j])
            d[i, j] = dist
            d[j, i] = dist  # symmetric

    np.fill_diagonal(d, 0)
    return n, d, coords

def get_graph(mode="manual", **kwargs):
    if mode == "file":
        path = kwargs.get("path")
        if path is None:
            raise ValueError("File path must be provided in file mode.")
        return load_graph_from_file(path)
    elif mode == "random":
        n = kwargs.get("n", 10)
        return generate_random_graph(n)
    else:
        raise ValueError(f"Unknown mode '{mode}'")