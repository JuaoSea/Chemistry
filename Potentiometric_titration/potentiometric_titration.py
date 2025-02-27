import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos
volumes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 8.5, 9, 9.5, 10, 10.2, 10.4, 10.6, 10.8, 11, 11.2, 11.4, 11.6, 11.8, 12, 12.2, 12.4, 12.6, 12.8, 13, 13.2, 13.4, 13.6, 13.8, 14, 14.2, 14.4, 14.6, 14.8, 15, 15.2, 15.4, 15.6, 15.8, 16, 17, 18, 19, 20])
ph_values = np.array([2.8, 3.11, 3.33, 3.49, 3.62, 3.73, 3.82, 3.93, 4.05, 4.12, 4.17, 4.24, 4.32, 4.35, 4.38, 4.4, 4.44, 4.47, 4.51, 4.54, 4.59, 4.63, 4.68, 4.72, 4.77, 4.83, 4.9, 4.99, 5.04, 5.13, 5.23, 5.38, 5.54, 5.76, 6.13, 8.58, 11.53, 11.93, 12.02, 12.23, 12.33, 12.43, 12.52, 12.88, 13.05, 13.17, 13.25])

# Calcular a primeira e a segunda derivada do pH em relação ao volume
first_derivative = np.gradient(ph_values, volumes)  # Primeira derivada (∆pH/∆V)
second_derivative = np.gradient(first_derivative, volumes)  # Segunda derivada (∆²pH/∆V²)

# Determinar o ponto de equivalência com base na máxima primeira derivada
volume_equiv = volumes[np.argmax(first_derivative)]  # Índice do maior valor da primeira derivada
ph_equiv = ph_values[np.argmax(first_derivative)]

# Cálculo do teor de ácido acetilsalicílico
concentration_naoh = 0.19  # Concentração de NaOH (mol/L)
sample_mass = 1000  # Massa da amostra (mg)
mols_naoh = volume_equiv * concentration_naoh  # mols de NaOH (Volume em litros)
mols_acid = mols_naoh  # Relação 1:1
mass_acid = mols_acid * 180.16  # Massa molar do ácido acetilsalicílico (g/mol) convertida para mg
percent_mass = (mass_acid / sample_mass) * 100

# Exibir os resultados no console
print(f"Ponto de equivalência: Volume = {volume_equiv:.2f} mL, pH = {ph_equiv:.2f}")
print(f"Teor de ácido acetilsalicílico: {mass_acid:.2f} mg ({percent_mass:.2f}% m/m)")

# Gráficos 
plt.figure(figsize=(16, 8))

# Gráfico do pH vs Volume
plt.subplot(2, 2, 1)
plt.plot(volumes, ph_values, marker='o', label='pH', color='blue')
plt.scatter(volume_equiv, ph_equiv,color='red', zorder=5, label='Ponto de Equivalência')
plt.xlabel("Volume de NaOH (mL)")
plt.ylabel("pH")
plt.title("Curva de Titulação (pH vs Volume)")
plt.grid(True)
plt.legend()

# Gráfico da primeira derivada vs Volume
plt.subplot(2, 2, 2)
plt.plot(volumes, first_derivative, marker='o', label='Primeira Derivada (∆pH/∆V)', color='orange')
plt.xlabel("Volume de NaOH (mL)")
plt.ylabel("Primeira Derivada (∆pH/∆V)")
plt.title("Curva da Primeira Derivada")
plt.grid(True)
plt.legend()

# Gráfico da segunda derivada vs Volume
plt.subplot(2, 2, 3)
plt.plot(volumes, second_derivative, marker='o', label='Segunda Derivada (∆²pH/∆V²)', color='green')
plt.xlabel("Volume de NaOH (mL)")
plt.ylabel("Segunda Derivada (∆²pH/∆V²)")
plt.title("Curva da Segunda Derivada")
plt.grid(True)
plt.legend()

# Zoom no ponto de equivalência
plt.subplot(2, 2, 4)
zoom_start = max(0, np.argmax(first_derivative) - 2)
zoom_end = min(len(volumes), np.argmax(first_derivative) + 3)
plt.plot(volumes[zoom_start:zoom_end], ph_values[zoom_start:zoom_end], marker='o', color='blue', label='Dados Experimentais')
plt.scatter(volume_equiv, ph_equiv, color='red', zorder=5, label='Ponto de Equivalência')  # Destacar ponto de equivalência no zoom

plt.xlabel("Volume de NaOH (mL)")
plt.ylabel("pH")
plt.title("Zoom no Ponto de Equivalência")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Potentiometric_titration.png")
plt.show()
