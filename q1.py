import numpy as np
import pandas as pd
import streamlit as st

# ================== GA SETTINGS ==================
POP_SIZE = 300
GENE_LENGTH = 80
N_GENERATIONS = 50
PC = 0.9          # crossover probability
PM = 0.01         # mutation probability
ELITE_COUNT = 2
TOUR_SIZE = 3
RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)

# ================== GA CORE ==================
def evaluate(chromosome):
    """OneMax fitness function"""
    return chromosome.sum()

def create_population():
    return rng.integers(0, 2, (POP_SIZE, GENE_LENGTH))

def select_parent(population, scores):
    candidates = rng.choice(len(population), TOUR_SIZE, replace=False)
    best_idx = candidates[np.argmax(scores[candidates])]
    return population[best_idx]

def recombine(parent_a, parent_b):
    if rng.random() < PC:
        cut = rng.integers(1, GENE_LENGTH)
        child1 = np.hstack((parent_a[:cut], parent_b[cut:]))
        child2 = np.hstack((parent_b[:cut], parent_a[cut:]))
        return child1, child2
    return parent_a.copy(), parent_b.copy()

def flip_bits(individual):
    mutation_mask = rng.random(GENE_LENGTH) < PM
    individual[mutation_mask] ^= 1
    return individual

def genetic_algorithm():
    population = create_population()
    log = []

    for gen in range(1, N_GENERATIONS + 1):
        fitness_scores = np.array([evaluate(ind) for ind in population])

        log.append({
            "Generation": gen,
            "Best Fitness": fitness_scores.max(),
            "Average Fitness": fitness_scores.mean()
        })

        # Preserve elites
        elite_indices = np.argsort(fitness_scores)[-ELITE_COUNT:]
        elites = population[elite_indices]

        offspring = []

        while len(offspring) < POP_SIZE - ELITE_COUNT:
            p1 = select_parent(population, fitness_scores)
            p2 = select_parent(population, fitness_scores)

            c1, c2 = recombine(p1, p2)
            offspring.append(flip_bits(c1))

            if len(offspring) < POP_SIZE - ELITE_COUNT:
                offspring.append(flip_bits(c2))

        population = np.vstack((offspring, elites))

    final_scores = np.array([evaluate(ind) for ind in population])
    best_idx = np.argmax(final_scores)

    return pd.DataFrame(log), population[best_idx], final_scores[best_idx]

# ================== STREAMLIT UI ==================
st.set_page_config(page_title="OneMax Genetic Algorithm", layout="wide")
st.title("Genetic Algorithm Optimization (OneMax Problem)")

if st.button("Run Genetic Algorithm"):
    history_df, best_individual, best_score = genetic_algorithm()

    st.subheader("Fitness Progress Over Generations")
    st.line_chart(history_df.set_index("Generation"))

    st.subheader("Optimal Chromosome")
    st.write(f"**Best Fitness:** {best_score} / {GENE_LENGTH}")
    st.code("".join(map(str, best_individual)))
