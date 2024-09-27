import msprime
import pandas as pd
import numpy as np
import os


def create_demography(file_name):
    all_data = np.loadtxt(file_name)

    all_data[:, 1] = all_data[:, 1] 
    initial_size = all_data[0, 1]
    demography = msprime.Demography()
    demography.add_population(name="A", initial_size=initial_size)

    m = all_data.shape[0]

    for i in range(1, m):
        demography.add_population_parameters_change(time=all_data[i, 0], initial_size=all_data[i, 1], population="A")

    return demography


synthetic_demography = create_demography("results/synthetic_model.txt")

# Set the parameters for the simulation
num_individuals = 108
sequence_length = 100e6  # 100 Mb
mutation_rate = 1.2e-8
recombination_rate = 1.2e-8

# Simulate the ancestry
ancestry = msprime.sim_ancestry(
    samples=[msprime.SampleSet(num_individuals, ploidy=2)],
    demography=synthetic_demography,
    sequence_length=sequence_length,
    recombination_rate=recombination_rate,
    random_seed=1000
)

# Add mutations
tree_sequence = msprime.sim_mutations(
    tree_sequence=ancestry,
    rate=mutation_rate,
    random_seed=1000
)

# Output file names based on the index
trees_output_file = f"results/synthetic_ts.trees"
vcf_output_file = f"results/synthetic_ts.vcf"

# Save the tree sequence
tree_sequence.dump(trees_output_file)

# Write the VCF file
with open(vcf_output_file, "w") as vcf_file:
    tree_sequence.write_vcf(vcf_file)
