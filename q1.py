import numpy as np
import random
import streamlit as st
import matplotlib.pyplot as plt

# ========================== #
# GA SETTINGS #
# ========================== #
POP_SIZE = 200  # Population size
CHROM_LEN = 70  # Length of each individual chromosome
TARGET_ONES = 40  # Target number of ones
MAX_FITNESS = 70  # Max fitness when the number of ones is 40
N_GENERATIONS = 50  # Number of generations

TOURNAMENT_K = 3  # Tournament selection parameter (k)
CROSSOVER_RATE = 0.9  # Crossover rate
MUTATION_RATE = 1.0 / CHROM_LEN  # Mutation rate (bit-flipping)

# ========================== #
# GA OPERATORS #
# ========================== #
def fitness(individual: np.ndarray) -> float:
    """
    Fitness function: Peaks when the number of ones is equal to TARGET_ONES.
    Max fitness is MAX_FITNESS when ones == TARGET_ONES.
    """
    ones = int(individual.sum())
    return MAX_FITNESS - abs(ones - TARGET_ONES)

def init_population(pop_size: int, chrom_len: int) -> np.ndarray:
    """Initialize the population randomly with bit strings."""
    return np.random.randint(0, 2, size=(pop_size, chrom_len), dtype=np.int8)

def tournament_selection(pop: np.ndarray, fits: np.ndarray, k: int) -> np.ndarray:
    """Tournament selection for selecting two parents."""
    idxs = np.random.randint(0, len(pop), size=k)
    best_idx = idxs[np.argmax(fits[idxs])]
    return pop[best_idx].copy()

def single_point_crossover(p1: np.ndarray, p2: np.ndarray):
    """Perform single-point crossover."""
    if np.random.rand() > CROSSOVER_RATE:
        return p1.copy(), p2.copy()
    point = np.random.randint(1, CHROM_LEN)  # Choose crossover point
    c1 = np.concatenate([p1[:point], p2[point:]])
    c2 = np.concatenate([p2[:point], p1[point:]])
    return c1, c2

def mutate(individual: np.ndarray) -> np.ndarray:
    """Flip bits for mutation."""
    mask = np.random.rand(CHROM_LEN) < MUTATION_RATE
    individual[mask] = 1 - individual[mask]
    return individual

def evolve(pop: np.ndarray, generations: int):
    """Evolve the population over generations."""
    best_fitness_per_gen = []
    best_individual = None
    best_f = -np.inf

    for _ in range(generations):
        fits = np.array([fitness(ind) for ind in pop])

        # Track best this generation and overall
        gen_best_idx = np.argmax(fits)
        gen_best = pop[gen_best_idx]
        gen_best_f = fits[gen_best_idx]
        best_fitness_per_gen.append(float(gen_best_f))

        if gen_best_f > best_f:
            best_f = float(gen_best_f)
            best_individual = gen_best.copy()

        # Create next generation
        new_pop = []
        while len(new_pop) < len(pop):
            p1 = tournament_selection(pop, fits, TOURNAMENT_K)
            p2 = tournament_selection(pop, fits, TOURNAMENT_K)
            c1, c2 = single_point_crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_pop.extend([c1, c2])
        pop = np.array(new_pop[:len(pop)], dtype=np.int8)

    return best_individual, best_f, best_fitness_per_gen

# ========================== #
# STREAMLIT INTERFACE #
# ========================== #
st.set_page_config(page_title="Genetic Algorithm (70 bits, target ones = 40)", layout="centered")

st.title("🧬 Genetic Algorithm: Evolve a 70-bit Pattern")
st.caption("Population = 200, Chromosome Length = 70, Target Ones = 40, Max Fitness = 70")

with st.expander("ℹ️ Problem Setup"):
    st.write("""
    - **Population size**: 200
    - **Chromosome length**: 70
    - **Target number of ones**: 40
    - **Max fitness at optimum**: 70 (when ones = 40)
    - **Generations**: 50
    - **Selection**: Tournament selection (k=3)
    - **Crossover**: Single-point (rate=0.9)
    - **Mutation**: Bit-flip (per-bit rate=1/70)
    """)

col1, col2 = st.columns(2)
with col1:
    seed = st.number_input("Random Seed (for reproducibility)", min_value=0, value=42)
with col2:
    run_btn = st.button("Run Genetic Algorithm")

if run_btn:
    # Reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Initialize and evolve
    population = init_population(POP_SIZE, CHROM_LEN)
    best_ind, best_fit, curve = evolve(population, N_GENERATIONS)

    # Results
    ones_count = int(best_ind.sum())
    zeros_count = CHROM_LEN - ones_count
    bitstring = "".join(map(str, best_ind.tolist()))

    st.subheader("🏁 Best Individual Found")
    st.metric(label="Best Fitness", value=f"{best_fit:.0f}")
    st.write(f"**Ones**: {ones_count} | **Zeros**: {zeros_count} | **Length**: {CHROM_LEN}")
    st.code(bitstring, language="text")

    # Convergence plot
    st.subheader("📉 Convergence (Best Fitness per Generation)")
    fig, ax = plt.subplots()
    ax.plot(range(1, len(curve) + 1), curve, linewidth=2)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness")
    ax.set_title("GA Convergence")
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

    # Validation
    if best_fit == MAX_FITNESS and ones_count == TARGET_ONES:
        st.success("Perfect match achieved: ones = 40 and fitness = 70 ✅")
    else:
        st.info("GA reached near-optimal solutions; try another seed to explore further.")

st.caption("© 2025 Simple GA demo (70 bits, optimum at 40 ones).")
