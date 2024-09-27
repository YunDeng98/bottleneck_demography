import os
import tskit
import subprocess


# Set the parameters for Relate inference
mutation_rate = 1.2e-8
recombination_rate = 1.2e-8
pop_size = 2e4

relate_convert_vcf = f"relate_v1.2.1_x86_64_static/bin/RelateFileFormats --mode ConvertFromVcf --haps results/synthetic_ts.haps --sample results/synthetic_ts.sample -i results/synthetic_ts"

subprocess.run(relate_convert_vcf, shell=True)

os.chdir("results/")

relate_main_cmd = f"../relate_v1.2.1_x86_64_static/bin/Relate --mode All -m {mutation_rate} -N {2*pop_size} --haps synthetic_ts.haps --sample synthetic_ts.sample --map ../map_file.txt --seed 1 -o relate_synthetic_ts"

subprocess.run(relate_main_cmd, shell=True)

relate_estimate_popsize = f"../relate_v1.2.1_x86_64_static/scripts/EstimatePopulationSize/EstimatePopulationSize.sh -i relate_synthetic_ts -m {mutation_rate} --poplabels all.poplabels --seed 1 -o relate_synthetic_ts_popsize"

subprocess.run(relate_estimate_popsize, shell=True)

relate_convert_ts = f"../relate_v1.2.1_x86_64_static/bin/RelateFileFormats --mode ConvertToTreeSequence -i relate_synthetic_ts_popsize -o relate_synthetic_ts"

subprocess.run(relate_convert_ts, shell=True)

clean_cmd = f"../relate/bin/Relate --mode Clean -o relate_synthetic_ts"

subprocess.run(clean_cmd, shell=True)
