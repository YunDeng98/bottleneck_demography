# bottleneck_demography
This repo is about the re-investigation into the severe bottleneck hypothesis in Africans introduced in [Hu et al, 2023, Science](https://www.science.org/doi/10.1126/science.abq7487). Here we maintained the code to reproduce the results, and a key package to install is `mushi`, and you can find installation instructions [here](https://harrispopgen.github.io/mushi/).

Here we proposed a "synthetic model" whose expected SFS leads FitCoal to falsely infer a severe bottleneck, whereas the "sythetic model" itself only involves rather smooth population size changes. 

To obtain the "synthetic model", we fist compute the expected SFS of the severe bottleneck model introduced in [Hu et al, 2023, Science](https://www.science.org/doi/10.1126/science.abq7487), and then use `mushi` to fit a demography model to it. This can be done by:

```
python3.8 scripts/synthetic_model.py
```

The above function also computed the expected SFS under the "synthetic model", and we can use FitCoal to infer the demography:

```
python3.12 scripts/fitcoal_synthetic.py
```

We also simulated data with `msprime` under the "synthetic model", whose documentation page is [here](https://tskit.dev/msprime/docs/stable/intro.html):

```
python3.12 scripts/simulate_synthetic_model.py
```

We then use `msmc2` and `Relate` to infer demography with the simulated haplotype data:

```
python3.12 scripts/relate_synthetic_ts.py
python3.12 scripts/run_msmc2.py results/synthetic_ts.vcf results/synthetic_ts results/msmc2_synthetic_input results/msmc2_synthetic_output
```

Note that `python3.8` and `python3.12` are the alias I used to make the python version explicit. You probably just have to type `python`, but if the version is incompatible with certain packages, these are the versions to use to make sure of coding running. 
