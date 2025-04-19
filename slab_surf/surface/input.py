import numpy as np
import mcdc
import sys

# =============================================================================
# Set model
# =============================================================================
# N slab layers

N_surfaces = int(sys.argv[1])
sigma_2 = float(sys.argv[2])
#delta_track = False
#collision_est = False
#N_surfaces = 6 # input!
#sigma_2 = 2.0 # input!


Len = 6
z_surfaces = np.linspace(0,Len, N_surfaces)
sigma_1 = 1.0

# Set materials
m1 = mcdc.material(capture=np.array([1.0]))
m2 = mcdc.material(capture=np.array([sigma_2]))

# Set surfaces
sLB = mcdc.surface("plane-z", z=z_surfaces[0], bc="vacuum")
surfaces = [sLB]

# fill in the middle surfaces
for i in range(1,N_surfaces-1,1):
    surf = mcdc.surface("plane-z", z=z_surfaces[i])
    surfaces.append(surf)

sRB = mcdc.surface("plane-z", z=z_surfaces[-1], bc="vacuum")
surfaces.append(sRB)

# Set cells
for i in range(N_surfaces-1):
    if i % 2 == 0: # if even index then matieral is 2
        mat = m2
    else: # if odd material is one
        mat = m1
    
    mcdc.cell(+surfaces[i] & -surfaces[i+1], mat)


# =============================================================================
# Set source
# =============================================================================
# Uniform isotropic source throughout the domain

mcdc.source(z=[0.0, 6.0], isotropic=True)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

# Tally: cell-average fluxes and currents
mcdc.tally.mesh_tally(
    scores=["flux"],
    z=np.linspace(0.0, 6.0, 61),
)

# Setting
mcdc.setting(N_particle=1e8)

# visualize if wanted
# mcdc.visualize('zy', y=[0.0, 4.0], z=[0,6.0], save_as="{}surfSlab.png".format(N_surfaces))


# Run
mcdc.run()