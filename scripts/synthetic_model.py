import mushi
import numpy as np
import pandas as pd

def compute_expected_sfs(sample_size, change_points, sizes):
    eta = mushi.eta(change_points, sizes)
    L = mushi.utils.C(sample_size) @ mushi.utils.M(sample_size, *eta.arrays())
    esfs = L.sum(1)
    return esfs


input_sfs = np.loadtxt("input_sfs.txt")
ksfs = mushi.kSFS(input_sfs)
ksfs.infer_eta(mu0=826650000*1.2e-8, trend_kwargs=(2, 1e2), ridge_penalty = 7.5e2, folded=False, max_iter=300, verbose=True)
synthetic_model = np.column_stack([ksfs.eta.change_points, ksfs.eta.y[0:-1]/2])
np.savetxt("results/synthetic_model.txt", synthetic_model)

yri_fitcoal_model = pd.read_csv("FitCoal1.2/example/YRI.test.ouput.txt", delim_whitespace=True)
yri_fitcoal_change_points = np.array(yri_fitcoal_model.iloc[:, 0])/24 + np.linspace(0, 1, yri_fitcoal_model.shape[0])
yri_fitcoal_sizes = np.append(yri_fitcoal_model.iloc[:, 1]*2, yri_fitcoal_model.iloc[-1, 1]*2)
yri_fitcoal_esfs = compute_expected_sfs(216, yri_fitcoal_change_points, yri_fitcoal_sizes)
synthetic_esfs = compute_expected_sfs(216, ksfs.eta.change_points, ksfs.eta.y)
np.savetxt("results/fitcoal_esfs.txt", yri_fitcoal_esfs)
np.savetxt("results/synthetic_esfs.txt", synthetic_esfs)
