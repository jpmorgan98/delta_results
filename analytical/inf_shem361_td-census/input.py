import mcdc
import numpy as np


# =============================================================================
# Set model
# =============================================================================
# The infinite homogenous medium is modeled with reflecting slab

# Load material data
with np.load("../data/MGXS-SHEM361.npz") as data:
    SigmaC = data["SigmaC"] * 1.5  # /cm
    SigmaS = data["SigmaS"]
    SigmaF = data["SigmaF"]
    nu_p = data["nu_p"]
    nu_d = data["nu_d"]
    chi_p = data["chi_p"]
    chi_d = data["chi_d"]
    G = data["G"]
    speed = data["v"]
    lamd = data["lamd"]

# Set material
m = mcdc.material(
    capture=SigmaC,
    scatter=SigmaS,
    fission=SigmaF,
    nu_p=nu_p,
    chi_p=chi_p,
    nu_d=nu_d,
    chi_d=chi_d,
    decay=lamd,
    speed=speed,
)

# Set surfaces
s1 = mcdc.surface("plane-x", x=-1e10, bc="reflective")
s2 = mcdc.surface("plane-x", x=1e10, bc="reflective")

# Set cells
c = mcdc.cell(+s1 & -s2, m)

# =============================================================================
# Set initial source
# =============================================================================

energy = np.zeros(G)
energy[-1] = 1.0
source = mcdc.source(energy=energy)

# =============================================================================
# Set problem and tally, and then run mcdc
# =============================================================================

# Tally
mcdc.tally.mesh_tally(
    scores=["flux"], t=np.insert(np.logspace(-8, 1, 100), 0, 0.0), g="all"
)

# Setting
mcdc.setting(N_particle=1000, active_bank_buff=10000, source_bank_buff=2)
mcdc.time_census(np.logspace(-5, 1, 6))
mcdc.population_control()

# Run
mcdc.run()
