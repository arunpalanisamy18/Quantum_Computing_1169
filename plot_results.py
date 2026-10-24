
import pandas as pd
import matplotlib.pyplot as plt

# Load the experimental results from your simulation
df = pd.read_csv("deutsch_jozsa_results.csv")

# Graph 1: Circuit depth versus number of input qubits
plt.figure(figsize=(9, 5))

for function_name, group in df.groupby("function"):
    plt.plot(
        group["n"],
        group["depth"],
        marker="o",
        label=function_name.replace("_", " ").title()
    )

plt.xlabel("Number of Input Qubits (n)")
plt.ylabel("Transpiled Circuit Depth")
plt.title("Deutsch-Jozsa Circuit Depth vs Input Size")
plt.xticks([2, 3, 4, 5])
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("circuit_depth_vs_n.png", dpi=300)
plt.show()

# Graph 2: Classical versus quantum oracle queries
comparison = df[["n", "quantum_queries",
                 "classical_worst_case_queries"]].drop_duplicates(
                     subset=["n"]
                 ).sort_values("n")

plt.figure(figsize=(9, 5))

plt.plot(
    comparison["n"],
    comparison["quantum_queries"],
    marker="o",
    label="Deutsch-Jozsa quantum queries"
)

plt.plot(
    comparison["n"],
    comparison["classical_worst_case_queries"],
    marker="s",
    label="Deterministic classical worst-case queries"
)

plt.xlabel("Number of Input Bits (n)")
plt.ylabel("Oracle Queries")
plt.title("Quantum vs Classical Query Complexity")
plt.xticks([2, 3, 4, 5])
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("quantum_vs_classical_queries.png", dpi=300)
plt.show()

print("Graphs saved:")
print("1. circuit_depth_vs_n.png")
print("2. quantum_vs_classical_queries.png")
