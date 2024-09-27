import os
import subprocess
import argparse

def run_command(command):
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Error: {process.stderr}")

def extract_individual_names(vcf_file):
    # Extract individual names from the VCF file header using bcftools query
    command = f"bcftools query -l {vcf_file}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if process.returncode != 0:
        print(f"Error extracting individual names: {process.stderr.decode()}")
        return []
    
    individual_names = process.stdout.decode().splitlines()
    return individual_names

def extract_individual_vcfs(vcf_file, ind_vcf_prefix, individual_names):
    # Extract individual VCFs
    for individual in individual_names:
        output_vcf = f"results/msmc2_results/{individual}.vcf.gz"
        command = f"bcftools view -s {individual} -Oz -o {ind_vcf_prefix}_{individual}.vcf.gz {vcf_file}"
        print(f"Extracting VCF for {individual}...")
        run_command(command)
    print("Individual VCF extraction complete.")


def convert_to_msmc2_input(ind_vcf_prefix, msmc_input_file, individual_names):
    command = f"python msmc-tools/generate_multihetsep.py"
    command += f" --chr 1"
    for ind in individual_names:
        command += f" {ind_vcf_prefix}_{ind}.vcf.gz"
    command += f" > {msmc_input_file}"
    print(command)        
    run_command(command)
    print("Conversion to MSMC2 input format complete.")

def run_msmc2(msmc_input_file, msmc_output_file, num_individuals):
    command = f"msmc2/build/release/msmc2 -I "
    for i in range(num_individuals):
        command += f"{2*i}-{2*i+1}"
        if i < num_individuals - 1:
            command += f","
    command += f" -o {msmc_output_file} {msmc_input_file}"
    print(command)
    run_command(command)
    return  


def main():
    parser = argparse.ArgumentParser(description="MSMC2 Workflow for Population Size Estimation")
    parser.add_argument("vcf_file", type=str, help="Input VCF file")
    parser.add_argument("ind_vcf_prefix", type=str, help="Prefix for the individual vcf file")
    parser.add_argument("msmc_input_file", type=str, help="Input filename for msmc2")
    parser.add_argument("msmc_output_file", type=str, help="Output pop size file")
    
    args = parser.parse_args()
    
    # Run the individual VCF extraction function
    individual_names = extract_individual_names(args.vcf_file)
    print(individual_names)
    extract_individual_vcfs(args.vcf_file, args.ind_vcf_prefix, individual_names)
    convert_to_msmc2_input(args.ind_vcf_prefix, args.msmc_input_file, individual_names)
    run_msmc2(args.msmc_input_file, args.msmc_output_file, len(individual_names))

if __name__ == "__main__":
    main()
