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
    # Parameters
    k = k if k != None else 0.1  # Overall stiffness of the building
    F0 = F0 if F0 != None else 5 * 10**-7  # Friction force
    A = A if A != None else 0.01  # Aplitude
    omega = omega if omega != None else 0.2  # Angular frequency
    # Mass of the building is 1 (to simplify the calculations)
    # If mass is not 1, differential each differential equation should be divided by mass

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
        # fmt: off
        return np.array([
                X[5],
                X[6],
                X[7],
                X[8],
                X[9],
                k*(-2*X[0] + X[1]) + F_f(X[5], X[0]) + A*np.sin(omega*t),
                k*(X[0] - 2*X[1] + X[2]) + F_f(X[6], X[1]),
                k*(X[1] - 2*X[2] + X[3]) + F_f(X[7], X[2]),
                k*(X[2] - 2*X[3] + X[4]) + F_f(X[8], X[3]),
                k*(X[3] - X[4]) + F_f(X[9], X[4])
                ])
        # fmt: on

    # Initial conditions
    X0 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) if X0 == None else X0

    # Time interval (s)
    t_stop = 120  # Mag. 5-6 earthquake lasts up to 30s
    nt = t_stop * 30  # Number of time steps

    # Time vector
    T = np.linspace(0, t_stop, nt)

    try:
        # Solve ODE
        X = odeint(D, X0, T)

        # Graphs - x
        vel_x = int(len(X[0, :]) / 2) - 1
        print(f"### Graph limits ###\nVel_x: {vel_x}")
        min_x = np.around(np.min(X[:, 0:vel_x]), decimals=3)
        max_x = np.around(np.max(X[:, 0:vel_x]), decimals=3)
        print("Min_x: ", min_x, "\nMax_x: ", max_x)
        # plt.xlim(min_x * 1.2, max_x * 1.2)
        # plt.ylim(0, t_stop + 5)
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

        # Graphs - v
        pol_x = int(len(X[0, :]) / 2)
        vel_x = int(len(X[0, :])) - 1
        print("Vel_x: ", vel_x)
        min_x = np.around(np.min(X[:, pol_x:vel_x]), decimals=3)
        max_x = np.around(np.max(X[:, pol_x:vel_x]), decimals=3)
        print("Min_x: ", min_x, "\nMax_x: ", max_x)
        # plt.plot(X[:, 5], T, label='v1', color='red') # Ground speed
        plt.plot(X[:, 6], T, label="v2", color="green")
        plt.plot(X[:, 7], T, label="v3", color="blue")
        plt.plot(X[:, 8], T, label="v4", color="orange")
        plt.plot(X[:, 9], T, label="v4", color="cyan")
        plt.xlabel("v (brzina)")
        plt.ylabel("t (vrijeme)")
        plt.legend()

        # Printing values
        print("\n### Values ###")
        print(f"Passed!\n- k = {k},\n- F0 = {F0},\n- A = {A},\n- omega = {omega}")
    except ValueError:
        print("\n### Values ###")
        print(f"Failed!\n- k = {k},\n- F0 = {F0},\n- A = {A},\n- omega = {omega}")


if __name__ == "__main__":
    calculate()
