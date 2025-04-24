import h5py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import shutil


import imageio

# Get results
with h5py.File('delta_c5g7_lassen.h5', 'r') as f:
    densities = f['tallies/mesh_tally_0/flux/mean'][()]
    fluxes = f['tallies/mesh_tally_1/flux/mean'][()]
    x = f['tallies/mesh_tally_1/grid/x'][()]
    y = f['tallies/mesh_tally_1/grid/y'][()]
    z = f['tallies/mesh_tally_1/grid/z'][()]
    t = f['tallies/mesh_tally_1/grid/t'][()]

# The grids
t_mid = 0.5 * (t[:-1] + t[1:])
XY_X, XY_Y = np.meshgrid(x, y, indexing='ij')
XZ_X, XZ_Z = np.meshgrid(x, z, indexing='ij')
YZ_Y, YZ_Z = np.meshgrid(y, z, indexing='ij')

# Create clean folder for output figures
# Check if the folder exists
if os.path.exists('flux'):
    shutil.rmtree('flux')  # Remove the existing folder
os.makedirs('flux')  # Create a new folder

frames = []

# Iterate over time step and create figures
N = len(fluxes)
for i in range(N):
    flux = fluxes[i]

    # Calculate flux averages
    flux_x = np.average(flux, axis=0)
    flux_y = np.average(flux, axis=1)
    flux_z = np.average(flux, axis=2)

    # Plot
    fig, ax = plt.subplots(2, 2, figsize=(8, 6), gridspec_kw={'width_ratios':[1,2], 'height_ratios':[1,1], 'hspace':0.5})

    # Density curve
    ax[0,0].plot(t_mid, densities, 'b')
    ax[0,0].set_yscale('log')
    ax[0,0].set_ylabel('Density')
    ax[0,0].set_xlabel('Time')
    ax[0,0].set_title('Density')

    # Density point
    ax[0,0].plot(t_mid[i], densities[i], 'ro', fillstyle='none')

    ax[0,0].axvspan(0, 5, facecolor="gray", alpha=0.2)
    ax[0,0].axvspan(5, 10, facecolor="green", alpha=0.2)
    ax[0,0].axvspan(10, 15, facecolor="red", alpha=0.2)
    ax[0,0].axvspan(15, 20, facecolor="blue", alpha=0.2)
    ax[0,0].annotate(
        "Phase 1",
        (2.5, 0.3),
        color="black",
        ha="center",
        va="center",
        backgroundcolor="white",
    )
    ax[0,0].annotate(
        "Phase 2",
        (7.5, 0.3),
        color="black",
        ha="center",
        va="center",
        backgroundcolor="white",
    )
    ax[0,0].annotate(
        "Phase 3",
        (12.5, 0.3),
        color="black",
        ha="center",
        va="center",
        backgroundcolor="white",
    )
    ax[0,0].annotate(
        "Phase 4",
        (17.5, 4.0),
        color="black",
        ha="center",
        va="center",
        backgroundcolor="white",
    )

    # XY flux
    ax[0,1].pcolormesh(XY_Y, XY_X, flux_z)
    ax[0,1].set_aspect('equal')
    ax[0,1].set_xlabel(r'$y$')
    ax[0,1].set_ylabel(r'$x$')
    ax[0,1].invert_yaxis()
    ax[0,1].set_title('Flux-XY (Top View)')

    # XZ flux
    ax[1,0].pcolormesh(XZ_X, XZ_Z, flux_y)
    ax[1,0].set_aspect('equal')
    ax[1,0].set_xlabel(r'$x$')
    ax[1,0].set_ylabel(r'$z$')
    ax[1,0].set_title('Flux-XZ (Front View)')

    # YZ flux
    ax[1,1].pcolormesh(YZ_Y, YZ_Z, flux_x)
    ax[1,1].set_aspect('equal')
    ax[1,1].set_xlabel(r'$y$')
    ax[1,1].set_ylabel(r'$z$')
    ax[1,1].set_title('Flux-YZ (Side View)')

    plt.suptitle('MC/DC result')
    plt.savefig(f"flux/figure_{i:03}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

    image = imageio.v2.imread(f'flux/figure_{i:03}.png')
    frames.append(image)


imageio.mimsave('flux.gif', # output gif
                frames,          # array of input frames
                fps = 5)