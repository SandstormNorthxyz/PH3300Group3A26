#field class to then plot
import numpy as np
import matplotlib.pyplot as plt

class Field:
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
    def generate_field_numerically(self, N):
        delta_r = self.radius / (N - 1)
        self.field_n = np.zeros(self.z_steps)
        #summation
        for i in range(N):
            r = i*delta_r
            if (i == 0 or i == N - 1):
                weight = 1
            else:
                weight = 2
            f = r / np.sqrt(r**2 + self.coord**2)
            self.field_n += f * weight
        self.field_n = self.field_n * (self.sigma / (2 * self.epsilon_0)) * (delta_r / 2)
        return self.field_n
    
    #generates field analytically
    def generate_field_analytically(self):
        self.field_a = (self.sigma / (2 * self.epsilon_0)) * (np.sqrt(self.radius**2 + self.coord**2) - np.abs(self.coord))

if __name__ == "__main__":
    field = Field(-5, 5, 500)
    n_array = [2, 5, 10, 100, 1000]
    n_field = np.zeros((len(n_array), 500))
    field.generate_field_analytically()
    #analytical plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
    ax1.plot(field.coord, field.field_a, label="Analytical")
    ax1.set_xlabel("z")
    ax1.set_ylabel("Electric Potentil (V)")
    ax1.set_title("Analytical Electric Potential")
    ax1.grid(True)
    ax1.legend()
    #numerical plot
    for i, N in enumerate(n_array):
        n_field[i] = field.generate_field_numerically(N)
        ax2.plot(field.coord, n_field[i], label=f"N = {N}")
    ax2.set_xlabel("z")
    ax2.set_ylabel("Electric Potential (V)")
    ax2.set_title("Numerical Electric Potential")
    ax2.grid(True)
    ax2.legend()
    #error plot
    for i, N in enumerate(n_array):
        n_field[i] = field.generate_field_numerically(N)
        error = np.abs((n_field[i] - field.field_a) / field.field_a)
        error = error * 100
        ax3.plot(field.coord, error, label=f"N = {N}")
    ax3.set_xlabel("z")
    ax3.set_ylabel("Percent Error")
    ax3.set_title("Percent Error Between Analytical and Numerical Solutions")
    ax3.grid(True)
    ax3.legend()
    # Prevent labels from overlapping
    plt.tight_layout()

    plt.show()