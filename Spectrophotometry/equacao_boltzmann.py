import numpy as np

def nj_no_percentagem(temperatura):
    numerador = 6 / 2 # Valor Pj/P0
    energia = 3.37e-19  # Energia de transição (J)
    k = 1.38e-23        # Constante de Boltzmann (J/K)
    expoente = -energia / (k * temperatura)
    resultado = numerador * np.exp(expoente)
    porcentagem = resultado * 100
    porcentagem_complementar = 100 - porcentagem
    return porcentagem, porcentagem_complementar, resultado

# Exemplo de uso:
temperatura = 10000  # Valor de temperatura desejada em '''Kelvin'''
porc, compl, resul = nj_no_percentagem(temperatura)
resul_crr = 1/round(resul, 6)

print(f"N0/Nj: {resul_crr:.1f}")
print(f"Nj (%): {porc:.5f}%")
print(f"N0 (%): {compl:.5f}%")
