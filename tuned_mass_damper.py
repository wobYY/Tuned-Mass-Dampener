# Importing the libraries
import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt

# from matplotlib.animation import FuncAnimation
# from matplotlib.patches import Rectangle


def calculate(
    k: float = None,
    F0: float = None,
    A: float = None,
    omega: float = None,
    X0: dict = None,
):
    # Variables
    print("Setting initial variables...")
    k = k if k != None else 1 * 10**-1  # Overall stiffness of the building [N/m]
    F0 = F0 if F0 != None else 5 * 10**-7  # Friction force [N]
    A = A if A != None else 1 * 10**-2  # Aplitude [m]
    omega = omega if omega != None else 0.1  # Angular frequency [rad/s]
    g = 9.81  # Gravitational acceleration [m/s^2]
    L = 1000  # Length of the pendalum rope [m]
    # Mass of the building is 1 (to simplify the calculations)
    # If mass is not 1, differential each differential equation should be divided by mass
    print("Initial variables set!\n")

    # Pendalum translation vector
    x_pendulum = []

    def _earthquake(t: float):
        if t < 0:
            raise ValueError("Time cannot be negative")

        # print("Time: ", t)
        if 5 <= t < 15:
            # print("Earthquake!")
            return A * np.sin(omega * t)
        else:
            return 0

    def _pendalum(v, x):
        print("Calculating pendalum...")
        if v > 0 and x > 0 or v < 0 and x > 0:
            u_pendulum = -g / L * float(x) - v
            x_pendulum.append(u_pendulum)
            return u_pendulum
        elif v > 0 and x < 0 or v < 0 and x < 0:
            u_pendulum = g / L * float(x) - v
            x_pendulum.append(u_pendulum)
            return u_pendulum
        elif v > 0 and x == 0:
            u_pendulum = -g / L * float(x) - v
            x_pendulum.append(u_pendulum)
            return u_pendulum
        elif v < 0 and x == 0:
            u_pendulum = g / L * float(x) - v
            x_pendulum.append(u_pendulum)
            return u_pendulum
        else:
            x_pendulum.append(0)
            return 0

    # Friction force
    def F_f(v, x):  # v = x_dot, x = x
        if v > 0:
            return -F0
        elif v < 0:
            return F0
        elif v == 0 and k * x <= F0:
            return k * x
        elif v == 0 and k * x > F0:
            return (F0 * x) / np.abs(x)
        else:
            raise ValueError("No conditions met for friction force calculation")

    # Differential equation
    def D(X, t):
        # X0, X1, X2, X3, X4, V5, V6, V7, V8, V9 = X
        print(f"Solving X for t = {t}...")
        # fmt: off
        return np.array([
                X[5],
                X[6],
                X[7],
                X[8],
                X[9],
                k*(-2*X[0] + X[1]) + F_f(X[5], X[0]) + _earthquake(t),
                k*(X[0] - 2*X[1] + X[2]) + F_f(X[6], X[1]),
                k*(X[1] - 2*X[2] + X[3]) + F_f(X[7], X[2]),
                k*(X[2] - 2*X[3] + X[4]) + F_f(X[8], X[3]),
                k*(X[3] - X[4]) + F_f(X[9], X[4]) + _pendalum(X[9], X[4])
                ])
        # fmt: on

    # Initial conditions
    print("Setting initial conditions...")
    X0 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) if X0 == None else X0

    # Time interval (s)
    t_stop = 300  # Mag. 5-6 earthquake lasts up to 30s
    nt = t_stop * 300  # Number of time steps

    # Time vector
    T = np.linspace(0, t_stop, nt)
    print("Initial conditions set!\n")

    try:
        # Solve ODE
        print("Solving ODE...")
        X = odeint(D, X0, T)
        print("ODE solved!\n")

        # Graph - x
        vel_x = int(len(X[0, :]) / 2) - 1
        print(f"### Graph limits ###\nVel_x: {vel_x}")
        min_x = np.around(np.min(X[:, 0:vel_x]), decimals=3)
        max_x = np.around(np.max(X[:, 0:vel_x]), decimals=3)
        print("Min_x: ", min_x, "\nMax_x: ", max_x)
        # plt.xlim(min_x * 1.2, max_x * 1.2)
        # plt.ylim(30, 830)
        # plt.plot(X[:, 0], T, label="x0", color="red")  # Ground floor
        plt.plot(X[:, 1], T, label="x1", color="green")
        plt.plot(X[:, 2], T, label="x2", color="blue")
        plt.plot(X[:, 3], T, label="x3", color="orange")
        plt.plot(X[:, 4], T, label="x4", color="cyan")
        plt.xlabel("x (pomak)")
        plt.ylabel("t (vrijeme)")
        plt.legend()

        # Split x and v graphs
        plt.figure()

        # Graph - v
        pol_x = int(len(X[0, :]) / 2)
        vel_x = int(len(X[0, :])) - 1
        print("Vel_x: ", vel_x)
        min_x = np.around(np.min(X[:, pol_x:vel_x]), decimals=3)
        max_x = np.around(np.max(X[:, pol_x:vel_x]), decimals=3)
        print("Min_x: ", min_x, "\nMax_x: ", max_x)
        # plt.xlim(min_x * 1.2, max_x * 1.2)
        # plt.ylim(25, 60)
        # plt.plot(X[:, 5], T, label='v1', color='red') # Ground speed
        plt.plot(X[:, 6], T, label="v2", color="green")
        plt.plot(X[:, 7], T, label="v3", color="blue")
        plt.plot(X[:, 8], T, label="v4", color="orange")
        plt.plot(X[:, 9], T, label="v5", color="cyan")
        plt.xlabel("v (brzina)")
        plt.ylabel("t (vrijeme)")
        plt.legend()

        # Spliting v and pendulum graphs
        plt.figure()

        # Graph - pendulum
        plt.ylim(0, t_stop)
        plt.plot(x_pendulum, T, label="pendulum", color="red")
        plt.xlabel("x (pomak njihala)")
        plt.ylabel("t (vrijeme)")
        plt.legend()

        # Printing values
        print("\n### Values ###")
        print(f"Passed!\n- k = {k},\n- F0 = {F0},\n- A = {A},\n- omega = {omega}")
    except ValueError:
        print("\n### Values ###")
        print(f"Failed!\n- k = {k},\n- F0 = {F0},\n- A = {A},\n- omega = {omega}")

    return [x_pendulum, T]


if __name__ == "__main__":
    calculate()
