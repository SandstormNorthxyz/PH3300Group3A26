#potential class to then plot
#simple plot made as example
import numpy as np
import matplotlib.pyplot as plt

#potential class
class Potential:
    #takes arguments as minimum and maximum z values as well as a step ammount for numerical solution
    #step value also declares the points measured for analytical solution and is used to create coordinate linspace
    def __init__(self, z_min, z_max, z_steps, radius=0.15, sigma=5e-6):
        self.z_min = z_min
        self.z_max = z_max
        self.z_steps = z_steps
        self.radius = radius
        self.sigma = sigma
        self.epsilon_0 = 8.854e-12
        self.coord = np.linspace(z_min, z_max, z_steps)
    
    #N is the precision of the integral
    #z_steps is the number of steps along the z axis to be counted
    #returns potential array
    def generate_potential_numerically(self, N):
        delta_r = self.radius / (N - 1)
        self.potential_n = np.zeros(self.z_steps)
        #summation
        for i in range(N):
            r = i*delta_r
            if (i == 0 or i == N - 1):
                weight = 1
            else:
                weight = 2
            f = r / np.sqrt(r**2 + self.coord**2)
            self.potential_n += f * weight
        #multiply by constants
        self.potential_n = self.potential_n * (self.sigma / (2 * self.epsilon_0)) * (delta_r / 2)
        #returns to make plotting multiple values easier
        return self.potential_n
    
    #generates potential analytically
    #returns potential array
    def generate_potential_analytically(self):
        self.potential_a = (self.sigma / (2 * self.epsilon_0)) * (np.sqrt(self.radius**2 + self.coord**2) - np.abs(self.coord))
        return self.potential_a

if __name__ == "__main__":
    potential = Potential(-5, 5, 500)
    # n_array = np.logspace(0, 3, 20, dtype=int)
    n_array = np.arange(2, 1001, dtype=int)
    n_array_lookup = {n_array[i]:i for i in range(len(n_array))}
    n_array_disp = [2, 5, 10, 100, 1000]
    n_potential = np.zeros((len(n_array), 500))
    n_error = np.zeros((len(n_array), 500))
    potential.generate_potential_analytically()

    for i, N in enumerate(n_array):
        n_potential[i] = potential.generate_potential_numerically(N)
        n_error[i] = np.abs((n_potential[i] - potential.potential_a) / potential.potential_a)
        n_error[i] = n_error[i] * 100



    #analytical plot
    # fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
    # ax = ax1
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.plot(potential.coord, potential.potential_a, label="Analytical")
    ax.set_xlabel("z")
    ax.set_ylabel("Electric Potential (V)")
    ax.set_title("Analytical Electric Potential")
    ax.grid(True)
    ax.legend()
    plt.show()
    #numerical plot
    # ax = ax2
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    for i, N in enumerate(n_array_disp):
        ax.plot(potential.coord, n_potential[n_array_lookup[N]], label=f"N = {N}")
    ax.set_xlabel("z")
    ax.set_ylabel("Electric Potential (V)")
    ax.set_title("Numerical Electric Potential")
    ax.grid(True)
    ax.legend()
    plt.show()
    #error plot
    #TODO fix title displaying incorrectly
    # ax = ax3
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    for i, N in enumerate(n_array_disp):
        ax.plot(potential.coord, n_error[n_array_lookup[N]], label=f"N = {N}")
    ax.set_xlabel("z")
    ax.set_ylabel("Percent Error")
    ax.set_title("Percent Error Between Analytical and Numerical Solutions")
    ax.grid(True)
    ax.legend()
    # Prevent labels from overlapping
    plt.tight_layout()
    plt.show()

    fig, (ax1) = plt.subplots(1, 1, figsize=(16, 10))
    ax = ax1
    #TODO align 0 on y axis to true 0, make integer y axis
    ax.plot(n_array[:n_array_lookup[20]], np.amax(n_error, axis=1)[:n_array_lookup[20]])
    ax.set_xlabel("Shells")
    ax.set_ylabel("Error (%)")
    ax.set_title("Percent Error vs. Number of shells in numerical method")
    plt.xlim([2, 20])
    plt.ylim([0, 50])
    plt.show()