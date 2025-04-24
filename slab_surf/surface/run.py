import numpy as np
import os
import timeit
import time
import h5py

mfp = np.logspace(-1, 1, 10)
ratio = np.array([1, 2.5, 5, 10])

delta_tracking = True
collision_est = False

dx = .06

runtimes = np.zeros((ratio.size, mfp.size)).astype(np.float64)
errors = np.zeros((ratio.size, mfp.size)).astype(np.float64)

for i in range(ratio.size):
    for j in range(mfp.size):
        print("\nRunning {} mfp and Σ2/Σ1 {}".format(mfp[j], ratio[i]))

        sigma_1 = mfp[j]/dx
        sigma_2 = sigma_1*ratio[i]

        #os.system("mpiexec -N 4 python input.py {} {} {} {}".format(surfaces[j], ratio[i], delta_tracking, collision_est)
        #        + " --no-progress_bar --mode=numba --delta_tracking --caching")

        start = time.time()

        os.system("mpiexec -N 4 python input.py {} {}".format(sigma_1, sigma_2))

        end = time.time()
        runtimes[i, j] = end-start


        with h5py.File("output.h5", "r") as f:
            phi_sd = f["tallies/mesh_tally_0/flux/sdev"][:]

        errors[i,j] = np.linalg.norm(phi_sd)

        print("  completed in {}, with a vairance {}".format(runtimes[i, j], errors[i,j]))

np.savez('data.npz', mfp = mfp, ratio=ratio, delta_tracking=delta_tracking, collision_est=collision_est, runtimes=runtimes, errors=errors)

print("Errors: ")
print(errors)
print("Runtime: ")
print(runtimes)
print("FOMs: ")
print(1/(errors*runtimes))