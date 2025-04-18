import numpy as np
import os
import timeit
import time
import h5py

surfaces = np.array([6, 10, 20, 50, 100])
ratio = np.array([1, 5, 10, 100])

delta_tracking = True
collision_est = False

runtimes = np.zeros((ratio.size, surfaces.size)).astype(np.float64)
errors = np.zeros((ratio.size, surfaces.size)).astype(np.float64)

for i in range(ratio.size):
    for j in range(surfaces.size):
        print("\nRunning {} surfaces and Σ2/Σ1 {}".format(surfaces[j], ratio[i]))

        os.system("srun -n 112 python input.py {} {} {} {}".format(surfaces[j], ratio[i], delta_tracking, collision_est)
                + " --no-progress_bar --mode=numba --caching")

        start = time.time()

        os.system("srun -n 112 python input.py {} {} {} {}".format(surfaces[j], ratio[i], delta_tracking, collision_est)
                + " --no-progress_bar --mode=numba --caching")
        
        end = time.time()
        runtimes[i, j] = end-start

        with h5py.File("output.h5", "r") as f:
            phi_sd = f["tallies/mesh_tally_0/flux/sdev"][:]

        errors[i,j] = np.linalg.norm(phi_sd)

        print("  completed in {}, with a vairance {}".format(runtimes[i, j], errors[i,j]))

np.savez('data.npz', surfaces = surfaces, ratio=ratio, delta_tracking=delta_tracking, collision_est=collision_est, runtimes=runtimes, errors=errors)

print("Errors: ")
print(errors)
print("Runtime: ")
print(runtimes)
print("FOMs: ")
print(1/(errors*runtimes))