import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import h5py
import matplotlib.animation as animation


# =============================================================================
# Plot results
# =============================================================================

# Results
with h5py.File("output_delta1.h5", "r") as f:
    tallies = f["tallies/mesh_tally_0"]
    flux = tallies["flux"]
    grid = tallies["grid"]
    x = grid["x"][:]
    x_mid = 0.5 * (x[:-1] + x[1:])
    y = grid["y"][:]
    y_mid = 0.5 * (y[:-1] + y[1:])
    t = grid["t"][:]
    t_mid = 0.5 * (t[:-1] + t[1:])
    t_mid = 0.5 * (t[:-1] + t[1:])
    X, Y = np.meshgrid(y_mid, x_mid)

    # print(y_mid, x_mid)

    phi = flux["mean"][:]
    phi_sd = flux["sdev"][:]


with h5py.File("output.h5", "r") as f:
    tallies = f["tallies/mesh_tally_0"]
    flux = tallies["flux"]
    grid = tallies["grid"]
    phi_ana = flux["mean"][:]
    phi_sd_ana = flux["sdev"][:]


t = 2.0*60
t_ana = 2.25*60
sdev = np.sum(phi_sd)
sdev_ana = np.sum(phi_sd_ana)
error = np.linalg.norm(phi_ana-phi)
print("Error: {}, σ_ana: {}, σ_delta: {}".format(error, sdev, sdev_ana))
print("FOM_ana: {}, FOM_delta: {}".format(1/(t_ana*sdev_ana), 1/(t*sdev)))


# ============ ANIMATION ===================

fig, axs = plt.subplots(ncols=2, nrows=2)
cax1 = axs[0,0].pcolormesh(X, Y, phi[0])
text1 = axs[0,0].text(0.02, 1.02, "", transform=axs[0,0].transAxes)
axs[0,0].set_aspect("equal", "box")
axs[0,0].set_xlabel("$y$ [cm]")
axs[0,0].set_ylabel("$x$ [cm]")

cax2 = axs[0,1].pcolormesh(X, Y, phi_sd[0], vmin=0, vmax=1)
axs[0,1].set_aspect("equal", "box")
axs[0,1].set_xlabel("$y$ [cm]")
axs[0,1].set_ylabel("$x$ [cm]")

cax3 = axs[1,0].pcolormesh(X, Y, phi_ana[0])
text3 = axs[1,0].text(0.02, 1.02, "", transform=axs[0,0].transAxes)
axs[1,0].set_aspect("equal", "box")
axs[1,0].set_xlabel("$y$ [cm]")
axs[1,0].set_ylabel("$x$ [cm]")

cax4 = axs[1,1].pcolormesh(X, Y, phi_sd_ana[0], vmin=0, vmax=1)
axs[1,1].set_aspect("equal", "box")
axs[1,1].set_xlabel("$y$ [cm]")
axs[1,1].set_ylabel("$x$ [cm]")


def animate(i):
    cax1.set_array(phi[i])
    cax1.set_clim(phi[i].min(), phi[i].max())
    text1.set_text(r"$t \in [%.1f,%.1f]$ s" % (t[i], t[i + 1]))
    cax2.set_array(phi_sd[i])
    cax2.set_clim(phi_sd[i].min(), phi_sd[i].max())

    cax3.set_array(phi_ana[i])
    cax3.set_clim(phi_ana[i].min(), phi_ana[i].max())
    text3.set_text(r"$t \in [%.1f,%.1f]$ s" % (t[i], t[i + 1]))
    cax4.set_array(phi_sd_ana[i])
    cax4.set_clim(phi_sd_ana[i].min(), phi_sd_ana[i].max())


anim = animation.FuncAnimation(fig, animate, interval=200, frames=len(t) - 1)
anim.save('koby.gif')


# ============ FIRST ATTEMPT ===================

from matplotlib import cm, ticker
import matplotlib

# define subplot grid
fig, axs = plt.subplots(
    nrows=2, ncols=3, figsize=(7.5 * 1.5, 4 * 1.5), dpi=300, layout="constrained"
)
plt.subplots_adjust(hspace=0.5)
# fig.suptitle("Daily closing prices", fontsize=18, y=0.95)

time_index = np.array([0, 7, 9, 11, 14, 19]).astype(int)

print(phi.shape)

max1 = np.max(phi[:10, :, :]) * 0.75
max2 = np.max(phi[10:, :, :]) * 0.75
min1 = np.min(phi[:12, :, :]) * 0.75
min2 = np.min(phi[12:, :, :]) * 0.75

maxer = np.array([max1, max1, max1, max2, max2, max2])
miner = np.array([min1, min1, min1, min2, min2, min2])

maxmax = np.max(phi)
minmin = np.min(phi)

# phi = np.ma.masked_where(phi <= 0, phi)

# loop through tickers and axes
for i, ax in enumerate(fig.axes):

    # ax.set_title("t={}".format(t_mid[time_index[i]]))
    ax.text(60, 52, r"$t={}$ [s]".format(t_mid[time_index[i]]), color="w")
    # ax.set_ylabel(r"$y$")
    # ax.set_xlabel(r"$x$")

    cont = ax.contourf(X, Y, phi[time_index[i]], levels=200)
    plt.colorbar(cont, ax=ax, format="%3.1e")
    cont.set_edgecolor("face")
    # ax.colorbar(cont)

# fig.colorbar(cont, ax=axs.ravel().tolist())


for ax in axs.flat:
    ax.set(xlabel=r"$x$ [cm]", ylabel=r"$y$ [cm]")

for ax in axs.flat:
    ax.label_outer()

# plt.tight_layout()

plt.savefig("koby.pdf")
