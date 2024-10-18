import os
import subprocess

command = [
    "java", 
    "-cp", "FitCoal.jar", 
    "FitCoal.calculate.SinglePopDecoder", 
    "-table", "tables/", 
    "-input", "../results/synthetic_esfs.txt", 
    "-output", "../results/fitcoal_synthetic", 
    "-mutationRate", "0.000012", 
    "-generationTime", "24", 
    "-genomeLength", "826650", 
    "-omitEndSFS", "27"
]

try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing the command:\n{e.stderr}")
