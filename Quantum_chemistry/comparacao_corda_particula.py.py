import numpy as np               
import matplotlib.pyplot as plt  

# Comprimento da corda/caixa
L = 1.0
# Cria 500 pontos igualmente espaçados entre 0 e L (posição x)
x = np.linspace(0, L, 500)

plt.figure(figsize=(14,6))

# Loop sobre o número do modo n (aqui só o n=3, mas poderia ter mais)
for n in [3]:
    # --- Corda vibrante (clássica) ---
    # Solução da equação da onda para uma corda presa nas extremidades
    # Representa o deslocamento transversal da corda no modo estacionário n
    y_classical = np.sin(n * np.pi * x / L)

    # --- Partícula na caixa (quântica) ---
    # Função de onda normalizada da partícula na caixa infinita 1D
    # O fator sqrt(2/L) garante que a integral de |ψ|² no intervalo [0,L] seja 1
    psi_quantum = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
    
    # Plota o modo da corda vibrante
    plt.plot(x, y_classical, label=f"Corda: Modo {n}")
    # Plota a densidade de probabilidade da partícula (|ψ|²), em linha tracejada
    plt.plot(x, psi_quantum**2, '--', label=rf"Partícula na caixa: $|\psi_{n}|^2$")

plt.title("Comparação: Corda vibrante x Partícula na caixa")
plt.xlabel("x (m)")
plt.ylabel("Deslocamento / Probabilidade")
plt.grid(True)
plt.legend()
plt.show()
