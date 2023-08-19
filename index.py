# Importing the libraries
import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


def F_f(v, x):
    return


def D(k, A, omega, X, t):
    # fmt: off
    np.array([X[5],
            X[6],
            X[7],
            X[8],
            X[9],
            k*(-2*X[0] + X[1]) + F_f(X[5], X[0]) + A*np.sin(omega*t),
            k*(X[0] - 2*X[1] + X[2]) + F_f(X[6], X[1]),
            k*(X[1] - 2*X[2] + X[3]) + F_f(X[7], X[2]),
            k*(X[2] - 2*X[3] + X[4]) + F_f(X[8], X[3]),
            k*(X[3] - 2*X[4]) + F_f(X[9], X[4])
            ])
    # fmt: on


def calculate(k: float = None, F0: float = None, A: float = None, omega: float = None):
    # Parameters
    k = k if k != None else 0  # Overall stiffness of the building
    F0 = F0 if F0 != None else 0  # Friction force
    A = A if A != None else 0  # Aplitude
    omega = omega if omega != None else 0  # Angular frequency


if __name__ == "__main__":
    calculate()
