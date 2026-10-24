
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import pandas as pd

SHOTS = 1024
SIMULATOR = AerSimulator()


def deutsch_jozsa(n, function_type):
    """Build a Deutsch-Jozsa circuit for a selected oracle."""

    qc = QuantumCircuit(n + 1, n)
    ancilla = n

    # Prepare ancilla |1> and apply Hadamards
    qc.x(ancilla)
    qc.h(range(n + 1))

    # Oracle implementations
    if function_type == "constant_0":
        pass

    elif function_type == "constant_1":
        qc.x(ancilla)

    elif function_type == "balanced_bit":
        qc.cx(0, ancilla)

    elif function_type == "balanced_parity":
        for qubit in range(n):
            qc.cx(qubit, ancilla)

    else:
        raise ValueError("Unknown function type")

    # Final Hadamards and measurements
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc


def classify_result(counts, n):
    zero_state = "0" * n

    # For an ideal Deutsch-Jozsa circuit, all shots
    # should produce the same classification.
    if set(counts.keys()) == {zero_state}:
        return "CONSTANT"
    return "BALANCED"


def main():
    records = []

    function_types = [
        "constant_0",
        "constant_1",
        "balanced_bit",
        "balanced_parity",
    ]

    for n in range(2, 6):
        for function_type in function_types:
            circuit = deutsch_jozsa(n, function_type)

            compiled = transpile(
                circuit,
                SIMULATOR,
                optimization_level=0,
            )

            result = SIMULATOR.run(
                compiled,
                shots=SHOTS,
            ).result()

            counts = result.get_counts()
            classification = classify_result(counts, n)

            expected = (
                "CONSTANT"
                if function_type.startswith("constant")
                else "BALANCED"
            )

            # Measure depth consistently on transpiled circuits.
            depth = compiled.depth()

            passed = classification == expected

            records.append({
                "n": n,
                "function": function_type,
                "counts": str(counts),
                "expected": expected,
                "observed": classification,
                "depth": depth,
                "passed": passed,
                "quantum_queries": 1,
                "classical_worst_case_queries": 2 ** (n - 1) + 1,
            })

            print(
                f"n={n} | {function_type:17} | "
                f"counts={counts} | "
                f"depth={depth} | "
                f"{'PASS' if passed else 'FAIL'}"
            )

    df = pd.DataFrame(records)
    df.to_csv("deutsch_jozsa_results.csv", index=False)

    print("\n========== VALIDATION SUMMARY ==========")
    print(f"Experiments: {len(df)}")
    print(f"Passed: {df['passed'].sum()}")
    print(f"Failed: {(~df['passed']).sum()}")

    print("\n========== CLASSICAL VS QUANTUM ==========")
    comparison = df[[
        "n",
        "function",
        "quantum_queries",
        "classical_worst_case_queries",
        "depth",
    ]]
    print(comparison.to_string(index=False))

    if df["passed"].all():
        print("\nAll experiments passed.")
    else:
        print("\nSome experiments failed. Inspect the counts above.")


if __name__ == "__main__":
    main()
