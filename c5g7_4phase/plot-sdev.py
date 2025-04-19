import h5py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import shutil

from PIL import Image

# Get results
with h5py.File('output_4.h5', 'r') as f:
    fluxes = f['tallies/mesh_tally_0/flux/mean'][()]
    densities = f['tallies/mesh_tally_1/density/mean'][()]
    fluxes_sd = f['tallies/mesh_tally_0/flux/sdev'][()]
    densities_sd = f['tallies/mesh_tally_1/density/sdev'][()]
    x = f['tallies/mesh_tally_0/grid/x'][()]
    y = f['tallies/mesh_tally_0/grid/y'][()]
    z = f['tallies/mesh_tally_0/grid/z'][()]
    t = f['tallies/mesh_tally_0/grid/t'][()]

# The grids
t_mid = 0.5 * (t[:-1] + t[1:])
XY_X, XY_Y = np.meshgrid(x, y, indexing='ij')
XZ_X, XZ_Z = np.meshgrid(x, z, indexing='ij')
YZ_Y, YZ_Z = np.meshgrid(y, z, indexing='ij')

# Relative stdevs
densities_sd /= densities
fluxes_sd[fluxes == 0.0] = 0.0
non_zeros = fluxes != 0.0
fluxes_sd[non_zeros] /= fluxes[non_zeros]

# Create clean folder for output figures
# Check if the folder exists
if os.path.exists('sdev'):
    shutil.rmtree('sdev')  # Remove the existing folder
os.makedirs('sdev')  # Create a new folder

# Iterate over time step and create figures
N = len(fluxes)
for i in range(N):
    flux_sd = fluxes_sd[i]

    # Calculate flux averages
    flux_x_sd = np.average(flux_sd, axis=0)
    flux_y_sd = np.average(flux_sd, axis=1)
    flux_z_sd = np.average(flux_sd, axis=2)

    # Plot
    fig, ax = plt.subplots(2, 2, figsize=(8, 6), gridspec_kw={'width_ratios':[1,2], 'height_ratios':[1,1], 'hspace':0.5})

    # Density curve
    ax[0,0].plot(t_mid, densities_sd, 'b')
    ax[0,0].set_yscale('log')
    ax[0,0].set_ylabel('Relative sdev.')
    ax[0,0].set_xlabel('Time')
    ax[0,0].set_title('Density')

    # Density point
    ax[0,0].plot(t_mid[i], densities_sd[i], 'ro', fillstyle='none')

    # XY flux
    ax[0,1].pcolormesh(XY_Y, XY_X, flux_z_sd)
    ax[0,1].set_aspect('equal')
    ax[0,1].set_xlabel(r'$y$')
    ax[0,1].set_ylabel(r'$x$')
    ax[0,1].invert_yaxis()
    ax[0,1].set_title('Flux-XY (Top View)')

    # XZ flux
    ax[1,0].pcolormesh(XZ_X, XZ_Z, flux_y_sd)
    ax[1,0].set_aspect('equal')
    ax[1,0].set_xlabel(r'$x$')
    ax[1,0].set_ylabel(r'$z$')
    ax[1,0].set_title('Flux-XZ (Front View)')

    # YZ flux
    ax[1,1].pcolormesh(YZ_Y, YZ_Z, flux_x_sd)
    ax[1,1].set_aspect('equal')
    ax[1,1].set_xlabel(r'$y$')
    ax[1,1].set_ylabel(r'$z$')
    ax[1,1].set_title('Flux-YZ (Side View)')

    plt.suptitle('MC/DC relative standard deviation')
    plt.savefig(f"sdev/figure_{i:03}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
