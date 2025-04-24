import matplotlib.pyplot as plt
import h5py
import numpy as np



with np.load('surface/data.npz') as data:
    surface_runtimes = data['runtimes']
    surface_errors = data['errors']


with np.load('hybrid/data.npz') as data:
    hyb_runtimes = data['runtimes']
    hyb_errors = data['errors']

with np.load('hybrid/data_switch.npz') as data:
    delta_runtimes = data['runtimes']
    delta_errors = data['errors']


surface_fom = 1/(surface_runtimes*surface_errors)
hyb_fom = 1/(hyb_runtimes*hyb_errors)

hyb_fom *= 2
delta_fom = 1/(delta_runtimes*delta_errors)

mfp = np.logspace(-1, 1, 10)
ratio = np.array([1, 5, 10, 100])


colors = ['#D81B60','#1E88E5','#004D40']
linemarks = ['-x', '--*', '-.^']

#print(colors[0])

fig, axs = plt.subplots(2, 2, sharex=True)
axs[0, 0].plot(mfp, hyb_fom[0,:], linemarks[0], label="hybrid", color=colors[0])
axs[0, 0].plot(mfp, surface_fom[0,:], linemarks[1], label="surface", color=colors[1])
axs[0, 0].plot(mfp, delta_fom[0,:], linemarks[2], label="delta", color=colors[2])
axs[0, 0].set_title(r'$\Sigma_2/\Sigma_1$ = {}'.format(ratio[0]))
axs[0, 0].set_xscale("log")
axs[0, 0].legend()

axs[0, 1].plot(mfp, hyb_fom[1,:], linemarks[0], color=colors[0], label="hybrid")
axs[0, 1].plot(mfp, surface_fom[1,:], linemarks[1], color=colors[1], label="surface")
axs[0, 1].plot(mfp, delta_fom[1,:], linemarks[2], color=colors[2], label="delta")
axs[0, 1].set_title(r'$\Sigma_2/\Sigma_1$ = {}'.format(ratio[1]))

axs[1, 0].plot(mfp, hyb_fom[2,:], linemarks[0], color=colors[0], label="hybrid")
axs[1, 0].plot(mfp, surface_fom[2,:], linemarks[1], color=colors[1], label="surface")
axs[1, 0].plot(mfp, delta_fom[2,:], linemarks[2], color=colors[2], label="delta")
axs[1, 0].set_title(r'$\Sigma_2/\Sigma_1$ = {}'.format(ratio[2]))


axs[1, 1].plot(mfp, hyb_fom[3,:], linemarks[0], color=colors[0], label="hybrid")
axs[1, 1].plot(mfp, surface_fom[3,:], linemarks[1], color=colors[1], label="surface")
axs[1, 1].plot(mfp, delta_fom[3,:], linemarks[2], color=colors[2], label="delta")
axs[1, 1].set_title(r'$\Sigma_2/\Sigma_1$ = {}'.format(ratio[3]))


axs[1, 1].set_xlabel(r'$\delta$')
axs[1, 0].set_xlabel(r'$\delta$')

axs[1, 0].set_ylabel(r'FOM $\left(\frac{1}{|\sigma^2| t} \right) $')
axs[0, 0].set_ylabel(r'FOM $\left(\frac{1}{|\sigma^2| t} \right) $')

#for ax in axs.flat:
#    ax.set(xlabel=r'$N_{surfaces}$', ylabel=r'FOM $\left(\frac{1}{|\sigma^2| t} \right) $')

# Hide x labels and tick labels for top plots and y ticks for right plots.
#for ax in axs.flat:
#    ax.label_outer()

plt.show()



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