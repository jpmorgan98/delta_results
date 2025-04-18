import matplotlib.pyplot as plt
import h5py
import numpy as np


# Load results
with h5py.File("output.h5", "r") as f:
    z = f["tallies/mesh_tally_0/grid/z"][:]
    dz = z[1:] - z[:-1]
    z_mid = 0.5 * (z[:-1] + z[1:])

    phi = f["tallies/mesh_tally_0/flux/mean"][:]
    phi_sd = f["tallies/mesh_tally_0/flux/sdev"][:]


# Normalize
phi /= dz
phi_sd /= dz

# Flux - spatial average
plt.plot(z_mid, phi, "-b", label="MC")
plt.fill_between(z_mid, phi - phi_sd, phi + phi_sd, alpha=0.2, color="b")
plt.xlabel(r"$z$, cm")
plt.ylabel("Flux")
plt.ylim([0.06, 0.16])
plt.grid()
plt.legend()
plt.title(r"$\bar{\phi}_i$")
plt.savefig("phi.png")