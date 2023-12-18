import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import numpy as np
import json

# uhhhhhhhhhhhhhhhhhhhhhhhhhhh, corporate said we had to get this version out! databases are for chumps anyway

plt.rcParams.update({"font.size": 16})
SIZE = 20
# plt.savefig("./zfigures/noise_vs_velocity_order.png")


def plot_noise_velocity_param():
    noise = np.flip(
        np.array(
            [
                1,
                0.95,
                0.9,
                0.85,
                0.8,
                0.75,
                0.7,
                0.65,
                0.6,
                0.55,
                0.5,
                0.45,
                0.4,
                0.35,
                0.3,
                0.25,
                0.2,
                0.15,
                0.14,
                0.13,
                0.12,
                0.11,
                0.109,
                0.108,
                0.107,
                0.106,
                0.105,
                0.104,
                0.103,
                0.102,
                0.101,
                0.1,
                0.05,
                0,
            ]
        )
    )

    noise_velocity_order = np.flip(
        np.array(
            [
                0.089136556,
                0.087715448,
                0.087477561,
                0.088313993,
                0.088361059,
                0.090561265,
                0.092000089,
                0.08896613,
                0.086419138,
                0.090085832,
                0.087892727,
                0.091743911,
                0.092068244,
                0.089312468,
                0.093494904,
                0.092770875,
                0.088752952,
                0.09699256,
                0.103102077,
                0.112760923,
                0.110792951,
                0.26898807,
                0.260260152,
                0.482870919,
                0.244003814,
                0.280332495,
                0.55654699,
                0.687545558,
                0.548806687,
                0.652803929,
                0.842987087,
                0.735455423,
                0.979605858,
                0.996486616,
            ]
        )
    )

    # # This is the function we are trying to fit to the data.
    def sigmoid(x, L, x0, k, b):
        y = L / (1 + np.exp(-k * (x - x0))) + b
        return y

    # # The actual curve fitting happens here
    optimizedParameters, pcov = curve_fit(
        sigmoid, noise, noise_velocity_order, method="lm"
    )

    x = np.linspace(0, 1, 1000)

    # print(optimizedParameters)

    plt.scatter(noise, noise_velocity_order, s=SIZE)
    # plt.plot(x, sigmoid(x, *optimizedParameters), label="fit")
    plt.xlabel("$\epsilon$")
    plt.ylabel("$A$")
    plt.savefig("./zfigures/noise_vs_velocity_order.png")
    plt.show()


def plot_velocity_order_vs_time():
    with open("./data/vicseks_vs_time_default.json") as f:
        noise = json.load(f)

    noise1 = np.array(noise["0"])
    noise2 = np.array(noise["1"])
    noise3 = np.array(noise["2"])
    noise4 = np.array(noise["3"])
    noise5 = np.array(noise["4"])

    xdata = [i for i in range(len(noise1))]

    plt.plot(xdata, (noise1 + noise2 + noise3 + noise4 + noise5) / 5)
    plt.xlabel("$t$")
    plt.xlim(0, 3000)
    plt.yticks([0.1 * (x + 1) for x in range(10)])
    plt.ylabel("$A$")
    plt.savefig("./zfigures/velocity_order_vs_time.png")
    plt.show()


def plot_file(filename):
    with open(filename) as f:
        data = json.load(f)

    data1 = np.array(data["0"])
    data2 = np.array(data["1"])
    data3 = np.array(data["2"])
    data4 = np.array(data["3"])
    data5 = np.array(data["4"])

    xdata = [i for i in range(len(data1))]
    plt.plot(xdata, (data1 + data2 + data3 + data4 + data5) / 5)
    plt.xlabel("$t$")
    plt.xlim(0, 3000)


def plot_lanchesters_vs_time_default():
    plot_file("./data/lanchesters_vs_time_default.json")
    # plt.title("A graph showing how the Lanchesters index increases over time")
    plt.ylabel("$L$")
    plt.savefig("./zfigures/lanchesters_vs_time_default.png")
    plt.show()


def plot_groups_vs_time_default():
    plot_file("./data/groups_vs_time_default.json")
    # plt.title("A graph showing how the number of groups decrease over time")
    # plt.ylabel("$M$", rotation=0)
    plt.ylabel("$M$")
    plt.savefig("./zfigures/groups_vs_time_default.png")
    plt.show()


def plot_alignment_vs_time_low_density():
    plot_file("./data/alignment_vs_time_low_density.json")
    plt.xlim(0, 1000)
    plt.ylabel("$A$")
    plt.savefig("./zfigures/alignment_vs_time_low_density.png")
    plt.show()


def plot_clustering_vs_time_low_density():
    plot_file("./data/clustering_vs_time_low_density.json")
    plt.xlim(0, 1000)
    plt.ylabel("$L$")
    plt.savefig("./zfigures/clustering_vs_time_low_density.png")
    plt.show()


def plot_groups_vs_time_low_density():
    plot_file("./data/groups_vs_time_low_density.json")
    plt.xlim(0, 1000)
    plt.ylabel("$M$")
    plt.savefig("./zfigures/groups_vs_time_low_density.png")
    plt.show()


def plot_align_rot_vs_radius():
    with open("./data/alignment_vs_radius.json") as f:
        data = json.load(f)

    keys = list(data.keys())
    values = list(data.values())

    plt.plot(keys, values, c="red", label="$A$")

    with open("./data/rotation_vs_radius.json") as f:
        data = json.load(f)

    keys = list(data.keys())
    values = list(data.values())

    plt.plot(keys, values, c="blue", label="$R$")
    # print(keys)
    # print(type(keys))
    plt.xticks(keys[::4])
    plt.xlabel("$k$")
    plt.legend()
    plt.savefig("./zfigures/align_rot_vs_radius.png")
    plt.show()


# plot_noise_velocity_param()
# plot_velocity_order_vs_time()
# plot_lanchesters_vs_time_default()
# plot_groups_vs_time_default()
# plot_alignment_vs_time_low_density()
# plot_clustering_vs_time_low_density()
# plot_groups_vs_time_low_density()
plot_align_rot_vs_radius()
