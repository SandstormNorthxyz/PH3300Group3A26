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
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
    ax1.plot(potential.coord, potential.potential_a, label="Analytical")
    ax1.set_xlabel("z")
    ax1.set_ylabel("Electric Potential (V)")
    ax1.set_title("Analytical Electric Potential")
    ax1.grid(True)
    ax1.legend()
    #numerical plot
    for i, N in enumerate(n_array_disp):
        ax2.plot(potential.coord, n_potential[n_array_lookup[N]], label=f"N = {N}")
    ax2.set_xlabel("z")
    ax2.set_ylabel("Electric Potential (V)")
    ax2.set_title("Numerical Electric Potential")
    ax2.grid(True)
    ax2.legend()
    #error plot
    #TODO fix title displaying incorrectly
    for i, N in enumerate(n_array_disp):
        ax3.plot(potential.coord, n_error[n_array_lookup[N]], label=f"N = {N}")
    ax3.set_xlabel("z")
    ax3.set_ylabel("Percent Error")
    ax3.set_title("Percent Error Between Analytical and Numerical Solutions")
    ax3.grid(True)
    ax3.legend()
    # Prevent labels from overlapping
    plt.tight_layout()

    plt.show()


    #TODO align 0 on y axis to true 0, make integer y axis
    plt.plot(n_array[:n_array_lookup[20]], np.amax(n_error, axis=1)[:n_array_lookup[20]])
    plt.xlabel("Shells")
    plt.ylabel("Error (%)")
    plt.title("Percent Error vs. Number of shells in numerical method")
    plt.show()