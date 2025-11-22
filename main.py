from src.data_generator import get_graph
from src.tsp_solver import  solve_tsp_constraint_generation

def main():
    print("Choose mode: [1] File [2] Random")
    choice = input("Enter your choice: ")

    if choice == "1":
        n, d, coords = get_graph(mode="file", path="data/example_input.txt")
    elif choice == "2":
        n = int(input("Enter number of nodes: "))
        n, d, coords = get_graph(mode="random", n=n)
    else:
        print("Invalid choice")
        return

    tour, cost = solve_tsp_constraint_generation(n, d)
    print("\nOptimal Tour: ", tour)
    print("Total cost: ", cost)

if __name__ == "__main__":
    main()